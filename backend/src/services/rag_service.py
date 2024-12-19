from typing import List, Dict
from ..services.bedrock_service import BedrockService
from ..services.pinecone_service import PineconeService

class RAGService:
    def __init__(self, bedrock: BedrockService, pinecone: PineconeService):
        self.bedrock = bedrock
        self.pinecone = pinecone
    
    async def get_scene_context(self, current_plot_point: str) -> Dict:
        """Get relevant context for scene generation"""
        # Generate embedding for current plot point
        embedding = await self.bedrock.generate_embedding(current_plot_point)
        
        # Get similar scenes from vector DB
        similar_scenes = await self.pinecone.similarity_search(
            vector=embedding,
            namespace="scenes",
            top_k=3
        )
        
        # Format context for Claude
        context = {
            "similar_scenes": similar_scenes,
            "plot_point": current_plot_point,
            "relevant_docs": await self._get_relevant_docs(embedding)
        }
        
        return context
    
    async def _get_relevant_docs(self, embedding: List[float]) -> List[Dict]:
        """Get relevant documentation for RAG"""
        # This would search through your reference documents
        # (world-building docs, character sheets, etc.)
        docs = await self.pinecone.similarity_search(
            vector=embedding,
            namespace="reference_docs",
            top_k=5
        )
        
        return [
            {
                "text": doc.text,
                "metadata": doc.metadata
            }
            for doc in docs
        ] 