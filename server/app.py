from flask import Flask, request, jsonify
from database import db, migrate
from api import ArtistAPI, SongAPI

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate.init_app(app, db)

# Initialize a cache for popularity scores
popularity_cache = {}

@app.route('/')
def index():
    return '<h1>Music World</h1>'

app.add_url_rule('/artists', view_func=ArtistAPI.get_all_artists, methods=['GET'])
app.add_url_rule('/artists', view_func=ArtistAPI.create_artist, methods=['POST'])

app.add_url_rule('/songs', view_func=SongAPI.get_all_songs, methods=['GET'])
app.add_url_rule('/songs', view_func=SongAPI.create_song, methods=['POST'])
app.add_url_rule('/songs/<uuid:song_id>', view_func=SongAPI.get_song, methods=['GET'])
app.add_url_rule('/songs/<uuid:song_id>', view_func=SongAPI.update_song, methods=['PUT'])

app.add_url_rule('/artists/popularity', view_func=ArtistAPI.get_all_artists_popularity, methods=['GET'])

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Server Error: {e}, Route: {request.url}")
    return jsonify(error='An unexpected error occurred'), 500

if __name__ == '__main__':
    app.run(debug=True, port=5555)