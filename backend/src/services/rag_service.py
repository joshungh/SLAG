from typing import List, Dict, Optional
from ..services.bedrock_service import BedrockService
from ..services.pinecone_service import PineconeService

class RAGService:
    def __init__(self, bedrock_service: BedrockService, pinecone_service: PineconeService):
        self.bedrock = bedrock_service
        self.pinecone = pinecone_service
    
    async def store_reference(
        self,
        text: str,
        metadata: Dict,
        namespace: str = "references"
    ):
        """Store a reference text with its embedding"""
        # Generate embedding
        embedding = await self.bedrock.generate_embedding(text)
        
        # Store in Pinecone
        await self.pinecone.upsert_vectors(
            vectors=[(metadata["id"], embedding, metadata)],
            namespace=namespace
        )
    
    async def find_similar_references(
        self,
        query: str,
        namespace: str = "references",
        top_k: int = 3,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """Find similar references using embedding similarity"""
        # Generate query embedding
        query_embedding = await self.bedrock.generate_embedding(query)
        
        # Search Pinecone
        results = await self.pinecone.similarity_search(
            vector=query_embedding,
            namespace=namespace,
            top_k=top_k,
            filter=filter
        )
        
        return results 