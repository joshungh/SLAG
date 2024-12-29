import pytest
import time
from typing import List
import logging
from src.core.services.pinecone_service import PineconeService
from src.core.services.bedrock_service import BedrockService
from src.core.utils.logging import setup_logger

logger = setup_logger('test_pinecone')

class TestContext:
    """Context for tracking test resources"""
    def __init__(self):
        self.vector_ids: List[str] = []
        self.logger = logger

@pytest.fixture
def test_context():
    return TestContext()

@pytest.fixture
def pinecone_service():
    return PineconeService()

@pytest.fixture
def bedrock_service():
    return BedrockService()

@pytest.fixture(autouse=True)
async def cleanup(pinecone_service, test_context):
    """Cleanup fixture that runs after each test"""
    logger.info("Starting test cleanup")
    yield
    
    if test_context.vector_ids:
        logger.info(f"Cleaning up {len(test_context.vector_ids)} vectors by ID")
        logger.debug(f"Vector IDs to delete: {test_context.vector_ids}")
        await pinecone_service.delete_vectors(test_context.vector_ids)
    
    logger.info("Cleaning up test story vectors by metadata")
    await pinecone_service.delete_by_metadata({
        'story_id': {'$in': ['test-story-1', 'test-story-2']}
    })
    logger.info("Cleanup complete")

@pytest.mark.asyncio
async def test_upsert_and_query(pinecone_service, bedrock_service, test_context):
    """Test upserting text and querying it back"""
    logger.info("Starting upsert and query test")
    
    # Generate test content
    text = "The curious cat prowled through the moonlit garden, her whiskers twitching."
    logger.debug(f"Generating embeddings for text: {text}")
    embeddings = await bedrock_service.get_embeddings(text)
    logger.debug(f"Generated embeddings of length: {len(embeddings)}")
    
    # Test metadata
    metadata = {
        'story_id': 'test-story-1',
        'phase': 'world-building',
        'timestamp': '2024-03-20T12:00:00Z'
    }
    logger.debug(f"Using metadata: {metadata}")
    
    # Upsert the vector
    logger.info("Upserting vector")
    vector_id = await pinecone_service.upsert_text(
        text=text,
        embeddings=embeddings,
        metadata=metadata
    )
    test_context.vector_ids.append(vector_id)
    logger.info(f"Vector upserted with ID: {vector_id}")
    
    # Wait for index to be ready
    logger.info("Waiting for index to be ready...")
    time.sleep(1)  # Give Pinecone time to index
    
    # Query it back
    query_text = "cat in garden at night"
    logger.info(f"Querying with text: {query_text}")
    query_embeddings = await bedrock_service.get_embeddings(query_text)
    
    results = await pinecone_service.query_similar(
        embeddings=query_embeddings,
        top_k=1,
        filter={'story_id': 'test-story-1'}
    )
    
    logger.info(f"Query returned {len(results)} results")
    
    # More defensive assertions
    assert len(results) > 0, "Query should return at least one result"
    
    if len(results) > 0:
        logger.debug(f"First result score: {results[0].score}")
        logger.debug(f"First result metadata: {results[0].metadata}")
        
        assert results[0].metadata['text'] == text
        assert results[0].metadata['story_id'] == 'test-story-1'
        assert results[0].score > 0.5  # Verify semantic similarity
        logger.info("All assertions passed")
    else:
        logger.error("No results found in query")
        logger.debug(f"Original vector ID: {vector_id}")
        raise AssertionError("No results found in query")

@pytest.mark.asyncio
async def test_metadata_filtering(pinecone_service, bedrock_service, test_context):
    """Test filtering by metadata"""
    logger.info("Starting metadata filtering test")
    
    texts = [
        "The dragon soared through clouds of amber and gold.",
        "The wizard's tower gleamed in the setting sun.",
        "The ancient spell book contained forbidden knowledge."
    ]
    
    logger.info(f"Upserting {len(texts)} test vectors")
    for i, text in enumerate(texts):
        logger.debug(f"Processing text {i+1}: {text}")
        embeddings = await bedrock_service.get_embeddings(text)
        
        metadata = {
            'story_id': 'test-story-2',
            'phase': f'phase-{i}',
            'genre': 'fantasy'
        }
        logger.debug(f"Using metadata: {metadata}")
        
        vector_id = await pinecone_service.upsert_text(
            text=text,
            embeddings=embeddings,
            metadata=metadata
        )
        test_context.vector_ids.append(vector_id)
        logger.debug(f"Vector {i+1} upserted with ID: {vector_id}")
    
    query = "magic and fantasy"
    logger.info(f"Querying with text: {query}")
    query_embeddings = await bedrock_service.get_embeddings(query)
    
    filter_params = {
        'genre': 'fantasy',
        'story_id': 'test-story-2'
    }
    logger.debug(f"Using filter: {filter_params}")
    
    results = await pinecone_service.query_similar(
        embeddings=query_embeddings,
        top_k=3,
        filter=filter_params
    )
    
    logger.info(f"Query returned {len(results)} results")
    for i, result in enumerate(results):
        logger.debug(f"Result {i+1} score: {result.score}")
    
    assert len(results) == 3
    for result in results:
        assert result.metadata['genre'] == 'fantasy'
        assert result.metadata['story_id'] == 'test-story-2'
    logger.info("All assertions passed") 