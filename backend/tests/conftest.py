import pytest
from src.services.rag_service import RAGService
from src.services.bedrock_service import BedrockService
from src.services.pinecone_service import PineconeService
from src.services.story_engine_service import StoryEngineService
from src.config.config import Settings
from src.utils.path_utils import get_reference_doc_path
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

@pytest.fixture
def settings():
    """Initialize settings"""
    load_dotenv()
    settings = Settings()
    logger.info(f"Pinecone API Key: {settings.PINECONE_API_KEY[:8]}...")
    logger.info(f"Pinecone Environment: {settings.PINECONE_ENVIRONMENT}")
    return settings

@pytest.fixture
async def rag_service(settings):
    """Initialize RAG service with test data"""
    logger.info("Initializing RAG service...")
    bedrock = BedrockService(settings)
    pinecone = PineconeService(settings)
    rag = RAGService(bedrock, pinecone)
    
    # Add debug logging
    logger.info("Indexing test documents...")
    
    # Index essential test documents
    test_docs = [
        {
            "path": get_reference_doc_path("characters/character-chen.txt"),
            "type": "character_profile",
            "metadata": {
                "type": "character_profile",
                "name": "Dr. James Chen",
                "current_location": "Station Omega"
            },
            "namespace": "characters"
        },
        {
            "path": get_reference_doc_path("world/slag-locations.txt"),
            "type": "location",
            "metadata": {
                "type": "location",
                "name": "Station Omega",
                "location_type": "station"
            },
            "namespace": "locations"
        },
        {
            "path": get_reference_doc_path("story-planning/initial-story-plan.txt"),
            "type": "story_planning",
            "metadata": {
                "type": "story_planning",
                "category": "initial_setup"
            },
            "namespace": "story_planning"
        }
    ]
    
    # Index each document
    for doc in test_docs:
        success = await rag.index_document(
            document_path=doc["path"],
            document_type=doc["type"],
            metadata=doc["metadata"],
            namespace=doc["namespace"]
        )
        assert success, f"Failed to index {doc['path']}"
        logger.info(f"Indexed test document: {doc['path']}")
    
    logger.info("RAG service initialization complete")
    return rag

@pytest.fixture
async def story_engine(rag_service):
    """Initialize story engine with test data"""
    # First await the rag_service since it's an async fixture
    rag = await rag_service
    # Then initialize the story engine
    engine = await StoryEngineService.initialize(rag)
    return engine

@pytest.fixture
def test_story_data():
    """Provide test story data"""
    return {
        "main_characters": ["Dr. James Chen", "Commander Drake"],
        "starting_location": "Station Omega",
        "initial_plot_thread": "initial_crisis",
        "chapter_1_scenes": [
            {
                "scene_type": "discovery",
                "characters": ["Dr. James Chen"],
                "location": "Research Lab",
                "plot_points": ["Strange Fragment readings"]
            }
        ]
    }
  