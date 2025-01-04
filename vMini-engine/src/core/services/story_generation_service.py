from typing import Dict, Any, List
import json
from datetime import datetime
from src.core.models.story import Story
from src.core.models.story_framework import StoryFramework
from src.core.services.llm_service import LLMService
from src.core.utils.logging_config import setup_logging
from src.config.config import settings
import os

logger = setup_logging("story_generation", "story_generation.log")

class StoryGenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def _generate_section(
        self,
        story_bible: Dict[str, Any],
        framework: StoryFramework,
        arc_index: int,
        beat_index: int,
        previous_content: str = "",
    ) -> str:
        """Generate a single story section based on framework beat"""
        arc = framework.arcs[arc_index]
        beat = arc.beats[beat_index]

        prompt = f"""Continue the story, focusing on this next beat:

        Current Arc: {arc.name}
        Current Beat: {beat.name}
        Description: {beat.description}
        Location: {beat.location}
        Characters: {', '.join(beat.characters_involved)}
        
        Previous Story Content:
        {previous_content}

        Write the next section of the story, maintaining flow and consistency with what came before."""

        response = await self.llm.generate(
            prompt=prompt,
            temperature=settings.STORY_TEMPERATURE,
            max_tokens=settings.SECTION_MAX_TOKENS
        )
        
        logger.info(f"Generated section for {beat.name} ({len(response.split())} words)")
        return response

    async def generate_story(
        self,
        story_bible: Dict[str, Any],
        framework: StoryFramework
    ) -> Story:
        """Generate complete story through sequential section generation"""
        try:
            logger.info(f"Generating story: {framework.title}")
            
            full_content = []
            
            # Generate each section based on framework beats
            for arc_idx, arc in enumerate(framework.arcs):
                for beat_idx, beat in enumerate(arc.beats):
                    section = await self._generate_section(
                        story_bible=story_bible,
                        framework=framework,
                        arc_index=arc_idx,
                        beat_index=beat_idx,
                        previous_content="\n\n".join(full_content) if full_content else ""
                    )
                    full_content.append(section)
                    
                    logger.info(f"Generated section for {arc.name} - {beat.name}")

            # Combine all sections
            complete_story = "\n\n".join(full_content)
            
            # Create and save story
            story = Story(
                title=framework.title,
                genre=framework.genre,
                content=complete_story,
                word_count=len(complete_story.split()),
                framework_id=framework.title,
                bible_id=story_bible.get("title", "")
            )
            
            await self._save_story(story)
            
            logger.info(f"Successfully generated complete story of {story.word_count} words")
            return story

        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            raise 

    async def _save_story(self, story: Story) -> str:
        """Save story content as markdown with front matter"""
        try:
            os.makedirs("output/stories", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output/stories/story_{timestamp}.md"
            
            with open(filename, "w") as f:
                # Add title and metadata as markdown front matter
                f.write(f"""---
title: {story.title}
genre: {story.genre}
author: {story.author}
created: {story.created_at.isoformat()}
word_count: {story.word_count}
framework: {story.framework_id}
bible: {story.bible_id}
---

# {story.title}

{story.content}
""")
                
            logger.info(f"Saved story to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving story: {str(e)}")
            raise 