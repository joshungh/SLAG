import os
from typing import List, Dict
from ..services.bedrock_service import BedrockService
from ..services.pinecone_service import PineconeService

class IngestionService:
    def __init__(self, bedrock: BedrockService, pinecone: PineconeService):
        self.bedrock = bedrock
        self.pinecone = pinecone
    
    async def ingest_document(self, file_path: str, namespace: str):
        """Ingest a single document into the vector store"""
        # Read document
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Split into chunks (we'll implement chunking strategy)
        chunks = self._chunk_document(content)
        
        # Generate embeddings and metadata for each chunk
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = await self.bedrock.generate_embedding(chunk)
            metadata = {
                "source": file_path,
                "chunk_index": i,
                "content": chunk
            }
            vectors.append((f"{os.path.basename(file_path)}_{i}", embedding, metadata))
        
        # Upload to Pinecone
        await self.pinecone.upsert_vectors(vectors, namespace)
    
    def _chunk_document(self, content: str, chunk_size: int = 1000) -> List[str]:
        """Split document into chunks for embedding"""
        # Implement smart chunking strategy
        # For now, simple character-based chunking
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)] 