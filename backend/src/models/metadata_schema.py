from enum import Enum
from typing import Optional, List
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

class DocumentMetadata(BaseModel):
    """Metadata schema for all documents"""
    # Basic info
    type: str
    category: str
    source: str
    
    # Character-specific
    species: Optional[Species] = None
    role: Optional[List[Role]] = None
    affiliation: Optional[Affiliation] = None
    expertise: Optional[List[Expertise]] = None
    
    # Location-specific
    location_type: Optional[LocationType] = None
    jurisdiction: Optional[Affiliation] = None
    security_level: Optional[SecurityLevel] = None
    
    # Content-specific
    time_period: Optional[TimePeriod] = None
    narrative_type: Optional[List[NarrativeType]] = None
    plot_relevance: Optional[str] = None
    crisis_related: Optional[bool] = None
    
    # Technical
    tech_category: Optional[TechCategory] = None
    classification: Optional[SecurityLevel] = None
    development_status: Optional[str] = None 