import uuid
from database import db
from sqlalchemy.dialects.sqlite import TEXT

class Artist(db.Model):
    id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    songs = db.relationship('Song', backref='artist', lazy=True)

class Song(db.Model):
    id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    plays = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    artist_id = db.Column(TEXT, db.ForeignKey('artist.id'), nullable=False)
    popularity_score = db.Column(db.Float, default=0.0)
