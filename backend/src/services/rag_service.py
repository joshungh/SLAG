from typing import List, Dict, Optional
import logging
import os
import json
from .bedrock_service import BedrockService
from .pinecone_service import PineconeService
from ..models.metadata_schema import DocumentMetadata
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, bedrock_service: BedrockService, pinecone_service: PineconeService):
        self.bedrock = bedrock_service
        self.pinecone = pinecone_service
        
    async def chunk_document(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """Split document into overlapping chunks"""
        if not text.strip():
            return []
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        # Split into words instead of sentences for better size control
        words = text.split()
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            
            if current_size + word_size > chunk_size and current_chunk:
                # Store current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        'chunk_id': len(chunks),
                        'size': len(chunk_text)
                    }
                })
                
                # Start new chunk with overlap
                overlap_words = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_chunk = overlap_words + [word]
                current_size = sum(len(w) + 1 for w in current_chunk)
            else:
                current_chunk.append(word)
                current_size += word_size
        
        # Add final chunk if any
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'metadata': {
                    'chunk_id': len(chunks),
                    'size': len(chunk_text)
                }
            })
        
        logger.info(f"Split document into {len(chunks)} chunks")
        return chunks
        
    async def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """Generate embeddings for chunks using Titan"""
        embedded_chunks = []
        
        for chunk in chunks:
            try:
                embedding = await self.bedrock.generate_embedding(chunk['text'])
                chunk['embedding'] = embedding
                embedded_chunks.append(chunk)
            except Exception as e:
                logger.error(f"Error embedding chunk {chunk['metadata']['chunk_id']}: {str(e)}")
                continue
        
        logger.info(f"Generated embeddings for {len(embedded_chunks)} chunks")
        return embedded_chunks
        
    async def index_document(self, document_path: str, document_type: str, metadata: Dict, namespace: str = "default") -> bool:
        """Index a document into the vector store"""
        try:
            # Read document
            with open(document_path, 'r', encoding='utf-8') as f:  # Add encoding
                content = f.read()
            
            logger.info(f"Indexing with metadata: {metadata}")
            logger.info(f"Document content length: {len(content)}")  # Add content length logging
            
            if not content.strip():
                logger.error(f"Empty content in document: {document_path}")
                return False
            
            # Split into chunks
            chunks = await self.chunk_document(content)
            
            # Generate embeddings
            embedded_chunks = await self.embed_chunks(chunks)
            
            # Add source and filename to metadata
            metadata.update({
                'source': document_path,
                'filename': os.path.basename(document_path)
            })
            
            # Index chunks
            vectors = []
            for i, chunk in enumerate(embedded_chunks):
                chunk_metadata = {
                    **metadata,
                    'chunk_id': i,
                    'size': len(chunk['text']),
                    'text': chunk['text']  # Store the actual text in metadata
                }
                vectors.append((
                    f"{os.path.basename(document_path)}_{i}",
                    chunk['embedding'],
                    chunk_metadata
                ))
            
            # Upsert to Pinecone
            await self.pinecone.upsert_vectors(vectors, namespace)
            
            logger.info(f"Successfully indexed document: {document_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}")
            return False
            
    async def query_knowledge(self, 
        query: str,
        filters: Optional[Dict] = None,
        namespace: str = "default",
        top_k: int = 5
    ) -> List[Dict]:
        """Query knowledge base for relevant context
        
        Args:
            query: Query text to find relevant documents
            filters: Metadata filters for Pinecone query
            namespace: Namespace to search in
            top_k: Number of results to return
            
        Returns:
            List of relevant document chunks with metadata
        """
        try:
            # Generate query embedding
            query_embedding = await self.bedrock.generate_embedding(query)
            
            # Process filters for list fields
            if filters:
                processed_filters = {}
                for key, value in filters.items():
                    if isinstance(value, list):
                        # For list fields, match any value in the list
                        processed_filters[key] = {"$in": value}
                    else:
                        processed_filters[key] = value
            else:
                processed_filters = None
            
            # Search Pinecone
            results = await self.pinecone.query_vectors(
                vector=query_embedding,
                namespace=namespace,
                filter=processed_filters,
                top_k=top_k
            )
            
            # Format and deduplicate results
            seen_chunks = set()
            formatted_results = []
            
            for result in results:
                chunk_id = result['metadata'].get('chunk_id')
                if chunk_id not in seen_chunks:
                    seen_chunks.add(chunk_id)
                    formatted_results.append({
                        'text': result['metadata'].get('text', ''),
                        'metadata': result['metadata'],
                        'score': result['score']
                    })
            
            logger.info(f"Found {len(formatted_results)} unique chunks for query")
            return formatted_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error querying knowledge base: {str(e)}")
            return []
            
    async def get_rag_response(self, query: str, context_type: str, max_tokens: int = 4096) -> str:
        """Get response from Claude with RAG context"""
        try:
            # Get relevant context
            context_results = await self.query_knowledge(
                query=query,
                filters={"type": context_type},
                namespace=context_type,
                top_k=5
            )
            
            # Format context for prompt
            context_text = "\n\n".join([
                f"Context {i+1}:\n{result['text']}" 
                for i, result in enumerate(context_results)
            ])
            
            # Add context to query
            full_prompt = f"""Context:\n{context_text}\n\nQuery:\n{query}"""
            
            logger.info(f"Sending prompt to Claude:\n{full_prompt[:200]}...")
            
            # Get response from Claude
            response = await self.bedrock.generate_text(
                prompt=full_prompt,
                max_tokens=max_tokens
            )
            
            logger.info(f"Raw response from Claude:\n{response[:200]}...")
            
            return response

        except Exception as e:
            logger.error(f"Error getting RAG response: {str(e)}")
            logger.error(f"Query: {query}")
            raise
        
    async def update_document_metadata(self, document_id: str, metadata_updates: Dict, namespace: str = "default") -> bool:
        """Update document metadata"""
        try:
            # Get current metadata
            current_metadata = await self.pinecone.get_vector_metadata(
                vector_id=document_id,
                namespace=namespace
            )
            
            if not current_metadata:
                logger.error(f"No metadata found for document {document_id}")
                return False
            
            # Merge metadata
            updated_metadata = {**current_metadata, **metadata_updates}
            
            # Update in Pinecone
            success = await self.pinecone.update_metadata(
                vector_id=document_id,
                metadata=updated_metadata,
                namespace=namespace
            )
            
            if success:
                logger.info(f"Updated metadata for document {document_id} in namespace {namespace}")
                logger.info(f"New metadata: {updated_metadata}")
            else:
                logger.error(f"Failed to update metadata for document {document_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating metadata: {str(e)}")
            return False
        
    async def index_scene(self, scene: Dict, chapter_number: int, scene_number: int) -> bool:
        """Index generated scene for future context"""
        try:
            logger.info(f"\n=== Indexing Scene {scene_number} of Chapter {chapter_number} ===")
            
            # Create rich metadata for the scene
            metadata = {
                "type": "generated_scene",
                "chapter_number": chapter_number,
                "scene_number": scene_number,
                "location": scene["location"],
                "characters": scene["characters"],
                "plot_thread": scene["metadata"].get("plot_thread", ""),
                "focus": scene["metadata"].get("focus", ""),
                "timestamp": datetime.utcnow().isoformat(),
                "content": scene["content"]
            }
            
            logger.info(f"Scene metadata prepared: {metadata}")

            # Generate embedding for scene content
            logger.info("Generating embedding for scene content...")
            embedding = await self.bedrock.generate_embedding(scene["content"])
            logger.info("Embedding generated successfully")

            # Create vector ID that maintains chronological order
            vector_id = f"scene_{chapter_number:04d}_{scene_number:04d}"
            namespace = f"chapter_{chapter_number}"
            
            logger.info(f"Vector ID: {vector_id}")
            logger.info(f"Target namespace: {namespace}")
            
            vectors = [(vector_id, embedding, metadata)]

            # Upsert to Pinecone
            logger.info("Upserting to Pinecone...")
            await self.pinecone.upsert_vectors(vectors, namespace)
            
            logger.info(f"Successfully indexed scene {scene_number} in chapter {chapter_number}")
            logger.info("=== Scene Indexing Complete ===\n")
            
            return True

        except Exception as e:
            logger.error(f"Error indexing scene: {str(e)}")
            logger.error(f"Scene data: {scene}")
            return False