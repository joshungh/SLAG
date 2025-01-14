import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
from src.core.utils.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from src.config.config import settings
from src.core.services import (
    redis_service,
    story_orchestration_service
)
import os
from src.core.services.redis_service import RedisService
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
from fastapi.responses import JSONResponse

logger = setup_logging("api", "api.log")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_story(request: StoryRequest):
    try:
        logger.info(f"Received story generation request: {request.prompt[:100]}...")
        result = await story_orchestration_service.generate_complete_story(request.prompt)
        return result
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_generation_status():
    try:
        status = story_orchestration_service.get_generation_status()
        return status
    except Exception as e:
        logger.error(f"Error getting generation status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get Redis configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Initialize Redis service
redis_client = RedisService(host=REDIS_HOST, port=REDIS_PORT)

# Simple in-memory cache for health check
_last_health_check = None
_health_check_cache_ttl = 5  # seconds

@app.get("/health")
async def health_check():
    global _last_health_check
    current_time = time.time()
    
    # Return cached result if available and not expired
    if _last_health_check and current_time - _last_health_check['timestamp'] < _health_check_cache_ttl:
        return _last_health_check['result']
    
    try:
        # Test Redis connection
        redis_client.redis.ping()
        result = {
            "status": "healthy",
            "redis": {
                "status": "healthy",
                "host": REDIS_HOST,
                "port": REDIS_PORT
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        result = {
            "status": "degraded",
            "redis": {
                "status": "error",
                "message": str(e),
                "host": REDIS_HOST,
                "port": REDIS_PORT
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    # Update cache
    _last_health_check = {
        'timestamp': current_time,
        'result': result
    }
    
    return result

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Client host: {request.client.host if request.client else 'Unknown'}")
    response = await call_next(request)
    return response 

class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=900)
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=504,
                content={"detail": "Request timeout"}
            )

app.add_middleware(TimeoutMiddleware) 