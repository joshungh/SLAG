from typing import List, Dict, Optional
from src.models.story_schema import PlotThread, CharacterArc, StoryState
import logging

logger = logging.getLogger(__name__)

class StoryArcManager:
    """Manages long-term story arcs, plot threads, and character development"""
    
    def __init__(self, story_state: Optional[StoryState] = None):
        self.major_arcs: List[PlotThread] = []
        self.minor_arcs: List[PlotThread] = []
        self.character_arcs: Dict[str, List[CharacterArc]] = {}
        self.tension_curve: Dict[int, float] = {}  # Maps chapter numbers to tension levels
        self.tension_threshold = 0.2  # Minimum change to be considered significant
        self.story_state = story_state
        
    def update_story_state(self, story_state: StoryState):
        """Update the story state reference"""
        self.story_state = story_state

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
            "recommended_focus": self._determine_focus(tension_analysis)
        }
        
        return suggestions
    
    def _determine_focus(self, tension_analysis: Dict) -> str:
        """Determine narrative focus based on tension analysis"""
        current_tension = tension_analysis.get("current_tension", 0.5)
        trend = tension_analysis.get("trend", "stable")
        needs_climax = tension_analysis.get("needs_climax", False)
        needs_relief = tension_analysis.get("needs_relief", False)
        
        if needs_climax:
            return "climax"
        elif needs_relief:
            return "relief"
        elif trend == "rising":
            return "escalation"
        elif trend == "falling":
            return "development"
        else:
            return "setup"

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

    async def analyze_tension_patterns(self, chapter_number: int, tensions: List[float] = None) -> Dict:
        """Analyze story tension and recommend adjustments"""
        if tensions:
            # Analyze provided tension values
            return {
                "patterns": {
                    "steady_rise": all(tensions[i] <= tensions[i+1] for i in range(len(tensions)-1)),
                    "plateau": all(abs(tensions[i] - tensions[i+1]) < self.tension_threshold 
                                 for i in range(len(tensions)-1)),
                    "oscillating": self._is_oscillating(tensions)
                },
                "current_tension": tensions[-1] if tensions else 0.5,
                "trend": "rising" if len(tensions) > 1 and tensions[-1] > tensions[0] else "falling",
                "needs_climax": any(t > 0.8 for t in tensions[-3:]) if len(tensions) >= 3 else False,
                "needs_relief": all(t > 0.7 for t in tensions[-3:]) if len(tensions) >= 3 else False
            }
        else:
            # Use historical tension curve
            recent_tension = [self.tension_curve.get(i, 0.5) 
                             for i in range(chapter_number-5, chapter_number)]
            
            return {
                "patterns": {
                    "steady_rise": all(recent_tension[i] <= recent_tension[i+1] 
                                     for i in range(len(recent_tension)-1)),
                    "plateau": False,
                    "oscillating": False
                },
                "current_tension": recent_tension[-1] if recent_tension else 0.5,
                "trend": "rising" if len(recent_tension) > 1 and recent_tension[-1] > recent_tension[0] else "falling",
                "needs_climax": any(t > 0.8 for t in recent_tension[-3:]),
                "needs_relief": all(t > 0.7 for t in recent_tension[-3:])
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

    async def get_chapter_transition_analysis(self, current_chapter: int) -> Dict:
        """Analyze previous chapter and suggest next developments"""
        if not self.story_state:
            return {
                "tension_state": await self.analyze_tension_patterns(current_chapter),
                "recommended_focus": "setup",
                "plot_suggestions": {},
                "world_state": {}
            }
            
        tension_analysis = await self.analyze_tension_patterns(current_chapter)
        
        return {
            "tension_state": tension_analysis,
            "recommended_focus": self._determine_focus(tension_analysis),
            "plot_suggestions": await self.suggest_plot_developments(self.story_state),
            "world_state": await self.analyze_world_state(self.story_state)
        }

    async def synthesize_chapter_context(self, previous_chapter: int) -> Dict:
        """Get key context from previous chapter"""
        return {
            "major_developments": self._extract_major_developments(previous_chapter),
            "unresolved_plots": self._get_unresolved_plots(),
            "character_arcs": self._get_active_character_arcs(),
            "tension_curve": self.tension_curve.get(previous_chapter, {})
        }

    def _suggest_world_focus(self, locations: set, tech: set, factions: set) -> str:
        """Suggest which world-building aspect needs most attention"""
        focus_scores = {
            "locations": len(locations),
            "technology": len(tech),
            "factions": len(factions)
        }
        
        # Find area with least development
        min_area = min(focus_scores.items(), key=lambda x: x[1])
        
        if min_area[1] < 2:  # If area has less than 2 elements
            return f"{min_area[0]}_development"
        
        # If all areas well developed, suggest integration
        if all(score >= 3 for score in focus_scores.values()):
            return "world_integration"
        
        return "balanced_development"

    def _extract_locations(self, event: str) -> set:
        """Extract location mentions from text"""
        # Simple implementation - could be enhanced with NLP
        locations = {"Station Omega", "Research Lab", "Command Center", "Habitat Ring"}
        return {loc for loc in locations if loc.lower() in event.lower()}

    def _extract_technology(self, event: str) -> set:
        """Extract technology mentions from text"""
        tech = {"Fragment", "quantum", "containment field", "AI Core"}
        return {t for t in tech if t.lower() in event.lower()}

    def _extract_factions(self, event: str) -> set:
        """Extract faction mentions from text"""
        factions = {"Command", "Research Team", "Security", "Engineering"}
        return {f for f in factions if f.lower() in event.lower()}