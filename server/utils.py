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
