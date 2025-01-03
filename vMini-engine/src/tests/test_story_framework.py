import pytest
import json
from pathlib import Path
from src.core.services.story_framework_service import StoryFrameworkService
from src.core.services.llm_service import LLMService
from src.core.models.story_bible import StoryBible

@pytest.mark.asyncio
class TestStoryFramework:
    @pytest.fixture(autouse=True)
    async def setup(self):
        """Setup test resources"""
        self.service = StoryFrameworkService(LLMService())
        
        # Load the sample bible
        bible_path = Path("output/final_story_bible_20250103_001301.json")
        with open(bible_path, "r") as f:
            bible_dict = json.load(f)
        self.bible = StoryBible(**bible_dict)
        yield
        
    async def test_framework_creation(self):
        """Test creating a story framework from the sample bible"""
        try:
            framework = await self.service.create_framework(self.bible)
            
            # Basic validation
            assert framework.title == self.bible.title
            assert framework.genre == self.bible.genre
            assert len(framework.arcs) > 0
            
            # Validate main conflict uses established elements
            assert any(
                conflict in framework.main_conflict 
                for conflict in ["Earth control", "independence", "resources"]
            )
            
            # Check arc structure
            main_arc = framework.arcs[0]
            assert len(main_arc.beats) >= 3
            assert all(beat.characters_involved for beat in main_arc.beats)
            
            # Validate character usage
            bible_characters = {char.name for char in self.bible.characters}
            framework_characters = set()
            for arc in framework.arcs:
                for beat in arc.beats:
                    framework_characters.update(beat.characters_involved)
            
            assert framework_characters.issubset(bible_characters)
            
            # Check theme consistency
            bible_themes = set(self.bible.themes)
            framework_themes = {theme for arc in framework.arcs for theme in arc.themes}
            assert bool(framework_themes.intersection(bible_themes))
            
            # Validate framework consistency
            issues = await self.service.validate_framework(framework, self.bible)
            assert not any(issues.values()), f"Framework validation failed: {issues}"
            
        except Exception as e:
            pytest.fail(f"Framework creation test failed: {str(e)}")

    async def test_framework_validation(self):
        """Test framework validation against bible"""
        framework = await self.service.create_framework(self.bible)
        issues = await self.service.validate_framework(framework, self.bible)
        
        assert isinstance(issues, dict)
        assert "character_issues" in issues
        assert "location_issues" in issues
        assert "theme_issues" in issues
        assert "plot_issues" in issues
        
        # Should have no issues with a properly generated framework
        assert not any(issues.values()), f"Unexpected validation issues: {issues}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 