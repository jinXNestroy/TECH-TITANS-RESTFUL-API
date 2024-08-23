from app import db

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    songs = db.relationship('Song', backref='artist', lazy=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    plays = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    popularity_score = db.Column(db.Float, default=0.0)
    is_deleted = db.Column(db.Boolean, default=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
