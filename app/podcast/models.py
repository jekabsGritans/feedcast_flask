from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app import db

class Model(db.Model):

    __abstract__  = True

    id = db.Column(Integer, primary_key=True)
    date_created  = db.Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                                           onupdate=func.current_timestamp())


class Podcast(Model):
    user_id = db.Column(Integer, db.ForeignKey('user.id'), nullable=False)
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(100), unique=True, nullable=False)
    link = db.Column(String(100), unique=True, nullable=False)
    description = db.Column(Text)
    language = db.Column(String(20), nullable=False)
    author_name = db.Column(String(100), nullable=False)
    author_email = db.Column(String(100), nullable=False)
    image = db.Column(String(100), nullable=False)
    explicit = db.Column(Boolean, nullable=False)
    categories = db.Column(String, nullable=False)
    series_episodic = db.Column(Boolean, nullable=False)
    allowed_regions = db.Column(String)
    ep_limit = db.Column(Integer)
    origin = db.Column(String(50), nullable=False)
    
    episodes = relationship('Episode', backref='podcast', lazy='select')

    def __init__(self, user_id):
        self.user_id = user_id
    
    def __repr__(self):
        return f"Podcast({self.title})"
    
class Episode(Model):
    id = db.Column(Integer, primary_key=True)
    podcast_id = db.Column(Integer, db.ForeignKey('podcast.id'), nullable=False)
    audio = db.Column(String(100), nullable=False)
    audio_type = db.Column(String(50), nullable=False)
    audio_bytes = db.Column(Integer, nullable=False)
    pubdate = db.Column(DateTime(timezone=True), server_default=func.now())
    title = db.Column(String(100))
    description = db.Column(Text)
    allowed_regions = db.Column(String)
    duration = db.Column(Integer, nullable=False)
    itunes_order = db.Column(Integer)
    explicit = db.Column(Boolean, nullable=False)
    image = db.Column(String(100), nullable=False)
    keywords = db.Column(Text)
    episode_type = db.Column(String(10), nullable=False)

    def __init__(self, podcast_id):
        self.podcast_id = podcast_id

    def __repr__(self):
        return f"Episode({self.title})"
