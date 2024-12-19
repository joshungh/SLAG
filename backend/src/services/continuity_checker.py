from typing import List, Dict
from src.models.story_schema import StoryState, CharacterArc
import logging

logger = logging.getLogger(__name__)

class ContinuityChecker:
    """Ensures story continuity and consistency"""
    
    def __init__(self, rag_service):
        self.rag = rag_service
        self.fact_cache = {}
        
    def get_character_state(self, character: str, story_state: StoryState) -> CharacterArc:
        """Get character state with fallback to defaults"""
        try:
            return story_state.character_states[character]
        except KeyError:
            # Create default state if character not found
            default_state = CharacterArc(
                character_id=character,
                current_state="Unknown",
                development_goals=[],
                relationships={},
                location="Unknown"
            )
            # Add to story state
            story_state.character_states[character] = default_state
            logger.info(f"Created default state for character: {character}")
            return default_state
    
    async def validate_scene(self, scene_content: Dict, story_state: StoryState) -> List[str]:
        """Validate scene continuity"""
        issues = []
        
        # Check character locations
        for character in scene_content["characters"]:
            char_state = self.get_character_state(character, story_state)
            if char_state.location != scene_content["location"]:
                # Log location change
                logger.info(f"Character {character} moved from {char_state.location} to {scene_content['location']}")
                char_state.location = scene_content["location"]
                
        return issues
    
    async def _verify_technology(self, scene_content: Dict) -> List[str]:
        """Verify technology usage is consistent with established rules"""
        tech_mentions = self._extract_technology(scene_content["content"])
        issues = []
        
        for tech in tech_mentions:
            # Query tech wiki
            tech_rules = await self.rag.query_knowledge(
                query=f"What are the limitations and rules for {tech}?",
                filters={"type": "technical"},
                namespace="technical"
            )
            
            if not self._verify_tech_usage(tech, tech_rules, scene_content):
                issues.append(f"Technology usage inconsistency: {tech}")
                
        return issues 