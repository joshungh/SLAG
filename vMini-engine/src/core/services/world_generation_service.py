from typing import Dict, Any
import json
import os
from datetime import datetime
from pydantic import ValidationError
from src.core.models.story_bible import StoryBible
from src.core.services.llm_service import LLMService
import logging
from pathlib import Path
from src.core.utils.logging_config import setup_logging
from src.config.config import settings

# Replace existing logging setup with:
logger = setup_logging("world_generation", "world_generation.log")

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
            "factions": [{"name": "", "description": "", "goals": [], "relationships": {}}],
            "technology": [{"name": "", "description": ""}],
            "timeline": {
                "pre_2145_mars_exploration": [
                    {"year": "2028", "event": "First Mars landing", "details": "..."}
                ]
            },
            "themes": [],
            "notes": []
        }
        
        Ensure all timeline entries follow the format of year, event, and optional details."""

        full_prompt = f"{system_prompt}\n\nUser Story Prompt: {prompt}"
        try:
            logger.info(f"Initializing bible from prompt: {prompt[:100]}...")
            response = await self.llm.generate(full_prompt)
            
            logger.debug(f"Raw LLM response: {response[:200]}...")
            
            bible_dict = json.loads(response)
            self.current_bible = StoryBible(**bible_dict)
            
            logger.info("Successfully created initial bible")
            self._save_bible(self.current_bible, "initial")
            return self.current_bible
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
            logger.debug(f"Invalid JSON response: {response}")
            raise
        except ValidationError as e:
            logger.error(f"Bible validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in initialize_bible: {str(e)}")
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

    async def expand_bible(self, bible: StoryBible, area: str) -> StoryBible:
        """Expand a specific area of the story bible"""
        try:
            logger.info(f"Expanding area: {area}")
            
            # Create expansion prompt
            system_prompt = f"""You are a world-building expert. Expand the following area of the story bible: {area}

            IMPORTANT: You must return your response as a valid JSON object that matches the story bible structure.
            
            Rules:
            1. Include ONLY the sections being expanded/modified
            2. Maintain the EXACT same structure as the original
            3. Include ALL required fields for any objects
            4. Use ONLY these top-level keys: title, genre, universe, characters, locations, factions, technology, timeline, themes, notes
            5. DO NOT include narrative descriptions or explanations outside the JSON structure
            
            Required field formats:
            - Factions: {{"name": "", "description": "", "goals": [], "relationships": {{}}}}
            - Characters: {{"name": "", "role": "", "description": "", "traits": [], "background": ""}}
            - Locations: {{"name": "", "description": "", "significance": ""}}
            - Technology: {{"name": "", "description": "", "impact": ""}}
            - Timeline events: {{"year": "", "event": "", "details": ""}}

            Example response format:
            {{
                "factions": [
                    {{
                        "name": "Example Faction",
                        "description": "Detailed description",
                        "goals": ["goal1", "goal2"],
                        "relationships": {{"other_faction": "relationship_type"}}
                    }}
                ],
                "technology": [
                    {{
                        "name": "Example Tech",
                        "description": "Detailed description",
                        "impact": "Impact description"
                    }}
                ]
            }}"""

            # Add current bible context
            bible_json = bible.model_dump_json()
            full_prompt = f"{system_prompt}\n\nCurrent Story Bible:\n{bible_json}"
            
            # Get LLM response with lower temperature for more structured output
            response = await self.llm.generate(
                prompt=full_prompt,
                max_tokens=settings.WORLD_BUILDING_MAX_TOKENS,
                temperature=0.3  # Lower temperature for more structured output
            )
            
            logger.info(f"LLM Response for {area}: {response[:200]}...")
            
            # Parse response
            try:
                expansion_dict = json.loads(response)
                logger.debug(f"Parsed expansion dict: {json.dumps(expansion_dict, indent=2)}")
                
                # Merge with existing bible
                merged_dict = bible.model_dump()
                for key, value in expansion_dict.items():
                    logger.debug(f"Merging key '{key}' of type {type(value)}")
                    if isinstance(value, list):
                        if key not in merged_dict:
                            merged_dict[key] = []
                        merged_dict[key].extend(value)
                        logger.debug(f"Extended list for key '{key}'")
                    elif isinstance(value, dict):
                        if key not in merged_dict:
                            merged_dict[key] = {}
                        merged_dict[key].update(value)
                        logger.debug(f"Updated dict for key '{key}'")
                    else:
                        merged_dict[key] = value
                        logger.debug(f"Set value for key '{key}'")
            
            except json.JSONDecodeError:
                # Try to extract JSON if wrapped in explanation
                import re
                json_match = re.search(r'\{[\s\S]*\}', response)
                if json_match:
                    expansion_dict = json.loads(json_match.group())
                else:
                    raise
            
            logger.info(f"Merged dict before validation: {json.dumps(merged_dict, indent=2)}")
            
            try:
                # Validate merged structure
                updated_bible = StoryBible(**merged_dict)
                logger.info(f"Successfully validated merged bible for area: {area}")
            except ValidationError as e:
                logger.error(f"Schema validation error: {str(e)}")
                logger.error(f"Failed validation for structure: {json.dumps(merged_dict, indent=2)}")
                raise
                
            self._save_bible(updated_bible, f"expansion_{area[:20]}")
            return updated_bible
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
            logger.error(f"Raw response: {response}")
            raise
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