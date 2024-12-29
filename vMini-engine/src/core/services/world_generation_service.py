from typing import Dict, Any
import json
import os
from datetime import datetime
from pydantic import ValidationError
from src.core.models.story_bible import StoryBible
from src.core.services.llm_service import LLMService
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/world_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorldGenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.current_bible: StoryBible = None
        self.output_dir = Path("output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("WorldGenerationService initialized")

    def _save_bible(self, bible: StoryBible, stage: str):
        """Save the bible to a JSON file with timestamp"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/bible_{stage}_{timestamp}.json"
            
            logger.info(f"Attempting to save bible to: {filename}")
            logger.info(f"Output directory exists: {self.output_dir.exists()}")
            logger.info(f"Output directory is writable: {os.access(self.output_dir, os.W_OK)}")
            
            with open(filename, 'w') as f:
                json.dump(bible.model_dump(), f, indent=2)
            
            logger.info(f"Successfully saved bible to: {filename}")
            print(f"\nSaved bible to: {filename}")
        except Exception as e:
            logger.error(f"Error saving bible: {str(e)}")
            raise

    async def initialize_bible(self, prompt: str) -> StoryBible:
        """Create initial story bible framework from user prompt"""
        system_prompt = """You are a world-building expert. Given the user's story prompt, 
        create an initial story bible framework. Focus on the core elements: setting, main characters, 
        key locations, and major factions. Return the response in valid JSON format matching this structure:
        {
            "title": "",
            "genre": "",
            "universe": {"setting": "", "era": ""},
            "characters": [{"name": "", "role": "", "description": ""}],
            "locations": [{"name": "", "description": ""}],
            "factions": [{"name": "", "description": "", "goals": []}],
            "technology": [{"name": "", "description": ""}],
            "timeline": {},
            "themes": [],
            "notes": []
        }"""

        full_prompt = f"{system_prompt}\n\nUser Story Prompt: {prompt}"
        response = await self.llm.generate(full_prompt)
        
        try:
            bible_dict = json.loads(response)
            self.current_bible = StoryBible(**bible_dict)
            self._save_bible(self.current_bible, "initial")
            return self.current_bible
        except Exception as e:
            print(f"Error parsing LLM response to StoryBible: {str(e)}")
            raise

    async def identify_expansion_areas(self) -> list[str]:
        """Identify areas in the story bible that need expansion"""
        if not self.current_bible:
            raise ValueError("No story bible initialized")

        system_prompt = """Analyze the current story bible and identify 3-5 specific areas that need 
        expansion or more detail. Focus on elements that would make the world more cohesive and interesting. 
        Return a list of specific aspects to expand, one per line."""

        bible_json = self.current_bible.model_dump_json()
        full_prompt = f"{system_prompt}\n\nCurrent Story Bible:\n{bible_json}"
        
        response = await self.llm.generate(full_prompt)
        return [area.strip() for area in response.split('\n') if area.strip()]

    async def expand_bible(self, expansion_area: str) -> StoryBible:
        """Expand a specific area of the story bible"""
        if not self.current_bible:
            raise ValueError("No story bible initialized")

        system_prompt = f"""Given the current story bible, expand and add more detail to this specific area: 
        {expansion_area}. 

        IMPORTANT: When modifying any section, you must maintain the complete structure for each element:
        - Characters must have: name, role, description, traits, background
        - Locations must have: name, description, significance
        - Factions must have: name, description, goals, relationships
        - Technology must have: name, description, impact

        Return only the new or modified content in valid JSON format that matches the original structure.
        Do not omit any required fields when modifying elements."""

        try:
            bible_json = self.current_bible.model_dump_json()
            full_prompt = f"{system_prompt}\n\nCurrent Story Bible:\n{bible_json}\n\n"
            full_prompt += """IMPORTANT: Your response must be valid JSON and include ALL required fields.
            For factions, you MUST include: name, description, goals, and relationships.
            Example faction structure:
            {
                "factions": [{
                    "name": "Example Faction",
                    "description": "Detailed description here",
                    "goals": ["goal1", "goal2"],
                    "relationships": {}
                }]
            }"""
            
            response = await self.llm.generate(full_prompt)
            
            # Log the response for debugging
            logger.info(f"LLM Response for {expansion_area}: {response[:200]}...")
            
            try:
                expansion_dict = json.loads(response)
                
                # Pre-validate faction structure
                if 'factions' in expansion_dict:
                    for faction in expansion_dict['factions']:
                        if 'description' not in faction:
                            logger.error(f"Missing description in faction: {faction}")
                            faction['description'] = "Description pending"  # Add default
                
                current_dict = self.current_bible.model_dump()
                updated_dict = {**current_dict, **expansion_dict}
                
                # Log the merged dictionary before validation
                logger.info(f"Merged dict before validation: {json.dumps(updated_dict, indent=2)[:200]}...")
                
                self.current_bible = StoryBible(**updated_dict)
                
            except ValidationError as e:
                logger.error(f"Schema validation error: {str(e)}")
                logger.error(f"Failed validation for structure: {json.dumps(updated_dict, indent=2)}")
                raise

            self._save_bible(self.current_bible, f"expansion_{expansion_area[:20]}")
            return self.current_bible
            
        except Exception as e:
            logger.error(f"Error in expand_bible: {str(e)}")
            raise

    async def enrich_story_elements(self, bible: StoryBible) -> StoryBible:
        """Add story-development focused details to the story bible to support future plot creation"""
        system_prompt = """You are a story structure expert. Analyze this story bible and enhance it with details 
        that will support compelling story development. Focus on elements that will help craft a strong plot structure:

        1. Conflict Sources
           - Power dynamics between factions
           - Resource limitations and their implications
           - Ideological differences between characters/groups
           - Personal stakes for key characters

        2. Story Drivers
           - Key historical events that influence present tensions
           - Ticking clock elements or deadlines
           - Competing goals and motivations
           - Hidden connections between elements

        3. Plot Potential
           - Possible crisis points
           - Character pressure points
           - Faction friction points
           - Technology/artifact implications
           - Environmental constraints or threats

        4. Story Limitations
           - Physical boundaries of the world
           - Technological limitations
           - Social/political constraints
           - Timeline boundaries

        Return the enhanced story bible in the same JSON format, maintaining all existing content while adding 
        these story-development elements. Focus on concrete details that can drive plot development rather than 
        atmospheric or narrative flourishes."""

        bible_json = bible.model_dump_json()
        full_prompt = f"{system_prompt}\n\nCurrent Story Bible:\n{bible_json}"
        
        try:
            response = await self.llm.generate(full_prompt)
            enriched_bible = StoryBible(**json.loads(response))
            self._save_bible(enriched_bible, "story_elements_enriched")
            return enriched_bible
        except Exception as e:
            logger.error(f"Error enriching story elements: {str(e)}")
            raise 