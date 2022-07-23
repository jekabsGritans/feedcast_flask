from flask import Blueprint, Response, request, session, render_template, flash, redirect, url_for, abort, current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app import db
from app.auth.models import User
from app.podcast.models import Podcast, Episode
from app.podcast.feeds import PodcastFeed
from app.podcast.forms import PodcastEdit, EpisodeEdit
import os
pod = Blueprint('podcast', __name__, url_prefix='')

@pod.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcasts = Podcast.query.filter_by(user_id=user_id).all()
    return render_template('podcast/index.html', podcasts=podcasts, user_id=user_id)

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
def new():
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcast = Podcast(user_id=user_id)
    db.session.add(podcast)
    db.session.commit()
    return redirect(url_for('podcast.edit', podcast_id=podcast.id))

@pod.route('/<int:podcast_id>/delete/')
def delete(podcast_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    podcast = Podcast.query.filter_by(id=podcast_id, user_id=user_id).first()
    if not podcast:
        abort(404)
    if os.exists(podcast.image):
        os.remove(podcast.image)
    db.session.delete(podcast)
    db.session.commit()
    return redirect(url_for('podcast.index'))

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
    user = User.query.get_or_404(user_id)
    podcast = Podcast.query.get_or_404(podcast_id)
    if podcast.user_id != user_id:
        abort(404)
    form = PodcastEdit()
    
    if form.validate_on_submit():
        podcast.title = form.title.data
        podcast.description = form.description.data
        podcast.language = form.language.data
        podcast.explicit = form.explicit.data
        podcast.categories = form.category.data#' '.join(form.category.data + form.sub_categories) #include sub categories
        podcast.ep_type = form.ep_type.data 
        podcast.ep_limit = form.ep_limit.data
        podcast.allowed_regions = ' '.join(form.allowed_regions.data)
        podcast.origin = form.origin.data
        image = form.image.data
        if image:
            if os.path.exists(podcast.image):
                os.remove(podcast.image)
            podcast.image = os.path.join(current_app.config['UPLOAD_DIR'], secure_filename(image.filename))
            form.image.data.save(podcast.image)
        podcast.link = url_for('podcast.feed', podcast_id=podcast.id)
        podcast.author_name = user.name
        podcast.author_email = user.email
        db.session.commit()
        return redirect(url_for('podcast.show', podcast_id=podcast_id))
    
    form.title.data = podcast.title
    form.description.data = podcast.description
    form.language.data = podcast.language
    form.category.data = podcast.categories
    form.explicit.data = podcast.explicit
    form.ep_type.data = podcast.ep_type
    form.ep_limit.data = podcast.ep_limit
    if podcast.allowed_regions:
        form.allowed_regions.data = podcast.allowed_regions.split(' ')
    return render_template('podcast/edit.html', form=form)

@pod.route('/episode/<episode_id>/edit/', methods=['POST','GET'])
def edit_ep(episode_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    user = User.query.get_or_404(user_id)
    episode = Episode.query.get_or_404(episode_id)
    if episode.podcast.user_id != user_id:
        abort(404)
    form = EpisodeEdit()

    if form.validate_on_submit():
        episode.title = form.title.data
        episode.description = form.description.data
        image = form.image.data
        if image:
            if os.path.exists(episode.image):
                os.remove(episode.image)
            episode.image = os.path.join(current_app.config['UPLOAD_DIR'], secure_filename(image.filename))
            form.image.data.save(episode.image)
        audio = form.audio.data
        if audio:
            if os.path.exists(episode.audio):
                os.remove(episode.audio)
            episode.audio = os.path.join(current_app.config['UPLOAD_DIR'], secure_filename(audio.filename))
            form.audio.data.save(episode.audio)
        episode.allowed_regions = ' '.join(form.allowed_regions.data)
        episode.explicit = form.explicit.data
        episode.episode_type = form.episode_type.data
        db.session.commit()
        return redirect(url_for('podcast.view', podcast_id=episode.podcast_id))
    
    form.title.data = episode.title
    form.description.data = episode.description
    if episode.allowed_regions:
        form.allowed_regions.data = episode.allowed_regions.split(' ')
    form.explicit.data = episode.explicit
    form.episode_type.data = episode.episode_type
    return render_template('podcast/edit_ep.html', form=form)

@pod.route('/episode/<episode_id>/delete/')
def delete_ep(episode_id):
    if 'user' not in session:
        return redirect(url_for('auth.signin'))
    user_id = session.get('user')
    episode = Episode.query.get_or_404(episode_id)
    if episode.podcast.user_id != user_id:
        abort(404)
    if os.exists(episode.image):
        os.remove(episode.image)
    if os.exists(episode.audio):
        os.remove(episode.audio)
    db.session.delete(episode)
    db.session.commit()
    return redirect(url_for('podcast.show', podcast_id=episode.podcast_id))

@pod.route('/<podcast_id>/rss/')
def feed(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)
    feed = PodcastFeed(podcast)
    rss = feed.to_str()
    return Response(rss, mimetype='application/rss+xml')