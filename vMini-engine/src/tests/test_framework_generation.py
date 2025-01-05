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

@pytest.mark.asyncio
async def test_framework_generation(framework_service, sample_bible):
    """Test basic framework generation"""
    try:
        framework = await framework_service.generate_framework(sample_bible)
        
        # Basic validation
        assert framework.title is not None, "Framework must have a title"
        assert framework.genre is not None, "Framework must have a genre"
        assert framework.main_conflict is not None, "Framework must have a main conflict"
        assert framework.central_theme is not None, "Framework must have a central theme"
        assert len(framework.arcs) > 0, "Framework must have at least one arc"
        
        # Check each arc
        for i, arc in enumerate(framework.arcs):
            assert len(arc.beats) >= 3, f"Arc {i} ({arc.name}) must have at least 3 beats"
            assert arc.themes, f"Arc {i} ({arc.name}) must have themes"
            assert arc.character_arcs, f"Arc {i} ({arc.name}) must have character arcs"
            
            # Validate characters exist in bible
            bible_characters = {char["name"] for char in sample_bible["characters"]}
            for beat in arc.beats:
                for char in beat.characters_involved:
                    assert char in bible_characters, f"Character {char} in beat {beat.name} not found in bible"
                
                # Validate location exists in bible
                bible_locations = {loc["name"] for loc in sample_bible["locations"]}
                assert beat.location in bible_locations, f"Location {beat.location} in beat {beat.name} not found in bible"
        
        # Save the framework for review
        print(json.dumps(framework.model_dump(), indent=2))
        return framework
        
    except Exception as e:
        pytest.fail(f"Framework generation test failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 