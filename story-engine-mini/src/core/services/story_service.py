from typing import Dict, List, Optional
from datetime import datetime
import uuid
import os
import json
import logging

from .bedrock_service import BedrockService
from .pinecone_service import PineconeService
from ...config import settings
from ..prompts.templates import PromptTemplates
from ..utils.response_parser import ResponseParser
from ..utils.namespace import create_story_namespace
from ..utils.logging_config import setup_logging
from ..models.phase_constants import StoryPhase

logger = logging.getLogger(__name__)

class StoryService:
    def __init__(self):
        self.bedrock = BedrockService()
        self.pinecone = PineconeService()
        self.templates = PromptTemplates()
        self.parser = ResponseParser()
        
        # Setup logging
        self.logger = setup_logging()
        self.logger.info("Initializing StoryService")
        
        # Ensure output directory exists
        try:
            os.makedirs('output', exist_ok=True)
            self.logger.info("Initialized output directory")
        except OSError as e:
            self.logger.error(f"Failed to create output directory: {str(e)}")
            raise
    
    async def generate_story(self, 
        prompt: str,
        genre: Optional[str] = None,
        style: Optional[Dict] = None,
        target_length: int = 5000
    ) -> tuple[str, Dict]:
        """
        Generate a complete story with all phases
        
        Returns:
            tuple: (final_story, context)
        """
        story_id = str(uuid.uuid4())
        self.logger.info(f"Starting story generation for ID: {story_id}")
        self.logger.debug(f"Parameters: prompt='{prompt}', genre='{genre}'")
        
        try:
            # Create context
            context = self._create_story_context(story_id, prompt, genre, style, target_length)
            self.logger.info(f"Created story context with namespace: {context['namespace']}")
            
            # Phase 1: World Building
            await self._update_phase(context, StoryPhase.WORLD_BUILDING)
            world_context = await self._generate_world_context(context)
            self.logger.debug("World building complete")
            
            # Phase 2: Characters
            await self._update_phase(context, StoryPhase.CHARACTER_DEV)
            characters = await self._develop_characters(context, world_context)
            self.logger.debug("Character development complete")
            
            # Phase 3: Basic Plot
            await self._update_phase(context, StoryPhase.PLOT_OUTLINE)
            plot = await self._create_plot_outline(context, world_context, characters)
            self.logger.debug("Plot outline complete")
            
            # Phase 4: Detailed Outline
            await self._update_phase(context, StoryPhase.DETAILED_OUTLINE)
            detailed_outline = await self._create_detailed_outline(
                context, world_context, characters, plot
            )
            context['outline'] = detailed_outline
            
            # Phase 5: Scene Generation
            await self._update_phase(context, StoryPhase.NARRATIVE)
            story = await self._generate_narrative_from_outline(context)
            
            # Check for completion
            if '[Continued' in story or 'Part' in story:
                self.logger.info("Story incomplete, generating continuation")
                final_story = await self._complete_story(context, story)
            else:
                final_story = story
            
            self.logger.info(f"Story generation complete for {story_id}")
            return final_story, context
            
        except Exception as e:
            self.logger.error(f"Error generating story: {str(e)}", exc_info=True)
            raise
    
    async def _generate_world_context(self, context: Dict) -> str:
        """Generate world-building context"""
        story_id = context['story_id']
        self.logger.debug(f"Generating world context for story {story_id}")
        
        try:
            prompt = self.templates.create_initial_prompt(context)
            self.logger.debug("Created world building prompt")
            
            response = await self.bedrock.generate_text(prompt)
            self.logger.debug("Received world building response")
            
            # Parse and validate
            world_data = self.parser.parse_json_response(response)
            self.logger.debug("Successfully parsed world building data")
            
            # Save and index
            await self._save_phase_output(StoryPhase.WORLD_BUILDING.value, response, context)
            await self._index_phase_result(response, StoryPhase.WORLD_BUILDING, context)
            
            self.logger.info(f"World building complete for story {story_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"World building failed: {str(e)}", exc_info=True)
            raise
    
    async def _develop_characters(self, context: Dict, world_context: str) -> str:
        """Develop story characters"""
        story_id = context['story_id']
        self.logger.debug(f"Developing characters for story {story_id}")
        
        try:
            # Generate character prompt
            prompt = await self._create_character_prompt(context, world_context)
            self.logger.debug("Created character development prompt")
            
            # Generate characters
            response = await self.bedrock.generate_text(
                prompt,
                max_tokens=self.templates.get_max_tokens()
            )
            self.logger.debug("Received character development response")
            
            # Save and validate
            await self._save_phase_output(StoryPhase.CHARACTER_DEV.value, response, context)
            await self._index_phase_result(response, StoryPhase.CHARACTER_DEV, context)
            character_data = self.parser.parse_json_response(response)
            context['characters'] = character_data
            
            self.logger.info(f"Character development complete for story {story_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Character development failed: {str(e)}", exc_info=True)
            raise
    
    async def _create_plot_outline(self, context: Dict, world_context: str, characters: str) -> str:
        """Create plot outline"""
        story_id = context['story_id']
        self.logger.debug(f"Creating plot outline for story {story_id}")
        
        try:
            # Generate plot prompt
            prompt = self.templates.create_plot_prompt(context, world_context, characters)
            self.logger.debug("Created plot outline prompt")
            
            # Generate plot
            response = await self.bedrock.generate_text(
                prompt,
                max_tokens=self.templates.get_max_tokens()
            )
            self.logger.debug("Received plot outline response")
            
            # Save and validate
            await self._save_phase_output(StoryPhase.PLOT_OUTLINE.value, response, context)
            await self._index_phase_result(response, StoryPhase.PLOT_OUTLINE, context)
            plot_data = self.parser.parse_json_response(response)
            context['plot'] = plot_data
            
            self.logger.info(f"Plot outline complete for story {story_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Plot outline failed: {str(e)}", exc_info=True)
            raise
    
    async def _create_narrative_prompt(self, context: Dict, world_context: str, characters: str, plot: str) -> str:
        """Create final narrative prompt"""
        return self.templates.create_narrative_prompt(context, world_context, characters, plot)
    
    async def _generate_narrative(self, context: Dict, world_context: str, characters: str, plot: str) -> str:
        """Generate complete narrative through multiple passes"""
        story_id = context['story_id']
        story_chunks = []
        plot_data = self.parser.parse_json_response(plot)
        max_retries = 3  # Maximum retry attempts per section
        
        try:
            self.logger.debug(f"Starting narrative generation for story {story_id}")
            
            # Track planned sections
            context['progress'] = {
                'planned_sections': [
                    'opening',
                    *[f"scene_{i}" for i, _ in enumerate(plot_data['plot_structure']['rising_action'], 1)],
                    'climax',
                    'resolution'
                ]
            }
            
            # 1. Opening/Setup
            await self._track_story_progress(context, 'opening')
            opening = await self._generate_section_with_retry(
                section_type='opening',
                context=context,
                world_context=world_context,
                characters=characters,
                plot_data=plot_data,
                max_retries=max_retries
            )
            if opening:
                story_chunks.append(opening)
            else:
                raise RuntimeError("Failed to generate valid opening section")

            # 2. Rising Action
            for i, action in enumerate(plot_data['plot_structure']['rising_action'], 1):
                await self._track_story_progress(context, f'scene_{i}')
                scene = await self._generate_section_with_retry(
                    section_type=f'scene_{i}',
                    context=context,
                    world_context=world_context,
                    characters=characters,
                    plot_data=plot_data,
                    scene_info=action,
                    previous_text=story_chunks[-1] if story_chunks else None,
                    max_retries=max_retries
                )
                if scene:
                    story_chunks.append(scene)
                else:
                    self.logger.error(f"Failed to generate valid scene {i}")
                    continue

            # 3. Climax
            await self._track_story_progress(context, 'climax')
            climax = await self._generate_section_with_retry(
                section_type='climax',
                context=context,
                world_context=world_context,
                characters=characters,
                plot_data=plot_data,
                previous_text=story_chunks[-1] if story_chunks else None,
                max_retries=max_retries
            )
            if climax:
                story_chunks.append(climax)

            # 4. Resolution
            await self._track_story_progress(context, 'resolution')
            resolution = await self._generate_section_with_retry(
                section_type='resolution',
                context=context,
                world_context=world_context,
                characters=characters,
                plot_data=plot_data,
                previous_text=story_chunks[-1] if story_chunks else None,
                max_retries=max_retries
            )
            if resolution:
                story_chunks.append(resolution)

            # Combine all chunks into final story
            if not story_chunks:
                raise RuntimeError("No valid story sections generated")
                
            complete_story = self._combine_story_chunks(story_chunks)
            
            # Save final story
            await self._save_phase_output(StoryPhase.NARRATIVE.value, complete_story, context)
            await self._index_phase_result(complete_story, StoryPhase.NARRATIVE, context)
            
            self.logger.info(f"Completed narrative generation for {story_id}")
            return complete_story
            
        except Exception as e:
            self.logger.error(f"Narrative generation failed: {str(e)}", exc_info=True)
            raise

    async def _generate_section_with_retry(self, section_type: str, context: Dict, world_context: str, 
                                         characters: str, plot_data: Dict, previous_text: Optional[str] = None,
                                         scene_info: Optional[Dict] = None, max_retries: int = 3) -> Optional[str]:
        """Generate a story section with retry logic"""
        for attempt in range(max_retries):
            try:
                if section_type == 'opening':
                    prompt = self.templates.create_opening_prompt(
                        context=context,
                        world_context=world_context,
                        characters=characters,
                        plot_hook=plot_data['plot_structure']['hook'],
                        plot_setup=plot_data['plot_structure']['setup']
                    )
                elif section_type.startswith('scene_'):
                    if not scene_info:
                        raise ValueError("scene_info required for scene generation")
                    prompt = self.templates.create_scene_prompt(
                        context=context,
                        previous_text=previous_text,
                        scene_info=scene_info,
                        characters=characters
                    )
                elif section_type == 'climax':
                    prompt = self.templates.create_climax_prompt(
                        context=context,
                        previous_text=previous_text,
                        climax_info=plot_data['plot_structure']['climax'],
                        characters=characters
                    )
                else:  # resolution
                    prompt = self.templates.create_resolution_prompt(
                        context=context,
                        previous_text=previous_text,
                        resolution_info=plot_data['plot_structure']['denouement'],
                        characters=characters
                    )

                section = await self.bedrock.generate_text(prompt)
                if await self._validate_story_section(section, section_type, context):
                    return section
                
                self.logger.warning(f"{section_type} attempt {attempt + 1} failed validation")
                
            except Exception as e:
                self.logger.error(f"Error generating {section_type} (attempt {attempt + 1}): {str(e)}")
                
        return None

    def _combine_story_chunks(self, chunks: List[str]) -> str:
        """Combine story chunks with proper transitions"""
        cleaned_chunks = []
        for chunk in chunks:
            # Clean continuation markers
            cleaned = chunk
            for marker in ['[Continued', '[To be continued', 'Would you like me to continue']:
                cleaned = cleaned.replace(marker, '')
            cleaned_chunks.append(cleaned.strip())

        # Join with scene breaks
        story = '\n\n* * *\n\n'.join(cleaned_chunks)
        
        # Ensure proper ending
        if not story.strip().endswith('THE END'):
            story += '\n\nTHE END'
            
        return story
    
    async def _index_phase_result(self, 
        content: str, 
        phase: StoryPhase,
        context: Dict
    ) -> None:
        """
        Index phase results for story bible building
        
        Args:
            content: Generated content to index
            phase: Current generation phase
            context: Story context including ID, genre, etc.
        """
        embeddings = await self.bedrock.get_embeddings(content)
        
        metadata = {
            'story_id': context['story_id'],
            'namespace': context['namespace'],
            'phase': phase.value,
            'genre': context.get('genre'),
            'timestamp': datetime.utcnow().isoformat(),
            'story_bible': True,
            'target_length': context.get('target_length'),
        }
        
        if phase == StoryPhase.INIT:
            metadata['original_prompt'] = context['original_prompt']
        
        await self.pinecone.upsert_text(
            text=content,
            embeddings=embeddings,
            metadata=metadata,
            namespace=context['namespace']
        ) 
    
    async def _create_character_prompt(self, context: Dict, world_context: str) -> str:
        """Create character development prompt"""
        return self.templates.create_character_prompt(context, world_context) 
    
    async def _save_phase_output(self, phase: str, content: str, context: Dict) -> None:
        """Save phase output to file"""
        if not StoryPhase.validate_phase(phase):
            raise ValueError(f"Invalid phase name: {phase}")
            
        output_dir = context['output_dir']
        story_id = context['story_id']
        extension = StoryPhase.get_file_extension(phase)
        
        try:
            # Ensure output directory exists
            if not os.path.exists(output_dir):
                self.logger.info(f"Creating output directory: {output_dir}")
                os.makedirs(output_dir, exist_ok=True)
            
            output_path = f'{output_dir}/{phase}.{extension}'
            self.logger.debug(f"Saving {phase} output for story {story_id}")
            
            if extension == 'json':
                parsed = self.parser.parse_json_response(content)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(parsed, f, indent=2, ensure_ascii=False)
            else:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            self.logger.info(f"Successfully saved {phase} output to {output_path}")
            
        except Exception as e:
            error_msg = f"Failed to save {phase} output for story {story_id}: {str(e)}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    async def _complete_story(self, context: Dict, partial_story: str) -> str:
        """Complete a partially generated story"""
        story_id = context['story_id']
        self.logger.debug(f"Completing partial story for {story_id}")
        
        try:
            # Create completion prompt
            completion_prompt = self.templates.create_completion_prompt(
                context, 
                partial_story
            )
            self.logger.debug("Created completion prompt")
            
            # Generate completion
            completion = await self.bedrock.generate_text(
                completion_prompt,
                max_tokens=self.templates.get_max_tokens()
            )
            self.logger.debug("Received completion response")
            
            final_story = f"{partial_story}\n\n{completion}"
            self.logger.info(f"Story completion successful for {story_id}")
            
            return final_story
            
        except Exception as e:
            self.logger.error(f"Story completion failed: {str(e)}", exc_info=True)
            raise
    
    async def get_story_bible(self, story_id: str, namespace: str) -> Dict:
        """Retrieve complete story bible"""
        self.logger.debug(f"Retrieving story bible for {story_id}")
        
        try:
            bible = {}
            required_phases = [
                StoryPhase.WORLD_BUILDING,
                StoryPhase.CHARACTER_DEV,
                StoryPhase.PLOT_OUTLINE,
                StoryPhase.NARRATIVE
            ]
            
            for phase in required_phases:
                try:
                    self.logger.debug(f"Querying {phase.value} content")
                    embeddings = await self.bedrock.get_embeddings(phase.value)
                    
                    results = await self.pinecone.query_similar(
                        embeddings=embeddings,
                        filter={
                            'story_id': story_id,
                            'phase': phase.value,
                            'story_bible': True
                        },
                        namespace=namespace,
                        top_k=1
                    )
                    
                    if results:
                        bible[phase.value] = results[0].metadata.get('text', '')
                        self.logger.debug(f"Retrieved {phase.value} content")
                    else:
                        self.logger.warning(f"No content found for phase {phase.value}")
                        
                except Exception as e:
                    self.logger.error(f"Error retrieving {phase.value}: {str(e)}")
                    raise RuntimeError(f"Failed to retrieve {phase.value} content: {str(e)}")
            
            # Verify all required phases are present
            missing_phases = [phase.value for phase in required_phases if phase.value not in bible]
            if missing_phases:
                raise RuntimeError(f"Missing required phases: {missing_phases}")
            
            self.logger.info(f"Successfully retrieved story bible for {story_id}")
            return bible
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve story bible: {str(e)}", exc_info=True)
            raise
    
    async def cleanup_story(self, story_id: str, namespace: str) -> None:
        """Clean up story data"""
        self.logger.debug(f"Cleaning up story {story_id}")
        
        try:
            await self.pinecone.delete_namespace(namespace)
            self.logger.info(f"Successfully cleaned up story {story_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup story {story_id}: {str(e)}", exc_info=True)
            raise 
    
    def _create_story_context(self, 
        story_id: str, 
        prompt: str, 
        genre: Optional[str], 
        style: Optional[Dict], 
        target_length: int
    ) -> Dict:
        """
        Create initial story context
        
        Args:
            story_id: Unique story identifier
            prompt: Original story prompt
            genre: Story genre
            style: Style parameters
            target_length: Target story length
            
        Returns:
            Dict containing story context
        """
        timestamp = datetime.utcnow().isoformat()
        output_dir = f'output/latest_story'
        namespace = create_story_namespace(story_id, genre)
        
        # Create base context
        context = {
            'story_id': story_id,
            'namespace': namespace,
            'original_prompt': prompt,
            'genre': genre,
            'style': style or {},
            'target_length': target_length,
            'timestamp': timestamp,
            'current_phase': StoryPhase.INIT.value,
            'output_dir': output_dir
        }
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        self.logger.debug(f"Created story context: {json.dumps(context, indent=2)}")
        
        return context 
    
    async def _update_phase(self, context: Dict, phase: StoryPhase) -> None:
        """Update context with current phase"""
        context['current_phase'] = phase.value
        self.logger.debug(f"Updated phase to: {phase.value}") 
    
    def _is_story_complete(self, story: str, target_length: int) -> bool:
        """Check if story is complete"""
        # Check length
        if len(story) < target_length * 0.8:  # Allow 20% shorter than target
            return False
            
        # Check for continuation markers
        incomplete_markers = [
            '[Continued',
            'Part',
            'To be continued',
            'Would you like me to continue'
        ]
        if any(marker in story for marker in incomplete_markers):
            return False
            
        # Check for proper ending (has resolution)
        ending_markers = [
            'THE END',
            'resolved',
            'finally'
        ]
        last_paragraphs = story.split('\n')[-3:]  # Check last 3 paragraphs
        if not any(marker.lower() in ' '.join(last_paragraphs).lower() 
                  for marker in ending_markers):
            return False
            
        return True 
    
    def _force_story_completion(self, story: str) -> str:
        """Force completion of an overlong story"""
        paragraphs = story.split('\n\n')
        
        # Keep introduction
        result = paragraphs[:3]
        
        # Skip to near the end
        result.extend(paragraphs[-5:])
        
        # Add proper ending if missing
        if not story.strip().endswith('THE END'):
            result.append('\nTHE END')
            
        return '\n\n'.join(result) 
    
    async def _validate_story_section(self, section: str, section_type: str, context: Dict) -> bool:
        """Validate a story section"""
        try:
            # Basic validation
            if not section or len(section.strip()) < 100:
                self.logger.warning(f"Section {section_type} too short")
                return False

            # Check for character presence
            character_names = self._get_character_names(context)
            if not any(name in section for name in character_names):
                self.logger.warning(f"No main characters found in {section_type}")
                return False

            # Check section-specific requirements
            if section_type == "opening":
                if not any(marker in section.lower() for marker in ["began", "started", "opened", "introduced"]):
                    self.logger.warning("Opening lacks clear beginning")
                    return False
            elif section_type == "climax":
                if not any(marker in section.lower() for marker in ["finally", "moment", "realized", "confronted"]):
                    self.logger.warning("Climax lacks clear peak moment")
                    return False
            elif section_type == "resolution":
                if not any(marker in section.lower() for marker in ["ended", "resolved", "concluded", "finished"]):
                    self.logger.warning("Resolution lacks clear ending")
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Validation error for {section_type}: {str(e)}")
            return False

    def _get_character_names(self, context: Dict) -> List[str]:
        """Extract character names from context"""
        try:
            characters = context.get('characters', {}).get('characters', [])
            return [char['name'] for char in characters]
        except Exception:
            return []

    async def _track_story_progress(self, context: Dict, current_section: str) -> None:
        """Track story generation progress"""
        progress = context.setdefault('progress', {})
        progress.update({
            'current_section': current_section,
            'sections_completed': progress.get('sections_completed', []) + [current_section],
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Log progress
        completed = len(progress['sections_completed'])
        total = len(progress.get('planned_sections', [])) or 1
        percent = (completed / total) * 100
        
        self.logger.info(f"Story Progress: {percent:.1f}% ({completed}/{total} sections)")
        self.logger.debug(f"Completed sections: {progress['sections_completed']}") 

    async def _create_detailed_outline(self, context: Dict, world_context: str, characters: str, plot: str) -> str:
        """Create detailed story outline"""
        story_id = context['story_id']
        self.logger.debug(f"Creating detailed outline for story {story_id}")
        
        try:
            # Generate detailed outline prompt
            prompt = self.templates.create_detailed_outline_prompt(
                context, world_context, characters, plot
            )
            self.logger.debug("Created detailed outline prompt")
            
            # Generate detailed outline
            response = await self.bedrock.generate_text(
                prompt,
                max_tokens=self.templates.get_max_tokens()
            )
            self.logger.debug("Received detailed outline response")
            
            # Save and validate
            await self._save_phase_output(StoryPhase.DETAILED_OUTLINE.value, response, context)
            await self._index_phase_result(response, StoryPhase.DETAILED_OUTLINE, context)
            outline_data = self.parser.parse_json_response(response)
            context['outline'] = outline_data
            
            self.logger.info(f"Detailed outline complete for story {story_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Detailed outline failed: {str(e)}", exc_info=True)
            raise

    async def _generate_narrative_from_outline(self, context: Dict) -> str:
        """Generate narrative following detailed outline"""
        try:
            # Parse outline if it's a string
            if isinstance(context['outline'], str):
                outline = self.parser.parse_json_response(context['outline'])
            else:
                outline = context['outline']

            story_chunks = []
            
            for chapter in outline['chapters']:
                for scene in chapter['scenes']:
                    scene_content = await self._generate_scene_from_outline(
                        context=context,
                        chapter=chapter,
                        scene=scene,
                        previous_text=story_chunks[-1] if story_chunks else None
                    )
                    if scene_content:
                        story_chunks.append(scene_content)
            
            # Combine chunks into final narrative
            complete_story = self._combine_story_chunks(story_chunks)
            
            # Save and index the narrative
            await self._save_phase_output(StoryPhase.NARRATIVE.value, complete_story, context)
            await self._index_phase_result(complete_story, StoryPhase.NARRATIVE, context)
            
            return complete_story
            
        except Exception as e:
            self.logger.error(f"Error generating narrative from outline: {str(e)}")
            raise

    async def _generate_scene_from_outline(self, context: Dict, chapter: Dict, 
                                         scene: Dict, previous_text: Optional[str] = None) -> Optional[str]:
        """Generate a scene from the outline"""
        try:
            # Create scene prompt
            prompt = f"""Write the following scene for our science fiction story. 
            Follow the analytical, methodical style of Isaac Asimov, focusing on logical progression and societal implications.

            Previous Text (ending):
            {previous_text[-500:] if previous_text else 'Story beginning...'}

            Scene Details:
            Title: {scene['title']}
            POV Character: {scene['pov_character']}
            Setting: {scene['setting']}
            Time: {scene['time']}
            Goal: {scene['goal']}
            Conflict: {scene['conflict']}
            
            Key Details to Include:
            {json.dumps(scene['key_details'], indent=2)}
            
            Plot Points to Cover:
            {json.dumps(scene['plot_points'], indent=2)}
            
            Characters Present:
            {json.dumps(scene['characters_present'], indent=2)}
            
            Emotional Tone: {scene['emotional_tone']}
            
            Chapter Context:
            Chapter {chapter['number']}: {chapter['title']}
            Theme: {chapter['theme']}
            Story Arc Point: {chapter['story_arc_point']}

            Write this scene maintaining the established style and ensuring continuity with previous content.
            Focus on logical progression and clear cause-and-effect relationships."""

            scene_content = await self.bedrock.generate_text(prompt)
            return scene_content

        except Exception as e:
            self.logger.error(f"Error generating scene: {str(e)}")
            return None 