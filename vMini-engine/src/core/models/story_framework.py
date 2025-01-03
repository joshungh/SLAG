from typing import List, Dict, Optional
from pydantic import BaseModel

class StoryBeat(BaseModel):
    name: str
    description: str
    purpose: str
    characters_involved: List[str]
    location: str
    conflict_type: str
    resolution_type: Optional[str]

class StoryArc(BaseModel):
    name: str
    description: str
    beats: List[StoryBeat]
    themes: List[str]
    character_arcs: Dict[str, str]

class StoryFramework(BaseModel):
    title: str
    genre: str
    main_conflict: str
    central_theme: str
    arcs: List[StoryArc]
    subplot_connections: Dict[str, List[str]]
    pacing_notes: List[str] 