from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from models.context import StoryContext, ChapterContext, SceneContext, FullContext

class ContextWindowManager:
    def __init__(self):
        self.story_context: Optional[StoryContext] = None
        self.chapter_context: Optional[ChapterContext] = None
        self.scene_contexts: List[Dict] = []
        self.max_scene_memory = 3  # Keep last 3 scenes in immediate context
        
    def initialize_story_context(self, world_rules: Dict, plot_arcs: List, 
                               timeline: List, tech_system: Dict):
        """Initialize the core story context"""
        self.story_context = StoryContext(
            world_rules=world_rules,
            major_plot_arcs=plot_arcs,
            timeline=timeline,
            tech_system=tech_system
        )
    
    def start_new_chapter(self):
        """Initialize a new chapter context with today's date + 2400 years"""
        future_date = datetime.now() + timedelta(days=365*2400)
        self.chapter_context = ChapterContext(
            date=future_date,
            active_plots=[],
            location={},
            recent_events=[]
        )
        self.scene_contexts = []  # Reset scene memory for new chapter
        
    def add_scene_context(self, scene_data: Dict):
        """Add a new scene to the context window"""
        if len(self.scene_contexts) >= self.max_scene_memory:
            self.scene_contexts.pop(0)  # Remove oldest scene
        self.scene_contexts.append(scene_data)
    
    def get_full_context(self) -> FullContext:
        """Get the complete context for scene generation"""
        current_scene_context = SceneContext(
            previous_scenes=self.scene_contexts,
            active_characters=self._get_active_characters(),
            current_situation=self._get_current_situation(),
            local_environment=self._get_local_environment()
        )
        
        return FullContext(
            story=self.story_context,
            chapter=self.chapter_context,
            scene=current_scene_context
        )
    
    def _get_active_characters(self) -> List[str]:
        """Extract active characters from recent scenes"""
        # Implementation to analyze recent scenes and return active characters
        pass
    
    def _get_current_situation(self) -> str:
        """Summarize current story situation"""
        # Implementation to analyze context and return current situation
        pass
    
    def _get_local_environment(self) -> Dict[str, str]:
        """Get current environmental context"""
        # Implementation to return current environment details
        pass 