from typing import Dict, List
import os
from src.services.rag_service import RAGService
from src.services.bedrock_service import BedrockService
from src.services.pinecone_service import PineconeService
from src.config.config import Settings
from src.utils.path_utils import get_reference_doc_path
from src.models.metadata_schema import Species, Role, Expertise, LocationType, SecurityLevel, TechCategory, TimePeriod, NarrativeType
import logging
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def index_documents():
    """Index all reference documents with appropriate metadata"""
    
    # Initialize services
    settings = Settings()
    bedrock = BedrockService(settings)
    pinecone = PineconeService(settings)
    rag = RAGService(bedrock, pinecone)
    
    # Define document metadata mapping
    document_configs = [
        # Character Profiles
        {
            "path": "characters/character-chen.txt",
            "type": "character_profile",
            "metadata": {
                "name": "Dr. James Chen",
                "type": "character_profile",
                "category": "main_character",
                "species": Species.HUMAN,
                "role": [Role.SCIENTIFIC],
                "expertise": [Expertise.GIANT_STUDIES, Expertise.QUANTUM_PHYSICS],
                "security_level": SecurityLevel.RESTRICTED
            },
            "namespace": "characters"
        },
        {
            "path": "characters/character-drake.txt",
            "type": "character_profile",
            "metadata": {
                "name": "Commander Thomas Drake",
                "type": "character_profile",
                "category": "main_character",
                "species": Species.HUMAN,
                "role": [Role.MILITARY],
                "expertise": [Expertise.ENGINEERING],
                "security_level": SecurityLevel.CLASSIFIED
            },
            "namespace": "characters"
        },
        {
            "path": "characters/character-nash.txt",
            "type": "character_profile",
            "metadata": {
                "name": "David Nash",
                "type": "character_profile",
                "category": "main_character",
                "species": Species.HUMAN,
                "role": [Role.SCIENTIFIC],
                "expertise": [Expertise.QUANTUM_PHYSICS, Expertise.GIANT_STUDIES],
                "security_level": SecurityLevel.RESTRICTED
            },
            "namespace": "characters"
        },
        {
            "path": "characters/character-vass.txt",
            "type": "character_profile",
            "metadata": {
                "name": "Dr. Victor Vass",
                "type": "character_profile",
                "category": "main_character",
                "species": Species.VESS,
                "role": [Role.SCIENTIFIC, Role.POLITICAL],
                "expertise": [Expertise.GIANT_STUDIES],
                "security_level": SecurityLevel.CLASSIFIED
            },
            "namespace": "characters"
        },
        {
            "path": "characters/character-webb.txt",
            "type": "character_profile",
            "metadata": {
                "name": "Marcus Webb",
                "type": "character_profile",
                "category": "main_character",
                "species": Species.HUMAN,
                "role": [Role.TECHNICAL],
                "expertise": [Expertise.ENGINEERING],
                "security_level": SecurityLevel.RESTRICTED
            },
            "namespace": "characters"
        },
        {
            "path": "characters/character-wells.txt",
            "type": "character_profile",
            "metadata": {
                "name": "Dr. Sarah Wells",
                "type": "character_profile",
                "category": "main_character",
                "species": Species.HUMAN,
                "role": [Role.SCIENTIFIC],
                "expertise": [Expertise.MEDICINE],
                "security_level": SecurityLevel.RESTRICTED
            },
            "namespace": "characters"
        },
        {
            "path": "characters/slag-characters-classic.txt",
            "type": "character_profile",
            "metadata": {
                "type": "character_overview",
                "category": "reference",
                "security_level": SecurityLevel.PUBLIC
            },
            "namespace": "characters"
        },

        # World Building Documents
        {
            "path": "world/slag-locations.txt",
            "type": "location",
            "metadata": {
                "type": "location",
                "category": "world_building",
                "security_level": SecurityLevel.PUBLIC,
                "location_type": LocationType.STATION
            },
            "namespace": "locations"
        },
        {
            "path": "world/slag-tech-wiki.txt",
            "type": "technical",
            "metadata": {
                "type": "technical",
                "category": "world_building",
                "security_level": SecurityLevel.RESTRICTED,
                "tech_category": TechCategory.HUMAN
            },
            "namespace": "technical"
        },
        {
            "path": "world/slag-worldbuilding.txt",
            "type": "world_building",
            "metadata": {
                "type": "world_building",
                "category": "core_reference",
                "security_level": SecurityLevel.PUBLIC,
                "time_period": TimePeriod.PRESENT
            },
            "namespace": "world"
        },
        {
            "path": "world/slag-worldbuilding-expanded.txt",
            "type": "world_building",
            "metadata": {
                "type": "world_building",
                "category": "detailed_reference",
                "security_level": SecurityLevel.RESTRICTED,
                "time_period": TimePeriod.PRESENT
            },
            "namespace": "world"
        },

        # Narrative Framework Documents
        {
            "path": "narrative-framework/crisis-scenarios.txt",
            "type": "narrative",
            "metadata": {
                "type": "plot_framework",
                "category": "crisis",
                "narrative_type": [NarrativeType.ACTION, NarrativeType.TECHNICAL],
                "security_level": SecurityLevel.RESTRICTED
            },
            "namespace": "narrative"
        },
        {
            "path": "narrative-framework/initial-crisis.txt",
            "type": "narrative",
            "metadata": {
                "type": "plot_framework",
                "category": "crisis",
                "narrative_type": [NarrativeType.ACTION],
                "security_level": SecurityLevel.RESTRICTED
            },
            "namespace": "narrative"
        },
        {
            "path": "narrative-framework/opening-situation.txt",
            "type": "narrative",
            "metadata": {
                "type": "plot_framework",
                "category": "setup",
                "narrative_type": [NarrativeType.DESCRIPTION],
                "security_level": SecurityLevel.PUBLIC
            },
            "namespace": "narrative"
        },
        {
            "path": "narrative-framework/story-framework.txt",
            "type": "narrative",
            "metadata": {
                "type": "writing_guide",
                "category": "framework",
                "narrative_type": [NarrativeType.TECHNICAL],
                "security_level": SecurityLevel.PUBLIC
            },
            "namespace": "narrative"
        },

        # Style Guides
        {
            "path": "style-guide/scifi-style-guide.txt",
            "type": "writing_guide",
            "metadata": {
                "type": "writing_guide",
                "category": "style",
                "narrative_type": [NarrativeType.TECHNICAL],
                "security_level": SecurityLevel.PUBLIC
            },
            "namespace": "style_guides"
        },
        {
            "path": "style-guide/detailed-style-examples.txt",
            "type": "writing_guide",
            "metadata": {
                "type": "writing_guide",
                "category": "style",
                "narrative_type": [NarrativeType.DESCRIPTION],
                "security_level": SecurityLevel.PUBLIC
            },
            "namespace": "style_guides"
        },
        {
            "path": "story-planning/initial-story-plan.txt",
            "type": "story_planning",
            "metadata": {
                "type": "story_planning",
                "category": "initial_setup",
                "security_level": SecurityLevel.RESTRICTED,
                "filename": "initial-story-plan.txt"
            },
            "namespace": "story_planning"
        }
    ]
    
    # Index each document
    for config in document_configs:
        try:
            full_path = get_reference_doc_path(config["path"])
            logger.info(f"Processing file: {config['path']}")
            logger.info(f"Full path: {full_path}")
            logger.info(f"Metadata: {config['metadata']}")
            logger.info(f"Namespace: {config['namespace']}")
            
            # Convert enum values to strings for Pinecone
            metadata = {k: v.value if hasattr(v, 'value') else v 
                       for k, v in config["metadata"].items()}
            
            success = await rag.index_document(
                document_path=full_path,
                document_type=config["type"],
                metadata=metadata,
                namespace=config["namespace"]
            )
            
            if success:
                logger.info(f"Successfully indexed: {config['path']}")
            else:
                logger.error(f"Failed to index: {config['path']}")
                
        except Exception as e:
            logger.error(f"Error indexing {config['path']}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(index_documents()) 