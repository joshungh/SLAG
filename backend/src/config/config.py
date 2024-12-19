from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # AWS Configuration
    AWS_REGION: str = "us-west-2"
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    STABLE_DIFFUSION_MODEL_ID: str = "stability.stable-image-ultra-v1:0"
    
    # Story Configuration
    SCENE_INTERVAL_MINUTES: int = 30
    SCENES_PER_CHAPTER: int = 48
    CONTEXT_WINDOW_SIZE: int = 3
    
    # Vector DB Configuration
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: str = "us-east1-gcp"
    
    class Config:
        env_file = ".env" 