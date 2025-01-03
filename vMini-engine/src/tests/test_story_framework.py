import pytest
from src.core.services.story_framework_service import StoryFrameworkService
from src.core.services.llm_service import LLMService
from src.core.models.story_bible import StoryBible
from src.core.models.story_framework import StoryFramework

@pytest.mark.asyncio
async def test_framework_creation():
    """Test creating a story framework from a bible"""
    try:
        service = StoryFrameworkService(LLMService())
        
        # Create test bible
        bible_dict = {
            "title": "Test Story",
            "genre": "Science Fiction",
            "universe": {"setting": "Mars", "era": "2145"},
            "characters": [
                {
                    "name": "John Smith",
                    "role": "Archaeologist",
                    "description": "Lead scientist",
                    "traits": ["curious", "determined"],
                    "background": "PhD from MIT"
                }
            ],
            "locations": [
                {
                    "name": "Olympus Base",
                    "description": "Main research facility",
                    "significance": "Central hub"
                }
            ],
            "themes": ["discovery", "perseverance"],
            "notes": []
        }
        
        bible = StoryBible(**bible_dict)
        
        # Generate framework
        framework = await service.create_framework(bible)
        
        # Validate framework
        assert framework.title == bible.title
        assert framework.genre == bible.genre
        assert len(framework.arcs) > 0
        assert all(arc.beats for arc in framework.arcs)
        
        # Test arc refinement
        refined = await service.refine_arcs(framework, bible)
        assert len(refined.arcs) >= len(framework.arcs)
        
        # Validate consistency
        issues = await service.validate_framework(refined, bible)
        assert not any(issues.values()), f"Framework validation failed: {issues}"
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 