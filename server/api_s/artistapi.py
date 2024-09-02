from flask import request, jsonify
from database import db
from models import Artist, Song
from utils import calculate_popularity, calculate_artist_revenue

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

    @staticmethod
    def get_all_revenue():
        artists = Artist.query.all()
        artist_revenues = []
        for artist in artists:
            artist_revenue = calculate_artist_revenue(artist)
            # Include the artist's revenue details in the response
            artist_revenues.append({
                'artist_id': str(artist.id),
                'artist_name': artist.name,
                'songs': artist_revenue  # Include song revenue details
            })
        return jsonify(artist_revenues)

    @staticmethod
    def get_artist_revenue(artist_id):
        artist = Artist.query.get(artist_id)
        artist_revenue = calculate_artist_revenue(artist)
        return jsonify(artist_revenue)
