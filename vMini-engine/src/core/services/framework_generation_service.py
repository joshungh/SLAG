from typing import Dict, Any, List, Tuple
import json
from src.core.models.story_framework import StoryFramework
from src.core.services.llm_service import LLMService
from src.core.utils.logging_config import setup_logging
from src.config.config import settings
from datetime import datetime
import os

logger = setup_logging("framework_generation", "framework_generation.log")

class FrameworkGenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        
    async def _get_genre_masters(self, genre: str) -> str:
        """Ask Claude to identify master storytellers for a given genre"""
        try:
            prompt = f"""Given the genre "{genre}", name 2-3 of the greatest storytellers 
            known for their mastery of this genre. Return only their names, separated by 
            'and', no other text."""
            
            response = await self.llm.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=200
            )
            return response.strip()
            
        except Exception as e:
            logger.warning(f"Could not get genre masters: {str(e)}")
            return ""
        
    async def _save_framework(self, framework: StoryFramework) -> str:
        """Save framework to JSON file"""
        try:
            # Create frameworks directory if it doesn't exist
            os.makedirs("output/frameworks", exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/frameworks/framework_{timestamp}.json"
            
            # Save framework
            with open(filename, "w") as f:
                json.dump(framework.model_dump(), f, indent=2)
                
            logger.info(f"Saved framework to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving framework: {str(e)}")
            raise

    async def generate_framework(self, story_bible: Dict[str, Any]) -> StoryFramework:
        """Generate a story framework from a story bible"""
        try:
            logger.info(f"Generating framework for story: {story_bible.get('title')}")
            
            # Get genre masters if possible
            genre = story_bible.get('genre', '')
            masters = await self._get_genre_masters(genre)
            
            # Extract available locations for prompt
            locations = [loc["name"] for loc in story_bible.get("locations", [])]
            locations_str = "\n".join(f"- {loc}" for loc in locations)
            
            # Define JSON structure separately
            json_structure = """{
                "title": "Story Title",
                "genre": "Genre based on bible",
                "main_conflict": "Core story tension",
                "central_theme": "Main theme",
                "arcs": [
                    {
                        "name": "Arc Name",
                        "description": "Arc description",
                        "beats": [
                            {
                                "name": "Beat Name",
                                "description": "Vivid description of what happens in this scene",
                                "characters_involved": ["Character names from bible"],
                                "location": "Location from bible"
                            }
                        ],
                        "themes": ["Themes explored in this arc"],
                        "character_arcs": {
                            "Character Name": "Their emotional/personal journey in this arc"
                        }
                    }
                ]
            }"""
            
            # Craft the prompt
            inspiration = f"Channel the imagination of {masters}. " if masters else ""
            
            system_prompt = f"""You are a master storyteller. Given this story bible, 
            create a compelling short story framework (20-30 minute read) that brings 
            this world to life.
            
            {inspiration}Be bold and creative. Don't feel constrained - surprise us with 
            unexpected combinations and fresh perspectives. Focus on dramatic character 
            moments and vivid scenes.

            IMPORTANT: Use ONLY these locations from the story bible:
            {locations_str}
            
            Return a JSON framework with exactly this structure:
            {json_structure}

            Make it dramatic, make it personal, make it memorable. But stick exactly to 
            this JSON structure and use only the locations listed above."""

            # Get framework from LLM
            response = await self.llm.generate(
                prompt=f"{system_prompt}\n\nStory Bible:\n{json.dumps(story_bible, indent=2)}",
                temperature=settings.FRAMEWORK_TEMPERATURE,
                max_tokens=settings.FRAMEWORK_MAX_TOKENS
            )
            
            # Parse response and create framework
            try:
                framework_data = json.loads(response)
                framework = StoryFramework(**framework_data)
                
                # Save framework to file
                await self._save_framework(framework)
                
                logger.info("Successfully generated story framework")
                return framework
                
            except json.JSONDecodeError:
                logger.error("Failed to parse framework response as JSON")
                raise
                
        except Exception as e:
            logger.error(f"Error generating story framework: {str(e)}")
            raise 