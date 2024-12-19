from typing import List, Dict, Optional
from src.models.story_schema import PlotThread, CharacterArc, StoryState
import logging

logger = logging.getLogger(__name__)

class StoryArcManager:
    """Manages long-term story arcs, plot threads, and character development"""
    
    def __init__(self):
        self.major_arcs: List[PlotThread] = []
        self.minor_arcs: List[PlotThread] = []
        self.character_arcs: Dict[str, List[CharacterArc]] = {}
        self.tension_curve: Dict[int, float] = {}  # Maps chapter numbers to tension levels
        self.tension_threshold = 0.2  # Minimum change to be considered significant
        
    async def analyze_tension_curve(self, chapter_number: int) -> Dict:
        """Analyze story tension and recommend adjustments"""
        recent_tension = [self.tension_curve.get(i, 0.5) 
                         for i in range(chapter_number-5, chapter_number)]
        
        return {
            "current_tension": recent_tension[-1] if recent_tension else 0.5,
            "trend": "rising" if len(recent_tension) > 1 and recent_tension[-1] > recent_tension[0] else "falling",
            "needs_climax": any(t > 0.8 for t in recent_tension[-3:]),
            "needs_relief": all(t > 0.7 for t in recent_tension[-3:])
        }
    
    async def suggest_plot_developments(self, story_state: StoryState) -> Dict:
        """Suggest plot developments based on current state"""
        active_plots = len(story_state.active_plot_threads)
        tension_analysis = await self.analyze_tension_curve(story_state.current_chapter)
        
        suggestions = {
            "new_plots_needed": active_plots < 3,
            "resolve_plots": active_plots > 5,
            "introduce_conflict": tension_analysis["trend"] == "falling",
            "provide_resolution": tension_analysis["needs_relief"],
            "build_to_climax": tension_analysis["needs_climax"],
            "recommended_focus": self._determine_focus(story_state, tension_analysis)
        }
        
        return suggestions
    
    def _determine_focus(self, story_state: StoryState, tension: Dict) -> str:
        """Determine recommended focus for next chapter"""
        if tension["needs_relief"]:
            return "character_development"
        elif tension["needs_climax"]:
            return "plot_resolution"
        elif tension["trend"] == "falling":
            return "conflict_introduction"
        else:
            return "world_building" 

    async def analyze_world_state(self, story_state: StoryState) -> Dict:
        """Analyze world state and suggest developments"""
        locations_used = set()
        tech_mentioned = set()
        factions_involved = set()
        
        # Analyze recent chapters
        for summary in story_state.chapter_summaries[-5:]:
            for event in summary.major_developments:
                locations_used.update(self._extract_locations(event))
                tech_mentioned.update(self._extract_technology(event))
                factions_involved.update(self._extract_factions(event))
        
        return {
            "world_coverage": {
                "locations": len(locations_used),
                "technology": len(tech_mentioned),
                "factions": len(factions_involved)
            },
            "needs_expansion": {
                "locations": len(locations_used) < 3,
                "technology": len(tech_mentioned) < 2,
                "factions": len(factions_involved) < 2
            },
            "suggested_focus": self._suggest_world_focus(locations_used, tech_mentioned, factions_involved)
        }

    async def analyze_tension_patterns(self, chapter_number: int) -> Dict:
        """Detailed analysis of tension patterns"""
        # Get last 10 chapters of tension data
        recent_tension = [self.tension_curve.get(i, 0.5) 
                         for i in range(chapter_number-10, chapter_number)]
        
        # Analyze patterns
        patterns = {
            "steady_rise": self._is_steady_rise(recent_tension),
            "plateau": self._is_plateau(recent_tension),
            "oscillating": self._is_oscillating(recent_tension),
            "sharp_changes": self._count_sharp_changes(recent_tension)
        }
        
        # Calculate optimal next tension
        optimal_next = self._calculate_optimal_tension(recent_tension, patterns)
        
        return {
            "patterns": patterns,
            "current_phase": self._determine_story_phase(patterns),
            "optimal_next_tension": optimal_next,
            "suggested_techniques": self._suggest_tension_techniques(optimal_next)
        }

    def _is_steady_rise(self, tension_values: List[float]) -> bool:
        """Check if tension is steadily rising"""
        if len(tension_values) < 2:
            return False
        return all(tension_values[i] < tension_values[i+1] 
                  for i in range(len(tension_values)-1))

    def _is_plateau(self, tension_values: List[float]) -> bool:
        """Check if tension is plateauing"""
        if len(tension_values) < 2:
            return False
        differences = [abs(tension_values[i] - tension_values[i+1])
                      for i in range(len(tension_values)-1)]
        return all(diff < self.tension_threshold for diff in differences)

    def _is_oscillating(self, tension_values: List[float]) -> bool:
        """Check if tension is oscillating"""
        if len(tension_values) < 3:
            return False
        differences = [tension_values[i+1] - tension_values[i]
                      for i in range(len(tension_values)-1)]
        sign_changes = sum(1 for i in range(len(differences)-1)
                         if differences[i] * differences[i+1] < 0)
        return sign_changes >= len(differences) // 2

    def _count_sharp_changes(self, tension_values: List[float]) -> int:
        """Count number of sharp tension changes"""
        if len(tension_values) < 2:
            return 0
        return sum(1 for i in range(len(tension_values)-1)
                  if abs(tension_values[i+1] - tension_values[i]) > self.tension_threshold)