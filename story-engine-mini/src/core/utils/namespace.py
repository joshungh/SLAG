import uuid
from datetime import datetime
import re
import time

def create_story_namespace(story_id: str, genre: str) -> str:
    """
    Create a unique namespace for story content
    Format: genre_storyid_timestamp
    Example: fantasy_abc123_20240318_123456
    """
    # Clean genre string
    clean_genre = re.sub(r'[^a-zA-Z0-9]', '_', genre.lower()) if genre else 'unspecified'
    clean_genre = re.sub(r'_+', '_', clean_genre).strip('_')
    
    # Clean story_id
    clean_id = re.sub(r'[^a-zA-Z0-9]', '_', story_id)
    
    # Add microseconds to ensure uniqueness
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')
    
    return f"{clean_genre}_{clean_id}_{timestamp}" 