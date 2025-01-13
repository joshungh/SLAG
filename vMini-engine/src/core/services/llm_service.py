from typing import Dict, Any, Optional
import boto3
from botocore.config import Config
import json
from src.config.config import settings
import asyncio
import random
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        config = Config(
            retries=dict(
                max_attempts=5,  # Increase from 4 to 5
                mode='adaptive',  # Use adaptive mode for exponential backoff
            ),
            read_timeout=300,    # 5 minute timeout
            connect_timeout=10    # 10 second connection timeout
        )
        
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=settings.AWS_REGION,
            config=config
        )
        
    async def generate(
        self, 
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
        """Generate text with retries and exponential backoff
        
        Args:
            prompt (str): The input prompt
            max_tokens (int, optional): Maximum tokens to generate. Defaults to 4096.
            temperature (float, optional): Sampling temperature. Defaults to 0.7.
            max_retries (int, optional): Maximum retry attempts. Defaults to 3.
        
        Returns:
            str: Generated text response
        """
        retry_count = 0
        base_delay = 1  # Start with 1 second delay
        
        while retry_count <= max_retries:
            try:
                response = self.client.invoke_model(
                    modelId=settings.BEDROCK_MODEL_ID,
                    body=json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_p": 0.9,
                        "messages": [{"role": "user", "content": prompt}]
                    })
                )
                
                response_body = json.loads(response.get('body').read())
                try:
                    return response_body['content'][0]['text']
                except (KeyError, IndexError) as e:
                    logger.error(f"Failed to parse LLM response: {response_body}")
                    logger.error(f"Parse error: {str(e)}")
                    raise ValueError(f"Unexpected response format from LLM: {str(e)}")
                
            except (
                self.client.exceptions.ThrottlingException,
                self.client.exceptions.ModelTimeoutException,
                self.client.exceptions.InternalServerException
            ) as e:
                retry_count += 1
                if retry_count > max_retries:
                    logger.error(f"Max retries ({max_retries}) exceeded for Bedrock request")
                    raise
                
                delay = (base_delay * 2 ** retry_count) + random.uniform(0, 1)
                logger.warning(f"Bedrock service error, retrying in {delay:.2f} seconds: {str(e)}")
                await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Unexpected error generating from LLM: {str(e)}")
                raise 