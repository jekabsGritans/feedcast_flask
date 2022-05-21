from flask import Blueprint, Response, request, session, render_template, flash, redirect, url_for, abort
from app import db
from app.auth.models import User
from app.podcast.models import Podcast, Episode
from app.podcast.feeds import PodcastFeed
from app.podcast.forms import PodcastEdit, EpisodeEdit

pod = Blueprint('podcast', __name__, url_prefix='')

def cache_route(routef):
    session['url'] = url_for(routef.__name__)
    return routef()


@pod.route('/all/')
def album():
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcasts = Podcast.query.filter_by(user_id=user_id)
    return render_template('podcast/album.html', podcasts=podcasts)


@pod.route('/')
#@cache_route
def index():
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcasts = Podcast.query.filter_by(user_id=user_id).all()
    return render_template('podcast/index.html', podcasts=podcasts)

@pod.route('/<podcast_id>/')
#@cache_route
def view(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)
    return render_template('podcast/view.html', podcast=podcast)

@pod.route('/<podcast_id>/edit/', methods=['POST','GET'])
#@cache_route
def edit(podcast_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcast = Podcast.query.get_or_404(podcast_id)
    if podcast.user.id != user_id:
        abort(404)

    form =  PodcastEdit(request.form)
    if form.validate_on_submit():
        form.populate_obj(podcast)
        return redirect(url_for('podcast.view', podcast_id=podcast_id))

    form = PodcastEdit(obj=podcast)
    return render_template('podcast/edit.html', form=form)

@pod.route('/episode/<episode_id>/')
#@cache_route
def view_ep(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    return render_template('podacst/view_ep.html', episode=episode)

@pod.route('/episode/<episode_id>/edit/', methods=['POST','GET'])
#@cache_route
def edit_ep(episode_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    episode = Episode.query.get_or_404(episode_id)
    if episode.podcast.user.id != user_id:
        abort(404)

    form = EpisodeEdit(request.form)
    if form.validate_on_submit():
        form.populate_obj(episode)
        return redirect(url_for('podcast.view_ep', episode_id=episode_id))

    form = EpisodeEdit(obj=episode)
    return render_template('podcast/edit_ep.html', form=form)

@pod.route('/<podcast_id>/rss/')
#@cache_route
def feed(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)
    feed = PodcastFeed(podcast)
    rss = feed.to_str()
    return Response(rss, mimetype='application/rss+xml')