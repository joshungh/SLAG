import pytest
from src.services.story_engine_service import StoryEngineService
from src.services.rag_service import RAGService
from src.services.bedrock_service import BedrockService
from src.services.pinecone_service import PineconeService
from src.config.config import Settings
from src.models.story_schema import (
    SceneConfig, 
    CharacterArc,
    StoryState,
    PlotThread,
    PlotStatus
)
import logging
from src.utils.path_utils import get_reference_doc_path

logger = logging.getLogger(__name__)

@pytest.fixture
def settings():
    """Initialize settings"""
    return Settings()

@pytest.fixture
def rag_service(settings):
    """Initialize RAG service with dependencies"""
    bedrock = BedrockService(settings)
    pinecone = PineconeService(settings)
    return RAGService(bedrock, pinecone)

@pytest.fixture
def story_engine(rag_service):
    """Initialize StoryEngineService"""
    return StoryEngineService(rag_service)

@pytest.mark.asyncio
async def test_story_initialization(story_engine):
    """Test story state initialization"""
    # First index test documents
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
        }
    ]
    
    for doc in test_docs:
        success = await story_engine.rag.index_document(
            document_path=doc["path"],
            document_type=doc["type"],
            metadata=doc["metadata"],
            namespace=doc["namespace"]
        )
        assert success, f"Failed to index document: {doc['path']}"
    
    # Initialize story
    success = await story_engine.initialize_story(
        main_characters=["Dr. James Chen"],
        starting_location="Station Omega",
        initial_plot_thread="initial_crisis"
    )
    
    assert success, "Story initialization should succeed"
    assert story_engine.current_state.characters, "Should have characters"
    assert story_engine.current_state.current_location, "Should have location"
    assert story_engine.current_state.plot_thread == "initial_crisis"
    
    # Verify character data
    chen = story_engine.current_state.characters[0]
    assert chen.name == "Dr. James Chen"
    assert chen.location == "Station Omega"
    assert chen.status == "active"
    
    # Verify location data
    location = story_engine.current_state.current_location
    assert location.name == "Station Omega"
    assert location.type == "station"
    assert location.current_status == "normal"

@pytest.mark.asyncio
async def test_scene_generation(story_engine):
    """Test basic scene generation"""
    # First initialize story
    await story_engine.initialize_story(
        main_characters=["Dr. James Chen"],
        starting_location="Station Omega",
        initial_plot_thread="initial_crisis"
    )
    
    # Configure test scene
    scene_config = SceneConfig(
        scene_type="dialogue",
        characters=["Dr. James Chen"],
        location="Station Omega",
        plot_points=[
            "Strange readings from Giant artifacts",
            "Growing concern about Fragment activity"
        ],
        tone="tense"
    )
    
    # Generate scene
    scene = await story_engine.generate_scene(scene_config)
    
    assert scene is not None, "Should generate scene"
    assert scene["content"], "Should have scene content"
    assert scene["metadata"], "Should have scene metadata"
    
    # Verify metadata
    metadata = scene["metadata"]
    assert "Station Omega" in metadata["location"]
    assert "Dr. James Chen" in metadata["characters"]
    assert metadata["plot_thread"] == "initial_crisis"

@pytest.mark.asyncio
async def test_scene_context_gathering(story_engine):
    """Test gathering context for scene generation"""
    # Initialize with test data
    await story_engine.initialize_story(
        main_characters=["Dr. James Chen"],
        starting_location="Station Omega",
        initial_plot_thread="initial_crisis"
    )
    
    scene_config = SceneConfig(
        scene_type="dialogue",
        characters=["Dr. James Chen"],
        location="Station Omega",
        plot_points=["Strange readings"]
    )
    
    # Get scene context
    context = await story_engine._gather_scene_context(scene_config)
    
    assert context is not None, "Should gather context"
    assert "characters" in context, "Should have character context"
    assert "location" in context, "Should have location context"
    assert "style" in context, "Should have style guide context"
    
    # Verify context relevance
    assert any("Chen" in str(c) for c in context["characters"]), "Should have character info"
    assert any("Station" in str(l) for l in context["location"]), "Should have location info"
    assert any("dialogue" in str(s) for s in context["style"]), "Should have style info"

@pytest.mark.asyncio
async def test_state_updates(story_engine):
    """Test story state updates after scene generation"""
    # Initialize story
    await story_engine.initialize_story(
        main_characters=["Dr. James Chen"],
        starting_location="Station Omega",
        initial_plot_thread="initial_crisis"
    )
    
    # Generate test scene
    scene_config = SceneConfig(
        scene_type="action",
        characters=["Dr. James Chen"],
        location="Station Omega",
        plot_points=["Emergency alarm activation"]
    )
    
    initial_time = story_engine.current_state.story_time
    scene = await story_engine.generate_scene(scene_config)
    
    # Verify state updates
    assert story_engine.current_state.story_time > initial_time, "Time should advance"
    assert len(story_engine.current_state.scene_history) > 0, "Should add to scene history"
    
    # Verify scene history
    latest_scene = story_engine.current_state.scene_history[-1]
    assert latest_scene["type"] == "action"
    assert "Dr. James Chen" in latest_scene["characters"]
    assert latest_scene["location"] == "Station Omega"