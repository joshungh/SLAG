import pytest
from src.core.clients.pinecone_client import init_pinecone

def test_pinecone_client_creation():
    """Test that Pinecone client can be created"""
    index = init_pinecone()
    assert index is not None
    # Verify index has expected methods
    assert hasattr(index, 'upsert')
    assert hasattr(index, 'query') 