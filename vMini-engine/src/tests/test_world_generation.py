import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import sys
import time
import pytest
from typing import Dict, Any
from src.core.services.world_generation_service import WorldGenerationService
from src.core.services.llm_service import LLMService

load_dotenv()

async def wait_for_service(session, max_retries=30, delay=1):
    """Wait for the API service to be ready"""
    for i in range(max_retries):
        try:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    print("Service is ready!")
                    return True
        except aiohttp.ClientConnectorError:
            print(f"Waiting for service... ({i+1}/{max_retries})")
            await asyncio.sleep(delay)
    return False

async def test_world_generation():
    """Test the complete world generation process"""
    try:
        timeout = aiohttp.ClientTimeout(total=600)  # 10 minute timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            if not await wait_for_service(session):
                pytest.fail("Service failed to start")

            prompt = "Write a sci-fi story about a group of archaeologists who discover an ancient alien artifact on Mars"
            
            async with session.post(
                "http://localhost:8000/generate-world",
                json={"prompt": prompt}
            ) as response:
                if response.status != 200:
                    error_body = await response.text()
                    pytest.fail(f"API request failed with status {response.status}. Error: {error_body}")
                result = await response.json()
                
                # Validate response structure
                assert isinstance(result, dict), "Response should be a dictionary"
                assert "title" in result, "Response should contain a title"
                assert "characters" in result, "Response should contain characters"
                assert "timeline" in result, "Response should contain a timeline"
                
                print(json.dumps(result, indent=2))
                return result

    except asyncio.TimeoutError:
        pytest.fail("Request timed out")
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_timeline_handling():
    """Test specific timeline generation and validation"""
    try:
        timeout = aiohttp.ClientTimeout(total=600)  # 10 minute timeout
        async with aiohttp.ClientSession(timeout=timeout) as session:
            if not await wait_for_service(session):
                pytest.fail("Service failed to start")

            prompt = "Write a story about Mars colonization with a detailed timeline of events"
            
            async with session.post(
                "http://localhost:8000/generate-world",
                json={"prompt": prompt}
            ) as response:
                assert response.status == 200, f"API request failed with status {response.status}"
                result = await response.json()
                
                # Validate timeline structure
                assert "timeline" in result, "Response should contain timeline"
                assert "pre_2145_mars_exploration" in result["timeline"], "Timeline should contain pre-2145 events"
                assert isinstance(result["timeline"]["pre_2145_mars_exploration"], list), "Timeline events should be a list"
                
                # Check timeline event structure
                for event in result["timeline"]["pre_2145_mars_exploration"]:
                    assert "year" in event, "Each event should have a year"
                    assert "event" in event, "Each event should have an event description"

    except asyncio.TimeoutError:
        pytest.fail("Request timed out")
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_bible_expansion():
    """Test the bible expansion process"""
    try:
        service = WorldGenerationService(LLMService())
        
        # Create initial bible
        bible = await service.initialize_bible(
            "Write a story about Mars colonization with a detailed timeline of events"
        )
        
        # Test expansion
        expansion_area = "Detail the Mars colony's infrastructure and life support systems"
        expanded_bible = await service.expand_bible(bible, expansion_area)
        
        # Validate expansion
        assert expanded_bible is not None
        assert len(expanded_bible.technology) > len(bible.technology)
        # Add more specific assertions based on what should be expanded
        
    except Exception as e:
        pytest.fail(f"Bible expansion test failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 