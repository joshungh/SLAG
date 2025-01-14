from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Make sure this is at the top

class Settings(BaseSettings):
    # AWS Settings
    AWS_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    
    # DynamoDB Settings
    DYNAMODB_USERS_TABLE: str = os.getenv("DYNAMODB_USERS_TABLE", "slag_users")
    DYNAMODB_STORIES_TABLE: str = os.getenv("DYNAMODB_STORIES_TABLE", "slag_stories")
    
    # Pinecone Settings
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "slag-index")
    
    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    TOKEN_EXPIRY_HOURS: int = int(os.getenv("TOKEN_EXPIRY_HOURS", "24"))
    
    # Google Auth Settings
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    
    # CORS Settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Bedrock Settings
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    BEDROCK_EMBEDDING_MODEL_ID: str = os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True