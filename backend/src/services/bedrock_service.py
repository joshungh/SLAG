import boto3
import json
import base64
from typing import Dict, List, Optional
from ..config.config import Settings

class BedrockService:
    def __init__(self, settings: Settings):
        self.client = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)
        self.settings = settings
        
    async def generate_text(self, prompt: str, context_docs: Optional[List[Dict]] = None) -> str:
        """Generate text using Claude with RAG if context_docs provided"""
        body = {
            "model": self.settings.BEDROCK_MODEL_ID,
            "prompt": prompt,
            "max_tokens": 4096,
            "temperature": 0.7,
        }
        
        if context_docs:
            body["context"] = context_docs
            
        response = self.client.invoke_model(
            modelId=self.settings.BEDROCK_MODEL_ID,
            body=json.dumps(body)
        )
        
        return json.loads(response['body'].read())['completion']
    
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
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for RAG"""
        # Note: Use the appropriate embedding model endpoint
        # Implementation depends on which embedding model you want to use
        pass 