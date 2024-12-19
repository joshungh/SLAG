import boto3
import json
import base64
from typing import Dict, List, Optional
from ..config.config import Settings
import asyncio
import logging
from botocore.config import Config

# Set up logging
logger = logging.getLogger(__name__)

class BedrockService:
    def __init__(self, settings: Settings):
        # Configure longer timeouts
        config = Config(
            read_timeout=300,  # 5 minutes
            connect_timeout=300,  # 5 minutes
            retries={'max_attempts': 3}
        )
        
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=settings.AWS_REGION,
            config=config
        )
        self.settings = settings
        
    async def _invoke_claude_with_retry(self, messages: List[Dict[str, str]], max_tokens: int = 4096) -> str:
        """Invoke Claude with exponential backoff retry"""
        max_retries = 5
        base_delay = 1  # Start with 1 second delay
        
        for attempt in range(max_retries):
            try:
                body = json.dumps({
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0,
                    "anthropic_version": "bedrock-2023-05-31"
                })
                
                logger.info(f"Attempt {attempt + 1}: Invoking Claude with {max_tokens} max tokens")
                response = await asyncio.to_thread(
                    self.client.invoke_model,
                    modelId=self.settings.BEDROCK_MODEL_ID,
                    body=body,
                    accept="application/json",
                    contentType="application/json"
                )
                
                response_body = json.loads(response['body'].read())
                return response_body['content'][0]['text']
                
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = (2 ** attempt) * base_delay
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    raise Exception(f"All retry attempts failed: {str(e)}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Titan Embeddings model (v1)
        
        Args:
            text: Text to embed (max 8k tokens)
            
        Returns:
            List[float]: 1536-dimensional embedding vector
        """
        try:
            # Use Titan Embeddings model
            request_body = {
                "inputText": text
            }
            
            logger.info(f"Generating embedding for text of length {len(text)}")
            response = await asyncio.to_thread(
                self.client.invoke_model,
                modelId="amazon.titan-embed-text-v1",
                body=json.dumps(request_body),
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            logger.debug(f"Raw response: {response_body}")
            
            # Titan returns embedding in 'embedding' field
            if 'embedding' not in response_body:
                logger.error(f"Unexpected response format: {response_body}")
                raise ValueError("Response missing 'embedding' field")
                
            embedding = response_body['embedding']
            
            # Verify dimensions and format
            if len(embedding) != 1536:
                raise ValueError(f"Expected 1536 dimensions, got {len(embedding)}")
            
            # Verify all elements are numeric
            for i, x in enumerate(embedding):
                if not isinstance(x, (int, float)):
                    raise ValueError(f"Element {i} is not numeric: {x}")
            
            # Convert all elements to float
            embedding = [float(x) for x in embedding]
            
            # Optional: Normalize the vector if needed
            # magnitude = math.sqrt(sum(x * x for x in embedding))
            # embedding = [x / magnitude for x in embedding]
            
            logger.info("Successfully generated embedding")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise Exception(f"Error generating embedding: {str(e)}")
    
    async def generate_text(self, prompt: str, max_tokens: int = 4096) -> str:
        """Generate text using Claude
        
        Args:
            prompt: Text prompt for Claude
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
        """
        messages = [{"role": "user", "content": prompt}]
        return await self._invoke_claude_with_retry(messages, max_tokens)
    
    async def generate_image(self, prompt: str) -> bytes:
        """Generate image using Stable Diffusion Ultra"""
        body = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 8.0,
            "steps": 50,
            "seed": 0,
            "style_preset": "comic-book",  # Good for graphic novel style
            "samples": 1
        }
        
        response = self.client.invoke_model(
            modelId=self.settings.STABLE_DIFFUSION_MODEL_ID,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        image_data = response_body['artifacts'][0]['base64']
        return base64.b64decode(image_data)
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings