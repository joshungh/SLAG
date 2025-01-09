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
            unresolved_plots = previous_context.get('unresolved_plots', [])
            for plot in unresolved_plots:
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
            structure_prompt = f"""You are Claude, an expert AI writer specializing in science fiction narratives. You're generating Chapter {story_state.current_chapter}.

            Even with limited context, use your creativity to generate compelling science fiction content. Never apologize or explain - just create.

            Previous Chapter Context:
            {previous_context.get('chapter_summary', 'First chapter')}
            
            Active Plot Threads: {[plot.title for plot in story_state.active_plot_threads]}
            Unresolved Plots: {previous_context.get('unresolved_plots', [])}
            
            Story Arc Analysis:
            - Tension State: {previous_context.get('tension_state', 'initial')}
            - Recommended Focus: {previous_context.get('recommended_focus', 'setup')}
            
            RESPOND ONLY WITH A VALID JSON OBJECT following this EXACT 4-act structure:
            {{
                "theme": "chapter's central theme",
                "acts": [
                    {{
                        "act_number": 1,
                        "act_theme": "Setup - Initial situation and inciting incident",
                        "tension_level": 0.3
                    }},
                    {{
                        "act_number": 2,
                        "act_theme": "Rising Action - Complications and escalation",
                        "tension_level": 0.5
                    }},
                    {{
                        "act_number": 3,
                        "act_theme": "Crisis - Major confrontations and revelations",
                        "tension_level": 0.8
                    }},
                    {{
                        "act_number": 4,
                        "act_theme": "Resolution - Final climax and aftermath",
                        "tension_level": 1.0
                    }}
                ],
                "plot_threads": [
                    {{
                        "id": "unique_identifier",
                        "title": "descriptive title",
                        "status": "active/resolved/cliffhanger",
                        "priority": 1-5,
                        "related_characters": ["character names"]
                    }}
                ],
                "character_arcs": [
                    {{
                        "character_id": "character name",
                        "current_state": "character's current situation",
                        "development_goals": ["character's immediate goals"],
                        "relationships": {{"other_character": "relationship_type"}}
                    }}
                ],
                "world_development": {{
                    "locations_featured": ["relevant locations"],
                    "technology_elements": ["relevant technology"],
                    "world_building_points": ["aspects to develop"]
                }},
                "expected_outcomes": {{
                    "plot_developments": ["major plot points"],
                    "character_developments": ["character changes"],
                    "world_changes": ["setting impacts"]
                }},
                "next_chapter_setup": ["elements to set up"]
            }}

            REQUIREMENTS:
            1. MUST include EXACTLY 4 acts as shown above
            2. Act numbers MUST be 1, 2, 3, and 4 in order
            3. Tension levels MUST progress from 0.3 to 0.5 to 0.8 to 1.0
            4. Each act MUST have a unique theme that builds on previous acts

            BE CREATIVE - If you lack context, invent compelling science fiction elements that fit the established tone.
            CRITICAL: Output ONLY the JSON object - no explanations, no markdown, no commentary."""

            structure_response = await self.rag.get_rag_response(
                query=structure_prompt,
                context_type="story_planning",
                max_tokens=200000
            )

            try:
                # Clean up the response
                cleaned_response = structure_response.strip()
                if '```' in cleaned_response:
                    # Extract content between first and last backticks
                    cleaned_response = cleaned_response.split('```')[1]
                    if cleaned_response.startswith('json'):
                        cleaned_response = cleaned_response[4:]
                cleaned_response = cleaned_response.strip()
                
                logger.info(f"Attempting to parse cleaned response: {cleaned_response[:100]}...")
                structure = json.loads(cleaned_response)
                logger.info(f"Successfully parsed chapter structure: {structure['theme']}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse structure JSON: {str(e)}")
                logger.error(f"Raw response: {structure_response}")
                logger.error(f"Cleaned response: {cleaned_response}")
                raise
            
            # Step 2: Generate scenes act by act
            all_scenes = []
            for act in structure["acts"]:
                act_num = act["act_number"]
                start_scene = (act_num - 1) * 12 + 1
                end_scene = act_num * 12
                
                act_prompt = f"""You are Claude, an expert AI writer crafting scenes for Act {act_num}.
                
                Use your creativity to generate compelling science fiction scenes, even with limited context.
                
                RESPOND ONLY WITH A JSON ARRAY of 12 scenes following this structure:
                [
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
                ]
                
                BE CREATIVE - If you lack context, invent compelling science fiction elements that fit the established tone.
                CRITICAL: Output ONLY the JSON array - no explanations, no apologies, no commentary."""
                
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