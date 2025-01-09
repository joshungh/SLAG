import pytest
from botocore.exceptions import ClientError
from src.core.services.bedrock_service import BedrockService

@pytest.fixture
def bedrock_service():
    return BedrockService()

@pytest.mark.asyncio
async def test_text_generation(bedrock_service):
    """Test basic text generation"""
    try:
        prompt = "Write a one-paragraph story about a curious cat."
        response = await bedrock_service.generate_text(prompt, max_tokens=200)
        
        assert isinstance(response, str)
        assert len(response) > 0
        # Look for cat-related terms instead of just "cat"
        cat_terms = ["whiskers", "paw", "purr", "meow", "feline", "cat"]
        assert any(term in response.lower() for term in cat_terms), "Story should contain cat-related terms"
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            pytest.skip("No access to Bedrock model - check AWS permissions")
        raise

@pytest.mark.asyncio
async def test_embedding_generation(bedrock_service):
    """Test embedding generation"""
    text = "This is a test sentence for embedding generation."
    embeddings = await bedrock_service.get_embeddings(text)
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == 1536  # Titan embeddings are 1536-dimensional
    assert all(isinstance(x, float) for x in embeddings) 