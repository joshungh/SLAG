import pytest
import json
from src.core.services.framework_generation_service import FrameworkGenerationService
from src.core.services.llm_service import LLMService

@pytest.fixture
def framework_service():
    llm_service = LLMService()
    return FrameworkGenerationService(llm_service)

@pytest.fixture
def sample_bible():
    with open("output/final_story_bible_20250104_141839.json") as f:
        return json.load(f)

async def test_framework_generation(framework_service, sample_bible):
    """Test basic framework generation"""
    try:
        framework = await framework_service.generate_framework(sample_bible)
        
        # Basic validation
        assert framework.title is not None
        assert framework.genre is not None
        assert framework.main_conflict is not None
        assert framework.central_theme is not None
        assert len(framework.arcs) > 0
        
        # Check first arc
        first_arc = framework.arcs[0]
        assert len(first_arc.beats) >= 3  # At least beginning, middle, end
        assert first_arc.themes
        assert first_arc.character_arcs
        
        # Validate characters exist in bible (this constraint makes sense)
        bible_characters = {char["name"] for char in sample_bible["characters"]}
        for arc in framework.arcs:
            for beat in arc.beats:
                for char in beat.characters_involved:
                    assert char in bible_characters
        
        # Save the framework for review
        print(json.dumps(framework.model_dump(), indent=2))
        return framework
        
    except Exception as e:
        pytest.fail(f"Framework generation test failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 