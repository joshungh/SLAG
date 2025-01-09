from typing import List, Dict, Any
import uuid
from pinecone import Pinecone
from ...config import settings

class PineconeService:
    def __init__(self):
        pc = Pinecone(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENVIRONMENT
        )
        self.index = pc.Index(settings.PINECONE_INDEX)
        
    async def upsert_text(self, 
        text: str, 
        embeddings: List[float],
        metadata: Dict[str, Any] = None,
        namespace: str = None
    ) -> str:
        """
        Insert or update text with its embeddings and metadata
        
        Args:
            text: The text content to store
            embeddings: Vector embeddings of the text
            metadata: Additional metadata (e.g., story_id, phase, timestamp)
            
        Returns:
            vector_id: ID of the inserted/updated vector
        """
        vector_id = str(uuid.uuid4())
        
        # Ensure metadata includes the text
        if metadata is None:
            metadata = {}
        metadata['text'] = text
        
        self.index.upsert(
            vectors=[(vector_id, embeddings, metadata)],
            namespace=namespace
        )
        
        return vector_id
    
    async def query_similar(self, 
        embeddings: List[float],
        top_k: int = 5,
        filter: Dict = None,
        namespace: str = None
    ) -> List:
        """
        Query for similar vectors
        
        Args:
            embeddings: Query vector
            top_k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of matches with scores and metadata
        """
        response = self.index.query(
            vector=embeddings,
            top_k=top_k,
            filter=filter,
            namespace=namespace,
            include_metadata=True
        )
        return response['matches']

    async def delete_vectors(self, vector_ids: List[str]) -> None:
        """
        Delete vectors by their IDs
        
        Args:
            vector_ids: List of vector IDs to delete
        """
        self.index.delete(ids=vector_ids)

    async def delete_by_metadata(self, filter: Dict) -> None:
        """
        Delete all vectors matching the metadata filter
        
        Args:
            filter: Metadata filter to match vectors for deletion
        """
        self.index.delete(filter=filter) 

    async def describe_index_stats(self) -> Dict:
        """
        Get index statistics for debugging
        """
        return self.index.describe_index_stats()

    async def fetch_vectors(self, vector_ids: List[str]) -> Dict:
        """
        Fetch specific vectors by their IDs
        """
        return self.index.fetch(ids=vector_ids) 

    async def delete_namespace(self, namespace: str) -> None:
        """
        Delete all vectors in a namespace
        
        Args:
            namespace: Namespace to delete
        """
        try:
            self.index.delete(delete_all=True, namespace=namespace)
        except Exception as e:
            raise RuntimeError(f"Failed to delete namespace {namespace}: {str(e)}")
            
    async def list_namespaces(self) -> List[str]:
        """
        List all available namespaces
        """
        stats = await self.describe_index_stats()
        return stats.get('namespaces', {}).keys() 