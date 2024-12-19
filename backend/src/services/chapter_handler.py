from typing import List, Dict, Optional
from datetime import datetime
from src.models.story_schema import ChapterPlan, ScenePlan, StoryState, PlotThread, CharacterArc
from src.services.rag_service import RAGService
import logging
import json
import re

logger = logging.getLogger(__name__)

class ChapterHandler:
    def __init__(self, rag_service: RAGService):
        self.rag = rag_service

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
            # Create planning prompt
            prompt = f"""You are a story planning assistant. Your task is to generate a chapter plan in JSON format.
            Return ONLY valid JSON - no explanations or other text.
            
            Current Story State:
            - Active Plot Threads: {[plot.title for plot in story_state.active_plot_threads]}
            - Unresolved Plots: {previous_context['unresolved_plots']}
            - Recent Developments: {previous_context.get('recent_developments', [])}
            
            Generate a chapter plan following this exact JSON structure:
            {{
                "theme": "chapter theme",
                "plot_threads": [
                    {{
                        "id": "thread_id",
                        "title": "thread title",
                        "status": "active",
                        "priority": 1,
                        "related_characters": ["character names"]
                    }}
                ],
                "character_arcs": [
                    {{
                        "character_id": "name",
                        "current_state": "description",
                        "development_goals": ["goal1", "goal2"],
                        "relationships": {{"other_char": "relationship_type"}}
                    }}
                ],
                "scene_plans": [
                    {{
                        "scene_number": 1,
                        "focus": "plot",
                        "key_characters": ["names"],
                        "location": "place",
                        "objective": "scene goal",
                        "expected_outcome": "result",
                        "plot_threads": ["thread_ids"]
                    }}
                ],
                "expected_outcomes": ["outcome1", "outcome2"]
            }}

            Requirements:
            1. Return ONLY the JSON object - no other text
            2. All fields must match the schema exactly
            3. Use 3-5 scenes per chapter
            4. All IDs must match existing story elements
            5. Status must be one of: "active", "resolved", "cliffhanger"
            """

            # Get response from Claude
            response = await self.rag.get_rag_response(
                query=prompt,
                context_type="story_planning",
                max_tokens=4096
            )

            # Try to extract JSON if there's surrounding text
            try:
                # First try direct JSON parsing
                plan_data = json.loads(response)
            except json.JSONDecodeError:
                # Look for JSON-like structure
                json_match = re.search(r'({[\s\S]*})', response)
                if json_match:
                    try:
                        plan_data = json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        logger.error("Failed to parse JSON from response")
                        logger.error(f"Response: {response}")
                        raise
                else:
                    logger.error("No JSON structure found in response")
                    logger.error(f"Response: {response}")
                    raise ValueError("Invalid response format")

            # Create ChapterPlan
            return ChapterPlan(
                created_at=datetime.utcnow(),
                theme=plan_data["theme"],
                plot_threads=[PlotThread(**thread) for thread in plan_data["plot_threads"]],
                character_arcs=[CharacterArc(**arc) for arc in plan_data["character_arcs"]],
                scene_plans=[ScenePlan(**scene) for scene in plan_data["scene_plans"]],
                expected_outcomes=plan_data["expected_outcomes"]
            )

        except Exception as e:
            logger.error(f"Error in _generate_plan: {str(e)}")
            logger.error(f"Response received: {response}")
            raise