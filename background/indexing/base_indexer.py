"""Base Indexer - Interface for vector store operations"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from background.utils.logger import get_logger

logger = get_logger(__name__)


class BaseIndexer(ABC):
    """Abstract base class for vector store indexers"""
    
    def __init__(self, collection_name: str = "default"):
        """
        Initialize indexer
        
        Args:
            collection_name: Name of the collection/index
        """
        self.collection_name = collection_name
        self.logger = logger
    
    @abstractmethod
    async def connect(self) -> bool:
        """
        Connect to vector store
        
        Returns:
            True if connection successful
        """
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Disconnect from vector store"""
        pass
    
    @abstractmethod
    async def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict] = None,
        embedding: Optional[List[float]] = None,
    ) -> bool:
        """
        Add a single document to the vector store
        
        Args:
            doc_id: Unique document identifier
            content: Document content/text
            metadata: Additional metadata
            embedding: Pre-computed embedding (optional)
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def add_documents(
        self,
        documents: List[Dict],
    ) -> int:
        """
        Add multiple documents to vector store
        
        Args:
            documents: List of documents with keys: id, content, metadata (optional)
            
        Returns:
            Number of documents added
        """
        pass
    
    @abstractmethod
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None,
    ) -> List[Tuple[str, float, Dict]]:
        """
        Search for similar documents
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of (doc_id, score, metadata) tuples
        """
        pass
    
    @abstractmethod
    async def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document from the vector store
        
        Args:
            doc_id: Document identifier
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def delete_collection(self) -> bool:
        """
        Delete entire collection
        
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def get_document_count(self) -> int:
        """
        Get number of documents in collection
        
        Returns:
            Document count
        """
        pass
    
    async def batch_add_documents(
        self,
        documents: List[Dict],
        batch_size: int = 100,
    ) -> int:
        """
        Add documents in batches
        
        Args:
            documents: List of documents
            batch_size: Size of each batch
            
        Returns:
            Total number of documents added
        """
        total_added = 0
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            self.logger.info(f"Adding batch {i // batch_size + 1} ({len(batch)} docs)")
            
            added = await self.add_documents(batch)
            total_added += added
        
        self.logger.info(f"Batch operation complete: {total_added} documents added")
        return total_added


class IndexerConfig:
    """Configuration for indexer operations"""
    
    def __init__(
        self,
        collection_name: str = "slides",
        embedding_model: str = "all-MiniLM-L6-v2",
        distance_metric: str = "cosine",
        batch_size: int = 100,
    ):
        """
        Initialize indexer configuration
        
        Args:
            collection_name: Name of the collection
            embedding_model: Embedding model to use
            distance_metric: Distance metric (cosine, euclidean, etc.)
            batch_size: Batch size for operations
        """
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.distance_metric = distance_metric
        self.batch_size = batch_size
