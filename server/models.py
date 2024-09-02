import uuid
from database import db
from sqlalchemy.dialects.sqlite import TEXT

# Association tables
label_artist = db.Table('label_artist',
    db.Column('label_id', TEXT, db.ForeignKey('label.id'), nullable=False),
    db.Column('artist_id', TEXT, db.ForeignKey('artist.id'), nullable=False),
    db.PrimaryKeyConstraint('label_id', 'artist_id')
)

label_song = db.Table('label_song',
    db.Column('label_id', TEXT, db.ForeignKey('label.id'), nullable=False),
    db.Column('song_id', TEXT, db.ForeignKey('song.id'), nullable=False),
    db.PrimaryKeyConstraint('label_id', 'song_id')
)

class Artist(db.Model):
    id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    songs = db.relationship('Song', back_populates='artist', lazy=True)
    labels = db.relationship('Label', secondary=label_artist, back_populates='artists')

class Song(db.Model):
    id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    plays = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    artist_id = db.Column(TEXT, db.ForeignKey('artist.id'), nullable=False)
    popularity_score = db.Column(db.Float, default=0.0)
    artist = db.relationship('Artist', back_populates='songs')
    labels = db.relationship('Label', secondary=label_song, back_populates='songs')

class Label(db.Model):
    id = db.Column(TEXT, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) 
    flat_rate = db.Column(db.Float, nullable=False, default=0.0)

    artists = db.relationship('Artist', secondary=label_artist, back_populates='labels')
    songs = db.relationship('Song', secondary=label_song, back_populates='labels')
