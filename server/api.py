from flask import request, jsonify
from database import db
from models import Artist, Song
from utils import calculate_popularity, popularity_cache

class ArtistAPI:
    @staticmethod
    def create_artist():
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({'error': 'Artist name is required'}), 400
        
        artist = Artist(name=data['name'])
        db.session.add(artist)
        db.session.commit()
        return jsonify({'id': str(artist.id), 'name': artist.name}), 201
    
    @staticmethod
    def get_all_artists():
        artists = Artist.query.all()
        return jsonify([{'id': str(artist.id), 'name': artist.name} for artist in artists])
    
    @staticmethod
    def get_all_artists_popularity():
        artists = Artist.query.all()
        popularity_scores = []
        for artist in artists:
            songs = Song.query.filter_by(artist_id=artist.id).all()
            if songs:
                song_popularity_scores = [calculate_popularity(song) for song in songs]
                average_popularity = sum(song_popularity_scores) / len(song_popularity_scores)
            else:
                average_popularity = 0
            popularity_scores.append({
                'artist_id': str(artist.id),
                'artist_name': artist.name,
                'popularity_score': average_popularity
            })
        return jsonify(popularity_scores)

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
