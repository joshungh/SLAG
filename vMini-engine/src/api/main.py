import time
from fastapi import FastAPI, HTTPException, Request, Response
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
import json

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

# Add rate limiting state
health_check_timestamps = []
RATE_LIMIT = 20  # requests
TIME_WINDOW = 60  # seconds

@app.get("/health")
async def health_check():
    """Health check endpoint for ELB with rate limiting"""
    try:
        # Clean old timestamps
        current_time = time.time()
        while health_check_timestamps and health_check_timestamps[0] < current_time - TIME_WINDOW:
            health_check_timestamps.pop(0)
            
        # Check rate limit
        if len(health_check_timestamps) >= RATE_LIMIT:
            return JSONResponse(
                status_code=429,  # Too Many Requests
                content={
                    "status": "error",
                    "detail": "Rate limit exceeded"
                }
            )
            
        health_check_timestamps.append(current_time)
        
        # Use cached result for 5 seconds to reduce Redis load
        cache_key = "health_check_cache"
        cached = await redis_client.get(cache_key)
        if cached:
            return JSONResponse(
                status_code=200,
                content=json.loads(cached)
            )

        # Only check Redis if cache miss
        redis_ok = await redis_client.ping()
        result = {
            "status": "healthy" if redis_ok else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "redis": redis_ok
        }
        
        # Cache result
        await redis_client.setex(cache_key, 5, json.dumps(result))
        return JSONResponse(status_code=200, content=result)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "detail": str(e)
            }
        )

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

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    try:
        # Test Redis connection
        await redis_client.ping()
        logger.info("Redis connection successful")
    except Exception as e:
        logger.error(f"Failed to initialize Redis: {str(e)}")
        # Don't raise here - let the app start but mark Redis as unavailable

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # Number of worker processes
        limit_concurrency=50,  # Max concurrent connections
        timeout_keep_alive=65,
        loop="uvloop",  # Faster event loop implementation
        access_log=True
    ) 