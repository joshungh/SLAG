from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Make sure this is at the top

class Settings(BaseSettings):
    AWS_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "slag-index")
    
    # Add Bedrock settings
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
    BEDROCK_EMBEDDING_MODEL_ID: str = os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v1")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"