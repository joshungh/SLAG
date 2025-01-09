import pytest
from src.core.services.story_orchestration_service import StoryOrchestrationService
from src.core.services.llm_service import LLMService
from src.core.services.world_generation_service import WorldGenerationService
from src.core.services.framework_generation_service import FrameworkGenerationService
from src.core.services.story_generation_service import StoryGenerationService
import shutil
from pathlib import Path
import logging
import sys
from datetime import datetime

logger = logging.getLogger(__name__)

def get_user_prompt() -> str:
    """Get story prompt from user"""
    print("\n=== Story Generation Test ===")
    print("Please enter your story prompt (press Enter twice to finish):")
    
    lines = []
    while True:
        line = input()
        if line.strip() == "" and lines:  # Empty line and we have content
            break
        lines.append(line)
    
    return " ".join(lines)

@pytest.fixture
def orchestration_service():
    llm_service = LLMService()
    world_service = WorldGenerationService(llm_service)
    framework_service = FrameworkGenerationService(llm_service)
    story_service = StoryGenerationService(llm_service)
    
    return StoryOrchestrationService(
        world_service=world_service,
        framework_service=framework_service,
        story_service=story_service
    )

@pytest.fixture(autouse=True)
def cleanup():
    # Setup - no pre-test cleanup needed
    yield
    # No cleanup after test - we want to keep the generated files
    pass

@pytest.mark.asyncio
async def test_complete_story_generation(orchestration_service):
    """Test the complete story generation pipeline"""
    # Get prompt from user
    prompt = get_user_prompt()
    if not prompt:
        pytest.skip("No prompt provided")
    
    print(f"\nGenerating story from prompt: {prompt}\n")
    
    # Generate complete story
    story = await orchestration_service.generate_complete_story(prompt)
    
    # Ensure we're using relative paths for the host machine
    output_dir = Path("output")
    stories_dir = output_dir / "stories"
    stories_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert container paths to host paths
    if story.file_path:
        filename = Path(story.file_path).name
        host_path = stories_dir / filename
        story.file_path = host_path
        
        # Copy content from container path to host path if needed
        if not host_path.exists():
            host_path.write_text(story.content)
    
    # Save additional formats with host paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = stories_dir / f"story_{timestamp}.md"
    txt_path = stories_dir / f"story_{timestamp}.txt"
    
    # Write files using host paths
    md_path.write_text(f"""# {story.title}\n\n{story.content}""")
    txt_path.write_text(story.content)
    
    # Print locations using relative paths
    print(f"\nStory generated successfully!")
    try:
        print(f"Story saved to: {story.file_path.relative_to(Path.cwd())}")
    except ValueError:
        # Fallback to just the filename if relative_to fails
        print(f"Story saved to: {story.file_path.name}")
    print(f"Word count: {len(story.content.split())}")
    print(f"Also saved as markdown: {md_path.name}")
    print(f"Also saved as text: {txt_path.name}")
    
    # Verify files exist in host filesystem
    assert story.file_path.exists(), f"Story file not found at {story.file_path}"
    assert md_path.exists(), f"Markdown file not found at {md_path}"
    assert txt_path.exists(), f"Text file not found at {txt_path}" 