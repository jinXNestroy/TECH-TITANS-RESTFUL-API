from app import app
from database import db
from utils import calculate_flat_rate
from models import Artist, Song, Label
from faker import Faker
import random

fake = Faker()

def seed_data():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create artists
    artists = [Artist(name=fake.name()) for _ in range(10)]
    db.session.add_all(artists)
    db.session.commit()
    
    # Create random songs and associate with artists
    songs = []
    for artist in artists:
        for _ in range(random.randint(2, 5)):  
            song = Song(
                title=fake.sentence(nb_words=3),
                genre=fake.word(ext_word_list=['Pop', 'Rock', 'Hip Hop', 'Afrobeat', 'Jazz']),
                plays=random.randint(100, 2000000),
                likes=random.randint(50, 500000),
                shares=random.randint(10, 100000),
                artist_id=artist.id,
                popularity_score=random.uniform(0.0, 100.0)  # Random popularity score
            )
            songs.append(song)
    db.session.add_all(songs)
    db.session.commit()

    # Create labels
    labels = [
        Label(
            name=fake.company(),
            type=random.choice(['local', 'international']),
            flat_rate=calculate_flat_rate(random.choice(['local', 'international']))
        )
        for _ in range(5)
    ]
    db.session.add_all(labels)
    db.session.commit()
    
    # Associate labels with artists and songs
    for label in labels:
        # Randomly select artists and songs to associate with the label
        chosen_artists = random.sample(artists, k=random.randint(1, len(artists)))
        chosen_songs = random.sample(songs, k=random.randint(1, len(songs)))
        
        label.artists.extend(chosen_artists)
        label.songs.extend(chosen_songs)
    
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        seed_data()
