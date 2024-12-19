import pytest
import logging
from src.services.story_engine_service import StoryEngineService
from src.models.story_schema import StoryState, PlotThread, CharacterArc, PlotStatus

logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def story_engine(rag_service):
    return StoryEngineService(rag_service)

@pytest.mark.asyncio
async def test_full_chapter_generation(story_engine):
    """Test detailed chapter generation with all components"""
    
    logger.info("\n=== Initializing Story State ===")
    # Initialize rich story state
    story_engine.story_state = StoryState(
        current_chapter=1,
        current_scene=0,
        active_plot_threads=[
            PlotThread(
                id="initial_crisis",
                title="Strange Fragment Behavior",
                status=PlotStatus.ACTIVE,
                priority=1,
                related_characters=["Dr. James Chen", "Commander Drake"]
            ),
            PlotThread(
                id="station_politics",
                title="Station Leadership Tensions",
                status=PlotStatus.PENDING,
                priority=2,
                related_characters=["Commander Drake", "Dr. Wells"]
            )
        ],
        character_states={
            "Dr. James Chen": CharacterArc(
                character_id="Dr. James Chen",
                current_state="Investigating anomalies",
                development_goals=["Understand Fragment behavior", "Prove theories"],
                relationships={"Commander Drake": "professional", "Dr. Wells": "mentor"},
                location="Station Omega"
            ),
            "Commander Drake": CharacterArc(
                character_id="Commander Drake",
                current_state="Managing crisis",
                development_goals=["Maintain station safety", "Balance military/science priorities"],
                relationships={"Dr. James Chen": "professional", "Dr. Wells": "tense"},
                location="Command Center"
            )
        }
    )

    logger.info("\n=== Generating Chapter Plan ===")
    # Generate chapter plan
    scene = await story_engine.generate_next_scene()
    
    logger.info("\n=== Validating Generated Content ===")
    # Validate structure
    assert scene is not None
    assert "content" in scene
    assert "characters" in scene
    assert "location" in scene
    
    # Log generated content
    logger.info("\n=== Generated Scene Details ===")
    logger.info(f"Location: {scene['location']}")
    logger.info(f"Characters: {scene['characters']}")
    logger.info("\nScene Content Preview:")
    logger.info("---")
    logger.info(scene['content'][:500] + "...")
    logger.info("---")
    
    # Validate character movements
    logger.info("\n=== Character Location Changes ===")
    for char in scene['characters']:
        original_loc = story_engine.story_state.character_states[char].location
        logger.info(f"{char}: {original_loc} -> {scene['location']}")

    # Log plot advancement
    logger.info("\n=== Plot Thread Status ===")
    for plot in story_engine.story_state.active_plot_threads:
        logger.info(f"- {plot.title}: {plot.status}") 