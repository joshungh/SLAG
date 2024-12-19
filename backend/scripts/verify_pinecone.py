from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_index():
    load_dotenv()
    
    api_key = os.getenv("PINECONE_API_KEY")
    logger.info(f"API Key (first 10 chars): {api_key[:10]}...")
    
    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=api_key)
        logger.info("Pinecone initialized successfully")
        
        # List indexes
        try:
            indexes = pc.list_indexes()
            logger.info(f"Available indexes: {indexes}")
            
            if 'slag-index' not in indexes.names():
                # Create index if it doesn't exist
                logger.info("Creating slag-index...")
                pc.create_index(
                    name='slag-index',
                    dimension=1536,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-west-2'
                    )
                )
                logger.info("Index created successfully")
            
            # Connect to index
            index = pc.Index("slag-index")
            stats = index.describe_index_stats()
            logger.info(f"\nIndex stats: {stats}")
                
        except Exception as e:
            logger.error(f"Error with index operations: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error initializing Pinecone: {str(e)}")

if __name__ == "__main__":
    verify_index()
