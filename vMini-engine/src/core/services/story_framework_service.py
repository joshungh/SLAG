from typing import List, Dict, Any
import json
from src.core.models.story_framework import StoryFramework, StoryArc, StoryBeat
from src.core.models.story_bible import StoryBible
from src.core.services.llm_service import LLMService
from src.core.utils.logging_config import setup_logging
from src.config.config import settings

logger = setup_logging("story_framework", "story_framework.log")

class StoryFrameworkService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        logger.info("StoryFrameworkService initialized")

    async def create_framework(self, bible: StoryBible) -> StoryFramework:
        """Create initial story framework from story bible"""
        try:
            logger.info("Creating story framework from bible")
            
            # Generate main story structure
            system_prompt = """You are a story structure expert. Using this story bible, create a detailed story framework.
            Focus on creating compelling arcs that utilize the world-building elements effectively.
            
            Return a JSON object with this structure:
            {
                "title": "Story Title",
                "genre": "Genre",
                "main_conflict": "Core conflict description",
                "central_theme": "Main theme",
                "arcs": [
                    {
                        "name": "Arc name",
                        "description": "Arc description",
                        "beats": [
                            {
                                "name": "Beat name",
                                "description": "What happens",
                                "purpose": "Story purpose",
                                "characters_involved": ["Character names"],
                                "location": "Where it happens",
                                "conflict_type": "Type of conflict",
                                "resolution_type": "How it resolves"
                            }
                        ],
                        "themes": ["Theme 1", "Theme 2"],
                        "character_arcs": {
                            "Character Name": "Their development arc"
                        }
                    }
                ],
                "subplot_connections": {
                    "Subplot A": ["Connected subplot B", "Connected subplot C"]
                },
                "pacing_notes": ["Pacing note 1", "Pacing note 2"]
            }"""

            bible_json = bible.model_dump_json()
            full_prompt = f"{system_prompt}\n\nStory Bible:\n{bible_json}"
            
            response = await self.llm.generate(
                prompt=full_prompt,
                max_tokens=settings.FRAMEWORK_MAX_TOKENS,
                temperature=settings.FRAMEWORK_TEMPERATURE
            )
            
            logger.debug(f"Raw framework response: {response[:200]}...")
            framework_dict = json.loads(response)
            
            # Validate and create framework
            framework = StoryFramework(**framework_dict)
            logger.info("Successfully created story framework")
            
            return framework
            
        except Exception as e:
            logger.error(f"Error creating story framework: {str(e)}")
            raise

    async def refine_arcs(self, framework: StoryFramework, bible: StoryBible) -> StoryFramework:
        """Refine and enhance story arcs"""
        try:
            logger.info("Refining story arcs")
            
            system_prompt = """Analyze these story arcs and enhance them for maximum dramatic impact.
            Focus on:
            1. Character motivation clarity
            2. Conflict escalation
            3. Theme reinforcement
            4. Subplot integration
            5. Pacing balance
            
            Return the enhanced framework maintaining the exact same JSON structure."""

            framework_json = framework.model_dump_json()
            bible_json = bible.model_dump_json()
            full_prompt = f"{system_prompt}\n\nCurrent Framework:\n{framework_json}\n\nStory Bible:\n{bible_json}"
            
            response = await self.llm.generate(
                prompt=full_prompt,
                max_tokens=settings.FRAMEWORK_MAX_TOKENS,
                temperature=settings.FRAMEWORK_TEMPERATURE
            )
            
            refined_framework = StoryFramework(**json.loads(response))
            logger.info("Successfully refined story arcs")
            
            return refined_framework
            
        except Exception as e:
            logger.error(f"Error refining story arcs: {str(e)}")
            raise

    async def validate_framework(self, framework: StoryFramework, bible: StoryBible) -> Dict[str, Any]:
        """Validate story framework for consistency and completeness"""
        issues = {
            "character_coverage": [],
            "location_usage": [],
            "theme_consistency": [],
            "plot_holes": [],
            "pacing_issues": []
        }
        
        try:
            # Check character coverage
            bible_characters = {char.name for char in bible.characters}
            framework_characters = set()
            for arc in framework.arcs:
                for beat in arc.beats:
                    framework_characters.update(beat.characters_involved)
            
            unused_characters = bible_characters - framework_characters
            if unused_characters:
                issues["character_coverage"].append(
                    f"Characters not used in framework: {unused_characters}"
                )

            # Check location usage
            bible_locations = {loc.name for loc in bible.locations}
            for arc in framework.arcs:
                for beat in arc.beats:
                    if beat.location not in bible_locations:
                        issues["location_usage"].append(
                            f"Beat '{beat.name}' uses undefined location: {beat.location}"
                        )

            # Check theme consistency
            bible_themes = set(bible.themes)
            framework_themes = {theme for arc in framework.arcs for theme in arc.themes}
            
            if not framework_themes.intersection(bible_themes):
                issues["theme_consistency"].append(
                    "No overlap between bible themes and framework themes"
                )

            return issues
            
        except Exception as e:
            logger.error(f"Error validating framework: {str(e)}")
            raise 