from flask import Blueprint, Response, request, session, render_template, flash, redirect, url_for
from app import db
from app.auth.models import User
from app.podcast.models import Podcast, Episode
from app.podcast.feeds import PodcastFeed

pod = Blueprint('auth', __name__, url_prefix='')

def cache_route(routef):
    session['url'] = url_for(routef.__name__)
    return routef()


@pod.route('/')
@cache_route
def index():
    if 'user' in session:
        user_id = session.get('user')
        podcasts = Podcast.query.filter_by(user_id=user_id)
        return render_template('podcast/overview.html', podcasts=podcasts)
    else:
        return redirect(url_for('auth.signin'))

@pod.route('/<podcast_id>/')
@cache_route
def view(podcast_id):
    podcast = Podcast.query.filter_by(id=podcast_id).first()
    if podcast:
        return render_template('podcast/view.html', podcast=podcast)
    else:
        return 'Podcast not found'

@pod.route('/<podcast_id>/edit/', methods=['POST','GET'])
@cache_route
def edit(podcast_id):
    if 'user' in session:
        user_id = session.get('user')
        podcast = Podcast.query.filter_by(id=podcast_id, user_id=user_id)
        if request.method == 'POST':
            ...
        else:
            if podcast:
                return render_template('podcast/edit.html', podcast=podcast)
            else:
                return 'Podcast not found'
    else:
        return redirect(url_for('auth.signin'))

@pod.route('/<podcast_id>/episode/<episode_id>/')
@cache_route
def view_ep(podcast_id, episode_id):
    episode = Episode.query.filter_by(id=episode_id, podcast_id=podcast_id)
    if episode:
        return render_template('podacst/view_ep.html', episode=episode)
    else:
        return 'Episode not found'

@pod.route('/<podcast_id>/episode/<episode_id>/edit/', methods=['POST','GET'])
@cache_route
def edit_ep(podcast_id, episode_id):
    if 'user' in session:
        user_id = session.get('user')
        episode = Episode.query.filter_by(id=episode_id, podcast_id=podcast_id, user_id=user_id)
        if request.method == 'GET':
            if episode:
                return render_template('podcast/edit_ep.html', episode=episode)
            else:
                return 'Episode not found'
        if request.method == 'POST':
            ...#also to create new 
    else:
        return redirect(url_for('auth.signin'))

@pod.route('/<podcast_id>/rss/')
@cache_route
def feed(podcast_id):
    podcast = Podcast.query.filter_by(id=podcast_id).first()
    if podcast:   
        feed = PodcastFeed(podcast)
        rss = feed.to_str()
        return Response(rss, mimetype='application/rss+xml')
    else:
        return "Podcast not found"