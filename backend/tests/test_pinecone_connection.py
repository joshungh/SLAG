import pytest
import asyncio
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from typing import List, Dict
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

@pytest.fixture(scope="module")
def pinecone_service():
    """Initialize Pinecone directly"""
    load_dotenv()
    
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index("slag-index")
    
    class PineconeWrapper:
        def __init__(self, index):
            self.index = index
            
        async def upsert_vectors(self, vectors, namespace):
            formatted_vectors = [
                {
                    "id": id,
                    "values": vec,
                    "metadata": meta
                }
                for id, vec, meta in vectors
            ]
            logger.info(f"Upserting vectors: {formatted_vectors}")
            self.index.upsert(vectors=formatted_vectors, namespace=namespace)
            
        async def similarity_search(self, vector, namespace, top_k=3, filter=None):
            logger.info(f"Searching in namespace: {namespace} with vector of length {len(vector)}")
            results = self.index.query(
                vector=vector,
                top_k=top_k,
                filter=filter,
                include_values=True,
                include_metadata=True,
                namespace=namespace
            )
            logger.info(f"Raw query results: {results}")
            return [
                {
                    "id": match["id"],
                    "score": match["score"],
                    "metadata": match["metadata"]
                }
                for match in results["matches"]
            ]
            
        async def delete_vectors(self, ids, namespace):
            self.index.delete(ids=ids, namespace=namespace)
            
        async def describe_index_stats(self):
            """Get index statistics"""
            return self.index.describe_index_stats()
    
    return PineconeWrapper(index)

@pytest.mark.asyncio
async def test_pinecone_connection(pinecone_service):
    """Test basic Pinecone operations"""
    logger.info("Starting Pinecone connection test")
    
    # Check initial index stats
    stats = await pinecone_service.describe_index_stats()
    logger.info(f"Initial index stats: {stats}")
    
    test_vector = [0.1] * 1536
    test_metadata = {"type": "test", "description": "connection test"}
    test_id = "test-id-1"
    
    try:
        # Upsert vector
        await pinecone_service.upsert_vectors(
            vectors=[(test_id, test_vector, test_metadata)],
            namespace="test"
        )
        logger.info("Vector upserted successfully")
        
        # Wait a moment for the upsert to be processed
        time.sleep(2)
        
        # Check stats after upsert
        stats = await pinecone_service.describe_index_stats()
        logger.info(f"Stats after upsert: {stats}")
        
        # Perform search
        results = await pinecone_service.similarity_search(
            vector=test_vector,
            namespace="test",
            top_k=1
        )
        logger.info(f"Search results: {results}")
        
        assert len(results) > 0, "No results returned from search"
        assert results[0]["id"] == test_id, f"Expected {test_id}, got {results[0]['id']}"
        
        # Cleanup
        await pinecone_service.delete_vectors([test_id], namespace="test")
        logger.info("Test completed successfully")
        
        # Final stats check
        stats = await pinecone_service.describe_index_stats()
        logger.info(f"Final index stats: {stats}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise