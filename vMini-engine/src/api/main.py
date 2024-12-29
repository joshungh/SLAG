import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.services.llm_service import LLMService
from src.core.services.world_generation_service import WorldGenerationService
from src.core.services.validation_service import ValidationService

app = FastAPI()

# Add startup delay to ensure services are properly initialized
@app.on_event("startup")
async def startup_event():
    time.sleep(2)  # Wait 2 seconds before accepting requests

# Initialize services
llm_service = LLMService()
world_gen_service = WorldGenerationService(llm_service)
validation_service = ValidationService(llm_service)

class WorldGenerationRequest(BaseModel):
    prompt: str

@app.post("/generate-world")
async def generate_world(request: WorldGenerationRequest):
    try:
        # Initial bible creation
        bible = await world_gen_service.initialize_bible(request.prompt)
        
        # First round of expansions
        expansion_areas = await world_gen_service.identify_expansion_areas()
        
        for area in expansion_areas:
            bible = await world_gen_service.expand_bible(area)
        
        # Cohesiveness check
        issues = await validation_service.check_cohesiveness(bible)
        
        if issues["inconsistencies"] or issues["gaps"]:
            bible = await validation_service.fix_inconsistencies(bible, issues)
        
        # Story element enrichment
        bible = await world_gen_service.enrich_story_elements(bible)
        
        return bible.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 