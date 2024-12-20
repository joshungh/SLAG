from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class Species(str, Enum):
    HUMAN = "human"
    VESS = "vess"
    OTHER = "other"

class Role(str, Enum):
    MILITARY = "military"
    SCIENTIFIC = "scientific"
    POLITICAL = "political"
    TECHNICAL = "technical"

class Affiliation(str, Enum):
    CONCORDAT = "concordat"
    FRONTIER = "frontier"
    INDEPENDENT = "independent"

class Expertise(str, Enum):
    GIANT_STUDIES = "giant_studies"
    QUANTUM_PHYSICS = "quantum_physics"
    ENGINEERING = "engineering"
    MEDICINE = "medicine"

class LocationType(str, Enum):
    STATION = "station"
    PLANET = "planet"
    SHIP = "ship"
    VOID = "void"

class SecurityLevel(str, Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    CLASSIFIED = "classified"

class TimePeriod(str, Enum):
    PRESENT = "present"
    HISTORICAL = "historical"
    FUTURE = "future"

class NarrativeType(str, Enum):
    ACTION = "action"
    DIALOGUE = "dialogue"
    DESCRIPTION = "description"
    TECHNICAL = "technical"

class TechCategory(str, Enum):
    GIANT = "giant"
    HUMAN = "human"
    VESS = "vess"
    HYBRID = "hybrid"
    FRAGMENT = "fragment"
    STATION = "station"
    QUANTUM = "quantum"
    CONTAINMENT = "containment"
    INTEGRATED = "integrated"

class SystemCategory(str, Enum):
    POWER = "power"
    LIFE_SUPPORT = "life_support"
    SECURITY = "security"
    RESEARCH = "research"
    MEDICAL = "medical"
    TRANSPORTATION = "transportation"
    STRUCTURAL = "structural"
    INTEGRATED = "integrated"

class StationSystem(str, Enum):
    POWER = "power"
    LIFE_SUPPORT = "life_support"
    SECURITY = "security"
    TRANSPORTATION = "transportation"
    COMMUNICATION = "communication"
    MEDICAL = "medical"
    RESEARCH = "research"
    ENVIRONMENTAL = "environmental"
    FRAGMENT_CONTAINMENT = "fragment_containment"
    EMERGENCY = "emergency"
    STRUCTURAL = "structural"

class StationZone(str, Enum):
    COMMAND_RING = "command_ring"
    RESEARCH_RING = "research_ring"
    HABITAT_RING = "habitat_ring"
    CORE = "core"
    DOCKING = "docking"
    EXTERNAL = "external"

class SystemStatus(str, Enum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"

class SecurityClearance(str, Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    HIGH = "high"
    MAXIMUM = "maximum"
    OMEGA = "omega"

class MaintenanceType(str, Enum):
    ROUTINE = "routine"
    SCHEDULED = "scheduled"
    EMERGENCY = "emergency"
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"

class ManufacturerOrigin(str, Enum):
    CONCORDAT = "concordat"
    FRONTIER = "frontier"
    EARTH = "earth"
    MARS = "mars"
    VESS = "vess"
    HYBRID = "hybrid"

class DocumentType(str, Enum):
    TECHNICAL_SPEC = "technical_spec"
    OPERATION_MANUAL = "operation_manual"
    MAINTENANCE_GUIDE = "maintenance_guide"
    EMERGENCY_PROCEDURE = "emergency_procedure"
    SECURITY_PROTOCOL = "security_protocol"
    SYSTEM_LAYOUT = "system_layout"
    TECHNICAL_RESEARCH = "technical_research"
    TECHNICAL_HISTORY = "technical_history"
    RESEARCH_DATA = "research_data"
    RESEARCH_STATION = "research_station"
    PERSONNEL = "personnel"
    CHARACTER_PROFILE = "character_profile"
    LOCATION = "location"
    WORLD_BUILDING = "world_building"
    WRITING_GUIDE = "writing_guide"
    STYLE_GUIDE = "style_guide"

class HistoricalPeriod(str, Enum):
    PRE_GIANT = "pre_giant"
    DISCOVERY = "discovery"
    INTEGRATION = "integration"
    GIANT_WARS = "giant_wars"
    POST_WAR = "post_war"
    MODERN = "modern"

class ConflictType(str, Enum):
    GIANT_ENGAGEMENT = "giant_engagement"
    HUMAN_CONFLICT = "human_conflict"
    CORPORATE_WAR = "corporate_war"
    REBELLION = "rebellion"
    FIRST_CONTACT = "first_contact"

class BattleScale(str, Enum):
    SKIRMISH = "skirmish"
    BATTLE = "battle"
    CAMPAIGN = "campaign"
    WAR = "war"
    CRISIS = "crisis"

class HistoricalSignificance(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"
    PARADIGM_SHIFT = "paradigm_shift"

class MilitaryUnit(str, Enum):
    REGULAR = "regular"
    SPECIAL_OPS = "special_ops"
    IRREGULAR = "irregular"
    ELITE = "elite"
    SUPPORT = "support"

class EquipmentClass(str, Enum):
    STANDARD = "standard"
    EXPERIMENTAL = "experimental"
    PROTOTYPE = "prototype"
    CLASSIFIED = "classified"
    RESTRICTED = "restricted"

class CombatRole(str, Enum):
    ASSAULT = "assault"
    RECON = "recon"
    SUPPORT = "support"
    SPECIALIST = "specialist"
    COMMAND = "command"

class ProjectStatus(str, Enum):
    CONCEPT = "concept"
    DEVELOPMENT = "development"
    TESTING = "testing"
    FIELD_TRIAL = "field_trial"
    DEPLOYED = "deployed"

class CulturalTradition(str, Enum):
    TRADITIONAL = "traditional"
    TECH_FUSION = "tech_fusion"
    NEO_TRADITIONAL = "neo_traditional"
    QUANTUM_ENHANCED = "quantum_enhanced"
    PURE_MODERN = "pure_modern"

class SocialStructure(str, Enum):
    MERITOCRACY = "meritocracy"
    CORPORATE = "corporate"
    MILITARY = "military"
    DEMOCRATIC = "democratic"
    HYBRID = "hybrid"

class CulturalEmphasis(str, Enum):
    ACADEMIC = "academic"
    TECHNOLOGICAL = "technological"
    MILITARY = "military"
    INDUSTRIAL = "industrial"
    COMMERCIAL = "commercial"

class UrbanStyle(str, Enum):
    ADVANCED = "advanced"
    CYBERPUNK = "cyberpunk"
    FORTRESS = "fortress"
    UNDERGROUND = "underground"
    FRONTIER = "frontier"

class HistoricalEra(str, Enum):
    EARLY_MARS = "early_mars"
    FRAGMENT_DISCOVERY = "fragment_discovery"
    WAR_PERIOD = "war_period"
    INDEPENDENCE = "independence"
    MODERN = "modern"

class PoliticalRelation(str, Enum):
    COOPERATIVE = "cooperative"
    TENSE = "tense"
    HOSTILE = "hostile"
    INTEGRATED = "integrated"
    AUTONOMOUS = "autonomous"

class SettlementType(str, Enum):
    CAPITAL = "capital"
    INDUSTRIAL = "industrial"
    RESEARCH = "research"
    AGRICULTURAL = "agricultural"
    MINING = "mining"

class PlanetaryRole(str, Enum):
    ADMINISTRATIVE = "administrative"
    MILITARY = "military"
    SCIENTIFIC = "scientific"
    ECONOMIC = "economic"
    CULTURAL = "cultural"

class ColonialStatus(str, Enum):
    EARTH_DEPENDENT = "earth_dependent"
    SEMI_AUTONOMOUS = "semi_autonomous"
    INDEPENDENT = "independent"
    INTERDEPENDENT = "interdependent"
    SOVEREIGN = "sovereign"

class ResearchField(str, Enum):
    XENOBIOLOGY = "xenobiology"
    AGRICULTURE = "agriculture"
    MEDICAL = "medical"
    ENVIRONMENTAL = "environmental"
    QUANTUM = "quantum"
    GIANT_STUDIES = "giant_studies"
    PHYSICS = "physics"
    FRAGMENT_STUDIES = "fragment_studies"

class ResearchStatus(str, Enum):
    CONCEPTUAL = "conceptual"
    EARLY_TRIALS = "early_trials"
    ADVANCED_TESTING = "advanced_testing"
    IMPLEMENTATION = "implementation"
    PRODUCTION = "production"

class SecurityProtocol(str, Enum):
    STANDARD = "standard"
    ENHANCED = "enhanced"
    HIGH = "high"
    MAXIMUM = "maximum"
    OMEGA = "omega"

class PersonnelRole(str, Enum):
    RESEARCH = "research"
    COMMAND = "command"
    TECHNICAL = "technical"
    SUPPORT = "support"
    SPECIALIST = "specialist"

class CharacterCategory(str, Enum):
    MAIN_CHARACTER = "main_character"
    SUPPORTING = "supporting"
    HISTORICAL = "historical"
    REFERENCE = "reference"

class PersonalityTrait(str, Enum):
    ANALYTICAL = "analytical"
    PRAGMATIC = "pragmatic"
    IDEALISTIC = "idealistic"
    INNOVATIVE = "innovative"
    PROTECTIVE = "protective"
    MYSTERIOUS = "mysterious"
    SARCASTIC = "sarcastic"

class CommunicationStyle(str, Enum):
    TECHNICAL = "technical"
    MILITARY = "military"
    ACADEMIC = "academic"
    INFORMAL = "informal"
    ALIEN = "alien"
    MEDICAL = "medical"
    ENGINEERING = "engineering"

class WritingStyle(str, Enum):
    ASIMOV = "asimov"
    HALDEMAN = "haldeman"
    TECHNICAL = "technical"
    DESCRIPTIVE = "descriptive"
    DIALOGUE = "dialogue"
    ACTION = "action"

class StyleCategory(str, Enum):
    STYLE_REFERENCE = "style_reference"
    STYLE_GUIDE = "style_guide"
    ANALYSIS = "analysis"
    FRAMEWORK = "framework"

class CombatRating(str, Enum):
    STANDARD = "standard"
    HIGH = "high"
    ELITE = "elite"
    LEGENDARY = "legendary"

class TechLevel(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    EXPERIMENTAL = "experimental"
    MIXED = "mixed"

class AugmentationLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VARIED = "varied"
    MAXIMUM = "maximum"

class ThreatLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    OMEGA = "omega"

class OperationalStatus(str, Enum):
    ACTIVE = "active"
    STANDBY = "standby"
    DEPLOYED = "deployed"
    TRAINING = "training"
    DISABLED = "disabled"

class ClassificationReason(str, Enum):
    SECURITY = "security"
    TECHNICAL = "technical"
    POLITICAL = "political"
    MILITARY = "military"
    RESEARCH = "research"
    FRAGMENT_BEHAVIOR = "fragment_behavior"
    QUANTUM_RESONANCE = "quantum_resonance"
    CONSCIOUSNESS_SIGNATURES = "consciousness_signatures"

class TheoreticalFoundation(str, Enum):
    QUANTUM = "quantum"
    RELATIVISTIC = "relativistic"
    GIANT = "giant"
    HYBRID = "hybrid"
    EXPERIMENTAL = "experimental"

class DevelopmentPhase(str, Enum):
    CONCEPTUAL = "conceptual"
    PROTOTYPE = "prototype"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    ESTABLISHED = "established"
    OBSOLETE = "obsolete"

class TechnicalDetailLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"

class ScientificAccuracy(str, Enum):
    SPECULATIVE = "speculative"
    PLAUSIBLE = "plausible"
    RIGOROUS = "rigorous"
    MAXIMUM = "maximum"

class PoliticalInfluence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    MAXIMUM = "maximum"

class DocumentMetadata(BaseModel):
    """Metadata schema for all documents"""
    # Basic info
    type: DocumentType
    category: str
    source: str


    
    # Station-specific
    station_system: Optional[StationSystem] = None
    station_zone: Optional[StationZone] = None
    security_clearance: Optional[SecurityClearance] = None
    system_status: Optional[SystemStatus] = None
    
    # Technical
    manufacturer: Optional[ManufacturerOrigin] = None
    maintenance_type: Optional[MaintenanceType] = None
    related_systems: Optional[List[StationSystem]] = None
    technical_dependencies: Optional[List[StationSystem]] = None
    
    # Character-specific
    species: Optional[Species] = None
    role: Optional[List[Role]] = None
    affiliation: Optional[Affiliation] = None
    expertise: Optional[List[Expertise]] = None
    character_category: Optional[CharacterCategory] = None
    personality_traits: Optional[List[PersonalityTrait]] = None
    communication_style: Optional[CommunicationStyle] = None
    age: Optional[int] = None
    biological_age: Optional[int] = None
    birth_location: Optional[str] = None
    augmentations: Optional[List[str]] = None
    special_abilities: Optional[List[str]] = None
    key_relationships: Optional[Dict[str, str]] = None
    personal_history: Optional[Dict[str, str]] = None
    character_arc: Optional[str] = None
    voice_examples: Optional[List[str]] = None
    
    # Location-specific
    location_type: Optional[LocationType] = None
    jurisdiction: Optional[Affiliation] = None
    
    # Content-specific
    time_period: Optional[TimePeriod] = None
    narrative_type: Optional[List[NarrativeType]] = None
    plot_relevance: Optional[str] = None
    crisis_related: Optional[bool] = None
    
    # System Integration
    connected_systems: Optional[Dict[StationSystem, str]] = None
    backup_systems: Optional[List[StationSystem]] = None
    emergency_protocols: Optional[List[str]] = None
    maintenance_schedule: Optional[Dict[str, MaintenanceType]] = None

    # Technical Specifications
    power_requirements: Optional[str] = None
    processing_capacity: Optional[str] = None
    response_time: Optional[str] = None
    redundancy_level: Optional[int] = None
    certification_level: Optional[str] = None 
    
    # Historical Context
    historical_period: Optional[HistoricalPeriod] = None
    conflict_type: Optional[ConflictType] = None
    battle_scale: Optional[BattleScale] = None
    historical_significance: Optional[HistoricalSignificance] = None
    historical_era: Optional[HistoricalEra] = None
    political_relation: Optional[PoliticalRelation] = None
    settlement_type: Optional[SettlementType] = None
    planetary_role: Optional[PlanetaryRole] = None
    colonial_status: Optional[ColonialStatus] = None
    
    # Event Details
    casualties: Optional[int] = None
    military_assets: Optional[Dict[str, int]] = None
    civilian_impact: Optional[str] = None
    technological_outcome: Optional[str] = None
    
    # Historical Figures
    key_figures: Optional[List[str]] = None
    military_commanders: Optional[List[str]] = None
    civilian_leaders: Optional[List[str]] = None
    notable_casualties: Optional[List[str]] = None
    
    # Long-term Impact
    doctrine_changes: Optional[List[str]] = None
    political_changes: Optional[List[str]] = None
    technological_developments: Optional[List[str]] = None
    social_impact: Optional[str] = None 
    
    # Military Specific
    unit_type: Optional[MilitaryUnit] = None
    equipment_class: Optional[EquipmentClass] = None
    combat_role: Optional[CombatRole] = None
    project_status: Optional[ProjectStatus] = None
    
    # Combat Equipment
    weapon_systems: Optional[List[str]] = None
    armor_systems: Optional[List[str]] = None
    support_systems: Optional[List[str]] = None
    special_equipment: Optional[List[str]] = None
    
    # Unit Details
    unit_size: Optional[int] = None
    success_rate: Optional[float] = None
    casualty_rate: Optional[float] = None
    mission_count: Optional[int] = None
    
    # R&D Information
    research_budget: Optional[int] = None
    development_stage: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    safety_rating: Optional[str] = None
    
    # Command Structure
    commanding_officer: Optional[str] = None
    chain_of_command: Optional[List[str]] = None
    base_location: Optional[str] = None
    deployment_status: Optional[str] = None
    
    # Cultural Elements
    cultural_tradition: Optional[CulturalTradition] = None
    social_structure: Optional[SocialStructure] = None
    cultural_emphasis: Optional[CulturalEmphasis] = None
    urban_style: Optional[UrbanStyle] = None
    
    # City Specifics
    population: Optional[int] = None
    founding_date: Optional[int] = None
    major_industries: Optional[List[str]] = None
    cultural_influences: Optional[List[str]] = None
    
    # Architecture and Planning
    building_styles: Optional[List[str]] = None
    city_zones: Optional[List[str]] = None
    transportation_systems: Optional[List[str]] = None
    environmental_controls: Optional[List[str]] = None
    
    # Social Elements
    major_institutions: Optional[List[str]] = None
    cultural_centers: Optional[List[str]] = None
    education_facilities: Optional[List[str]] = None
    entertainment_districts: Optional[List[str]] = None
    
    # Settlement Details
    population_size: Optional[int] = None
    government_type: Optional[str] = None
    economic_focus: Optional[List[str]] = None
    major_exports: Optional[List[str]] = None
    
    # Political Elements
    governing_body: Optional[str] = None
    diplomatic_status: Optional[str] = None
    military_presence: Optional[str] = None
    trade_agreements: Optional[List[str]] = None
    political_alliances: Optional[List[str]] = None
    
    # Infrastructure
    environmental_systems: Optional[List[str]] = None
    transportation_network: Optional[List[str]] = None
    communication_systems: Optional[List[str]] = None
    defense_capabilities: Optional[List[str]] = None
    
    # Historical Events
    major_incidents: Optional[List[str]] = None
    historical_figures: Optional[List[str]] = None
    significant_dates: Optional[Dict[str, str]] = None
    development_milestones: Optional[List[str]] = None
    crisis_events: Optional[List[str]] = None
    
    # Research Details
    research_field: Optional[ResearchField] = None
    research_status: Optional[ResearchStatus] = None
    security_protocol: Optional[SecurityProtocol] = None
    personnel_role: Optional[PersonnelRole] = None
    
    # Project Information
    project_name: Optional[str] = None
    project_lead: Optional[str] = None
    team_size: Optional[int] = None
    start_date: Optional[str] = None
    completion_date: Optional[str] = None
    
    # Research Metrics
    success_rate: Optional[float] = None
    efficiency_gain: Optional[float] = None
    resource_usage: Optional[Dict[str, float]] = None
    breakthrough_level: Optional[str] = None
    impact_assessment: Optional[str] = None
    
    # Personnel Details
    staff_count: Optional[int] = None
    species_diversity: Optional[List[str]] = None
    department_structure: Optional[Dict[str, List[str]]] = None
    reporting_chain: Optional[List[str]] = None
    security_clearance: Optional[str] = None
    
    # Style guide specific
    writing_style: Optional[WritingStyle] = None
    style_influences: Optional[List[str]] = None
    dialogue_patterns: Optional[List[str]] = None
    narrative_techniques: Optional[List[str]] = None
    pacing_guidelines: Optional[str] = None
    tone_guidelines: Optional[str] = None
    perspective_rules: Optional[str] = None
    
    # Technical writing
    technical_detail_level: Optional[str] = None
    scientific_accuracy: Optional[str] = None
    jargon_guidelines: Optional[str] = None
    explanation_style: Optional[str] = None
    
    # Scene construction
    scene_types: Optional[List[str]] = None
    pov_characters: Optional[List[str]] = None
    location_descriptions: Optional[Dict[str, str]] = None
    atmosphere_guidelines: Optional[str] = None
    tension_elements: Optional[List[str]] = None
    
    # Character interaction
    relationship_dynamics: Optional[Dict[str, Dict[str, str]]] = None
    dialogue_styles: Optional[Dict[str, str]] = None
    conflict_patterns: Optional[List[str]] = None
    team_dynamics: Optional[Dict[str, str]] = None
    
    # Story elements
    plot_threads: Optional[List[str]] = None
    story_beats: Optional[List[str]] = None
    dramatic_elements: Optional[List[str]] = None
    thematic_elements: Optional[List[str]] = None
    
    # World interaction
    tech_understanding: Optional[str] = None
    giant_interaction: Optional[str] = None
    species_relations: Optional[Dict[str, str]] = None
    cultural_background: Optional[Dict[str, str]] = None