from typing import Dict, List
import os
from src.services.rag_service import RAGService
from src.services.bedrock_service import BedrockService
from src.services.pinecone_service import PineconeService
from src.config.config import Settings
from src.utils.path_utils import get_reference_doc_path
from src.models.metadata_schema import (
    Species, Role, Expertise, LocationType, SecurityLevel, 
    TechCategory, TimePeriod, NarrativeType, Affiliation,
    ResearchField, ResearchStatus, SystemCategory, StationSystem,
    StationZone, CharacterCategory, PersonalityTrait,
    CommunicationStyle, WritingStyle, HistoricalSignificance,
    PoliticalInfluence, CulturalEmphasis, UrbanStyle,
    SocialStructure, TechnicalDetailLevel, ScientificAccuracy,
    SecurityClearance, SystemStatus, MaintenanceType,
    ManufacturerOrigin, MilitaryUnit, PersonnelRole,
    CombatRating, TechLevel, AugmentationLevel,
    OperationalStatus, ThreatLevel
)
import logging
import asyncio
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def index_documents():
    """Index all reference documents with appropriate metadata"""
    try:
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
                    "character_category": CharacterCategory.MAIN_CHARACTER,
                    "species": Species.HUMAN,
                    "role": [Role.SCIENTIFIC],
                    "expertise": [Expertise.GIANT_STUDIES, Expertise.QUANTUM_PHYSICS],
                    "security_level": SecurityLevel.RESTRICTED,
                    "personality_traits": [
                        PersonalityTrait.ANALYTICAL,
                        PersonalityTrait.PRAGMATIC
                    ],
                    "communication_style": CommunicationStyle.ACADEMIC,
                    "writing_style": WritingStyle.ASIMOV,
                    "age": 45,
                    "birth_location": "New Geneva, Earth",
                    "augmentations": ["Neural Interface", "Quantum Sensitivity Enhancement"],
                    "key_relationships": {
                        "Dr. Alexander Fontaine": "Medical Oversight",
                        "David Nash": "Mentee",
                        "Commander Drake": "Complex History"
                    }
                },
                "namespace": "characters"
            },
            {
                "path": "characters/character-drake.txt",
                "type": "character_profile",
                "metadata": {
                    "name": "Commander Thomas Drake",
                    "type": "character_profile",
                    "character_category": CharacterCategory.MAIN_CHARACTER,
                    "species": Species.HUMAN,
                    "role": [Role.MILITARY],
                    "expertise": [Expertise.GIANT_STUDIES, Expertise.ENGINEERING],
                    "security_level": SecurityLevel.CLASSIFIED,
                    "personality_traits": [
                        PersonalityTrait.PRAGMATIC,
                        PersonalityTrait.PROTECTIVE
                    ],
                    "communication_style": CommunicationStyle.MILITARY,
                    "writing_style": WritingStyle.HALDEMAN,
                    "age": 42,
                    "birth_location": "Mars Military Complex",
                    "augmentations": ["Combat Neural Suite", "Tactical Enhancement System"],
                    "key_relationships": {
                        "Dr. Chen": "Complex History",
                        "Marcus Webb": "Trusted Operative",
                        "Dr. Vass": "Cautious Alliance"
                    }
                },
                "namespace": "characters"
            },
            {
                "path": "characters/character-nash.txt",
                "type": "character_profile",
                "metadata": {
                    "name": "David Nash",
                    "type": "character_profile",
                    "character_category": CharacterCategory.MAIN_CHARACTER,
                    "species": Species.HUMAN,
                    "role": [Role.SCIENTIFIC],
                    "expertise": [Expertise.QUANTUM_PHYSICS, Expertise.GIANT_STUDIES],
                    "security_level": SecurityLevel.RESTRICTED,
                    "personality_traits": [
                        PersonalityTrait.IDEALISTIC,
                        PersonalityTrait.INNOVATIVE
                    ],
                    "communication_style": CommunicationStyle.TECHNICAL,
                    "writing_style": WritingStyle.TECHNICAL,
                    "age": 28,
                    "birth_location": "New Geneva, Earth",
                    "augmentations": ["Basic Research Interface", "Data Processing Enhancement"],
                    "key_relationships": {
                        "Dr. Chen": "Mentor",
                        "Dr. Fontaine": "Medical Monitor",
                        "Dr. Vass": "Research Interest"
                    }
                },
                "namespace": "characters"
            },
            {
                "path": "characters/character-vass.txt",
                "type": "character_profile",
                "metadata": {
                    "name": "Dr. Victor Vass",
                    "type": "character_profile",
                    "character_category": CharacterCategory.MAIN_CHARACTER,
                    "species": Species.VESS,
                    "role": [Role.SCIENTIFIC, Role.POLITICAL],
                    "expertise": [Expertise.GIANT_STUDIES, Expertise.QUANTUM_PHYSICS],
                    "security_level": SecurityLevel.CLASSIFIED,
                    "personality_traits": [
                        PersonalityTrait.MYSTERIOUS,
                        PersonalityTrait.ANALYTICAL
                    ],
                    "communication_style": CommunicationStyle.ALIEN,
                    "writing_style": WritingStyle.TECHNICAL,
                    "age": None,  # Unknown/Non-human
                    "birth_location": "Vess Homeworld",
                    "special_abilities": ["Multi-dimensional Processing", "Quantum State Awareness"],
                    "key_relationships": {
                        "Dr. Chen": "Scientific Partnership",
                        "Commander Drake": "Cautious Alliance",
                        "David Nash": "Subject of Study"
                    }
                },
                "namespace": "characters"
            },
            {
                "path": "characters/character-fontaine.txt",
                "type": "character_profile",
                "metadata": {
                    "name": "Dr. Alexander Fontaine",
                    "type": "character_profile",
                    "character_category": CharacterCategory.MAIN_CHARACTER,
                    "species": Species.HUMAN,
                    "role": [Role.SCIENTIFIC],
                    "expertise": [Expertise.MEDICINE],
                    "security_level": SecurityLevel.RESTRICTED,
                    "personality_traits": [
                        PersonalityTrait.SARCASTIC,
                        PersonalityTrait.PROTECTIVE
                    ],
                    "communication_style": CommunicationStyle.MEDICAL,
                    "writing_style": WritingStyle.TECHNICAL,
                    "age": 48,
                    "birth_location": "Luna Medical Center",
                    "augmentations": ["Medical Neural Suite", "Diagnostic Interface"],
                    "key_relationships": {
                        "Dr. Chen": "Medical Oversight",
                        "Commander Drake": "Military Understanding",
                        "David Nash": "Mentorship"
                    }
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

            # Earth-Mars Relations Documents
            {
                "path": "world/earth-mars-historical-events.txt",
                "type": "world_building",
                "metadata": {
                    "type": "historical",
                    "category": "earth_mars_relations",
                    "time_period": TimePeriod.HISTORICAL,
                    "security_level": SecurityLevel.PUBLIC,
                    "historical_significance": HistoricalSignificance.MAJOR,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "world"
            },
            {
                "path": "world/earth-mars-political-figures.txt",
                "type": "world_building",
                "metadata": {
                    "type": "political",
                    "category": "earth_mars_relations",
                    "time_period": TimePeriod.PRESENT,
                    "security_level": SecurityLevel.PUBLIC,
                    "political_influence": PoliticalInfluence.HIGH,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "world"
            },
            {
                "path": "world/earth-mars-relations.txt",
                "type": "world_building",
                "metadata": {
                    "type": "political",
                    "category": "earth_mars_relations",
                    "time_period": TimePeriod.PRESENT,
                    "security_level": SecurityLevel.PUBLIC,
                    "political_influence": PoliticalInfluence.HIGH,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "world"
            },

            # Earth Cities
            {
                "path": "world/locations/new-geneva.txt",
                "type": "location",
                "metadata": {
                    "type": "city",
                    "category": "earth_city",
                    "location_type": LocationType.PLANET,
                    "security_level": SecurityLevel.PUBLIC,
                    "cultural_emphasis": CulturalEmphasis.ACADEMIC,
                    "urban_style": UrbanStyle.ADVANCED,
                    "population": 12000000,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
            },
            {
                "path": "world/locations/new-geneva-culture.txt",
                "type": "location",
                "metadata": {
                    "type": "culture",
                    "category": "earth_city",
                    "location_type": LocationType.PLANET,
                    "security_level": SecurityLevel.PUBLIC,
                    "cultural_emphasis": CulturalEmphasis.ACADEMIC,
                    "social_structure": SocialStructure.MERITOCRACY,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
            },
            {
                "path": "world/locations/neo-tokyo.txt",
                "type": "location",
                "metadata": {
                    "type": "city",
                    "category": "earth_city",
                    "location_type": LocationType.PLANET,
                    "security_level": SecurityLevel.PUBLIC,
                    "cultural_emphasis": CulturalEmphasis.TECHNOLOGICAL,
                    "urban_style": UrbanStyle.CYBERPUNK,
                    "population": 35000000,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
            },

            # Mars Cities
            {
                "path": "world/locations/olympus-city.txt",
                "type": "location",
                "metadata": {
                    "type": "city",
                    "category": "mars_city",
                    "location_type": LocationType.PLANET,
                    "security_level": SecurityLevel.PUBLIC,
                    "cultural_emphasis": CulturalEmphasis.MILITARY,
                    "urban_style": UrbanStyle.FORTRESS,
                    "population": 5000000,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
            },
            {
                "path": "world/locations/valles-marineris-strip.txt",
                "type": "location",
                "metadata": {
                    "type": "city",
                    "category": "mars_city",
                    "location_type": LocationType.PLANET,
                    "security_level": SecurityLevel.PUBLIC,
                    "cultural_emphasis": CulturalEmphasis.INDUSTRIAL,
                    "urban_style": UrbanStyle.UNDERGROUND,
                    "population": 8000000,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
            },

            # Research Stations
            {
                "path": "world/locations/havens-rest.txt",
                "type": "location",
                "metadata": {
                    "type": "research_station",
                    "category": "research_facility",
                    "location_type": LocationType.STATION,
                    "security_level": SecurityLevel.RESTRICTED,
                    "research_field": ResearchField.GIANT_STUDIES,
                    "research_status": ResearchStatus.IMPLEMENTATION,
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "locations"
            },
            {
                "path": "world/locations/havens-rest-research.txt",
                "type": "location",
                "metadata": {
                    "type": "research_data",
                    "category": "research_facility",
                    "location_type": LocationType.STATION,
                    "security_level": SecurityLevel.CLASSIFIED,
                    "research_field": ResearchField.GIANT_STUDIES,
                    "research_status": ResearchStatus.IMPLEMENTATION,
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "locations"
            },
            {
                "path": "world/locations/havens-rest-personnel.txt",
                "type": "location",
                "metadata": {
                    "type": "personnel",
                    "category": "research_facility",
                    "location_type": LocationType.STATION,
                    "security_level": SecurityLevel.RESTRICTED,
                    "personnel_role": PersonnelRole.RESEARCH,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
            },

            # Frontier Cities
            {
                "path": "world/locations/landing-city.txt",
                "type": "location",
                "metadata": {
                    "type": "city",
                    "category": "frontier_city",
                    "location_type": LocationType.PLANET,
                    "security_level": SecurityLevel.PUBLIC,
                    "cultural_emphasis": CulturalEmphasis.COMMERCIAL,
                    "urban_style": UrbanStyle.FRONTIER,
                    "population": 2000000,
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
            },
            {
                "path": "world/locations/landing-city-species.txt",
                "type": "location",
                "metadata": {
                    "type": "demographics",
                    "category": "frontier_city",
                    "location_type": LocationType.PLANET,
                    "security_level": SecurityLevel.PUBLIC,
                    "species_diversity": ["human", "vess", "other"],
                    "narrative_type": NarrativeType.DESCRIPTION
                },
                "namespace": "locations"
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
            {
                "path": "narrative-framework/character-voices.txt",
                "type": "narrative",
                "metadata": {
                    "type": "writing_guide",
                    "category": "character_development",
                    "narrative_type": [NarrativeType.DIALOGUE],
                    "security_level": SecurityLevel.PUBLIC,
                    "writing_style": WritingStyle.TECHNICAL
                },
                "namespace": "narrative"
            },
            {
                "path": "narrative-framework/scene-structure.txt",
                "type": "narrative",
                "metadata": {
                    "type": "writing_guide",
                    "category": "scene_construction",
                    "narrative_type": [NarrativeType.TECHNICAL, NarrativeType.DESCRIPTION],
                    "security_level": SecurityLevel.PUBLIC,
                    "writing_style": WritingStyle.TECHNICAL
                },
                "namespace": "narrative"
            },
            {
                "path": "narrative-framework/scene-transitions.txt",
                "type": "narrative",
                "metadata": {
                    "type": "writing_guide",
                    "category": "scene_construction",
                    "narrative_type": [NarrativeType.DESCRIPTION],
                    "security_level": SecurityLevel.PUBLIC,
                    "writing_style": WritingStyle.TECHNICAL
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
            },
            {
                "path": "style-guide/novel-analysis.txt",
                "type": "writing_guide",
                "metadata": {
                    "type": "writing_guide",
                    "category": "analysis",
                    "narrative_type": [NarrativeType.TECHNICAL],
                    "security_level": SecurityLevel.PUBLIC,
                    "writing_style": WritingStyle.TECHNICAL,
                    "style_influences": ["Asimov", "Haldeman", "Clarke"],
                    "analysis_focus": ["Structure", "Pacing", "Technical Detail"],
                    "narrative_techniques": [
                        "Hard Science Integration",
                        "Character Development",
                        "World Building"
                    ]
                },
                "namespace": "style_guides"
            },
            {
                "path": "style-guide/scifi-style-guide.txt",
                "type": "writing_guide",
                "metadata": {
                    "type": "writing_guide",
                    "category": "style_guide",
                    "narrative_type": [NarrativeType.TECHNICAL],
                    "security_level": SecurityLevel.PUBLIC,
                    "writing_style": WritingStyle.TECHNICAL,
                    "style_influences": ["Asimov", "Haldeman", "Clarke"],
                    "technical_detail_level": "High",
                    "scientific_accuracy": "Maximum",
                    "jargon_guidelines": "Technical terms must be accurate",
                    "explanation_style": "Clear, precise, scientific",
                    "scene_types": [
                        "Technical Discussion",
                        "Scientific Discovery",
                        "Crisis Response",
                        "Character Development"
                    ]
                },
                "namespace": "style_guides"
            },

            # Military Documentation
            {
                "path": "military/concordat-defense-force.txt",
                "type": "military",
                "metadata": {
                    "type": "military_organization",
                    "category": "defense_force",
                    "security_level": SecurityLevel.RESTRICTED,
                    "affiliation": Affiliation.CONCORDAT,
                    "time_period": TimePeriod.PRESENT,
                    "tech_category": [TechCategory.HUMAN, TechCategory.GIANT],
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "military"
            },
            {
                "path": "military/corporate-security-forces.txt",
                "type": "military",
                "metadata": {
                    "type": "military_organization",
                    "category": "security_force",
                    "security_level": SecurityLevel.PUBLIC,
                    "affiliation": Affiliation.INDEPENDENT,
                    "time_period": TimePeriod.PRESENT,
                    "tech_category": TechCategory.HUMAN,
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "military"
            },
            {
                "path": "military/frontier-defense-alliance.txt",
                "type": "military",
                "metadata": {
                    "type": "military_organization",
                    "category": "defense_force",
                    "security_level": SecurityLevel.RESTRICTED,
                    "affiliation": Affiliation.FRONTIER,
                    "time_period": TimePeriod.PRESENT,
                    "tech_category": [TechCategory.HUMAN, TechCategory.HYBRID],
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "military"
            },
            {
                "path": "military/rd-projects.txt",
                "type": "military",
                "metadata": {
                    "type": "research_development",
                    "category": "military_research",
                    "security_level": SecurityLevel.CLASSIFIED,
                    "tech_category": [TechCategory.GIANT, TechCategory.HYBRID],
                    "research_field": ResearchField.QUANTUM,
                    "research_status": ResearchStatus.ADVANCED_TESTING,
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "military"
            },

            # Special Military Units
            {
                "path": "military/special-military-units.txt",
                "type": "military",
                "metadata": {
                    "type": "military_organization",
                    "category": "special_forces",
                    "security_level": SecurityLevel.CLASSIFIED,
                    "affiliation": Affiliation.CONCORDAT,
                    "time_period": TimePeriod.PRESENT,
                    "tech_category": [TechCategory.HUMAN, TechCategory.GIANT, TechCategory.HYBRID],
                    "narrative_type": NarrativeType.TECHNICAL,
                    "unit_type": MilitaryUnit.SPECIAL_OPS,
                    "combat_rating": CombatRating.ELITE,
                    "mission_types": [
                        "Fragment Containment",
                        "Giant Tech Recovery",
                        "Deep Space Operations",
                        "Crisis Response"
                    ],
                    "equipment_level": TechLevel.ADVANCED,
                    "personnel_augmentation": AugmentationLevel.HIGH,
                    "security_clearance": SecurityClearance.MAXIMUM,
                    "operational_status": OperationalStatus.ACTIVE
                },
                "namespace": "military"
            },

            # Void Raiders
            {
                "path": "military/void-raiders-alliance.txt",
                "type": "military",
                "metadata": {
                    "type": "military_organization",
                    "category": "rogue_force",
                    "security_level": SecurityLevel.RESTRICTED,
                    "affiliation": Affiliation.INDEPENDENT,
                    "time_period": TimePeriod.PRESENT,
                    "tech_category": [TechCategory.HYBRID, TechCategory.FRAGMENT],
                    "narrative_type": NarrativeType.TECHNICAL,
                    "unit_type": MilitaryUnit.IRREGULAR,
                    "combat_rating": CombatRating.HIGH,
                    "mission_types": [
                        "Raiding",
                        "Tech Theft",
                        "Fragment Recovery",
                        "Black Market Operations"
                    ],
                    "equipment_level": TechLevel.MIXED,
                    "personnel_augmentation": AugmentationLevel.VARIED,
                    "threat_level": ThreatLevel.HIGH,
                    "operational_status": OperationalStatus.ACTIVE
                },
                "namespace": "military"
            },
            # Station Documentation
            {
                "path": "station-omega/life-support.txt",
                "type": "technical",
                "metadata": {
                    "type": "station_systems",
                    "category": "life_support",
                    "system_category": SystemCategory.LIFE_SUPPORT,
                    "station_system": StationSystem.LIFE_SUPPORT,
                    "station_zone": StationZone.CORE,
                    "security_level": SecurityLevel.RESTRICTED,
                    "tech_category": TechCategory.STATION,
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "technical"
            },
            {
                "path": "station-omega/power-systems.txt",
                "type": "technical",
                "metadata": {
                    "type": "station_systems",
                    "category": "power",
                    "system_category": SystemCategory.POWER,
                    "station_system": StationSystem.POWER,
                    "station_zone": StationZone.CORE,
                    "security_level": SecurityLevel.RESTRICTED,
                    "tech_category": TechCategory.STATION,
                    "narrative_type": NarrativeType.TECHNICAL
                },
                "namespace": "technical"
            },
            
            # Technical Documentation
            {
                "path": "technical/fragment-analysis.txt",
                "type": "technical",
                "metadata": {
                    "type": "technical_research",
                    "category": "fragment_studies",
                    "security_level": SecurityLevel.CLASSIFIED,
                    "tech_category": [TechCategory.FRAGMENT, TechCategory.GIANT],
                    "research_field": ResearchField.QUANTUM,
                    "research_status": ResearchStatus.IMPLEMENTATION,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "technical_detail_level": TechnicalDetailLevel.MAXIMUM,
                    "scientific_accuracy": ScientificAccuracy.RIGOROUS,
                    "related_systems": [
                        StationSystem.FRAGMENT_CONTAINMENT,
                        StationSystem.RESEARCH,
                        StationSystem.POWER
                    ],
                    "classification_reason": [
                        "Fragment behavior patterns",
                        "Quantum resonance data",
                        "Consciousness signatures"
                    ]
                },
                "namespace": "technical"
            },
            {
                "path": "technical/ftl-physics-principles.txt",
                "type": "technical",
                "metadata": {
                    "type": "technical_research",
                    "category": "physics_fundamentals",
                    "security_level": SecurityLevel.RESTRICTED,
                    "tech_category": [TechCategory.HUMAN, TechCategory.GIANT],
                    "research_field": ResearchField.QUANTUM,
                    "research_status": ResearchStatus.IMPLEMENTATION,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "technical_detail_level": TechnicalDetailLevel.HIGH,
                    "scientific_accuracy": ScientificAccuracy.RIGOROUS,
                    "related_technologies": [
                        "Void Drive Systems",
                        "Reality Phase Manipulation",
                        "Quantum Field Harmonics"
                    ],
                    "theoretical_foundations": [
                        "Quantum Mechanics",
                        "Spacetime Topology",
                        "Giant Tech Principles"
                    ]
                },
                "namespace": "technical"
            },
            {
                "path": "technical/quantum-physics-principles.txt",
                "type": "technical",
                "metadata": {
                    "type": "technical_research",
                    "category": "physics_fundamentals",
                    "security_level": SecurityLevel.PUBLIC,
                    "tech_category": TechCategory.HUMAN,
                    "research_field": ResearchField.QUANTUM,
                    "research_status": ResearchStatus.IMPLEMENTATION,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "technical_detail_level": TechnicalDetailLevel.HIGH,
                    "scientific_accuracy": ScientificAccuracy.MAXIMUM,
                    "theoretical_foundations": [
                        "Standard Quantum Theory",
                        "Consciousness Integration",
                        "Giant Tech Applications"
                    ],
                    "key_principles": [
                        "Quantum Entanglement",
                        "Wave-Particle Duality",
                        "Observer Effect",
                        "Reality Phase States"
                    ]
                },
                "namespace": "technical"
            },
            {
                "path": "technical/technology-evolution-timeline.txt",
                "type": "technical",
                "metadata": {
                    "type": "technical_history",
                    "category": "technology_development",
                    "security_level": SecurityLevel.PUBLIC,
                    "tech_category": [
                        TechCategory.HUMAN,
                        TechCategory.GIANT,
                        TechCategory.HYBRID
                    ],
                    "time_period": TimePeriod.HISTORICAL,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "technical_detail_level": TechnicalDetailLevel.HIGH,
                    "historical_significance": HistoricalSignificance.MAJOR,
                    "development_phases": [
                        "Pre-Giant Discovery",
                        "Initial Giant Tech Integration",
                        "Fragment Research Era",
                        "Modern Hybrid Systems"
                    ],
                    "key_breakthroughs": [
                        "FTL Travel",
                        "Quantum Computing",
                        "Fragment Containment",
                        "Consciousness Transfer"
                    ]
                },
                "namespace": "technical"
            },
            # Station Omega Documentation
            {
                "path": "station-omega/station-layout.txt",
                "type": "technical",
                "metadata": {
                    "type": "station_systems",
                    "category": "station_layout",
                    "system_category": SystemCategory.STRUCTURAL,
                    "station_system": StationSystem.STRUCTURAL,
                    "station_zone": [
                        StationZone.COMMAND_RING,
                        StationZone.RESEARCH_RING,
                        StationZone.HABITAT_RING,
                        StationZone.CORE,
                        StationZone.DOCKING,
                        StationZone.EXTERNAL
                    ],
                    "security_level": SecurityLevel.RESTRICTED,
                    "tech_category": TechCategory.STATION,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "connected_systems": {
                        StationSystem.POWER: "Primary distribution network",
                        StationSystem.LIFE_SUPPORT: "Environmental zones",
                        StationSystem.TRANSPORTATION: "Transit systems",
                        StationSystem.SECURITY: "Access control points"
                    },
                    "emergency_protocols": [
                        "Section isolation",
                        "Emergency bulkhead deployment",
                        "Zone depressurization",
                        "Evacuation routing"
                    ]
                },
                "namespace": "technical"
            },
            {
                "path": "station-omega/station-systems.txt",
                "type": "technical",
                "metadata": {
                    "type": "station_systems",
                    "category": "systems_overview",
                    "system_category": SystemCategory.INTEGRATED,
                    "station_system": [
                        StationSystem.POWER,
                        StationSystem.LIFE_SUPPORT,
                        StationSystem.SECURITY,
                        StationSystem.TRANSPORTATION,
                        StationSystem.COMMUNICATION,
                        StationSystem.FRAGMENT_CONTAINMENT
                    ],
                    "security_level": SecurityLevel.RESTRICTED,
                    "tech_category": TechCategory.STATION,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "system_status": SystemStatus.OPERATIONAL,
                    "maintenance_type": MaintenanceType.SCHEDULED,
                    "manufacturer": ManufacturerOrigin.CONCORDAT,
                    "certification_level": "Omega-class",
                    "redundancy_level": 3,
                    "emergency_protocols": [
                        "System isolation",
                        "Power rerouting",
                        "Emergency backup activation",
                        "Critical systems prioritization"
                    ]
                },
                "namespace": "technical"
            },
            {
                "path": "station-omega/life-support.txt",
                "type": "technical",
                "metadata": {
                    "type": "station_systems",
                    "category": "life_support",
                    "system_category": SystemCategory.LIFE_SUPPORT,
                    "station_system": StationSystem.LIFE_SUPPORT,
                    "station_zone": StationZone.CORE,
                    "security_level": SecurityLevel.RESTRICTED,
                    "tech_category": TechCategory.STATION,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "system_status": SystemStatus.OPERATIONAL,
                    "maintenance_type": MaintenanceType.ROUTINE,
                    "manufacturer": ManufacturerOrigin.CONCORDAT,
                    "power_requirements": "15% station capacity",
                    "processing_capacity": "2.1 million inhabitants",
                    "response_time": "0.3 seconds",
                    "backup_systems": [
                        StationSystem.EMERGENCY,
                        StationSystem.ENVIRONMENTAL
                    ]
                },
                "namespace": "technical"
            },
            {
                "path": "station-omega/power-systems.txt",
                "type": "technical",
                "metadata": {
                    "type": "station_systems",
                    "category": "power",
                    "system_category": SystemCategory.POWER,
                    "station_system": StationSystem.POWER,
                    "station_zone": StationZone.CORE,
                    "security_level": SecurityLevel.RESTRICTED,
                    "tech_category": TechCategory.STATION,
                    "narrative_type": NarrativeType.TECHNICAL,
                    "system_status": SystemStatus.OPERATIONAL,
                    "maintenance_type": MaintenanceType.SCHEDULED,
                    "manufacturer": ManufacturerOrigin.CONCORDAT,
                    "power_requirements": "1.2 terawatts nominal",
                    "processing_capacity": "150% maximum load",
                    "response_time": "0.1 seconds",
                    "backup_systems": [
                        StationSystem.EMERGENCY,
                        StationSystem.FRAGMENT_CONTAINMENT
                    ],
                    "connected_systems": {
                        StationSystem.LIFE_SUPPORT: "Primary power",
                        StationSystem.SECURITY: "Critical power",
                        StationSystem.FRAGMENT_CONTAINMENT: "Priority power",
                        StationSystem.RESEARCH: "Variable load"
                    }
                },
                "namespace": "technical"
            },
            # Asimov Style Guide Parts
            *[{
                "path": f"style-guide/asimov-foundation-part{i}.txt",
                "type": "writing_guide",
                "metadata": {
                    "type": "style_guide",
                    "category": "writing_style",
                    "writing_style": WritingStyle.ASIMOV,
                    "narrative_type": [NarrativeType.TECHNICAL, NarrativeType.DESCRIPTION],
                    "security_level": SecurityLevel.PUBLIC,
                    "part_number": i,
                    "total_parts": 8
                },
                "namespace": "style_guides"
            } for i in range(1, 9)],  # Parts 1-8

            # Haldeman Style Guide Parts
            *[{
                "path": f"style-guide/haldeman-the-forever-war-part{i}.txt",
                "type": "writing_guide",
                "metadata": {
                    "type": "style_guide",
                    "category": "writing_style",
                    "writing_style": WritingStyle.HALDEMAN,
                    "narrative_type": [NarrativeType.ACTION, NarrativeType.DIALOGUE],
                    "security_level": SecurityLevel.PUBLIC,
                    "part_number": i,
                    "total_parts": 3
                },
                "namespace": "style_guides"
            } for i in range(1, 4)],  # Parts 1-3
        ]
        
        # Index each document
        for config in document_configs:
            try:
                full_path = get_reference_doc_path(config["path"])
                if not os.path.exists(full_path):
                    logger.error(f"File not found: {config['path']}")
                    continue

                # Convert enum values and handle None values
                metadata = {}
                for k, v in config["metadata"].items():
                    if v is None:
                        continue  # Skip None values
                    elif isinstance(v, Enum):
                        metadata[k] = v.value
                    elif isinstance(v, list):
                        metadata[k] = [x.value if isinstance(x, Enum) else x for x in v]
                    elif isinstance(v, dict):
                        if k in ["key_relationships", "connected_systems"]:
                            # Convert dictionaries to lists of strings
                            metadata[k] = [f"{key}:{value}" for key, value in v.items()]
                        else:
                            # Skip other dictionaries as they're not supported by Pinecone
                            continue
                    else:
                        metadata[k] = v

                success = await rag.index_document(
                    document_path=full_path,
                    document_type=config["type"],
                    metadata=metadata,
                    namespace=config["namespace"]
                )
                
                if success:
                    logger.info(f"✓ {config['path']}")
                else:
                    logger.error(f"✗ {config['path']}")
                    
            except Exception as e:
                logger.error(f"✗ {config['path']}: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")

if __name__ == "__main__":
    asyncio.run(index_documents()) 