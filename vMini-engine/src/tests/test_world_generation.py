import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import sys
import time

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
    try:
        async with aiohttp.ClientSession() as session:
            # Wait for service to be ready
            if not await wait_for_service(session):
                print("Error: Service failed to start after maximum retries")
                sys.exit(1)

            # Test world generation
            prompt = "Write a sci-fi story about a group of archaeologists who discover an ancient alien artifact on Mars"
            
            try:
                async with session.post(
                    "http://localhost:8000/generate-world",
                    json={"prompt": prompt},
                    timeout=aiohttp.ClientTimeout(total=300)  # 5 minute timeout
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(json.dumps(result, indent=2))
                    else:
                        error = await response.text()
                        print(f"Error: {error}")
                        sys.exit(1)
            except aiohttp.ClientError as e:
                print(f"Network error: {str(e)}")
                sys.exit(1)

    except Exception as e:
        print(f"Error during test: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_world_generation()) 