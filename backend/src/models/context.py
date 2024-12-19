from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class StoryContext:
    world_rules: Dict[str, str]
    major_plot_arcs: List[str]
    timeline: List[Dict[str, str]]
    tech_system: Dict[str, str]

@dataclass
class ChapterContext:
    date: datetime
    active_plots: List[str]
    location: Dict[str, str]
    recent_events: List[Dict[str, str]]

@dataclass
class SceneContext:
    previous_scenes: List[Dict[str, str]]
    active_characters: List[str]
    current_situation: str
    local_environment: Dict[str, str]

@dataclass
class FullContext:
    story: StoryContext
    chapter: ChapterContext
    scene: SceneContext 