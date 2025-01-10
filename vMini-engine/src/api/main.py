import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
from src.core.services.llm_service import LLMService
from src.core.services.world_generation_service import WorldGenerationService
from src.core.utils.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware

logger = setup_logging("api", "api.log")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()
world_generation_service = WorldGenerationService(llm_service)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-world")
async def generate_world(request: PromptRequest):
    try:
        logger.info(f"Received request with prompt: {request.prompt}")
        
        # Initialize bible
        bible = await world_generation_service.initialize_bible(request.prompt)
        logger.info("Initial bible created")
        
        # Identify areas for expansion
        expansion_areas = await world_generation_service.identify_expansion_areas()
        logger.info(f"Identified expansion areas: {expansion_areas}")
        
        # Expand each area
        for area in expansion_areas:
            logger.info(f"Expanding area: {area}")
            try:
                bible = await world_generation_service.expand_bible(bible, area)
            except Exception as e:
                logger.error(f"Error expanding area '{area}': {str(e)}")
                # Continue with next area instead of failing completely
                continue
        
        return bible.model_dump()
        
    except Exception as e:
        logger.error(f"Error in generate_world: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Client host: {request.client.host if request.client else 'Unknown'}")
    response = await call_next(request)
    return response 