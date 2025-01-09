from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .core.clients import bedrock, pinecone_client

app = FastAPI(
    title="Story Engine Mini",
    description="A streamlined version of SLAG for short story generation",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
bedrock_client = None
pinecone_index = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global bedrock_client, pinecone_index
    
    bedrock_client = bedrock.get_bedrock_client()
    pinecone_index = pinecone_client.init_pinecone()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Import and include routers
# from .api.routes import story_router
# app.include_router(story_router) 