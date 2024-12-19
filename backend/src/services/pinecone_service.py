from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Optional
from ..config.config import Settings

class PineconeService:
    def __init__(self, settings: Settings):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        
        # Create index if it doesn't exist
        if 'slag-index' not in self.pc.list_indexes().names():
            self.pc.create_index(
                name='slag-index',
                dimension=1536,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-west-2'
                )
            )
        
        self.index = self.pc.Index("slag-index")
    
    async def similarity_search(
        self,
        vector: List[float],
        namespace: str,
        top_k: int = 3,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for similar vectors in Pinecone"""
        response = self.index.query(
            vector=vector,
            top_k=top_k,
            filter=filter,
            include_values=True,
            include_metadata=True,
            namespace=namespace
        )
        
        return [
            {
                "id": match["id"],
                "score": match["score"],
                "metadata": match["metadata"]
            }
            for match in response["matches"]
        ]
    
    async def upsert_vectors(
        self,
        vectors: List[tuple[str, List[float], Dict]],
        namespace: str
    ):
        """Insert or update vectors in Pinecone"""
        formatted_vectors = [
            {
                "id": id,
                "values": vec,
                "metadata": meta
            }
            for id, vec, meta in vectors
        ]
        
        self.index.upsert(
            vectors=formatted_vectors,
            namespace=namespace
        )
    
    async def delete_vectors(
        self,
        ids: List[str],
        namespace: str
    ):
        """Delete vectors from Pinecone"""
        self.index.delete(
            ids=ids,
            namespace=namespace
        ) 