from dotenv import load_dotenv
import asyncio
import logging
from src.utils.initialize_services import initialize_services
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_namespace(rag, namespace: str, query: str, filters: Dict = None) -> List[Dict]:
    """Query and verify a specific namespace"""
    results = await rag.query_knowledge(
        query=query,
        filters=filters,
        namespace=namespace,
        top_k=5
    )
    logger.info(f"\nNamespace '{namespace}' results:")
    logger.info(f"Found {len(results)} matches")
    if results:
        for i, result in enumerate(results):
            logger.info(f"\nMatch {i+1}:")
            logger.info(f"Score: {result.get('score', 'N/A')}")
            logger.info(f"Metadata: {result.get('metadata', {})}")
            logger.info(f"Text preview: {result.get('text', '')[:200]}...")
    return results

async def verify_index():
    """Verify index contents and metadata across all namespaces"""
    # Load environment variables
    load_dotenv()
    
    services = await initialize_services()
    rag = services["rag"]
    
    # Define verification queries for each namespace
    namespace_queries = {
        "technical": {
            "query": "Fragment containment systems",
            "filters": {"type": "technical_research"}
        },
        "narrative": {
            "query": "Story progression and plot development",
            "filters": {"type": "narrative"}
        },
        "locations": {
            "query": "Station Omega layout and systems",
            "filters": {"type": "location"}
        },
        "style_guides": {
            "query": "Writing technical discussions",
            "filters": {"type": "writing_guide"}
        },
        "world": {
            "query": "Giant civilization and technology",
            "filters": {"type": "world_building"}
        },
        "characters": {
            "query": "Dr. Chen background and personality",
            "filters": {"type": "character_profile"}
        },
        "chapter_1": {
            "query": "Initial Fragment crisis",
            "filters": {"type": "generated_scene"}
        },
        "military": {
            "query": "Station security protocols",
            "filters": {"type": "military"}
        },
        "style_guide": {
            "query": "Asimov writing style characteristics",
            "filters": {"type": "style_guide"}
        },
        "default": {
            "query": "General story elements",
            "filters": None
        },
        "test": {
            "query": "Test documents",
            "filters": {"type": "test"}
        },
        "character": {
            "query": "Character interactions and development",
            "filters": {"type": "character"}
        },
        "story_planning": {
            "query": "Plot structure and development",
            "filters": {"type": "story_planning"}
        }
    }
    
    # Test each namespace
    results_summary = {}
    for namespace, query_info in namespace_queries.items():
        logger.info(f"\n{'='*20} Testing namespace: {namespace} {'='*20}")
        results = await verify_namespace(
            rag=rag,
            namespace=namespace,
            query=query_info["query"],
            filters=query_info["filters"]
        )
        results_summary[namespace] = len(results)
    
    # Print summary
    logger.info("\n\n=== Index Verification Summary ===")
    for namespace, count in results_summary.items():
        logger.info(f"{namespace}: {count} results")
    
    # Verify cross-references
    logger.info("\n=== Verifying Cross-References ===")
    cross_ref_query = "Fragment effects on station systems"
    cross_results = await rag.query_knowledge(
        query=cross_ref_query,
        filters=None,  # No filters to check across all types
        namespace="technical",  # Start in technical namespace
        top_k=10
    )
    logger.info(f"Cross-reference query found {len(cross_results)} related documents")

if __name__ == "__main__":
    asyncio.run(verify_index()) 