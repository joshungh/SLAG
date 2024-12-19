from datetime import datetime
from typing import Dict, List
import asyncio
import json
import logging

from ..models.context import FullContext
from ..core.context_manager import ContextWindowManager
from ..utils.prompt_templates import PromptTemplates

logger = logging.getLogger(__name__)

class StoryEngine:
    def __init__(self, context_manager: ContextWindowManager):
        self.context_manager = context_manager
        self.current_chapter_number = 0
        self.current_scene_number = 0
    
    async def initialize_story(self, initial_world_state: Dict):
        """Initialize the story with world rules and initial state"""
        try:
            self.context_manager.initialize_story_context(
                world_rules=initial_world_state["world_rules"],
                plot_arcs=initial_world_state["plot_arcs"],
                timeline=initial_world_state["timeline"],
                tech_system=initial_world_state["tech_system"]
            )
            logger.info("Story initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize story: {str(e)}")
            raise
    
    async def generate_next_scene(self) -> Dict:
        """Generate the next scene in the story"""
        try:
            context = self.context_manager.get_full_context()
            
            # Generate scene
            scene_text = await self.bedrock.generate_text(
                prompt=self.prompt_templates.get_scene_generation_prompt(context)
            )
            
            # Generate embedding and store in Pinecone
            embedding = await self.bedrock.generate_embedding(scene_text)
            await self.pinecone.upsert_vectors(
                vectors=[(
                    f"scene_{self.current_chapter_number}_{self.current_scene_number}",
                    embedding,
                    {
                        "type": "scene",
                        "chapter": self.current_chapter_number,
                        "scene": self.current_scene_number,
                        "content": scene_text,
                        "timestamp": datetime.now().isoformat()
                    }
                )],
                namespace="scenes"
            )
            
            self.current_scene_number += 1
            return {"scene": scene_text, "embedding": embedding}
            
        except Exception as e:
            logger.error(f"Scene generation failed: {str(e)}")
            raise 