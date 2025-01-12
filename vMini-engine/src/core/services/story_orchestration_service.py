from typing import Optional, Dict, Any
import logging
from src.core.utils.logging_config import setup_logging
from src.core.models.story_bible import StoryBible
from src.core.models.story_framework import StoryFramework
from src.core.models.story import Story
from src.core.services.world_generation_service import WorldGenerationService
from src.core.services.story_framework_service import StoryFrameworkService
from src.core.services.story_generation_service import StoryGenerationService
from src.core.services.validation_service import ValidationService

logger = setup_logging("orchestration", "orchestration.log")

class StoryOrchestrationService:
    def __init__(
        self,
        world_service: WorldGenerationService,
        framework_service: StoryFrameworkService,
        story_service: StoryGenerationService,
        validation_service: ValidationService
    ):
        if not all([world_service, framework_service, story_service]):
            raise ValueError("All services must be provided")
            
        self.world_service = world_service
        self.framework_service = framework_service
        self.story_service = story_service
        self.validation = validation_service
        self.current_state: Dict[str, Any] = {}
        
    async def generate_complete_story(self, prompt: str) -> Dict[str, Any]:
        try:
            logger.info(f"Starting story generation for prompt: {prompt}")
            
            # Step 1: Generate Story Bible
            bible = await self.world_service.generate_complete_bible(prompt)
            self.current_state["bible"] = bible
            
            # Step 1.5: Validate bible
            issues = await self.validation.check_cohesiveness(bible)
            if any(issues.values()):
                bible = await self.validation.fix_inconsistencies(bible, issues)
                logger.info("Fixed bible inconsistencies")
            
            # Step 2: Create Story Framework
            framework = await self.framework_service.create_framework(bible)
            self.current_state["framework"] = framework
            
            # Step 3: Generate Story
            story = await self.story_service.generate_story(
                story_bible=bible.model_dump(),
                framework=framework
            )
            self.current_state["story"] = story
            
            return {
                "bible": bible.model_dump(),
                "framework": framework.model_dump(),
                "story": story.model_dump(),
                "word_count": story.word_count
            }
            
        except Exception as e:
            logger.error(f"Error in story generation pipeline: {str(e)}")
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