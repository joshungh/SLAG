from redis import Redis
import logging

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self, host: str, port: int):
        logger.info(f"Connecting to Redis at {host}:{port}")
        self.redis = Redis(
            host=host,
            port=port,
            decode_responses=True,
            socket_timeout=5,
            retry_on_timeout=True
        )
        # Test connection
        self.redis.ping()
        logger.info("Successfully connected to Redis") 