from app import app
from database import db
from models import Artist, Song
from faker import Faker
import random

fake = Faker()

def seed_data():

    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()
    # Create random artists
    artists = [Artist(name=fake.name()) for _ in range(10)]  # Generate 10 artists
    
    # Add artists to the session
    db.session.add_all(artists)
    
    # Commit to save artists
    db.session.commit()
    
    # Create random songs
    songs = []
    for artist in artists:
        for _ in range(random.randint(2, 5)):  # Each artist has between 2 and 5 songs
            song = Song(
                title=fake.sentence(nb_words=3),
                genre=fake.word(ext_word_list=['Pop', 'Rock', 'Hip Hop', 'Afrobeat', 'Jazz']),
                plays=random.randint(100, 2000000),
                likes=random.randint(50, 500000),
                shares=random.randint(10, 100000),
                artist_id=artist.id
            )
            songs.append(song)
    
    # Add songs to the session
    db.session.add_all(songs)
    
    # Commit to save songs
    db.session.commit()
    
    print("Seed data inserted successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_data()
