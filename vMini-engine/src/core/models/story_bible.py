from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Extra
from src.core.utils.logging_config import setup_logging

# Initialize logger
logger = setup_logging("story_bible", "story_bible.log")

# Make base models extensible
class ExtensibleModel(BaseModel):
    model_config = {
        'extra': 'allow',
        'arbitrary_types_allowed': True
    }

    def model_dump(self, **kwargs):
        """Custom dump method to ensure proper serialization"""
        data = super().model_dump(**kwargs)
        # Convert any nested models to dicts
        for key, value in data.items():
            if isinstance(value, list):
                data[key] = [
                    item.model_dump() if isinstance(item, BaseModel) else item 
                    for item in value
                ]
        return data

class Universe(ExtensibleModel):
    setting: str
    era: str
    environment: Optional[Dict[str, Any]] = None
    infrastructure: Optional[Dict[str, Any]] = None

class Character(ExtensibleModel):
    name: str
    role: str
    description: str
    traits: Optional[List[str]] = None
    background: Optional[str] = None
    relationships: Optional[Dict[str, Union[str, Dict[str, str]]]] = None  # Allow both string and dict relationships
    arc: Optional[Dict[str, Any]] = None

class Location(ExtensibleModel):
    name: str
    description: str
    significance: Optional[str] = None
    features: Optional[List[str]] = None
    hazards: Optional[List[str]] = None
    infrastructure: Optional[Dict[str, Any]] = None

class Faction(ExtensibleModel):
    name: str
    description: str
    goals: Optional[List[str]] = None
    relationships: Optional[Dict[str, str]] = None
    resources: Optional[Dict[str, Any]] = None
    territory: Optional[List[str]] = None

class Technology(ExtensibleModel):
    name: str
    description: str
    limitations: Optional[List[str]] = None
    requirements: Optional[Dict[str, Any]] = None
    risks: Optional[List[str]] = None
    development_stage: Optional[str] = None

class TimelineEvent(ExtensibleModel):
    year: str
    event: str
    details: Optional[str] = None
    impact: Optional[List[str]] = None
    key_figures: Optional[List[str]] = None

class SocialStructure(ExtensibleModel):
    governance: Dict[str, Any]
    economy: Dict[str, Any]
    culture: Dict[str, Any]
    education: Optional[Dict[str, Any]] = None
    healthcare: Optional[Dict[str, Any]] = None

class StoryBible(ExtensibleModel):
    title: str
    genre: str
    universe: Universe
    characters: List[Character]
    locations: List[Location]
    factions: List[Faction]
    technology: List[Technology]
    timeline: Dict[str, List[TimelineEvent]]
    themes: List[str]
    notes: List[str]
    social_structure: Optional[SocialStructure] = None
    infrastructure: Optional[Dict[str, Any]] = None
    environmental_systems: Optional[Dict[str, Any]] = None
    resource_management: Optional[Dict[str, Any]] = None
    transportation_network: Optional[Dict[str, Any]] = None
    
    def add_expansion(self, expansion_data: Dict[str, Any]) -> None:
        """Add expansion data to the story bible, creating new fields as needed"""
        try:
            for key, value in expansion_data.items():
                if not value:  # Skip empty values
                    continue
                    
                if hasattr(self, key):
                    current_value = getattr(self, key)
                    if isinstance(current_value, list):
                        # Handle lists of model objects
                        if key in ["technology", "characters", "locations", "factions"]:
                            model_class = {
                                "technology": Technology,
                                "characters": Character,
                                "locations": Location,
                                "factions": Faction
                            }[key]
                            
                            # Convert dict items to model objects
                            new_items = []
                            for item in value:
                                if isinstance(item, dict):
                                    try:
                                        # Ensure required fields
                                        if "name" not in item:
                                            logger.warning(f"Skipping {key} item without name")
                                            continue
                                            
                                        model_instance = model_class(**item)
                                        new_items.append(model_instance)
                                    except Exception as e:
                                        logger.error(f"Error creating {model_class.__name__}: {str(e)}")
                                        continue
                                elif isinstance(item, model_class):
                                    new_items.append(item)
                            
                            # Only add items with unique names
                            existing_names = {t.name for t in current_value}
                            for item in new_items:
                                if item.name not in existing_names:
                                    current_value.append(item)
                                    
                        else:
                            # Handle other list types (like notes)
                            if isinstance(value, list):
                                current_value.extend(value)
                                
                    elif isinstance(current_value, dict) and isinstance(value, dict):
                        # Deep merge dictionaries
                        current_value.update(value)
                    else:
                        # Replace value if not None
                        if value is not None:
                            setattr(self, key, value)
                else:
                    # Add new field
                    setattr(self, key, value)
        except Exception as e:
            logger.error(f"Error in add_expansion: {str(e)}")
            raise 