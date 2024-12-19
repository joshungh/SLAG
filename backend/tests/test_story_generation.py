import pytest
from src.services.story_engine_service import StoryEngineService
from src.services.story_arc_manager import StoryArcManager
from src.services.continuity_checker import ContinuityChecker
from src.models.story_schema import StoryState, PlotThread, ChapterSummary, PlotStatus, CharacterArc
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
async def story_engine(rag_service):
    """Initialize story engine with awaited RAG service"""
    engine = StoryEngineService(await rag_service)
    return engine

@pytest.mark.asyncio
async def test_chapter_generation(story_engine):
    """Test complete chapter generation flow"""
    # First await the story_engine fixture
    engine = await story_engine
    
    # Initialize story state
    engine.story_state = StoryState(
        current_chapter=1,
        current_scene=0,
        active_plot_threads=[
            PlotThread(
                id="initial_crisis",
                title="Strange Fragment Behavior",
                status=PlotStatus.ACTIVE,
                priority=1,
                related_characters=["Dr. James Chen"]
            )
        ],
        character_states={
            "Dr. James Chen": CharacterArc(
                character_id="Dr. James Chen",
                current_state="Working",
                development_goals=["Understand Fragment behavior"],
                relationships={"Commander Drake": "professional"},
                location="Station Omega"
            )
        },
        chapter_summaries=[],
        unresolved_cliffhangers=[]
    )
    
    # Generate first scene
    scene = await engine.generate_next_scene()
    
    # Add logging for debugging
    logger.info(f"Generated scene: {scene}")
    
    assert scene is not None, "Scene should not be None"
    assert "content" in scene, "Scene should have content"
    assert "characters" in scene, "Scene should have characters"
    assert "location" in scene, "Scene should have location"

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