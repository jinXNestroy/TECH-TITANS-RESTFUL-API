from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after initializing db to avoid circular imports
from models import Artist, Song

def calculate_popularity(song):
    """Calculate and store the popularity score."""
    if song.popularity_score == 0.0:
        song.popularity_score = (song.plays * 0.5) + (song.likes * 0.3) + (song.shares * 0.2)
        db.session.commit()
    return song.popularity_score

# Routes
@app.route('/artists', methods=['POST'])
def create_artist():
    data = request.get_json()
    artist = Artist(name=data['name'])
    db.session.add(artist)
    db.session.commit()
    return jsonify({'id': artist.id, 'name': artist.name}), 201

@app.route('/songs', methods=['POST'])
def create_song():
    data = request.get_json()
    song = Song(
        title=data['title'], 
        genre=data['genre'], 
        plays=data.get('plays', 0),
        likes=data.get('likes', 0), 
        shares=data.get('shares', 0), 
        artist_id=data['artist_id']
    )
    db.session.add(song)
    db.session.commit()
    calculate_popularity(song)
    return jsonify({'id': song.id, 'title': song.title, 'genre': song.genre, 'artist_id': song.artist_id}), 201

@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = Song.query.get_or_404(song_id)
    popularity = calculate_popularity(song)
    return jsonify({
        'id': song.id,
        'title': song.title,
        'genre': song.genre,
        'plays': song.plays,
        'likes': song.likes,
        'shares': song.shares,
        'popularity_score': popularity,
        'artist_id': song.artist_id
    })

@app.route('/songs', methods=['GET'])
def get_songs():
    songs = Song.query.filter_by(is_deleted=False).all()
    return jsonify([{
        'id': song.id, 
        'title': song.title, 
        'genre': song.genre, 
        'artist_id': song.artist_id, 
        'popularity_score': calculate_popularity(song)
    } for song in songs])

@app.route('/songs/<int:song_id>', methods=['DELETE'])
def soft_delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    song.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Song soft deleted successfully'})

@app.route('/songs/<int:song_id>/restore', methods=['PATCH'])
def restore_song(song_id):
    song = Song.query.get_or_404(song_id)
    if song.is_deleted:
        song.is_deleted = False
        db.session.commit()
        return jsonify({'message': 'Song restored successfully'})
    else:
        return jsonify({'message': 'Song is not deleted'}), 400

@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    data = request.get_json()
    song = Song.query.get_or_404(song_id)
    song.plays = data.get('plays', song.plays)
    song.likes = data.get('likes', song.likes)
    song.shares = data.get('shares', song.shares)
    db.session.commit()
    calculate_popularity(song)
    return jsonify({'message': 'Song updated successfully', 'popularity_score': song.popularity_score})

if __name__ == '__main__':
    app.run(debug=True)
