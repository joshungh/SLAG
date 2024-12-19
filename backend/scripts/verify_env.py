from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_env():
    """Verify environment variables are loaded"""
    load_dotenv()
    
    # Check critical variables
    env_vars = {
        'PINECONE_API_KEY': os.getenv('PINECONE_API_KEY'),
        'PINECONE_ENVIRONMENT': os.getenv('PINECONE_ENVIRONMENT'),
        'AWS_REGION': os.getenv('AWS_REGION')
    }
    
    logger.info("Environment Variables:")
    for key, value in env_vars.items():
        masked_value = value[:8] + '...' if value else None
        logger.info(f"{key}: {masked_value}")
        
    # Verify all required vars are present
    missing = [k for k, v in env_vars.items() if not v]
    if missing:
        logger.error(f"Missing environment variables: {missing}")
    else:
        logger.info("All required environment variables are set")

if __name__ == "__main__":
    verify_env() 