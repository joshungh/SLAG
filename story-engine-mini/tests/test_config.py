import pytest
from src.config import settings

def test_settings_load():
    """Test that settings load correctly"""
    assert settings.AWS_REGION == "us-west-2"
    assert settings.PINECONE_DIMENSION == 1536
    assert settings.BEDROCK_MODEL_ID == "anthropic.claude-3-5-sonnet-20241022-v2:0"

def test_required_env_vars():
    """Test that required environment variables are set"""
    assert settings.PINECONE_API_KEY is not None, "PINECONE_API_KEY must be set"
    assert settings.AWS_ACCESS_KEY_ID is not None, "AWS_ACCESS_KEY_ID must be set"
    assert settings.AWS_SECRET_ACCESS_KEY is not None, "AWS_SECRET_ACCESS_KEY must be set" 