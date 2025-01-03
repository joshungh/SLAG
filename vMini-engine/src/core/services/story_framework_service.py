import json
import logging
from typing import List, Dict, Any
from src.core.models.story_framework import StoryFramework, StoryArc, StoryPart
from src.core.models.story_bible import StoryBible
from src.core.services.llm_service import LLMService
from src.core.services.validation_service import ValidationService

logger = logging.getLogger(__name__)

class StoryFrameworkService:
    def __init__(self, llm_service: LLMService, validation_service: ValidationService):
        self.llm = llm_service
        self.validation = validation_service
        self.target_part_length = 1000  # Estimated words per part

    async def generate_initial_arc(self, bible: StoryBible) -> StoryArc:
        """Generate the initial story arc from the story bible"""
        system_prompt = """You are a master storyteller. Using the provided story bible, 
        create a compelling story arc that includes:
        
        1. A main plot with clear beginning, middle, and end
        2. Character arcs for each major character
        3. Relevant subplots that enhance the main story
        4. Consistent themes and tone
        
        Return the story arc in valid JSON format matching the StoryArc model structure."""

        prompt = f"{system_prompt}\n\nStory Bible:\n{bible.model_dump_json()}"
        
        try:
            response = await self.llm.generate(prompt)
            story_arc = StoryArc(**json.loads(response))
            logger.info(f"Generated initial story arc: {story_arc.title}")
            return story_arc
        except Exception as e:
            logger.error(f"Error generating story arc: {str(e)}")
            raise

    async def expand_story_arc(self, arc: StoryArc, bible: StoryBible) -> StoryArc:
        """Expand and enrich the story arc with additional detail"""
        system_prompt = """Analyze this story arc and expand it with:
        
        1. More detailed plot points
        2. Deeper character development moments
        3. Enhanced subplot integration
        4. Clear setup and payoff elements
        
        Maintain consistency with the story bible while adding depth."""

        prompt = f"{system_prompt}\n\nStory Arc:\n{arc.model_dump_json()}\n\nStory Bible:\n{bible.model_dump_json()}"
        
        try:
            response = await self.llm.generate(prompt)
            expanded_arc = StoryArc(**json.loads(response))
            return expanded_arc
        except Exception as e:
            logger.error(f"Error expanding story arc: {str(e)}")
            raise

    async def segment_into_parts(self, arc: StoryArc, target_parts: int = 10) -> List[StoryPart]:
        """Break the story arc into sequential parts for generation"""
        system_prompt = f"""Break this story arc into {target_parts} sequential parts for generation.
        Each part should:
        1. Flow naturally from the previous part
        2. Advance the plot and character development
        3. Maintain narrative tension
        4. Include callbacks to previous events when relevant
        5. Set up future events when appropriate
        
        Target word count per part: {self.target_part_length}
        
        Return an array of {target_parts} parts in valid JSON format matching the StoryPart model."""

        prompt = f"{system_prompt}\n\nStory Arc:\n{arc.model_dump_json()}"
        
        try:
            response = await self.llm.generate(prompt)
            parts = [StoryPart(**part) for part in json.loads(response)]
            return parts
        except Exception as e:
            logger.error(f"Error segmenting story: {str(e)}")
            raise

    async def create_framework(self, bible: StoryBible, target_length: int = 10000) -> StoryFramework:
        """Create complete story framework from bible"""
        try:
            # Calculate number of parts based on target length
            num_parts = max(3, round(target_length / self.target_part_length))
            
            # Generate initial arc
            arc = await self.generate_initial_arc(bible)
            arc.target_length = target_length
            
            # Expand the arc
            expanded_arc = await self.expand_story_arc(arc, bible)
            
            # Segment into parts
            parts = await self.segment_into_parts(expanded_arc, num_parts)
            
            # Create framework
            framework = StoryFramework(
                story_arc=expanded_arc,
                parts=parts,
                metadata={
                    "target_length": target_length,
                    "num_parts": num_parts,
                    "target_part_length": self.target_part_length
                }
            )
            
            return framework
            
        except Exception as e:
            logger.error(f"Error creating story framework: {str(e)}")
            raise 