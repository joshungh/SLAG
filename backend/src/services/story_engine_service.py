from typing import Dict, Optional, List
from datetime import datetime
from src.models.story_schema import StoryState, ChapterPlan, ScenePlan, SceneConfig, CharacterArc, PlotThread, PlotStatus
from src.services.rag_service import RAGService
from src.services.chapter_handler import ChapterHandler
from src.services.story_arc_manager import StoryArcManager
from src.services.continuity_checker import ContinuityChecker
import logging
import json

logger = logging.getLogger(__name__)

class StoryEngineService:
    def __init__(self, rag_service: RAGService):
        self.rag = rag_service
        self.chapter_handler = ChapterHandler(self.rag)
        self.arc_manager = StoryArcManager()
        self.continuity_checker = ContinuityChecker(self.rag)
        self.current_chapter_plan: Optional[ChapterPlan] = None
        self.story_state = StoryState()
        self.context_window = 3

    @classmethod
    async def initialize(cls, rag_service: RAGService) -> 'StoryEngineService':
        """Async factory method to create and initialize StoryEngineService"""
        instance = cls(rag_service)
        # Add any async initialization here if needed
        return instance

    async def get_chapter_context(self) -> Dict:
        """Get context from previous chapters including unresolved plots and cliffhangers"""
        recent_chapters = self.story_state.chapter_summaries[-self.context_window:]
        
        # Collect unresolved elements
        context = {
            "unresolved_plots": [],
            "active_cliffhangers": [],
            "character_arcs": {},
            "recent_developments": []
        }
        
        for chapter in recent_chapters:
            context["unresolved_plots"].extend(chapter.unresolved_plots)
            context["active_cliffhangers"].extend(chapter.cliffhangers)
            context["recent_developments"].extend(chapter.major_developments)
            
            # Update character developments
            for char_id, development in chapter.character_developments.items():
                if char_id not in context["character_arcs"]:
                    context["character_arcs"][char_id] = []
                context["character_arcs"][char_id].append(development)
        
        return context

    async def generate_next_scene(self) -> Dict:
        """Generate the next scene based on chapter plan and story state"""
        try:
            # If no chapter plan or all scenes used, generate new chapter
            if not self.current_chapter_plan:
                # Get context from previous chapters
                chapter_context = await self.get_chapter_context()
                
                # Generate new chapter plan with context
                self.current_chapter_plan = await self.chapter_handler.generate_chapter_plan(
                    story_state=self.story_state,
                    previous_context=chapter_context
                )
                logger.info(f"Generated new chapter plan with {len(self.current_chapter_plan.scene_plans)} scenes")

            # Get next scene plan
            scene_plan = self.current_chapter_plan.scene_plans[self.story_state.current_scene]
            logger.info(f"Generating scene {scene_plan.scene_number}")

            # Generate scene content
            scene_content = await self.generate_scene_content(scene_plan)
            
            # Update story state
            self.story_state.current_scene += 1
            if self.story_state.current_scene >= len(self.current_chapter_plan.scene_plans):
                self.story_state.current_scene = 0
                self.story_state.current_chapter += 1
                self.current_chapter_plan = None

            return scene_content

        except Exception as e:
            logger.error(f"Error generating scene: {str(e)}")
            raise

    async def generate_scene_content(self, scene_plan: ScenePlan) -> Dict:
        """Generate detailed scene content from plan"""
        try:
            # Get plot development suggestions
            plot_suggestions = await self.arc_manager.suggest_plot_developments(self.story_state)
            
            # Create scene generation prompt
            prompt = f"""Generate a scene in JSON format that advances the story according to the plan and suggestions.
            The response must be a valid JSON object with the following structure:
            {{
                "content": "The actual scene text here...",
                "characters": ["Character1", "Character2"],
                "location": "Scene location",
                "metadata": {{
                    "plot_thread": "thread_id",
                    "focus": "plot/character/world",
                    "scene_number": 1
                }}
            }}

            Scene Plan:
            {scene_plan.model_dump_json()}

            Plot Suggestions:
            {plot_suggestions}

            Story Focus: {plot_suggestions['recommended_focus']}

            Requirements:
            1. Maintain continuity with previous scenes
            2. Follow established world rules
            3. Develop characters naturally
            4. {plot_suggestions['recommended_focus'].replace('_', ' ').title()}
            5. Return ONLY a valid JSON object following the structure above
            """

            # Generate scene
            response = await self.rag.get_rag_response(
                query=prompt,
                context_type="story_planning",
                max_tokens=4096
            )
            
            # Parse JSON response
            try:
                scene_content = json.loads(response)
                logger.info("Successfully parsed scene content JSON")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse scene content as JSON: {str(e)}")
                # Create structured content from raw response
                scene_content = {
                    "content": response,
                    "characters": scene_plan.key_characters,
                    "location": scene_plan.location,
                    "metadata": {
                        "plot_thread": scene_plan.plot_threads[0] if scene_plan.plot_threads else None,
                        "focus": scene_plan.focus,
                        "scene_number": scene_plan.scene_number
                    }
                }
                
            # Validate continuity
            issues = await self.continuity_checker.validate_scene(scene_content, self.story_state)
            if issues:
                logger.warning(f"Continuity issues detected: {issues}")
                
            return scene_content
            
        except Exception as e:
            logger.error(f"Error generating scene content: {str(e)}")
            raise

    async def update_story_state(self, scene_content: Dict):
        """Update story state based on scene content"""
        # Implementation details... 

    async def generate_scene(self, scene_config: SceneConfig) -> Dict:
        """Generate a single scene"""
        try:
            # Get chapter plan if not already loaded
            if not self.current_chapter_plan:
                context = await self.get_chapter_context()
                self.current_chapter_plan = await self.chapter_handler.generate_chapter_plan(
                    self.story_state,
                    context
                )

            # Generate scene content
            scene_content = await self.generate_scene_content(scene_config)
            
            # Parse scene content into proper structure
            if isinstance(scene_content, str):
                scene_content = {
                    "content": scene_content,
                    "characters": scene_config.characters,
                    "location": scene_config.location,
                    "metadata": {
                        "plot_thread": scene_config.plot_threads[0] if scene_config.plot_threads else None,
                        "focus": scene_config.scene_type,
                        "scene_number": scene_config.scene_number
                    }
                }

            # Validate scene
            issues = await self.continuity_checker.validate_scene(scene_content, self.story_state)
            if issues:
                logger.warning(f"Scene validation issues: {issues}")

            return scene_content

        except Exception as e:
            logger.error(f"Error generating scene: {str(e)}")
            raise

    async def initialize_story(self, main_characters: List[str], starting_location: str, initial_plot_thread: str) -> bool:
        """Initialize story state with starting conditions"""
        try:
            # Initialize character states
            for character in main_characters:
                char_info = await self.rag.query_knowledge(
                    query=f"Get profile for {character}",
                    filters={"type": "character_profile", "name": character},
                    namespace="characters"
                )
                
                if char_info:
                    self.story_state.character_states[character] = CharacterArc(
                        character_id=character,
                        current_state="Starting position",
                        development_goals=[],
                        relationships={},
                        location=starting_location
                    )

            # Initialize first plot thread
            self.story_state.active_plot_threads.append(
                PlotThread(
                    id=initial_plot_thread,
                    title=initial_plot_thread.replace("_", " ").title(),
                    status=PlotStatus.ACTIVE,
                    priority=1,
                    related_characters=main_characters
                )
            )

            # Set initial chapter
            self.story_state.current_chapter = 1
            self.story_state.current_scene = 0

            logger.info(f"Initialized story with {len(main_characters)} characters at {starting_location}")
            return True

        except Exception as e:
            logger.error(f"Error initializing story: {str(e)}")
            return False