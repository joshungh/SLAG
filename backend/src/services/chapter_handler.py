from typing import List, Dict, Optional
from datetime import datetime
from src.models.story_schema import ChapterPlan, ScenePlan, StoryState, PlotThread, CharacterArc
from src.services.rag_service import RAGService
from src.services.story_arc_manager import StoryArcManager
import logging
import json
import re

logger = logging.getLogger(__name__)

class ChapterHandler:
    def __init__(self, rag_service: RAGService):
        self.rag = rag_service
        self.arc_manager = StoryArcManager()

    async def generate_chapter_plan(self, story_state: StoryState, previous_context: Dict) -> ChapterPlan:
        """Generate a plan for the next chapter including scene outlines"""
        try:
            logger.info(f"\n{'='*20} Generating Chapter {story_state.current_chapter} Plan {'='*20}")
            logger.info(f"Active Plot Threads:")
            for plot in story_state.active_plot_threads:
                logger.info(f"- {plot.title} (Priority: {plot.priority}, Status: {plot.status})")
            
            logger.info(f"\nUnresolved Plots from Previous Chapters:")
            for plot in previous_context['unresolved_plots']:
                logger.info(f"- {plot}")
            
            # Generate chapter plan...
            plan = await self._generate_plan(story_state, previous_context)
            
            logger.info(f"\nChapter Plan Generated:")
            logger.info(f"Theme: {plan.theme}")
            logger.info("\nPlot Threads:")
            for thread in plan.plot_threads:
                logger.info(f"- {thread.title} ({thread.status})")
            
            logger.info("\nCharacter Arcs:")
            for arc in plan.character_arcs:
                logger.info(f"- {arc.character_id}: {arc.current_state}")
                logger.info(f"  Goals: {', '.join(arc.development_goals)}")
            
            logger.info("\nScene Plans:")
            for scene in plan.scene_plans:
                logger.info(f"\nScene {scene.scene_number}:")
                logger.info(f"Location: {scene.location}")
                logger.info(f"Focus: {scene.focus}")
                logger.info(f"Characters: {', '.join(scene.key_characters)}")
                logger.info(f"Objective: {scene.objective}")
                logger.info(f"Expected Outcome: {scene.expected_outcome}")
            
            logger.info(f"\nExpected Chapter Outcomes:")
            for outcome in plan.expected_outcomes:
                logger.info(f"- {outcome}")
            
            return plan
            
        except Exception as e:
            logger.error(f"Error generating chapter plan: {str(e)}")
            raise 

    async def _generate_plan(self, story_state: StoryState, previous_context: Dict) -> ChapterPlan:
        """Internal method to generate chapter plan using RAG"""
        try:
            # Step 1: Generate chapter structure without scenes
            structure_prompt = f"""You are generating a detailed chapter structure for a science fiction graphic novel.
            Return ONLY valid JSON following this exact structure - no wrapper objects, no chapter_1 key.

            The chapter MUST have exactly 4 acts with these themes:
            1. Act 1 (Setup): Initial situation and inciting incident
            2. Act 2 (Rising Action): Complications and escalation
            3. Act 3 (Crisis): Major confrontations and revelations
            4. Act 4 (Resolution): Final climax and aftermath

            Return JSON structure:
            {{
                "theme": "chapter theme",
                "acts": [
                    {{
                        "act_number": 1,
                        "act_theme": "Setup - initial situation",
                        "tension_level": 0.3
                    }},
                    {{
                        "act_number": 2,
                        "act_theme": "Rising Action - complications",
                        "tension_level": 0.5
                    }},
                    {{
                        "act_number": 3,
                        "act_theme": "Crisis - confrontations",
                        "tension_level": 0.8
                    }},
                    {{
                        "act_number": 4,
                        "act_theme": "Resolution - climax",
                        "tension_level": 1.0
                    }}
                ],
                "plot_threads": [
                    {{
                        "id": "thread_id",
                        "title": "thread title",
                        "status": "active/resolved/cliffhanger",
                        "priority": 1-5,
                        "related_characters": ["names"]
                    }}
                ],
                "character_arcs": [
                    {{
                        "character_id": "name",
                        "current_state": "description",
                        "development_goals": ["goals"],
                        "relationships": {{"other_char": "relationship_type"}}
                    }}
                ],
                "world_development": {{
                    "locations_featured": ["places"],
                    "technology_elements": ["tech"],
                    "world_building_points": ["developments"]
                }},
                "expected_outcomes": {{
                    "plot_developments": ["developments"],
                    "character_developments": ["developments"],
                    "world_changes": ["changes"]
                }},
                "next_chapter_setup": ["setups"]
            }}

            Requirements:
            1. MUST include exactly 4 acts as shown above
            2. Each act must have a distinct theme and purpose
            3. Tension should progress logically (0.3 → 0.5 → 0.8 → 1.0)
            4. Acts must be numbered 1 through 4 sequentially

            Current Story State:
            - Chapter: {story_state.current_chapter}
            - Active Plot Threads: {[plot.title for plot in story_state.active_plot_threads]}
            - Unresolved Plots: {previous_context['unresolved_plots']}
            """
            
            structure_response = await self.rag.get_rag_response(
                query=structure_prompt,
                context_type="story_planning",
                max_tokens=200000  # Increased token limit
            )
            
            try:
                structure = json.loads(structure_response)
                # If response is nested under chapter_1, extract it
                if "chapter_1" in structure:
                    structure = structure["chapter_1"]
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse structure JSON: {str(e)}")
                logger.error(f"Raw response: {structure_response}")
                raise
            
            # Step 2: Generate scenes act by act
            all_scenes = []
            for act in structure["acts"]:
                act_num = act["act_number"]
                start_scene = (act_num - 1) * 12 + 1
                end_scene = act_num * 12
                
                act_prompt = f"""Generate exactly 12 scenes for Act {act_num}.
                Return ONLY a JSON array of scenes - no wrapper objects, no extra text.
                
                Act Theme: {act['act_theme']}
                Target Tension: {act['tension_level']}
                Previous scenes: {all_scenes[-2:] if all_scenes else 'Chapter start'}
                
                Each scene must follow this structure:
                {{
                    "scene_number": {start_scene}-{end_scene},
                    "act": {act_num},
                    "focus": "plot/character/world",
                    "key_characters": ["names"],
                    "location": "place",
                    "time_of_day": "morning/afternoon/evening/night",
                    "objective": "scene goal",
                    "expected_outcome": "result",
                    "plot_threads": ["thread_ids"],
                    "tension_level": 0.1-1.0,
                    "pacing": "slow/medium/fast",
                    "scene_type": "action/dialogue/investigation/revelation"
                }}
                
                Requirements:
                1. Exactly 12 scenes
                2. Scene numbers must be sequential
                3. Time must progress logically
                4. Build tension towards act climax
                5. Mix different scene types
                6. Maintain character consistency
                """
                
                act_response = await self.rag.get_rag_response(
                    query=act_prompt,
                    context_type="story_planning",
                    max_tokens=200000  # Increased token limit
                )
                
                try:
                    act_scenes = json.loads(act_response)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse act scenes JSON: {str(e)}")
                    logger.error(f"Raw response: {act_response}")
                    raise
                
                # Validate act scenes
                assert len(act_scenes) == 12, f"Act {act_num} must have exactly 12 scenes"
                
                # Use self.arc_manager instead of story_engine.arc_manager
                scene_tensions = [scene["tension_level"] for scene in act_scenes]
                tension_analysis = await self.arc_manager.analyze_tension_patterns(
                    chapter_number=story_state.current_chapter,
                    tensions=scene_tensions
                )
                
                if not tension_analysis["patterns"]["steady_rise"]:
                    logger.warning(f"Act {act_num} tension progression may need adjustment")
                
                all_scenes.extend(act_scenes)
            
            # Step 3: Combine everything into final plan
            plan_data = {
                **structure,
                "scene_plans": all_scenes
            }
            
            # Final validation
            assert len(plan_data["acts"]) == 4, "Chapter must have exactly 4 acts"
            assert len(plan_data["scene_plans"]) == 48, "Chapter must have exactly 48 scenes"
            
            # Create and return ChapterPlan
            return ChapterPlan(
                created_at=datetime.utcnow(),
                theme=plan_data["theme"],
                acts=plan_data["acts"],
                plot_threads=[PlotThread(**thread) for thread in plan_data["plot_threads"]],
                character_arcs=[CharacterArc(**arc) for arc in plan_data["character_arcs"]],
                scene_plans=[ScenePlan(**scene) for scene in plan_data["scene_plans"]],
                world_development=plan_data["world_development"],
                expected_outcomes=plan_data["expected_outcomes"],
                next_chapter_setup=plan_data["next_chapter_setup"]
            )

        except Exception as e:
            logger.error(f"Error in _generate_plan: {str(e)}")
            # Store all responses for debugging
            error_context = {
                "structure_response": structure_response if 'structure_response' in locals() else None,
                "act_response": act_response if 'act_response' in locals() else None,
                "structure": structure if 'structure' in locals() else None,
                "act_scenes": act_scenes if 'act_scenes' in locals() else None
            }
            logger.error(f"Context at error: {error_context}")
            raise