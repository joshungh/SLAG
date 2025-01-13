from typing import List, Dict
import json
import os
from datetime import datetime
from src.core.models.story_bible import StoryBible
from src.core.models.story_framework import StoryFramework, StoryArc, StoryBeat
from src.core.services.llm_service import LLMService
from src.core.services.s3_service import S3Service
from src.core.utils.logging_config import setup_logging
from src.config.config import settings
from pathlib import Path

logger = setup_logging("story_framework", "story_framework.log")

class StoryFrameworkService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.s3 = S3Service()

    async def create_framework(self, bible: StoryBible) -> StoryFramework:
        """Create a story framework from a story bible"""
        try:
            logger.info(f"Creating initial framework for: {bible.title}")
            
            system_prompt = """You are a story structure expert. Analyze this story bible and create a 
            compelling story framework. Focus on creating interconnected arcs that utilize the established 
            world elements and conflict sources.

            CRITICAL REQUIREMENTS:
            1. Each story arc MUST have at least 3 beats (beginning, middle, end)
            2. Use ONLY themes from the story bible
            3. Each beat must involve characters from the bible
            4. All locations must exist in the bible
            5. Create meaningful character arcs that reflect the bible's conflicts

            Return a JSON object with this exact structure:
            {
                "title": "Story Title",
                "genre": "Genre",
                "main_conflict": "Core conflict description",
                "central_theme": "Main theme from bible",
                "arcs": [
                    {
                        "name": "Main Arc Name",
                        "description": "Arc description",
                        "beats": [
                            {
                                "name": "Opening Beat",
                                "description": "What happens",
                                "purpose": "Story purpose",
                                "characters_involved": ["Character names from bible"],
                                "location": "Location from bible",
                                "conflict_type": "Type of conflict",
                                "resolution_type": "How it resolves"
                            },
                            {
                                "name": "Middle Beat",
                                "description": "...",
                                "purpose": "...",
                                "characters_involved": ["..."],
                                "location": "...",
                                "conflict_type": "...",
                                "resolution_type": "..."
                            },
                            {
                                "name": "Closing Beat",
                                "description": "...",
                                "purpose": "...",
                                "characters_involved": ["..."],
                                "location": "...",
                                "conflict_type": "...",
                                "resolution_type": "..."
                            }
                        ],
                        "themes": ["Theme 1 from bible", "Theme 2 from bible"],
                        "character_arcs": {
                            "Character Name": "Their arc description"
                        }
                    }
                ],
                "subplot_connections": {
                    "Arc Name": ["Connected Arc 1", "Connected Arc 2"]
                },
                "pacing_notes": ["Pacing note 1", "Pacing note 2"]
            }

            Available themes from bible: ${bible.themes}
            Available characters: ${[c.name for c in bible.characters]}
            Available locations: ${[l.name for l in bible.locations]}"""

            bible_json = bible.model_dump_json()
            full_prompt = f"{system_prompt}\n\nStory Bible:\n{bible_json}"
            
            response = await self.llm.generate(
                full_prompt,
                temperature=settings.FRAMEWORK_TEMPERATURE,
                max_tokens=settings.FRAMEWORK_MAX_TOKENS
            )
            
            try:
                framework_dict = json.loads(response)
                framework_dict = await self._validate_arc_beats(framework_dict)
                framework = StoryFramework(**framework_dict)
                
                # Save initial framework
                initial_url = await self.save_framework(framework)
                logger.info(f"Saved initial framework to: {initial_url}")
                
                # Validate initial framework
                for arc in framework.arcs:
                    if len(arc.beats) < 3:
                        logger.warning(f"Arc {arc.name} has fewer than 3 beats. Regenerating...")
                        return await self.create_framework(bible)
                        
                bible_themes = set(bible.themes)
                framework_themes = {theme for arc in framework.arcs for theme in arc.themes}
                if not framework_themes.intersection(bible_themes):
                    logger.warning("No matching themes found. Regenerating...")
                    return await self.create_framework(bible)
                
                # Expand the framework
                logger.info("Starting framework expansion...")
                expanded_framework = await self.expand_framework(framework, bible)
                
                # Save expanded framework
                final_url = await self.save_framework(expanded_framework)
                logger.info(f"Saved expanded framework to: {final_url}")
                
                logger.info(f"Successfully created and expanded framework with {len(expanded_framework.arcs)} arcs")
                return expanded_framework
                
            except json.JSONDecodeError:
                logger.error("Failed to parse framework response as JSON")
                logger.debug(f"Invalid response: {response[:200]}...")
                raise
                
        except Exception as e:
            logger.error(f"Error creating story framework: {str(e)}")
            raise

    async def validate_framework(self, framework: StoryFramework, bible: StoryBible) -> Dict[str, List[str]]:
        """Validate framework against story bible for consistency"""
        issues = {
            "character_issues": [],
            "location_issues": [],
            "theme_issues": [],
            "plot_issues": []
        }
        
        # Check characters
        bible_characters = {char.name for char in bible.characters}
        framework_characters = set()
        for arc in framework.arcs:
            for beat in arc.beats:
                for char in beat.characters_involved:
                    if char not in bible_characters:
                        issues["character_issues"].append(
                            f"Character '{char}' in beat '{beat.name}' not found in bible"
                        )
                    framework_characters.add(char)
        
        # Check locations
        bible_locations = {loc.name for loc in bible.locations}
        for arc in framework.arcs:
            for beat in arc.beats:
                if beat.location not in bible_locations:
                    issues["location_issues"].append(
                        f"Location '{beat.location}' in beat '{beat.name}' not found in bible"
                    )
        
        # Check themes
        bible_themes = set(bible.themes)
        framework_themes = {theme for arc in framework.arcs for theme in arc.themes}
        if not framework_themes.intersection(bible_themes):
            issues["theme_issues"].append("No themes from bible used in framework")
        
        # Check plot elements
        if not any(arc.character_arcs for arc in framework.arcs):
            issues["plot_issues"].append("No character arcs defined")
            
        if not framework.subplot_connections:
            issues["plot_issues"].append("No subplot connections defined")
            
        return issues 

    async def _validate_arc_beats(self, framework_dict: dict) -> dict:
        """Ensure each arc has at least 3 beats (beginning, middle, end)"""
        if "arcs" not in framework_dict:
            return framework_dict
        
        for arc in framework_dict["arcs"]:
            if len(arc.get("beats", [])) < 3:
                # Get context from the arc
                arc_name = arc.get("name", "")
                arc_desc = arc.get("description", "")
                existing_beats = arc.get("beats", [])
                
                # Construct prompt for additional beats
                prompt = f"""Given this story arc:
                Name: {arc_name}
                Description: {arc_desc}
                Current Beats: {json.dumps(existing_beats, indent=2)}
                
                Add additional story beats to ensure we have a complete beginning, middle, and end. 
                Return ONLY the new beats as a JSON array. Each beat must have:
                - name
                - description
                - characters_involved (array)
                - location
                
                Current locations and characters must be maintained for consistency."""
                
                try:
                    response = await self.llm.generate(prompt, temperature=0.7)
                    new_beats = json.loads(response)
                    
                    # Merge new beats with existing ones
                    arc["beats"].extend(new_beats)
                    
                    logger.info(f"Added {len(new_beats)} beats to arc '{arc_name}'")
                    
                except Exception as e:
                    logger.error(f"Error adding beats to arc: {str(e)}")
                    
        return framework_dict 

    async def save_framework(self, framework: StoryFramework) -> str:
        """Save framework to file with timestamp"""
        try:
            content = framework.model_dump_json(indent=2)
            framework_id = framework.title.lower().replace(' ', '_')
            return await self.s3.save_story(content, framework_id, 'framework')
        except Exception as e:
            logger.error(f"Error saving framework: {str(e)}")
            raise

    async def expand_framework(self, framework: StoryFramework, bible: StoryBible) -> StoryFramework:
        """Recursively expand and enrich the framework using itself as context"""
        try:
            # Get the current framework as context
            framework_json = framework.model_dump_json(indent=2)
            
            # 1. Expand beat descriptions
            for arc in framework.arcs:
                for beat in arc.beats:
                    try:
                        expansion_prompt = f"""Given this story framework:
                        {framework_json}
                        
                        Expand and enrich this specific beat:
                        Arc: {arc.name}
                        Beat: {beat.name}
                        Current Description: {beat.description}
                        
                        Consider:
                        - How this beat connects to others in the framework
                        - The emotional journey of {', '.join(beat.characters_involved)}
                        - The atmosphere and details of {beat.location}
                        - How this moment builds the overall story
                        
                        Provide a richer, more detailed description while maintaining story consistency."""
                        
                        expanded_description = await self.llm.generate(
                            expansion_prompt,
                            temperature=0.7,
                            max_tokens=200000
                        )
                        
                        # Only update if we got a meaningful expansion
                        if expanded_description and len(expanded_description) > len(beat.description):
                            beat.description = expanded_description
                            framework_json = framework.model_dump_json(indent=2)
                            logger.info(f"Successfully expanded beat: {beat.name}")
                        else:
                            logger.info(f"Keeping original description for beat: {beat.name}")
                            
                    except Exception as e:
                        logger.warning(f"Failed to expand beat {beat.name}: {str(e)}")
                        continue  # Move to next beat if this one fails
                
            # 2. Enrich character arcs with full framework context
            for arc in framework.arcs:
                for char, arc_desc in arc.character_arcs.items():
                    try:
                        char_prompt = f"""Given the complete story framework:
                        {framework_json}
                        
                        Deepen the character arc for {char}.
                        Current arc description: {arc_desc}
                        
                        Consider:
                        - Their journey across all story beats
                        - Their relationships and conflicts
                        - Their growth and changes
                        - How their arc supports the main themes
                        
                        Provide a richer character arc that ties into the overall framework."""
                        
                        enriched_arc = await self.llm.generate(char_prompt)
                        
                        # Only update if we got a meaningful enrichment
                        if enriched_arc and len(enriched_arc) > len(arc_desc):
                            arc.character_arcs[char] = enriched_arc
                            framework_json = framework.model_dump_json(indent=2)
                            logger.info(f"Successfully enriched character arc for: {char}")
                        else:
                            logger.info(f"Keeping original arc for character: {char}")
                            
                    except Exception as e:
                        logger.warning(f"Failed to enrich character arc for {char}: {str(e)}")
                        continue  # Move to next character if this one fails
                    
            return framework
            
        except Exception as e:
            logger.error(f"Error in framework expansion: {str(e)}")
            return framework  # Return whatever we have even if expansion partially failed