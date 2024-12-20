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
            # Get chapter plan if not already loaded
            if not self.current_chapter_plan:
                context = await self.get_chapter_context()
                self.current_chapter_plan = await self.chapter_handler.generate_chapter_plan(
                    self.story_state,
                    context
                )
            
            # Get current scene plan using current_scene counter
            scene_plan = self.current_chapter_plan.scene_plans[self.story_state.current_scene]
            
            # Generate scene content
            scene_content = await self.generate_scene_content(scene_plan)
            
            # Validate scene content before proceeding
            if not scene_content or 'content' not in scene_content:
                logger.error("Invalid scene content generated")
                # Create a default scene structure
                scene_content = {
                    "content": "Scene generation failed - using fallback content",
                    "characters": scene_plan.key_characters,
                    "location": scene_plan.location,
                    "metadata": {
                        "plot_thread": scene_plan.plot_threads[0] if scene_plan.plot_threads else "initial_crisis",
                        "focus": scene_plan.focus,
                        "scene_number": self.story_state.current_scene + 1
                    }
                }
            
            logger.info(f"Generated scene content: {len(scene_content['content'])} characters")
            
            # Index the validated scene
            logger.info("Indexing scene...")
            indexed = await self.rag.index_scene(
                scene=scene_content,
                chapter_number=self.story_state.current_chapter,
                scene_number=self.story_state.current_scene + 1
            )
            
            if not indexed:
                logger.error("Failed to index scene")
            else:
                logger.info("Scene successfully indexed")

            # Increment scene counter for next time
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
            # Get context from recent scenes
            recent_scenes = await self.rag.query_knowledge(
                query=f"Previous scenes in chapter {self.story_state.current_chapter}",
                filters={"type": "generated_scene", "chapter_number": self.story_state.current_chapter},
                namespace=f"chapter_{self.story_state.current_chapter}",
                top_k=3
            )

            # Format previous scene context
            previous_context = "Chapter start"
            if recent_scenes:
                previous_context = "\n".join([
                    f"Scene {scene['metadata']['scene_number']}: {scene['text'][:300]}..."
                    for scene in recent_scenes
                ])

            # Construct narrative prompt
            narrative_prompt = f"""You are Claude, an expert storyteller who studied under Isaac Asimov, writing scene {scene_plan.scene_number} for SLAG: Starfall - Lost Age of Giants, a hard science fiction graphic novel.

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
2. Includes realistic scientific/technical elements
3. Balances dialogue with action
4. Advances the plot toward the expected outcome

Focus on creating an engaging narrative that brings the scene to life. Write in present tense and maintain a cinematic quality suitable for a graphic novel.

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

    async def generate_scene_narrative(self, scene_number: int) -> Dict:
        """Generate narrative for a specific scene using stored chapter plan"""
        try:
            if not self.current_chapter_plan:
                raise ValueError("No chapter plan loaded - must run generate_chapter_outline first")
            
            # Get the scene plan for this time slot
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

            # Generate the narrative
            narrative_prompt = f"""You are Claude, an expert storyteller who studied under Isaac Asimov, writing scene {scene_number} for SLAG: Starfall - Lost Age of Giants, a hard science fiction graphic novel.

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
2. Includes realistic scientific/technical elements
3. Balances dialogue with action
4. Advances the plot toward the expected outcome

Focus on creating an engaging narrative that brings the scene to life. Write in present tense and maintain a cinematic quality suitable for a graphic novel.

Remember: This is scene {scene_number} of 48 in Chapter {self.story_state.current_chapter}."""

            # Generate with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
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

                    # Package scene
                    scene_content = {
                        "content": narrative.strip(),
                        "characters": scene_plan.key_characters,
                        "location": scene_plan.location,
                        "metadata": {
                            "plot_thread": scene_plan.plot_threads[0] if scene_plan.plot_threads else "initial_crisis",
                            "focus": scene_plan.focus,
                            "scene_number": scene_number,
                            "chapter_number": self.story_state.current_chapter,
                            "generated_at": datetime.utcnow().isoformat()
                        }
                    }

                    # Index for future context
                    indexed = await self.rag.index_scene(
                        scene=scene_content,
                        chapter_number=self.story_state.current_chapter,
                        scene_number=scene_number
                    )

                    if indexed:
                        logger.info(f"Successfully generated and indexed scene {scene_number}")
                        return scene_content
                    else:
                        raise ValueError("Failed to index scene")

                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                        await asyncio.sleep(2 ** attempt)
                    else:
                        raise

        except Exception as e:
            logger.error(f"Error generating scene {scene_number}: {str(e)}")
            raise