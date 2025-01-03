from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class PlotPoint(BaseModel):
    description: str
    characters_involved: List[str]
    location: Optional[str] = None
    significance: str
    setup_elements: List[str] = Field(default_factory=list)
    payoff_elements: List[str] = Field(default_factory=list)

class StorySection(BaseModel):
    events: List[PlotPoint]
    conflicts: List[Dict[str, str]]
    character_developments: List[Dict[str, str]]
    themes: List[str] = Field(default_factory=list)

class CharacterArc(BaseModel):
    character: str
    arc_points: List[Dict[str, str]]
    development: List[str]
    relationships: Dict[str, List[str]] = Field(default_factory=dict)

class Subplot(BaseModel):
    description: str
    arc: List[PlotPoint]
    related_characters: List[str]
    resolution: str

class StoryArc(BaseModel):
    title: str
    main_plot: Dict[str, StorySection]  # beginning, middle, end
    character_arcs: List[CharacterArc]
    subplots: List[Subplot]
    themes: List[str]
    tone: str
    target_length: int = Field(default=10000)

class StoryPart(BaseModel):
    part_number: int
    scenes: List[Dict[str, str]]
    character_moments: List[Dict[str, str]]
    plot_points: List[str]
    callbacks: List[str] = Field(default_factory=list)
    setup_elements: List[str] = Field(default_factory=list)
    target_length: int
    estimated_word_count: int = 0

class StoryFramework(BaseModel):
    story_arc: StoryArc
    parts: List[StoryPart]
    metadata: Dict[str, Any] = Field(default_factory=dict) 