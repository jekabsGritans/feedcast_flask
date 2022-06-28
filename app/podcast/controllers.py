from flask import Blueprint, Response, request, session, render_template, flash, redirect, url_for, abort
from app import db
from app.auth.models import User
from app.podcast.models import Podcast, Episode
from app.podcast.feeds import PodcastFeed
from app.podcast.forms import PodcastEdit, EpisodeEdit

pod = Blueprint('podcast', __name__, url_prefix='')

@pod.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcasts = Podcast.query.filter_by(user_id=user_id).all()
    return render_template('podcast/index.html', podcasts=podcasts)

@pod.route('/<int:podcast_id>/')
def show(podcast_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcast = Podcast.query.filter_by(id=podcast_id, user_id=user_id).first()
    if not podcast:
        abort(404)
    episodes = Episode.query.filter_by(podcast_id=podcast_id).all()
    return render_template('podcast/show.html', podcast=podcast, episodes=episodes)

@pod.route('/new/')
def new_pod():
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcast = Podcast(user_id=user_id)
    db.session.add(podcast)
    db.session.commit()
    return redirect(url_for('podcast.edit', podcast_id=podcast.id))

@pod.route('/<int:podcast_id>/new/')
def new_ep(podcast_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcast = Podcast.query.filter_by(id=podcast_id, user_id=user_id).first()
    if not podcast:
        abort(404)
    episode = Episode(podcast_id=podcast_id)
    db.session.add(episode)
    db.session.commit()
    return redirect(url_for('podcast.edit_ep', episode_id=episode.id))

@pod.route('/<podcast_id>/edit/', methods=['POST','GET'])
def edit(podcast_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcast = Podcast.query.get_or_404(podcast_id)
    if podcast.user_id != user_id:
        abort(404)
    form =  PodcastEdit(obj=podcast)
    if form.validate_on_submit():
        form.populate_obj(podcast)
        db.session.commit()
        return redirect(url_for('podcast.show', podcast_id=podcast_id))
    return render_template('podcast/edit.html', form=form)

@pod.route('/episode/<episode_id>/edit/', methods=['POST','GET'])
def edit_ep(episode_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    episode = Episode.query.get_or_404(episode_id)
    if episode.podcast.user.id != user_id:
        abort(404)
    form = EpisodeEdit(obj=episode)
    if form.validate_on_submit():
        form.populate_obj(episode)
        db.session.commit()
        return redirect(url_for('podcast.view_ep', episode_id=episode_id))
    return render_template('podcast/edit_ep.html', form=form)

@pod.route('/<podcast_id>/rss/')
def feed(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)
    feed = PodcastFeed(podcast)
    rss = feed.to_str()
    return Response(rss, mimetype='application/rss+xml')