from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API Settings
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    
    # AWS Bedrock
    AWS_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    BEDROCK_MODEL_ID: str = os.getenv(
        "BEDROCK_MODEL_ID", 
        "anthropic.claude-3-5-sonnet-20241022-v2:0"
    )
    BEDROCK_EMBEDDING_MODEL_ID: str = os.getenv(
        "BEDROCK_EMBEDDING_MODEL_ID",
        "amazon.titan-embed-text-v1"
    )
    
    # Pinecone
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "story-engine-mini")
    PINECONE_DIMENSION: int = 1536
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    
    # LLM Generation Settings
    WORLD_BUILDING_TEMPERATURE: float = 0.3
    WORLD_BUILDING_MAX_TOKENS: int = 120000
    
    FRAMEWORK_TEMPERATURE: float = 0.6
    FRAMEWORK_MAX_TOKENS: int = 200000

    # Story Generation Settings
    STORY_TEMPERATURE: float = 0.7
    STORY_MAX_TOKENS: int = 200000  # Full context window
    SECTION_MAX_TOKENS: int = 200000  # Nearly full window per beat
    
    # Default top_p value
    TOP_P: float = 0.9
    
    # Story Improvement Settings
    IMPROVEMENT_TEMPERATURE: float = 0.8
    IMPROVEMENT_MAX_TOKENS: int = 200000  # Full context for improvements
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Create cached instance of settings.
    Returns:
        Settings: Application settings
    """
    return Settings()

# Create a global instance
settings = get_settings() 