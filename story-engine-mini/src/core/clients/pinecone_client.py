from pinecone import Pinecone
from ...config import settings

def init_pinecone():
    """
    Initialize Pinecone client and return the index
    """
    pc = Pinecone(
        api_key=settings.PINECONE_API_KEY,
        environment=settings.PINECONE_ENVIRONMENT
    )
    
    # Get the index
    return pc.Index(settings.PINECONE_INDEX) 