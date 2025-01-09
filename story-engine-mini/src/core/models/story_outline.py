from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Scene:
    id: str
    title: str
    pov_character: str
    setting: str
    time: str
    goal: str
    conflict: str
    outcome: str
    emotional_tone: str
    key_details: List[str]
    characters_present: List[str]
    plot_points: List[str]
    transitions: Dict[str, str]  # previous/next scene hooks

@dataclass
class Chapter:
    number: int
    title: str
    theme: str
    scenes: List[Scene]
    story_arc_point: str  # setup/rising action/climax/etc
    character_arcs: Dict[str, str]  # character -> development in this chapter

@dataclass
class StoryOutline:
    title: str
    hook: str
    central_conflict: str
    themes: List[str]
    chapters: List[Chapter]
    character_arcs: Dict[str, Dict]
    plot_threads: Dict[str, List[Dict]]
    story_beats: List[Dict]
    resolution_points: List[str] 