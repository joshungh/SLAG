from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Optional
from ..config.config import Settings
import asyncio
import logging

logger = logging.getLogger(__name__)

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
    
    async def query_vectors(
        self,
        vector: List[float],
        namespace: str = "default",
        filter: Optional[Dict] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """Query vectors from Pinecone
        
        Args:
            vector: Query vector (1536D)
            namespace: Namespace to search in
            filter: Metadata filters
            top_k: Number of results to return
            
        Returns:
            List of matches with metadata and scores
        """
        try:
            # Convert to sync operation
            response = await asyncio.to_thread(
                self.index.query,
                vector=vector,
                namespace=namespace,
                filter=filter,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format response
            results = []
            for match in response['matches']:
                results.append({
                    'id': match['id'],
                    'score': float(match['score']),
                    'metadata': match['metadata']
                })
                
            logger.info(f"Found {len(results)} matches in namespace: {namespace}")
            return results
            
        except Exception as e:
            logger.error(f"Error querying vectors: {str(e)}")
            raise 
    
    async def get_vector_metadata(self, vector_id: str, namespace: str = "default") -> Dict:
        """Get metadata for a vector"""
        try:
            response = self.index.fetch(
                ids=[vector_id],
                namespace=namespace
            )
            
            if vector_id in response['vectors']:
                return response['vectors'][vector_id]['metadata']
            return {}
            
        except Exception as e:
            logger.error(f"Error getting vector metadata: {str(e)}")
            raise
    
    async def update_metadata(self, vector_id: str, metadata: Dict, namespace: str = "default") -> bool:
        """Update metadata for a vector"""
        try:
            # Convert to sync operation
            await asyncio.to_thread(
                self.index.update,
                id=vector_id,
                set_metadata=metadata,
                namespace=namespace
            )
            
            # Retry verification a few times with increasing delays
            max_retries = 3
            for attempt in range(max_retries):
                await asyncio.sleep(1 * (attempt + 1))
                
                # Verify update
                updated = await self.get_vector_metadata(vector_id, namespace)
                if not updated:
                    logger.error(f"Attempt {attempt + 1}: Metadata not found")
                    continue
                    
                # Verify all updates were applied
                mismatch = False
                for key, value in metadata.items():
                    if key not in updated:
                        logger.error(f"Attempt {attempt + 1}: {key} not found in updated metadata")
                        mismatch = True
                        break
                    if isinstance(value, list):
                        if not all(v in updated[key] for v in value):
                            logger.error(f"Attempt {attempt + 1}: {key} list values don't match")
                            mismatch = True
                            break
                    elif updated[key] != value:
                        logger.error(f"Attempt {attempt + 1}: {key} value doesn't match: expected {value}, got {updated[key]}")
                        mismatch = True
                        break
                
                if not mismatch:
                    logger.info(f"Successfully updated and verified metadata for {vector_id} on attempt {attempt + 1}")
                    return True
                
            logger.error(f"Failed to verify metadata update after {max_retries} attempts")
            return False
            
        except Exception as e:
            logger.error(f"Error updating metadata: {str(e)}")
            return False