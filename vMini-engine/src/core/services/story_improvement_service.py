from typing import Dict, List, Any
import json
from datetime import datetime
import os
from src.core.services.llm_service import LLMService
from src.core.utils.logging_config import setup_logging
from src.config.config import settings

logger = setup_logging("story_improvement", "story_improvement.log")

class StoryImprovementService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def _apply_improvement(
        self,
        content: str,
        focus: str,
        prompt: str
    ) -> str:
        """Apply a specific improvement pass to the story"""
        
        full_prompt = f"""{prompt}

Story Content:
{content}

Provide specific improvements and the revised text."""

        response = await self.llm.generate(
            prompt=full_prompt,
            temperature=settings.IMPROVEMENT_TEMPERATURE,
            max_tokens=settings.IMPROVEMENT_MAX_TOKENS
        )
        
        logger.info(f"Completed {focus} improvement pass")
        return response

    async def improve_story(self, story_path: str) -> str:
        """Run multiple improvement passes on a story"""
        try:
            # Read the story
            with open(story_path, "r") as f:
                content = f.read()
            
            # Define improvement passes
            improvements = [
                {
                    "focus": "plot_consistency",
                    "prompt": """Analyze this story for plot holes, logical inconsistencies, 
                    or unexplained elements. For each issue found:
                    1. Identify the specific problem
                    2. Explain why it's an issue
                    3. Provide revised text that fixes the problem
                    
                    Focus on maintaining internal logic and ensuring all story elements 
                    are properly set up and resolved."""
                },
                {
                    "focus": "scene_expansion",
                    "prompt": """Identify 2-3 key scenes that would benefit from expansion.
                    For each scene:
                    1. Note what details are missing (sensory, emotional, environmental)
                    2. Explain how expanding the scene would improve the story
                    3. Provide the expanded version with richer detail
                    
                    Ensure expansions enhance the story without disrupting pacing."""
                },
                {
                    "focus": "character_voices",
                    "prompt": """Review all dialogue and character interactions. For each
                    main character:
                    1. Define their unique voice patterns and mannerisms
                    2. Identify dialogue that doesn't match their character
                    3. Provide revised dialogue that better reflects their personality
                    
                    Focus on making each character's voice distinct and consistent."""
                },
                {
                    "focus": "pacing_flow",
                    "prompt": """Analyze the story's pacing and flow. Look for:
                    1. Rushed transitions between scenes
                    2. Uneven pacing in action sequences
                    3. Abrupt mood shifts
                    
                    Provide specific revisions to smooth out pacing issues and improve
                    the overall flow of the narrative."""
                }
            ]
            
            # Apply improvements sequentially
            improved_content = content
            for improvement in improvements:
                improved_content = await self._apply_improvement(
                    content=improved_content,
                    focus=improvement["focus"],
                    prompt=improvement["prompt"]
                )
                
                # Save intermediate version
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                interim_path = f"output/stories/improvements/story_{timestamp}_{improvement['focus']}.md"
                os.makedirs(os.path.dirname(interim_path), exist_ok=True)
                
                with open(interim_path, "w") as f:
                    f.write(improved_content)
                
                logger.info(f"Saved {improvement['focus']} improvements to: {interim_path}")
            
            # Save final version
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_path = f"output/stories/story_{timestamp}_improved.md"
            
            with open(final_path, "w") as f:
                f.write(improved_content)
            
            logger.info(f"Saved final improved story to: {final_path}")
            return final_path

        except Exception as e:
            logger.error(f"Error improving story: {str(e)}")
            raise 