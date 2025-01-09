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
    unresolved_plots: List[PlotThread]
    character_developments: Dict[str, CharacterArc]
    cliffhangers: List[str] = []  # Add default empty list
    
    class Config:
        arbitrary_types_allowed = True

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

    def update_for_new_chapter(self, chapter_number: int, previous_context: Dict, arc_analysis: Dict):
        """Update story state for a new chapter"""
        self.current_chapter = chapter_number
        self.current_scene = 0

        # For first chapter, initialize with default state
        if chapter_number == 1:
            return  # Keep initial state from story initialization

        # For subsequent chapters...
        # Update plot threads based on arc analysis
        if arc_analysis.get("plot_suggestions", {}).get("new_plots_needed"):
            # Keep existing active plots
            self.active_plot_threads = [
                plot for plot in self.active_plot_threads 
                if plot.status == PlotStatus.ACTIVE
            ]

        # Update character states based on previous chapter
        for char_id, char_arc in previous_context.get("character_arcs", {}).items():
            if char_id in self.character_states:
                self.character_states[char_id].current_state = char_arc.get("current_state", "active")
                self.character_states[char_id].development_goals = char_arc.get("development_goals", [])

        # Update world state
        self.world_state.update(arc_analysis.get("world_state", {}))

        # Add previous chapter summary if exists
        if previous_context.get("chapter_summary"):
            self.chapter_summaries.append(previous_context["chapter_summary"])

class SceneConfig(BaseModel):
    """Configuration for scene generation"""
    scene_type: str
    scene_number: Optional[int] = None
    characters: List[str]
    location: str
    plot_threads: Optional[List[str]] = None
    tone: Optional[str] = None
    plot_points: Optional[List[str]] = None