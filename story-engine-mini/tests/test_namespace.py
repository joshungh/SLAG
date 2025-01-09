import pytest
from src.core.utils.namespace import create_story_namespace
import re

def test_namespace_creation():
    """Test namespace creation format and uniqueness"""
    story_id = "abc123"
    genre = "Science Fiction"
    
    # Test basic creation
    namespace = create_story_namespace(story_id, genre)
    
    # Check format: genre_storyid_timestamp
    pattern = r'science_fiction_abc123_\d{8}_\d{6}'
    assert re.match(pattern, namespace)
    
    # Test uniqueness
    namespace2 = create_story_namespace(story_id, genre)
    assert namespace != namespace2  # Should be different due to timestamp

def test_namespace_special_characters():
    """Test namespace handling of special characters"""
    story_id = "test#123"
    genre = "Magical-Realism & Fantasy"
    
    namespace = create_story_namespace(story_id, genre)
    assert ' ' not in namespace
    assert '&' not in namespace
    assert '-' not in namespace 