from flask import request, jsonify
from database import db
from models import Artist, Song, Label
from utils import popularity_cache, calculate_popularity

class SongAPI:
    @staticmethod
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
    def get_song(song_id):
        song = Song.query.get_or_404(str(song_id))
        artist = song.artist
        popularity_score = calculate_popularity(song)  # Use cached value if available
        return jsonify({
            'id': str(song.id),
            'title': song.title,
            'genre': song.genre,
            'plays': song.plays,
            'likes': song.likes,
            'shares': song.shares,
            'popularity_score': popularity_score,
            'artist': {'id': str(artist.id), 'name': artist.name}
        })

    @staticmethod
    def update_song(song_id):
        data = request.get_json()
        song = Song.query.get_or_404(str(song_id))

        song.title = data.get('title', song.title)
        song.genre = data.get('genre', song.genre)
        song.plays = data.get('plays', song.plays)
        song.likes = data.get('likes', song.likes)
        song.shares = data.get('shares', song.shares)

        db.session.commit()

        # Invalidate the cache for this song's popularity score
        popularity_cache[song.id] = calculate_popularity(song)

        return jsonify({
            'message': 'Song updated successfully',
            'popularity_score': popularity_cache[song.id]
        })
    
    @staticmethod
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
    
    @staticmethod
    def get_all_songs_popularity():
        songs = Song.query.all()
        popularity_scores = []
        for song in songs:
            popularity_scores.append({
                'song_id': str(song.id),
                'popularity_score': calculate_popularity(song)
            })
        return jsonify(popularity_scores)