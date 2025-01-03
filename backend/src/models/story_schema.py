from pydantic import BaseModel, ConfigDict, SkipValidation
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class PlotStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    CLIFFHANGER = "cliffhanger"
    PENDING = "pending"

class PlotThread(BaseModel):
    id: str
    title: str
    status: PlotStatus
    priority: int
    related_characters: List[str]
    cliffhanger_scene: Optional[str] = None  # Reference to scene where cliffhanger occurred
    resolution_required_by: Optional[int] = None  # Chapter number by which this should resolve
    
class CharacterArc(BaseModel):
    character_id: str
    current_state: str
    development_goals: List[str]
    relationships: Dict[str, str]
    location: str = "Unknown"
    status: str = "active"
    last_appearance: Optional[int] = None

class Act(BaseModel):
    act_number: int
    act_theme: str
    tension_level: float

class ScenePlan(BaseModel):
    scene_number: int
    act: int
    focus: str
    key_characters: List[str]
    location: str
    time_of_day: str
    objective: str
    expected_outcome: str
    plot_threads: List[str]
    tension_level: float
    pacing: str
    scene_type: str

class WorldDevelopment(BaseModel):
    locations_featured: List[str]
    technology_elements: List[str]
    world_building_points: List[str]

class ChapterOutcomes(BaseModel):
    plot_developments: List[str]
    character_developments: List[str]
    world_changes: List[str]

class ChapterPlan(BaseModel):
    created_at: datetime
    theme: str
    acts: List[Act]
    plot_threads: List[PlotThread]
    character_arcs: List[CharacterArc]
    scene_plans: List[ScenePlan]
    world_development: WorldDevelopment
    expected_outcomes: ChapterOutcomes
    next_chapter_setup: List[str]

class ChapterSummary(BaseModel):
    chapter_number: int
    theme: str
    major_developments: List[str]
    unresolved_plots: List[str]
    cliffhangers: List[Dict[str, str]]  # Maps plot_thread_id to cliffhanger description
    character_developments: Dict[str, str]

class StoryState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    current_chapter: int = 0
    current_scene: int = 0
    active_plot_threads: List[PlotThread] = []
    character_states: Dict[str, CharacterArc] = {}
    world_state: Dict[str, SkipValidation[Any]] = {}
    timeline: List[Dict] = []
    chapter_summaries: List[ChapterSummary] = []
    unresolved_cliffhangers: List[Dict[str, str]] = []

class SceneConfig(BaseModel):
    """Configuration for scene generation"""
    scene_type: str
    scene_number: Optional[int] = None
    characters: List[str]
    location: str
    plot_threads: Optional[List[str]] = None
    tone: Optional[str] = None
    plot_points: Optional[List[str]] = None