# utils.py
popularity_cache = {}

def calculate_popularity(song):
    """Calculate and store the popularity score as a percentage, using a cache for optimization."""
    if song.id in popularity_cache:
        return popularity_cache[song.id]

    # Calculate the popularity score if not already in cache
    total_engagement = song.plays + song.likes + song.shares
    score = (song.likes + song.shares) / total_engagement if total_engagement > 0 else 0
    popularity_cache[song.id] = score 

    return score

def calculate_flat_rate(label_type):
    if label_type == 'local':
        return 50000.0
    elif label_type == 'international':
        return 75000.0
    else:
        raise ValueError('Invalid label type')
    

def calculate_artist_revenue(artist):
    artist_revenue = {}
    total_artist_revenue = 0
    
    for song in artist.songs:
        revenue = 0
        popularity_score = calculate_popularity(song)
        for label in song.labels:  
            flat_rate = calculate_flat_rate(label.type)
            revenue += popularity_score * flat_rate
        
        artist_revenue[song.id] = {
            'song_name': song.title, 
            'revenue': int(revenue)
        }
        total_artist_revenue += revenue
    
    artist_revenue['total_artist_revenue'] = int(total_artist_revenue)
    return artist_revenue


def calculate_label_revenue(label):
    label_revenue = {}
    total_label_revenue = 0
    
    for song in label.songs:
        revenue = 0
        popularity_score = calculate_popularity(song)
        
        # Iterate over labels associated with the song to compute revenue
        for song_label in song.labels:
            if song_label.id == label.id:  # Only consider the current label
                flat_rate = calculate_flat_rate(label.type)
                revenue += popularity_score * flat_rate
        
        label_revenue[song.id] = {
            'song_name': song.title,  # Include song name
            'revenue': int(revenue)
        }
        total_label_revenue += revenue
    
    label_revenue['total_label_revenue'] = int(total_label_revenue)
    return label_revenue
