from .llm_service import LLMService
from .embedding_service import EmbeddingService
from .redis_service import RedisService
from .world_generation_service import WorldGenerationService
from .story_framework_service import StoryFrameworkService
from .story_generation_service import StoryGenerationService
from .validation_service import ValidationService
from .vector_store_service import VectorStoreService
from .s3_service import S3Service
from .story_orchestration_service import StoryOrchestrationService
import os
import logging

logger = logging.getLogger(__name__)

# Initialize core services
llm_service = LLMService()
embedding_service = EmbeddingService()

# Initialize Redis with environment variables
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
redis_service = RedisService(redis_host, redis_port)

# Initialize dependent services
vector_store_service = VectorStoreService()
world_generation_service = WorldGenerationService(llm_service)
story_framework_service = StoryFrameworkService(llm_service)
story_generation_service = StoryGenerationService(llm_service)
validation_service = ValidationService(llm_service)

# Initialize orchestration service
story_orchestration_service = StoryOrchestrationService(
    world_generation_service,
    story_framework_service,
    story_generation_service,
    validation_service
)

# Initialize S3 service
s3_service = S3Service()

# Export all services
__all__ = [
    'llm_service',
    'embedding_service',
    'redis_service',
    'vector_store_service',
    'world_generation_service',
    'story_framework_service',
    'story_generation_service',
    'validation_service',
    'story_orchestration_service',
    's3_service'
]
