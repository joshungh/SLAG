import pytest
from src.services.story_engine_service import StoryEngineService
from src.services.story_arc_manager import StoryArcManager
from src.services.continuity_checker import ContinuityChecker
from src.models.story_schema import StoryState, PlotThread, ChapterSummary, SceneConfig
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def story_engine(rag_service):
    return StoryEngineService(rag_service)

@pytest.mark.asyncio
async def test_chapter_generation(story_engine):
    """Test complete chapter generation flow"""
    # Initialize story state
    story_engine.story_state = StoryState(
        current_chapter=1,
        current_scene=0,
        active_plot_threads=[
            PlotThread(
                id="initial_crisis",
                title="Strange Fragment Behavior",
                status="active",
                priority=1,
                related_characters=["Dr. James Chen"]
            )
        ],
        chapter_summaries=[],
        unresolved_cliffhangers=[]
    )
    
    # Generate first scene
    scene = await story_engine.generate_next_scene()
    
    assert scene is not None
    assert "content" in scene
    assert "characters" in scene
    assert "location" in scene

@pytest.mark.asyncio
async def test_tension_curve(story_engine):
    """Test tension management"""
    arc_manager = story_engine.arc_manager
    
    # Simulate 5 chapters of tension
    for i in range(5):
        arc_manager.tension_curve[i] = 0.2 * (i + 1)  # Rising tension
    
    analysis = await arc_manager.analyze_tension_patterns(5)
    
    assert analysis["patterns"]["steady_rise"]
    assert analysis["optimal_next_tension"] > arc_manager.tension_curve[4]
    assert "build_conflict" in analysis["suggested_techniques"]

@pytest.mark.asyncio
async def test_continuity_checking(story_engine):
    """Test continuity validation"""
    test_scene = {
        "content": "Dr. Chen activated the quantum resonance scanner...",
        "characters": ["Dr. James Chen"],
        "location": "Station Omega",
        "technology": ["quantum resonance scanner"]
    }
    
    issues = await story_engine.continuity_checker.validate_scene(
        test_scene,
        story_engine.story_state
    )
    
    assert len(issues) == 0, f"Unexpected continuity issues: {issues}"

@pytest.mark.asyncio
async def test_complete_story_flow(initialized_story_engine, test_story_data):
    """Test complete story generation flow"""
    story_engine = await initialized_story_engine  # Await the fixture
    
    # Initialize story
    success = await story_engine.initialize_story(
        main_characters=test_story_data["main_characters"],
        starting_location=test_story_data["starting_location"],
        initial_plot_thread=test_story_data["initial_plot_thread"]
    )
    assert success, "Story initialization failed"
    
    # Generate first chapter
    for scene_config in test_story_data["chapter_1_scenes"]:
        scene = await story_engine.generate_scene(SceneConfig(**scene_config))
        
        # Verify scene structure
        assert scene is not None
        assert "content" in scene
        assert "characters" in scene
        assert "location" in scene
        
        # Log scene details
        logger.info("\n=== Generated Scene ===")
        logger.info(f"Location: {scene['location']}")
        logger.info(f"Characters: {scene['characters']}")
        logger.info("\nContent Preview:")
        logger.info("---")
        logger.info(scene['content'][:500] + "...")
        logger.info("---")