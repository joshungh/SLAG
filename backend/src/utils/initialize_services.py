import boto3
import pinecone
from ..config.config import Settings
from ..services.bedrock_service import BedrockService
from ..services.pinecone_service import PineconeService
from ..services.rag_service import RAGService

async def initialize_services():
    """Initialize all services"""
    settings = Settings()
    
    # Initialize Bedrock service
    bedrock = BedrockService(settings)
    
    # Initialize Pinecone
    pinecone = PineconeService(settings)
    
    # Initialize RAG service
    rag = RAGService(bedrock, pinecone)
    
    return {
        "bedrock": bedrock,
        "pinecone": pinecone,
        "rag": rag
    } 