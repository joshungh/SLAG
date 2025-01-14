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
from src.core.services import redis_client
import time

logger = setup_logging("orchestration", "orchestration.log")

class StoryOrchestrationService:
    def __init__(
        self,
        world_service,
        framework_service,
        story_service,
        validation_service
    ):
        if not all([world_service, framework_service, story_service]):
            raise ValueError("All services must be provided")
            
        self.world_service = world_service
        self.framework_service = framework_service
        self.story_service = story_service
        self.validation = validation_service
        
    async def generate_complete_story(self, prompt: str) -> Dict[str, Any]:
        request_id = f"story:{prompt[:32]}:{int(time.time())}"
        
        try:
            logger.info(f"Starting story generation for request {request_id}")
            
            # Step 1: Generate Story Bible
            bible = await self.world_service.generate_complete_bible(prompt)
            try:
                await redis_client.hset(request_id, "bible", bible.model_dump_json())
            except Exception as e:
                logger.error(f"Redis operation failed: {str(e)}")
                # Continue without Redis - at least return the generated content
                return {
                    "request_id": request_id,
                    "bible": bible.model_dump()
                }
            
            # Step 1.5: Validate bible
            issues = await self.validation.check_cohesiveness(bible)
            if any(issues.values()):
                bible = await self.validation.fix_inconsistencies(bible, issues)
                await redis_client.hset(request_id, "bible", bible.model_dump_json())
            
            # Step 2: Create Story Framework
            framework = await self.framework_service.create_framework(bible)
            await redis_client.hset(request_id, "framework", framework.model_dump_json())
            
            # Step 3: Generate Story
            story = await self.story_service.generate_story(
                story_bible=bible.model_dump(),
                framework=framework
            )
            await redis_client.hset(request_id, "story", story.model_dump_json())
            
            # Set expiration for cleanup
            await redis_client.expire(request_id, 3600)  # 1 hour TTL
            
            return {
                "request_id": request_id,
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
            "status": "active",
            "current_stage": "processing"
        } 