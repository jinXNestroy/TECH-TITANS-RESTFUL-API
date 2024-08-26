from flask import Flask, request, jsonify
from database import db, migrate
from models import Artist, Song

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate.init_app(app, db)

class ArtistAPI:
    @staticmethod
    @app.route('/artists', methods=['POST'])
    def create_artist():
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Artist name is required'}), 400
        
        artist = Artist(name=data['name'])
        db.session.add(artist)
        db.session.commit()
        return jsonify({'id': str(artist.id), 'name': artist.name}), 201
    
    @staticmethod
    @app.route('/artists', methods=['GET'])
    def get_all_artists():
        artists = Artist.query.all()
        return jsonify([{'id': str(artist.id), 'name': artist.name} for artist in artists])

class SongAPI:
    @staticmethod
    @app.route('/songs', methods=['POST'])
    def create_song():
        data = request.get_json()
        if not data or not data.get('title') or not data.get('artist_id'):
            return jsonify({'error': 'Song title and artist ID are required'}), 400

        artist = Artist.query.get(data['artist_id'])
        if not artist:
            return jsonify({'error': 'Artist not found'}), 404

        song = Song(
            title=data['title'],
            genre=data.get('genre', ''),
            plays=data.get('plays', 0),
            likes=data.get('likes', 0),
            shares=data.get('shares', 0),
            artist_id=artist.id
        )
        db.session.add(song)
        db.session.commit()

        return jsonify({
            'id': str(song.id),
            'title': song.title,
            'genre': song.genre,
            'artist': {'id': str(artist.id), 'name': artist.name}
        }), 201

    @staticmethod
    @app.route('/songs/<uuid:song_id>', methods=['GET'])
    def get_song(song_id):
        song = Song.query.get_or_404(str(song_id))
        artist = song.artist
        return jsonify({
            'id': str(song.id),
            'title': song.title,
            'genre': song.genre,
            'plays': song.plays,
            'likes': song.likes,
            'shares': song.shares,
            'popularity_score': calculate_popularity(song),
            'artist': {'id': str(artist.id), 'name': artist.name}
        })

    @staticmethod
    @app.route('/songs/<uuid:song_id>', methods=['PUT'])
    def update_song(song_id):
        data = request.get_json()
        song = Song.query.get_or_404(str(song_id))

        song.title = data.get('title', song.title)
        song.genre = data.get('genre', song.genre)
        song.plays = data.get('plays', song.plays)
        song.likes = data.get('likes', song.likes)
        song.shares = data.get('shares', song.shares)

        db.session.commit()
        calculate_popularity(song)
        return jsonify({
            'message': 'Song updated successfully',
            'popularity_score': song.popularity_score
        })
    @staticmethod
    @app.route('/songs', methods=['GET'])
    def get_all_songs():
        songs = Song.query.all()
        return jsonify([{
            'id': str(song.id),
            'title': song.title,
            'genre': song.genre,
            'artist': {
                'id': str(song.artist.id),
                'name': song.artist.name
            }
        } for song in songs])

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return jsonify(error='An unexpected error occurred'), 500

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Server Error: {e}, Route: {request.url}")
    return jsonify(error='An unexpected error occurred'), 500

def calculate_popularity(song):
    """Calculate and store the popularity score."""
    if song.popularity_score == 0.0:
        song.popularity_score = (song.plays * 0.5) + (song.likes * 0.3) + (song.shares * 0.2)
        db.session.commit()
    return song.popularity_score

if __name__ == '__main__':
    app.run(debug=True)
