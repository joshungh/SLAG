import pytest
import json
from pathlib import Path
from src.core.services.story_framework_service import StoryFrameworkService
from src.core.services.llm_service import LLMService
from src.core.models.story_bible import StoryBible

@pytest.mark.asyncio
async def test_framework_from_existing_bible():
    """Test creating a story framework from an existing expanded bible file"""
    try:
        # Load test bible from expansion file
        bible_path = Path("output/bible_expansion_1. Ancient Martian C_20250103_002548.json")
        with open(bible_path, "r") as f:
            bible_dict = json.load(f)
        
        bible = StoryBible(**bible_dict)
        
        # Create framework
        service = StoryFrameworkService(LLMService())
        framework = await service.create_framework(bible)
        
        # Basic validation
        assert framework.title == bible.title
        assert framework.genre == bible.genre
        assert len(framework.arcs) > 0
        
        # Check arc structure
        main_arc = framework.arcs[0]
        assert len(main_arc.beats) >= 3  # At least beginning, middle, end
        assert all(beat.characters_involved for beat in main_arc.beats)
        
        # Validate character usage
        bible_characters = {char.name for char in bible.characters}
        framework_characters = set()
        for arc in framework.arcs:
            for beat in arc.beats:
                framework_characters.update(beat.characters_involved)
        
        # All framework characters should exist in bible
        assert framework_characters.issubset(bible_characters)
        
        # Check theme consistency
        bible_themes = set(bible.themes)
        framework_themes = {theme for arc in framework.arcs for theme in arc.themes}
        assert bool(framework_themes.intersection(bible_themes))
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}") 