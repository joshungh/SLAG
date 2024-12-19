import pinecone
from typing import List, Dict, Optional
from ..config.config import Settings

class PineconeService:
    def __init__(self, settings: Settings):
        pinecone.init(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENVIRONMENT
        )
        self.index = pinecone.Index("slag-index")
        self.index_url = "slag-index-22tqnba.svc.apw5-4e34-81fa.pinecone.io"
    
    async def similarity_search(
        self,
        vector: List[float],
        namespace: str,
        top_k: int = 3,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for similar vectors in Pinecone"""
        results = self.index.query(
            namespace=namespace,
            vector=vector,
            top_k=top_k,
            filter=filter,
            include_metadata=True
        )
        
        return [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]
    
    async def upsert_vectors(
        self,
        vectors: List[tuple[str, List[float], Dict]],
        namespace: str
    ):
        """Insert or update vectors in Pinecone"""
        self.index.upsert(
            vectors=[(id, vec, meta) for id, vec, meta in vectors],
            namespace=namespace
        )
    
    async def delete_vectors(
        self,
        ids: List[str],
        namespace: str
    ):
        """Delete vectors from Pinecone"""
        self.index.delete(ids=ids, namespace=namespace) 