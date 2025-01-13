from redis import asyncio as aioredis
from contextlib import asynccontextmanager
import logging
import asyncio
from src.config.config import settings
from typing import Optional

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self, host: str, port: int):
        """Initialize Redis service with connection pool
        
        Args:
            host (str): Redis host address
            port (int): Redis port number
        """
        logger.info(f"Connecting to Redis at {host}:{port}")
        
        # Configure connection pool
        self.pool = aioredis.ConnectionPool(
            host=host,
            port=port,
            db=0,
            max_connections=50,
            decode_responses=True,
            retry_on_timeout=True,
            socket_timeout=5,
            socket_connect_timeout=5
        )
        
        # Initialize Redis client
        self.client = aioredis.Redis(
            connection_pool=self.pool,
            decode_responses=True,
            retry_on_timeout=True
        )
        
    async def ping(self) -> bool:
        """Quick health check with retry"""
        retries = 3
        for attempt in range(retries):
            try:
                return await asyncio.wait_for(self.client.ping(), timeout=2.0)
            except (asyncio.TimeoutError, Exception) as e:
                if attempt == retries - 1:
                    logger.error(f"Redis ping failed after {retries} attempts: {str(e)}")
                    return False
                await asyncio.sleep(0.5 * (attempt + 1))  # Backoff between retries
        return False

    async def hset(self, key: str, field: str, value: str) -> bool:
        """Set hash field to value
        
        Args:
            key (str): Redis key
            field (str): Hash field
            value (str): Value to set
            
        Returns:
            bool: True if successful
        """
        try:
            return await self.client.hset(key, field, value)
        except Exception as e:
            logger.error(f"Redis hset failed for {key}.{field}: {str(e)}")
            raise

    async def expire(self, key: str, seconds: int) -> bool:
        """Set key expiration
        
        Args:
            key (str): Redis key
            seconds (int): Expiration time in seconds
            
        Returns:
            bool: True if successful
        """
        try:
            return await self.client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Redis expire failed for {key}: {str(e)}")
            raise

    async def get(self, key: str) -> Optional[str]:
        """Get value for key
        
        Args:
            key (str): Redis key
            
        Returns:
            Optional[str]: Value if exists, None otherwise
        """
        try:
            return await self.client.get(key)
        except Exception as e:
            logger.error(f"Redis get failed for {key}: {str(e)}")
            raise

    async def setex(self, key: str, seconds: int, value: str) -> bool:
        """Set key value with expiration
        
        Args:
            key (str): Redis key
            seconds (int): Expiration time in seconds
            value (str): Value to set
            
        Returns:
            bool: True if successful
        """
        try:
            return await self.client.setex(key, seconds, value)
        except Exception as e:
            logger.error(f"Redis setex failed for {key}: {str(e)}")
            raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Properly close Redis connections"""
        if hasattr(self, 'pool'):
            await self.pool.disconnect()

    def __del__(self):
        """Cleanup connections on garbage collection"""
        if hasattr(self, 'pool'):
            # Create event loop if needed
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run disconnect in the event loop
            if not loop.is_closed():
                loop.run_until_complete(self.pool.disconnect()) 