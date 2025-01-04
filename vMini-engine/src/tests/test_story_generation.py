import pytest
import json
from src.core.services.story_generation_service import StoryGenerationService
from src.core.services.llm_service import LLMService
from src.core.models.story_framework import StoryFramework
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def story_service():
    llm_service = LLMService()
    return StoryGenerationService(llm_service)

@pytest.fixture
def sample_bible():
    with open("output/final_story_bible_20250104_141839.json") as f:
        return json.load(f)

@pytest.fixture
def sample_framework():
    with open("output/frameworks/framework_20250104_150749.json") as f:
        data = json.load(f)
        return StoryFramework(**data)

async def test_story_generation(story_service, sample_bible, sample_framework):
    """Test basic story generation"""
    try:
        story = await story_service.generate_story(sample_bible, sample_framework)
        
        # Basic validation
        assert story.title == sample_framework.title
        assert story.genre == sample_framework.genre
        assert story.content is not None
        
        # Print detailed info for review
        print("\nStory Generation Results:")
        print(f"Title: {story.title}")
        print(f"Total words: {story.word_count}")
        print(f"\nFirst section preview:")
        print("\n".join(story.content.split("\n")[:10]))
        print("\n...")
        
        # Log section count
        sections = story.content.split("\n\n")
        logger.info(f"Generated {len(sections)} sections")
        
        return story
        
    except Exception as e:
        logger.error(f"Story generation failed: {str(e)}")
        pytest.fail(f"Story generation test failed: {str(e)}") 