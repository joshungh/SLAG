from typing import Dict, Any, List
import json
from datetime import datetime
from src.core.models.story import Story
from src.core.models.story_framework import StoryFramework
from src.core.services.llm_service import LLMService
from src.core.utils.logging_config import setup_logging
from src.config.config import settings
import os
from pathlib import Path

logger = setup_logging("story_generation", "story_generation.log")

class StoryGenerationService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        # Define base paths
        self.base_dir = Path("/app")
        self.output_dir = self.base_dir / "output"
        self.stories_dir = self.output_dir / "stories"
        
        # Ensure directories exist with proper permissions
        for directory in [self.output_dir, self.stories_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            # Ensure directory is writable
            directory.chmod(0o777)

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

        # Modify prompt based on whether this is the first section
        is_first_section = arc_index == 0 and beat_index == 0
        
        # Pre-format the conditional parts to avoid complex f-string
        section_type = "opening section" if is_first_section else "next section"
        story_style = "opening" if is_first_section else "continuation"
        story_goal = "sets up the story" if is_first_section else "maintains flow and consistency with what came before"
        previous_content_section = "" if is_first_section else f"Previous Story Content:\n{previous_content}"
        
        prompt = f"""Write the {section_type} of the story. Do not include any meta-commentary or section headers.
        Write in a clear narrative style, starting directly with the story content.

        Current Arc: {arc.name}
        Current Beat: {beat.name}
        Description: {beat.description}
        Location: {beat.location}
        Characters: {', '.join(beat.characters_involved)}
        
        {previous_content_section}

        Write a vivid, engaging {story_style} that {story_goal}. Start directly with the narrative."""

        response = await self.llm.generate(
            prompt=prompt,
            temperature=settings.STORY_TEMPERATURE,
            max_tokens=settings.SECTION_MAX_TOKENS
        )
        
        # Clean up any meta-text from the response
        response = response.replace("Here's an opening for this story beat:", "")
        response = response.replace("Here's the next section:", "")
        response = response.replace("Here's a continuation of the scene:", "")
        response = response.replace("Here's the next section of the story:", "")
        response = response.split("---")[-1].strip()  # Remove any headers
        
        # Remove excessive newlines
        response = "\n\n".join(line.strip() for line in response.split("\n") if line.strip())
        
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
                bible_id=story_bible.get("title", ""),
                created=datetime.now(),
                file_path=None
            )
            
            file_path = await self._save_story(story)
            story.file_path = Path(file_path)
            
            logger.info(f"Successfully generated complete story of {story.word_count} words")
            return story

        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            raise 

    async def _save_story(self, story: Story) -> str:
        """Save story content as markdown with front matter"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.stories_dir / f"story_{timestamp}.md"
            
            # Debug logging
            logger.debug(f"Base directory: {self.base_dir}")
            logger.debug(f"Output directory: {self.output_dir}")
            logger.debug(f"Stories directory: {self.stories_dir}")
            logger.debug(f"Attempting to save story to: {filename}")
            logger.debug(f"Directory exists: {self.stories_dir.exists()}")
            logger.debug(f"Directory is writable: {os.access(self.stories_dir, os.W_OK)}")
            
            # Write the file
            filename.write_text(f"""---
title: {story.title}
genre: {story.genre}
author: {story.author}
created: {story.created.isoformat()}
word_count: {story.word_count}
framework: {story.framework_id}
bible: {story.bible_id}
---

# {story.title}

{story.content}
""")
            
            logger.info(f"Saved story to: {filename}")
            return str(filename)
            
        except Exception as e:
            logger.error(f"Error saving story: {str(e)}")
            logger.error(f"Current working directory: {os.getcwd()}")
            logger.error(f"Directory contents: {list(self.stories_dir.glob('*'))}")
            raise 