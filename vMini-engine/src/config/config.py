from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from functools import lru_cache
from dotenv import load_dotenv
import boto3
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    @classmethod
    def get_aws_parameters(cls) -> dict:
        """Fetch parameters from AWS Parameter Store"""
        try:
            ssm = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'us-west-2'))
            path = os.getenv('AWS_PARAMETER_PATH', '/vMini-engine/dev')
            
            # Debug log environment variables
            logger.info("Environment variables:")
            logger.info(f"REDIS_HOST: {os.getenv('REDIS_HOST')}")
            logger.info(f"REDIS_PORT: {os.getenv('REDIS_PORT')}")
            logger.info(f"AWS_REGION: {os.getenv('AWS_REGION')}")
            logger.info(f"ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
            
            params = {}
            paginator = ssm.get_paginator('get_parameters_by_path')
            
            for page in paginator.paginate(
                Path=path,
                Recursive=True,
                WithDecryption=True
            ):
                for param in page['Parameters']:
                    # Convert /vMini-engine/prod/pinecone/api_key to PINECONE_API_KEY
                    name_parts = param['Name'].split('/')[-2:]  # ['pinecone', 'api_key']
                    env_name = f"{name_parts[0]}_{name_parts[1]}".upper()
                    params[env_name] = param['Value']
                    logger.info(f"Loaded parameter {env_name}: {param['Value']}")
            
            return params
        except Exception as e:
            logger.error(f"Error fetching AWS parameters: {e}")
            return {}

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API Settings
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    
    # AWS Bedrock
    AWS_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    AWS_ACCESS_KEY_ID: str | None = None  # Will be loaded from Parameter Store
    AWS_SECRET_ACCESS_KEY: str | None = None  # Will be loaded from Parameter Store
    BEDROCK_MODEL_ID: str = os.getenv(
        "BEDROCK_MODEL_ID", 
        "anthropic.claude-3-5-sonnet-20241022-v2:0"
    )
    BEDROCK_EMBEDDING_MODEL_ID: str = os.getenv(
        "BEDROCK_EMBEDDING_MODEL_ID",
        "amazon.titan-embed-text-v1"
    )
    
    # Pinecone
    PINECONE_API_KEY: str | None = None  # Will be loaded from Parameter Store
    PINECONE_ENVIRONMENT: str | None = None  # Will be loaded from Parameter Store
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "story-engine-mini")
    PINECONE_DIMENSION: int = 1536
    
    # Redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_SSL: bool = os.getenv("ENVIRONMENT") == "production"
    REDIS_TIMEOUT: int = int(os.getenv("REDIS_TIMEOUT", "5"))
    
    # LLM Generation Settings
    WORLD_BUILDING_TEMPERATURE: float = 0.3
    WORLD_BUILDING_MAX_TOKENS: int = 200000
    
    FRAMEWORK_TEMPERATURE: float = 0.6
    FRAMEWORK_MAX_TOKENS: int = 200000

    # Story Generation Settings
    STORY_TEMPERATURE: float = 0.8
    STORY_MAX_TOKENS: int = 200000  # Full context window
    SECTION_MAX_TOKENS: int = 200000  # Nearly full window per beat
    
    # Default top_p value
    TOP_P: float = 0.9
    
    # Story Improvement Settings
    IMPROVEMENT_TEMPERATURE: float = 0.8
    IMPROVEMENT_MAX_TOKENS: int = 200000  # Full context for improvements
    
    def __init__(self, **kwargs):
        # First load environment variables from .env files (lowest priority)
        load_dotenv()
        
        # Log current Redis settings before potential overrides
        logger.info("Initial Redis Configuration:")
        logger.info(f"REDIS_HOST from env: {os.getenv('REDIS_HOST')}")
        logger.info(f"REDIS_PORT from env: {os.getenv('REDIS_PORT')}")
        
        # Then load AWS parameters if not in local environment
        if os.getenv('ENVIRONMENT') != 'local':
            aws_params = self.get_aws_parameters()
            kwargs.update(aws_params)
        
        # Environment variables from ECS should take highest priority
        kwargs.update({
            "REDIS_HOST": os.getenv("REDIS_HOST", kwargs.get("REDIS_HOST", "localhost")),
            "REDIS_PORT": int(os.getenv("REDIS_PORT", str(kwargs.get("REDIS_PORT", 6379))))
        })
        
        super().__init__(**kwargs)
    
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