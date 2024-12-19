import pytest
from dotenv import load_dotenv
from src.services.pinecone_service import PineconeService
from src.config.config import Settings

@pytest.fixture
def pinecone_service():
    load_dotenv()
    settings = Settings()
    return PineconeService(settings)

async def test_pinecone_connection(pinecone_service):
    """Test basic Pinecone operations"""
    # Test vector
    test_vector = [0.1] * 1536  # 1536-dimensional test vector
    test_metadata = {"type": "test", "description": "connection test"}
    
    # Test upsert
    await pinecone_service.upsert_vectors(
        vectors=[("test-id", test_vector, test_metadata)],
        namespace="test"
    )
    
    # Test query
    results = await pinecone_service.similarity_search(
        vector=test_vector,
        namespace="test",
        top_k=1
    )
    
    assert len(results) > 0
    assert results[0]["id"] == "test-id"
    
    # Cleanup
    await pinecone_service.delete_vectors(["test-id"], namespace="test") 