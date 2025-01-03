import pytest
import json
from src.core.services.story_framework_service import StoryFrameworkService
from src.core.services.llm_service import LLMService
from src.core.services.validation_service import ValidationService
from src.core.models.story_bible import StoryBible

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.fixture
def validation_service(llm_service):
    return ValidationService(llm_service)

@pytest.fixture
def framework_service(llm_service, validation_service):
    return StoryFrameworkService(llm_service, validation_service)

@pytest.fixture
def sample_bible():
    # Load test bible from JSON file
    with open("src/tests/data/test_bible.json", "r") as f:
        return StoryBible(**json.load(f))

async def test_generate_initial_arc(framework_service, sample_bible):
    arc = await framework_service.generate_initial_arc(sample_bible)
    assert arc.title is not None
    assert len(arc.main_plot) == 3  # beginning, middle, end
    assert len(arc.character_arcs) > 0
    assert len(arc.themes) > 0

async def test_expand_story_arc(framework_service, sample_bible):
    initial_arc = await framework_service.generate_initial_arc(sample_bible)
    expanded_arc = await framework_service.expand_story_arc(initial_arc, sample_bible)
    
    # Verify expansion added more detail
    assert len(expanded_arc.main_plot["beginning"].events) >= len(initial_arc.main_plot["beginning"].events)
    assert len(expanded_arc.subplots) >= len(initial_arc.subplots)

async def test_segment_into_parts(framework_service, sample_bible):
    arc = await framework_service.generate_initial_arc(sample_bible)
    parts = await framework_service.segment_into_parts(arc, target_parts=5)
    
    assert len(parts) == 5
    assert all(isinstance(part.part_number, int) for part in parts)
    assert all(len(part.scenes) > 0 for part in parts)

async def test_create_framework(framework_service, sample_bible):
    framework = await framework_service.create_framework(sample_bible, target_length=5000)
    
    assert framework.story_arc is not None
    assert len(framework.parts) > 0
    assert framework.metadata["target_length"] == 5000 