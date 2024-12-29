import pytest
from src.core.clients.bedrock import get_bedrock_client

def test_bedrock_client_creation():
    """Test that Bedrock client can be created"""
    client = get_bedrock_client()
    assert client is not None
    # Verify client has expected methods
    assert hasattr(client, 'invoke_model') 