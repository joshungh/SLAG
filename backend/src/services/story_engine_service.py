from typing import Dict, Optional, List
from datetime import datetime
from src.models.story_schema import StoryState, ChapterPlan, ScenePlan, SceneConfig, CharacterArc, PlotThread, PlotStatus
from src.services.rag_service import RAGService
from src.services.chapter_handler import ChapterHandler
from src.services.story_arc_manager import StoryArcManager
from src.services.continuity_checker import ContinuityChecker
import logging
import json
import asyncio

logger = logging.getLogger(__name__)

class StoryEngineService:
    @classmethod
    async def initialize(cls, rag_service: RAGService):
        """Initialize the story engine with all required components"""
        instance = cls(rag_service)
        instance.arc_manager = StoryArcManager()
        instance.continuity_checker = ContinuityChecker(rag_service)
        instance.chapter_handler = ChapterHandler(rag_service)
        return instance

    def __init__(self, rag_service: RAGService):
        self.rag = rag_service
        self.story_state = None
        self.current_chapter_plan = None
        # These will be initialized in the initialize class method
        self.arc_manager = None
        self.continuity_checker = None
        self.chapter_handler = None
        self.current_chapter_plan: Optional[ChapterPlan] = None
        self.story_state = StoryState()
        self.context_window = 3
        self.environmental_state = {
            "time_of_day": "morning",
            "active_alerts": set(),
            "compromised_sections": set(),
            "fragment_effects": {},
            "character_locations": {}
        }

    async def get_chapter_context(self) -> Dict:
        """Get rich context from previous chapters including unresolved plots and key developments"""
        if self.story_state.current_chapter <= 1:
            return {}
        
        previous_chapter = self.story_state.current_chapter - 1
        
        # Get key scenes from previous chapter
        final_scenes = await self.rag.query_knowledge(
            query="Key developments and climactic moments",
            filters={"type": "generated_scene", "chapter_number": previous_chapter},
            namespace=f"chapter_{previous_chapter}",
            top_k=5  # Get last few scenes for context
        )
        
        # Get unresolved plot threads
        unresolved_plots = [
            plot for plot in self.story_state.active_plot_threads 
            if plot.status != PlotStatus.RESOLVED
        ]
        
        return {
            "recent_developments": [scene['content'] for scene in final_scenes],
            "unresolved_plots": unresolved_plots,
            "character_states": self.story_state.character_states,
            "world_state": self.story_state.world_state
        }

    async def generate_next_scene(self) -> Dict:
        """Generate the next scene based on chapter plan and story state"""
        try:
            # Check if we need to transition chapters
            if (self.current_chapter_plan and 
                self.story_state.current_scene >= len(self.current_chapter_plan.scene_plans)):
                logger.info("Reached end of chapter, initiating transition...")
                success = await self.transition_to_next_chapter()
                if not success:
                    raise ValueError("Failed to transition to next chapter")
            
            # Get chapter plan if not already loaded
            if not self.current_chapter_plan:
                logger.info(f"Generating plan for Chapter {self.story_state.current_chapter}")
                context = await self.get_chapter_context()
                self.current_chapter_plan = await self.chapter_handler.generate_chapter_plan(
                    self.story_state,
                    context
                )
            
            # Generate and index scene
            scene_content = await self.generate_scene_content(self.story_state.current_scene + 1)
            
            # Increment scene counter
            self.story_state.current_scene += 1
            
            return scene_content

        except Exception as e:
            logger.error(f"Error generating scene: {str(e)}")
            raise

    async def generate_scene_content(self, scene_number: int) -> Dict:
        """Generate narrative for a specific scene using stored chapter plan"""
        try:
            if not self.current_chapter_plan:
                raise ValueError("No chapter plan loaded - must run generate_chapter_outline first")
            
            scene_plan = self.current_chapter_plan.scene_plans[scene_number - 1]
            
            # Get context from recent scenes
            recent_scenes = await self.rag.query_knowledge(
                query=f"Previous scenes in chapter {self.story_state.current_chapter}",
                filters={"type": "generated_scene", "chapter_number": self.story_state.current_chapter},
                namespace=f"chapter_{self.story_state.current_chapter}",
                top_k=3
            )
            
            # Format context
            previous_context = "Chapter start"
            if recent_scenes:
                previous_context = "\n".join([
                    f"Scene {scene['metadata']['scene_number']}: {scene['text'][:300]}..."
                    for scene in recent_scenes
                ])

            # Construct narrative prompt
            narrative_prompt = f"""You are Claude, an expert storyteller and novelist. Your style, tone, pacing, and narrative structure resemble Asimov and Haldeman. You are writing a scifi novel, scene by scene, and are currently on scene {scene_plan.scene_number} for SLAG: Starfall - Lost Age of Giants. You are the creator of this story, and will progress the development of the plots, characters, and world as you see fit.

Previous Scene Context:
{previous_context}

Scene Parameters:
- Location: {scene_plan.location}
- Characters: {', '.join(scene_plan.key_characters)}
- Time: {scene_plan.time_of_day}
- Objective: {scene_plan.objective}
- Expected Outcome: {scene_plan.expected_outcome}
- Scene Type: {scene_plan.scene_type}
- Tension Level: {scene_plan.tension_level}
- Pacing: {scene_plan.pacing}

Write a vivid, visual scene that:
1. Shows rather than tells through detailed description
2. Balance technical elements with human drama
3. Balances dialogue with action
4. Advances the plot toward the expected outcome, but feel free to be creative and deviate from the plan if it makes sense
5. Focus on natural narrative flow without artificial scene markers; don't mention the scene number or chapter number, or acknowledge the reader; only mention Location or Time when relevant
6. You are creating a story scene by scene, chapter by chapter. Treat each chapter holistically, seamlessly tieing together the scenes so that each chapter is a cohesive story.
7. Make it fun, make it technical, make it nerdy and edgy. Create a captivating story that your heros Isaac Asimov and John Haldeman would be proud of.
8. Reference previous scene's emotional impact and maintain character relationship continuity
9. Ground all technology in realistic physics while balancing technical detail with drama
10. Build tension gradually through careful pacing and atmosphere

Focus on creating an engaging narrative that brings the scene to life. Write in present tense and maintain a cinematic quality suitable for a 1960s science fiction novel.

Remember: This is scene {scene_plan.scene_number} of 48 in Chapter {self.story_state.current_chapter}."""

            # Generate scene content with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Get narrative from Claude
                    narrative = await self.rag.get_rag_response(
                        query=narrative_prompt,
                        context_type="story_planning",
                        max_tokens=4096
                    )

                    if not narrative or len(narrative.strip()) < 100:
                        if attempt < max_retries - 1:
                            logger.warning(f"Generated narrative too short on attempt {attempt + 1}, retrying...")
                            continue
                        else:
                            raise ValueError("Failed to generate valid narrative content")

                    # Package scene content
                    scene_content = {
                        "content": narrative.strip(),
                        "characters": scene_plan.key_characters,
                        "location": scene_plan.location,
                        "metadata": {
                            "plot_thread": scene_plan.plot_threads[0] if scene_plan.plot_threads else "initial_crisis",
                            "focus": scene_plan.focus,
                            "scene_number": scene_plan.scene_number,
                            "chapter_number": self.story_state.current_chapter,
                            "generated_at": datetime.utcnow().isoformat()
                        }
                    }

                    # Log success
                    logger.info(f"Generated scene {scene_plan.scene_number} ({len(narrative)} chars)")

                    # Index the scene
                    indexed = await self.rag.index_scene(
                        scene=scene_content,
                        chapter_number=self.story_state.current_chapter,
                        scene_number=scene_plan.scene_number
                    )

                    if not indexed:
                        logger.warning(f"Failed to index scene {scene_plan.scene_number}")
                    else:
                        logger.info(f"Successfully indexed scene {scene_plan.scene_number}")

                    return scene_content

                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise

        except Exception as e:
            logger.error(f"Error in scene generation: {str(e)}")
            logger.error(f"Scene plan: {scene_plan}")
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

            # Index the scene for future context
            try:
                await self.rag.index_scene(
                    scene=scene_content,
                    chapter_number=self.story_state.current_chapter,
                    scene_number=scene_config.scene_number
                )
                logger.info(f"Successfully indexed scene {scene_config.scene_number} for future context")
            except Exception as e:
                logger.error(f"Failed to index scene: {str(e)}")

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

    async def generate_chapter_outline(self) -> ChapterPlan:
        """Generate detailed outline for all 48 scenes in the next chapter"""
        try:
            context = await self.get_chapter_context()
            chapter_plan = await self.chapter_handler.generate_chapter_plan(
                self.story_state, 
                context
            )
            
            # Store the plan for use throughout the day
            self.current_chapter_plan = chapter_plan
            
            # Log the outline for monitoring
            logger.info(f"Generated chapter {self.story_state.current_chapter} outline:")
            for scene in chapter_plan.scene_plans:
                logger.info(f"Scene {scene.scene_number}: {scene.objective}")
            
            return chapter_plan
            
        except Exception as e:
            logger.error(f"Error generating chapter outline: {str(e)}")
            raise

    async def update_environmental_state(self, scene_content: Dict):
        """Track environmental changes through scenes"""
        # Update time
        # Track damage
        # Monitor Fragment spread
        # Log character movements

    async def transition_to_next_chapter(self) -> bool:
        """Handle transition between chapters"""
        try:
            previous_chapter = self.story_state.current_chapter
            logger.info(f"Transitioning from Chapter {previous_chapter} to {previous_chapter + 1}")
            
            # Get final state of previous chapter
            final_scenes = await self.rag.query_knowledge(
                query="Key developments and climactic moments from chapter ending",
                filters={"type": "generated_scene", "chapter_number": previous_chapter},
                namespace=f"chapter_{previous_chapter}",
                top_k=5
            )
            
            logger.info("Analyzing final chapter state...")
            # Update plot threads based on final scenes
            for plot in self.story_state.active_plot_threads:
                # Check if plot was resolved in final scenes
                if any(plot.id in scene['content'] and "resolved" in scene['content'].lower() 
                      for scene in final_scenes):
                    plot.status = PlotStatus.RESOLVED
                # Check for cliffhangers
                elif any(plot.id in scene['content'] and "cliffhanger" in scene['content'].lower() 
                        for scene in final_scenes):
                    plot.status = PlotStatus.CLIFFHANGER
            
            # Clean up resolved plots
            self.story_state.active_plot_threads = [
                plot for plot in self.story_state.active_plot_threads 
                if plot.status != PlotStatus.RESOLVED
            ]
            
            # Update state for next chapter
            self.story_state.current_chapter += 1
            self.story_state.current_scene = 0
            self.current_chapter_plan = None
            
            logger.info(f"Successfully transitioned to Chapter {self.story_state.current_chapter}")
            logger.info(f"Active plots remaining: {len(self.story_state.active_plot_threads)}")
            return True
            
        except Exception as e:
            logger.error(f"Error during chapter transition: {str(e)}")
            return False