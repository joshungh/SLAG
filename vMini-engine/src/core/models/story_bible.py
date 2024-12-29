from typing import List, Dict, Optional
from pydantic import BaseModel, field_validator
import json

class Universe(BaseModel):
    setting: str
    era: str

class Character(BaseModel):
    name: str
    role: str
    description: str
    traits: List[str] = []
    background: Optional[str] = None

class Location(BaseModel):
    name: str
    description: str
    significance: Optional[str] = None

class Faction(BaseModel):
    name: str
    description: str = "No description provided"
    goals: List[str] = []
    relationships: Dict[str, str] = {}

    @field_validator('relationships')
    @classmethod
    def validate_relationships(cls, v):
        return v or {}

class Technology(BaseModel):
    name: str
    description: str
    impact: Optional[str] = None

class StoryBible(BaseModel):
    title: str
    genre: str
    universe: Universe
    characters: List[Character]
    locations: List[Location]
    factions: List[Faction]
    technology: List[Technology]
    timeline: Dict[str, str] = {}
    themes: List[str] = []
    notes: List[str] = []

    @field_validator('factions')
    @classmethod
    def validate_factions(cls, v):
        validated_factions = []
        for i, faction in enumerate(v):
            if isinstance(faction, dict):
                faction_dict = {
                    "name": faction.get("name", f"Unnamed Faction {i}"),
                    "description": faction.get("description", "No description provided"),
                    "goals": faction.get("goals", []),
                    "relationships": faction.get("relationships", {})
                }
                validated_factions.append(Faction(**faction_dict))
            else:
                validated_factions.append(faction)
        return validated_factions

    @field_validator('characters', 'locations', 'technology')
    @classmethod
    def ensure_lists(cls, v):
        """Ensure lists are initialized even if empty"""
        return v or []

    def debug_json(self) -> str:
        """Return a formatted JSON string with all fields for debugging"""
        return json.dumps(self.model_dump(), indent=2) 