import pytest
from dotenv import load_dotenv
import os
from src.services.bedrock_service import BedrockService
from src.config.config import Settings
import logging
import json
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

@pytest.fixture(scope="module")
def bedrock_service():
    """Initialize BedrockService"""
    load_dotenv()
    settings = Settings()
    return BedrockService(settings)

@pytest.mark.asyncio
async def test_claude_api_interaction(bedrock_service):
    """Test basic interaction with Claude API"""
    logger.info("Starting Claude API test")
    
    try:
        messages = [
            {
                "role": "assistant",
                "content": "I am a helpful assistant. I keep my responses brief and to the point."
            },
            {
                "role": "user",
                "content": "Say hello in exactly 5 words."
            }
        ]
        
        response = await bedrock_service._invoke_claude(messages)
        logger.info(f"Claude response: {response}")
        
        assert isinstance(response, str), "Response should be a string"
        assert len(response.split()) == 5, "Response should be exactly 5 words"
        
        logger.info("Claude API test passed")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

@pytest.mark.asyncio
async def test_generate_embedding(bedrock_service):
    """Test embedding generation using Titan model"""
    logger.info("Starting embedding generation test")
    
    test_cases = [
        "This is a short test sentence.",
        "A" * 100,  # Test longer input
        "Special chars: !@#$%^&*()",  # Test special characters
        " ".join(["word"] * 100),  # Test many words
    ]
    
    for test_text in test_cases:
        try:
            logger.info(f"\nTesting text: {test_text[:50]}...")
            
            # Generate embedding
            embedding = await bedrock_service.generate_embedding(test_text)
            logger.info(f"Generated embedding of length: {len(embedding)}")
            logger.info(f"First 5 values: {embedding[:5]}")
            
            # Verify format
            assert isinstance(embedding, list), "Embedding should be a list"
            assert len(embedding) == 1536, f"Embedding should be 1536-dimensional, got {len(embedding)}"
            assert all(isinstance(x, float) for x in embedding), "All elements should be floats"
            
            # Verify values are not all the same
            unique_values = len(set(embedding[:10]))  # Check first 10 values
            assert unique_values > 1, "Embedding values should vary"
            
            # Log some stats about the embedding
            min_val = min(embedding)
            max_val = max(embedding)
            avg_val = sum(embedding) / len(embedding)
            logger.info(f"Embedding stats - min: {min_val:.3f}, max: {max_val:.3f}, avg: {avg_val:.3f}")
            
            logger.info("Test case passed")
            
        except Exception as e:
            logger.error(f"Test failed for text: {test_text[:50]}...")
            logger.error(f"Error: {str(e)}")
            raise
    
    logger.info("All embedding tests passed")