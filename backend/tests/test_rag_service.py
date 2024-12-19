import pytest
from src.services.rag_service import RAGService
from src.services.bedrock_service import BedrockService
from src.services.pinecone_service import PineconeService
from src.config.config import Settings
import logging
import os
from src.utils.path_utils import get_reference_doc_path
from src.models.metadata_schema import DocumentMetadata

logger = logging.getLogger(__name__)

@pytest.fixture
def settings():
    """Initialize settings"""
    return Settings()

@pytest.fixture
def bedrock_service(settings):
    """Initialize BedrockService"""
    return BedrockService(settings)

@pytest.fixture
def pinecone_service(settings):
    """Initialize PineconeService"""
    return PineconeService(settings)

@pytest.fixture
def rag_service(bedrock_service, pinecone_service):
    """Initialize RAGService with dependencies"""
    return RAGService(bedrock_service, pinecone_service)

@pytest.mark.asyncio
async def test_document_chunking(rag_service):
    """Test document chunking functionality"""
    # Test with a simple document first
    test_text = "This is a test document. " * 100  # Long enough to create multiple chunks
    
    chunks = await rag_service.chunk_document(test_text)
    
    # Basic validation
    assert len(chunks) > 0, "Should create at least one chunk"
    assert all('text' in chunk for chunk in chunks), "All chunks should contain text"
    assert all('metadata' in chunk for chunk in chunks), "All chunks should have metadata"
    
    # Size validation
    for chunk in chunks:
        assert len(chunk['text']) <= 550, "Chunks should not exceed max size (500 + some overlap)"
        assert chunk['metadata']['size'] == len(chunk['text']), "Size metadata should match actual text length"
    
    # Overlap validation
    for i in range(len(chunks) - 1):
        current_text = chunks[i]['text']
        next_text = chunks[i + 1]['text']
        # Should share some content
        assert any(sent in next_text for sent in current_text.split('. ')[-2:]), "Chunks should have overlapping content"

@pytest.mark.asyncio
async def test_document_chunking_edge_cases(rag_service):
    """Test document chunking with edge cases"""
    test_cases = [
        # Empty text
        "",
        # Single short sentence
        "This is a short test.",
        # Very long sentence
        "Very " * 1000 + "long sentence.",
        # Text with special characters
        "Special chars: !@#$%^&*(). New sentence. Another one.",
        # Multiple newlines
        "Line one.\n\nLine two.\n\nLine three.",
    ]
    
    for test_text in test_cases:
        logger.info(f"Testing chunking with text length: {len(test_text)}")
        chunks = await rag_service.chunk_document(test_text)
        
        if test_text:
            assert len(chunks) > 0, "Should create at least one chunk for non-empty text"
            assert all('text' in chunk for chunk in chunks), "All chunks should contain text"
            assert all('metadata' in chunk for chunk in chunks), "All chunks should have metadata"
            
            # Validate chunk sizes
            for chunk in chunks:
                assert len(chunk['text']) <= 550, f"Chunk too large: {len(chunk['text'])} chars"
        else:
            assert len(chunks) == 0, "Empty text should produce no chunks"

@pytest.mark.asyncio
async def test_chunk_embedding(rag_service):
    """Test chunk embedding generation"""
    test_chunks = [
        {"text": "Test chunk 1", "metadata": {"type": "test"}},
        {"text": "Test chunk 2", "metadata": {"type": "test"}}
    ]
    
    embedded_chunks = await rag_service.embed_chunks(test_chunks)
    
    assert len(embedded_chunks) == len(test_chunks), "Should embed all chunks"
    assert all('embedding' in chunk for chunk in embedded_chunks), "All chunks should have embeddings"
    assert all(len(chunk['embedding']) == 1536 for chunk in embedded_chunks), "Embeddings should be 1536D"

@pytest.mark.asyncio
async def test_document_indexing(rag_service):
    """Test full document indexing process"""
    test_doc_path = get_reference_doc_path("characters/character-chen.txt")
    
    success = await rag_service.index_document(
        document_path=test_doc_path,
        document_type="character",
        metadata={"name": "Dr. James Chen", "type": "character_profile"}
    )
    
    assert success, "Document indexing should succeed"

@pytest.mark.asyncio
async def test_knowledge_query(rag_service):
    """Test knowledge base querying"""
    # First index a test document
    doc_path = get_reference_doc_path("characters/character-chen.txt")
    await rag_service.index_document(
        document_path=doc_path,
        document_type="character_profile",
        metadata={"type": "character_profile", "name": "Dr. James Chen"},
        namespace="characters"
    )
    
    test_query = "What are Dr. Chen's key personality traits?"
    results = await rag_service.query_knowledge(
        query=test_query,
        filters={"type": "character_profile"},
        namespace="characters"  # Use correct namespace
    )
    
    assert len(results) > 0, "Should return relevant results"
    assert all('text' in result for result in results), "All results should contain text"
    assert all('metadata' in result for result in results), "All results should have metadata" 

@pytest.mark.asyncio
async def test_document_indexing_comprehensive(rag_service):
    """Test full document indexing process with different document types"""
    test_cases = [
        {
            "path": get_reference_doc_path("characters/character-chen.txt"),
            "type": "character",
            "metadata": {
                "name": "Dr. James Chen",
                "type": "character_profile",
                "category": "main_character"
            },
            "namespace": "characters"
        },
        {
            "path": get_reference_doc_path("style-guide/scifi-style-guide.txt"),
            "type": "style_guide",
            "metadata": {
                "name": "SciFi Style Guide",
                "type": "writing_guide",
                "category": "style"
            },
            "namespace": "style_guides"
        }
    ]
    
    for test_case in test_cases:
        logger.info(f"\nTesting document indexing: {test_case['path']}")
        
        try:
            # Verify file exists before attempting to index
            assert os.path.exists(test_case["path"]), f"Test file not found: {test_case['path']}"
            
            # Index the document
            success = await rag_service.index_document(
                document_path=test_case["path"],
                document_type=test_case["type"],
                metadata=test_case["metadata"],
                namespace=test_case["namespace"]
            )
            
            assert success, f"Document indexing failed for {test_case['path']}"
            logger.info(f"Successfully indexed document: {test_case['path']} in namespace: {test_case['namespace']}")
            
        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}")
            raise

@pytest.mark.asyncio
async def test_knowledge_query_comprehensive(rag_service):
    """Test knowledge base querying across different document types"""
    test_queries = [
        {
            "query": "What are Dr. Chen's key personality traits?",
            "namespace": "characters",
            "filters": {"type": "character_profile"},
            "expected_count": 1
        },
        {
            "query": "How should technical discussions be written in dialogue?",
            "namespace": "style_guides",
            "filters": {"type": "writing_guide"},
            "expected_count": 1
        }
    ]
    
    for test_case in test_queries:
        logger.info(f"\nTesting query: {test_case['query']}")
        
        results = await rag_service.query_knowledge(
            query=test_case["query"],
            filters=test_case["filters"],
            namespace=test_case["namespace"]
        )
        
        assert len(results) > 0, "Should return relevant results"
        assert all('text' in r for r in results), "All results should contain text"
        assert all('metadata' in r for r in results), "All results should have metadata"
        assert all('score' in r for r in results), "All results should have relevance scores"
        
        # Log results for inspection
        logger.info(f"Found {len(results)} results")
        for i, result in enumerate(results):
            logger.info(f"\nResult {i+1} (score: {result['score']:.3f}):")
            logger.info(f"Text snippet: {result['text'][:200]}...")

@pytest.mark.asyncio
async def test_rag_response_generation(rag_service):
    """Test full RAG response generation"""
    # First, index the test documents
    test_docs = [
        {
            "path": get_reference_doc_path("characters/character-chen.txt"),
            "type": "character",
            "metadata": {"type": "character_profile"},
            "namespace": "characters"
        },
        {
            "path": get_reference_doc_path("style-guide/scifi-style-guide.txt"),
            "type": "style_guide",
            "metadata": {"type": "writing_guide"},
            "namespace": "style_guides"
        }
    ]
    
    # Index documents
    for doc in test_docs:
        success = await rag_service.index_document(
            document_path=doc["path"],
            document_type=doc["type"],
            metadata=doc["metadata"],
            namespace=doc["namespace"]
        )
        assert success, f"Failed to index document: {doc['path']}"
        
        # Add debug logging
        logger.info(f"Indexed document in namespace: {doc['namespace']} with metadata: {doc['metadata']}")
    
    # Now test queries
    test_cases = [
        {
            "query": "What are Dr. Chen's research interests and achievements?",
            "context_type": "character",
            "expected_keywords": ["Giant", "quantum", "research"]
        },
        {
            "query": "How should I write a scene with technical dialogue?",
            "context_type": "style_guide",
            "expected_keywords": ["dialogue", "technical", "character"]
        }
    ]
    
    for test_case in test_cases:
        logger.info(f"\nTesting RAG response for: {test_case['query']}")
        
        response = await rag_service.get_rag_response(
            query=test_case["query"],
            context_type=test_case["context_type"]
        )
        
        assert response, "Should return a non-empty response"
        assert any(keyword.lower() in response.lower() 
                  for keyword in test_case["expected_keywords"]), \
            "Response should contain relevant keywords"
        
        # Log response for inspection
        logger.info(f"\nQuery: {test_case['query']}")
        logger.info(f"Response:\n{response}")

@pytest.mark.asyncio
async def test_metadata_validation(rag_service):
    """Test metadata validation and filtering"""
    test_cases = [
        {
            # Character document with full metadata
            "path": get_reference_doc_path("characters/character-chen.txt"),
            "type": "character_profile",
            "metadata": {
                "category": "main_character",
                "species": "human",
                "role": ["scientific", "technical"],
                "affiliation": "independent",
                "expertise": ["giant_studies", "quantum_physics"],
                "time_period": "present",
                "security_level": "restricted"
            },
            "namespace": "characters",
            "expected_count": 1
        },
        {
            # Location document with metadata
            "path": get_reference_doc_path("world/slag-locations.txt"),
            "type": "location",
            "metadata": {
                "category": "world_building",
                "location_type": "station",
                "jurisdiction": "concordat",
                "security_level": "public",
                "time_period": "present"
            },
            "namespace": "locations",
            "expected_count": 1
        }
    ]
    
    # Test indexing with metadata
    for test_case in test_cases:
        success = await rag_service.index_document(
            document_path=test_case["path"],
            document_type=test_case["type"],
            metadata=test_case["metadata"],
            namespace=test_case["namespace"]
        )
        assert success, f"Failed to index document: {test_case['path']}"
    
    # Test querying with metadata filters
    filter_tests = [
        {
            "query": "What are Dr. Chen's research interests?",
            "filters": {
                "type": "character_profile",
                "species": "human",
                "expertise": ["giant_studies"]
            },
            "namespace": "characters",
            "expected_count": 1,
            "min_score": 0.5
        }
    ]
    
    for test in filter_tests:
        results = await rag_service.query_knowledge(
            query=test["query"],
            filters=test["filters"],
            namespace=test["namespace"]
        )
        
        # Filter by relevance score
        relevant_results = [r for r in results if r['score'] > test.get('min_score', 0.5)]
        
        assert len(relevant_results) >= test["expected_count"], \
            f"Expected at least {test['expected_count']} relevant results, got {len(relevant_results)}"
        
        # Verify metadata in results
        for result in relevant_results:
            metadata = result['metadata']
            for key, value in test["filters"].items():
                if isinstance(value, list):
                    assert any(v in metadata[key] for v in value), \
                        f"Expected one of {value} in metadata[{key}]"
                else:
                    assert metadata[key] == value, \
                        f"Expected {value} for metadata[{key}], got {metadata[key]}"
            
            logger.info(f"Metadata validation passed for result: {metadata}")

@pytest.mark.asyncio
async def test_metadata_validation_errors(rag_service):
    """Test metadata validation error handling"""
    invalid_cases = [
        {
            # Invalid species
            "metadata": {
                "type": "character_profile",
                "category": "main_character",
                "species": "invalid_species"
            }
        },
        {
            # Invalid security level
            "metadata": {
                "type": "location",
                "category": "world_building",
                "security_level": "super_secret"
            }
        }
    ]
    
    for case in invalid_cases:
        with pytest.raises(ValueError):
            DocumentMetadata(**case["metadata"])

@pytest.mark.asyncio
async def test_metadata_updates(rag_service):
    """Test metadata update functionality"""
    # First index a document
    doc_path = get_reference_doc_path("characters/character-chen.txt")
    initial_metadata = {
        "type": "character_profile",
        "category": "main_character",
        "species": "human",
        "security_level": "public"
    }
    
    success = await rag_service.index_document(
        document_path=doc_path,
        document_type="character",
        metadata=initial_metadata,
        namespace="test"
    )
    assert success
    
    # Update metadata
    doc_id = f"{os.path.basename(doc_path)}_0"  # First chunk
    updates = {
        "security_level": "restricted",
        "expertise": ["giant_studies", "quantum_physics"]
    }
    
    success = await rag_service.update_document_metadata(
        document_id=doc_id,
        metadata_updates=updates,
        namespace="test"
    )
    assert success
    
    # Verify updates
    results = await rag_service.query_knowledge(
        query="Dr Chen",
        filters={"security_level": "restricted"},
        namespace="test"
    )
    
    assert len(results) > 0
    assert results[0]["metadata"]["security_level"] == "restricted"
    assert "giant_studies" in results[0]["metadata"]["expertise"]