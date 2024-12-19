import pytest
from src.core.story_engine import StoryEngine
from src.core.context_manager import ContextWindowManager

@pytest.fixture
def story_engine():
    context_manager = ContextWindowManager()
    return StoryEngine(context_manager)

@pytest.fixture
def initial_world_state():
    return {
        "world_rules": {
            "technology": "Post-singularity civilization",
            "setting": "Solar system spanning human civilization",
            "physics": "Hard science fiction with limited FTL"
        },
        "plot_arcs": [
            "Discovery of ancient giant artifacts",
            "Political tensions between Earth and colonies"
        ],
        "timeline": [],
        "tech_system": {
            "space_travel": "Fusion drives, limited FTL",
            "computing": "Quantum AI networks",
            "energy": "Antimatter and fusion"
        }
    }

async def test_story_initialization(story_engine, initial_world_state):
    await story_engine.initialize_story(initial_world_state)
    assert story_engine.context_manager.story_context is not None 