from dotenv import load_dotenv
import asyncio
import logging
from src.utils.initialize_services import initialize_services

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_index():
    """Verify index contents and metadata"""
    # Load environment variables
    load_dotenv()
    
    services = await initialize_services()
    rag = services["rag"]
    
    # Test character retrieval
    char_results = await rag.query_knowledge(
        query="Tell me about Dr. Chen",
        filters={"type": "character_profile"},
        namespace="characters"
    )
    logger.info(f"Found {len(char_results)} character matches")
    
    # Test style guide retrieval
    style_results = await rag.query_knowledge(
        query="How should technical discussions be written?",
        filters={"type": "writing_guide"},
        namespace="style_guides"
    )
    logger.info(f"Found {len(style_results)} style guide matches")
    
    # Test world building retrieval
    world_results = await rag.query_knowledge(
        query="What are Giants?",
        filters={"type": "world_building"},
        namespace="world"
    )
    logger.info(f"Found {len(world_results)} world building matches")

if __name__ == "__main__":
    asyncio.run(verify_index()) 