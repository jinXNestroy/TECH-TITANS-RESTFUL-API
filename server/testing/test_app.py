import unittest
import json
from app import app, db
from models import Artist, Song

class BasicTests(unittest.TestCase):

    # Executed before each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
        self.app = app.test_client()
        
        # Push an application context
        self.ctx = app.app_context()
        self.ctx.push()

        db.create_all()

    # Executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

        # Pop the application context
        self.ctx.pop()

    def test_create_artist(self):
        response = self.app.post('/artists', data=json.dumps({
            'name': 'Test Artist'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Test Artist')

    def test_create_song(self):
        # First create an artist
        artist_response = self.app.post('/artists', data=json.dumps({
            'name': 'Test Artist'
        }), content_type='application/json')
        artist_data = json.loads(artist_response.data)
        
        # Now create a song with the artist's UUID
        response = self.app.post('/songs', data=json.dumps({
            'title': 'Test Song',
            'genre': 'Test Genre',
            'artist_id': artist_data['id']
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Test Song')
        self.assertEqual(data['artist']['id'], artist_data['id'])

    def test_get_song(self):
        # First create an artist
        artist_response = self.app.post('/artists', data=json.dumps({
            'name': 'Test Artist'
        }), content_type='application/json')
        artist_data = json.loads(artist_response.data)

        # Then create a song with the artist's UUID
        song_response = self.app.post('/songs', data=json.dumps({
            'title': 'Test Song',
            'genre': 'Test Genre',
            'artist_id': artist_data['id']
        }), content_type='application/json')
        song_data = json.loads(song_response.data)

        # Now get the song using the UUID
        response = self.app.get(f'/songs/{song_data["id"]}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], song_data['id'])
        self.assertEqual(data['title'], 'Test Song')
        self.assertEqual(data['artist']['id'], artist_data['id'])

    def test_get_all_songs(self):
        # First create an artist
        artist_response = self.app.post('/artists', data=json.dumps({
            'name': 'Test Artist'
        }), content_type='application/json')
        artist_data = json.loads(artist_response.data)

        # Create a couple of songs with the artist's UUID
        self.app.post('/songs', data=json.dumps({
            'title': 'Test Song 1',
            'genre': 'Test Genre',
            'artist_id': artist_data['id']
        }), content_type='application/json')

        self.app.post('/songs', data=json.dumps({
            'title': 'Test Song 2',
            'genre': 'Test Genre',
            'artist_id': artist_data['id']
        }), content_type='application/json')

        # Now get all songs
        response = self.app.get('/songs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_update_song(self):
        # First create an artist
        artist_response = self.app.post('/artists', data=json.dumps({
            'name': 'Test Artist'
        }), content_type='application/json')
        artist_data = json.loads(artist_response.data)

        # Then create a song with the artist's UUID
        song_response = self.app.post('/songs', data=json.dumps({
            'title': 'Test Song',
            'genre': 'Test Genre',
            'artist_id': artist_data['id']
        }), content_type='application/json')
        song_data = json.loads(song_response.data)

        # Now update the song
        response = self.app.put(f'/songs/{song_data["id"]}', data=json.dumps({
            'title': 'Updated Song Title',
            'plays': 100,
            'likes': 50,
            'shares': 20
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Song updated successfully')
    
    def test_get_all_artists(self):
        # Create a couple of artists
        self.app.post('/artists', data=json.dumps({
            'name': 'Test Artist 1'
        }), content_type='application/json')

        self.app.post('/artists', data=json.dumps({
            'name': 'Test Artist 2'
        }), content_type='application/json')

        # Now get all artists
        response = self.app.get('/artists')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

if __name__ == "__main__":
    unittest.main()
