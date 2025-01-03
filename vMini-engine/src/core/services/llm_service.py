from typing import Dict, Any, Optional
import boto3
import json
from src.config.config import settings

class LLMService:
    def __init__(self):
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    async def generate(
        self, 
        prompt: str, 
        max_tokens: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "messages": [{"role": "user", "content": prompt}]
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            print(f"Error generating from LLM: {str(e)}")
            raise 