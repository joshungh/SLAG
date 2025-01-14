import os
import logging
from .redis_service import RedisService

logger = logging.getLogger(__name__)

# Initialize Redis client
try:
    redis_host = os.getenv("REDIS_HOST")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    if not redis_host:
        raise ValueError("REDIS_HOST environment variable not set")
    redis_client = RedisService(redis_host, redis_port)
    logger.info(f"Redis client initialized with host: {redis_host}")
except Exception as e:
    logger.error(f"Failed to initialize Redis client: {str(e)}")
    redis_client = None 