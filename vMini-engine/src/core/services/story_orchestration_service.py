from typing import Optional, Dict, Any
from src.core.services.world_generation_service import WorldGenerationService
from src.core.services.framework_generation_service import FrameworkGenerationService
from src.core.services.story_generation_service import StoryGenerationService
from src.core.models.story_bible import StoryBible
from src.core.models.story_framework import StoryFramework
from src.core.models.story import Story
from src.core.utils.logging_config import setup_logging
from pathlib import Path
import os

logger = setup_logging("orchestration", "orchestration.log")

class StoryOrchestrationService:
    def __init__(
        self,
        world_service: WorldGenerationService,
        framework_service: FrameworkGenerationService,
        story_service: StoryGenerationService
    ):
        if not all([world_service, framework_service, story_service]):
            raise ValueError("All services must be provided")
            
        self.world_service = world_service
        self.framework_service = framework_service
        self.story_service = story_service
        self.current_state: Dict[str, Any] = {}
        
        # Define base paths
        self.base_dir = Path("/app")
        self.output_dir = self.base_dir / "output"
        self.stories_dir = self.output_dir / "stories"
        self.frameworks_dir = self.output_dir / "frameworks"
        
        # Ensure directories exist with proper permissions
        for directory in [self.output_dir, self.stories_dir, self.frameworks_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            directory.chmod(0o777)
            
        logger.debug(f"Initialized directories:")
        logger.debug(f"Base dir: {self.base_dir}")
        logger.debug(f"Output dir: {self.output_dir}")
        logger.debug(f"Stories dir: {self.stories_dir}")
        logger.debug(f"Frameworks dir: {self.frameworks_dir}")

    async def generate_complete_story(self, prompt: str) -> Story:
        """Orchestrate the complete story generation pipeline"""
        try:
            logger.info(f"Starting story generation for prompt: {prompt}")
            
            # Step 1: Generate Story Bible
            logger.info("Generating story bible...")
            bible = await self.world_service.generate_complete_bible(prompt)
            self.current_state["bible"] = bible
            logger.info("Story bible generated successfully")

            # Step 2: Create Story Framework
            logger.info("Generating story framework...")
            framework = await self.framework_service.generate_framework(bible.model_dump())
            self.current_state["framework"] = framework
            logger.info("Story framework generated successfully")

            # Step 3: Generate Story
            logger.info("Generating final story...")
            story = await self.story_service.generate_story(
                story_bible=bible.model_dump(),
                framework=framework
            )
            self.current_state["story"] = story
            logger.info("Story generation complete")

            return story

        except Exception as e:
            logger.error(f"Error in story generation pipeline: {str(e)}")
            # Could add recovery/retry logic here
            raise

    def get_generation_status(self) -> Dict[str, Any]:
        """Get current status of story generation process"""
        return {
            "has_bible": "bible" in self.current_state,
            "has_framework": "framework" in self.current_state,
            "has_story": "story" in self.current_state,
            "current_stage": self._determine_current_stage()
        }

    def _determine_current_stage(self) -> str:
        """Determine current stage of story generation"""
        if "story" in self.current_state:
            return "complete"
        if "framework" in self.current_state:
            return "generating_story"
        if "bible" in self.current_state:
            return "generating_framework"
        return "generating_bible" 