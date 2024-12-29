import pytest
import json
from src.core.services.story_service import StoryService, StoryPhase
from src.core.utils.response_parser import ResponseParser
import os
from src.core.models.phase_constants import StoryPhase
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def story_service():
    return StoryService()

@pytest.fixture
async def story_context(story_service):
    """Create and cleanup a story context"""
    context = None
    try:
        # Generate test story
        story_params = {
            "prompt": "A chef inherits an ancient family recipe book",
            "genre": "magical realism",
            "style": {
                "tone": "warm",
                "pacing": "gentle",
                "voice": "intimate"
            },
            "target_length": 5000
        }
        _, context = await story_service.generate_story(**story_params)
        yield context
    finally:
        # Cleanup after test
        if context:
            try:
                await story_service.cleanup_story(
                    story_id=context['story_id'],
                    namespace=context['namespace']
                )
            except Exception as e:
                logger.error(f"Failed to cleanup test story: {str(e)}")

@pytest.mark.asyncio
async def test_complete_story_generation(story_service, caplog):
    """Test complete story generation process"""
    # Set logging level for detailed output
    caplog.set_level(logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting story generation test")
    
    # Story parameters
    story_params = {
        "prompt": "Thelonius, a rogue commando in a resistance force, fights against an oppressive regime on a peripheral planet in a nearby galaxy",
        "genre": "science fiction",
        "style": {
            "tone": "analytical",
            "pacing": "methodical",
            "voice": "objective",
            "influences": ["Isaac Asimov", "Foundation Series"],
            "themes": [
                "individual vs system",
                "technological determinism",
                "societal evolution"
            ]
        },
        "target_length": 5000
    }
    
    logger.info(f"Story parameters configured: {json.dumps(story_params, indent=2)}")
    
    # Generate story
    logger.info("Beginning story generation process")
    story, context = await story_service.generate_story(**story_params)
    
    # Log story metadata
    logger.info(f"Story ID: {context['story_id']}")
    logger.info(f"Namespace: {context['namespace']}")
    logger.info(f"Output Directory: {context['output_dir']}")
    
    # Validate and log phase completion
    output_dir = context['output_dir']
    required_files = [
        (StoryPhase.WORLD_BUILDING.value, "World-building"),
        (StoryPhase.CHARACTER_DEV.value, "Character Development"),
        (StoryPhase.PLOT_OUTLINE.value, "Plot Outline"),
        (StoryPhase.DETAILED_OUTLINE.value, "Detailed Outline"),
        (StoryPhase.NARRATIVE.value, "Narrative")
    ]
    
    # Check each phase's output
    for phase, phase_name in required_files:
        file_path = f'{output_dir}/{phase}.{StoryPhase.get_file_extension(phase)}'
        
        logger.info(f"\nValidating {phase_name} Phase:")
        assert os.path.exists(file_path), f"Missing {phase} file"
        
        file_size = os.path.getsize(file_path)
        logger.info(f"- File size: {file_size} bytes")
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        if phase == StoryPhase.NARRATIVE.value:
            # Log narrative statistics
            word_count = len(content.split())
            paragraph_count = len(content.split('\n\n'))
            logger.info(f"- Word count: {word_count}")
            logger.info(f"- Paragraph count: {paragraph_count}")
            logger.info(f"- Scene breaks: {content.count('* * *')}")
        else:
            # Parse and validate JSON structure
            try:
                data = json.loads(content)
                logger.info(f"- Valid JSON structure")
                logger.info(f"- Top-level keys: {list(data.keys())}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {phase}: {str(e)}")
                raise
    
    # Verify story bible contents
    logger.info("\nRetrieving story bible")
    bible = await story_service.get_story_bible(
        story_id=context['story_id'],
        namespace=context['namespace']
    )
    
    # Log bible contents summary
    logger.info("Story Bible Contents:")
    for phase in bible:
        content = bible[phase]
        if isinstance(content, str):
            size = len(content)
            preview = content[:100] + "..." if len(content) > 100 else content
            logger.info(f"- {phase}: {size} chars")
            logger.debug(f"  Preview: {preview}")
        else:
            logger.info(f"- {phase}: {list(content.keys())}")
    
    # Validate story structure
    logger.info("\nValidating story structure:")
    assert isinstance(story, str), "Story is not a string"
    assert len(story) >= 2000, f"Story too short: {len(story)} chars"
    assert '[Continued in Part' not in story, "Story is incomplete"
    
    # Log final statistics
    word_count = len(story.split())
    paragraph_count = len(story.split('\n\n'))
    logger.info(f"Final story statistics:")
    logger.info(f"- Total words: {word_count}")
    logger.info(f"- Total paragraphs: {paragraph_count}")
    logger.info(f"- Average paragraph length: {word_count/paragraph_count:.1f} words")
    
    # Log completion
    logger.info("Story generation test completed successfully") 