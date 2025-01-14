from typing import List
import boto3
import json
import numpy as np
from src.config.config import settings
from src.core.utils.logging_config import setup_logging

logger = setup_logging("embedding", "embedding.log")

class EmbeddingService:
    def __init__(self):
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_REGION
        )
        self.model_id = "amazon.titan-embed-text-v1"
        logger.info("EmbeddingService initialized")

    async def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding from Titan embedding model"""
        try:
            body = json.dumps({
                "inputText": text
            })
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=body
            )
            
            response_body = json.loads(response.get('body').read())
            embedding = np.array(response_body['embedding'])
            
            logger.debug(f"Generated embedding of shape {embedding.shape}")
            return embedding
            
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            raise

    async def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Get embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            try:
                embedding = await self.get_embedding(text)
                embeddings.append(embedding)
            except Exception as e:
                logger.error(f"Error getting embedding for text: {text[:100]}... Error: {str(e)}")
                continue
        return embeddings 