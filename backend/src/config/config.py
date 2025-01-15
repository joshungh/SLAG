from pydantic_settings import BaseSettings
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

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

    # Application Settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # CORS Settings
    _ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    _ALLOWED_ORIGIN_REGEX: Optional[str] = os.getenv("ALLOWED_ORIGIN_REGEX")

    @property
    def cors_origins(self) -> List[str]:
        """Get the list of allowed origins based on the environment."""
        if self.ENVIRONMENT == "development":
            # In development, allow localhost with any port
            base_origins = self._ALLOWED_ORIGINS.split(",")
            localhost_origins = [f"http://localhost:{port}" for port in range(3000, 4000)]
            return list(set(base_origins + localhost_origins))
        return self._ALLOWED_ORIGINS.split(",")

    @property
    def cors_origin_regex(self) -> Optional[str]:
        """Get the regex pattern for allowed origins."""
        if self.ENVIRONMENT == "development":
            return r"^http://localhost:\d+"
        return self._ALLOWED_ORIGIN_REGEX

    # Bedrock Settings
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    BEDROCK_EMBEDDING_MODEL_ID: str = os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")

    class Config:
        env_file_encoding = "utf-8"
        case_sensitive = True