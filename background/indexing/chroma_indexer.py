"""ChromaDB Indexer Implementation"""
import asyncio
from typing import List, Dict, Optional, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
from background.indexing.base_indexer import BaseIndexer
from background.utils.logger import get_logger

# Import ChromaDB client - assuming it's available or we can import from backend
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

logger = get_logger(__name__)


class ChromaIndexer(BaseIndexer):
    """ChromaDB implementation of the indexer"""

    def __init__(self, collection_name: str = "slides", persist_directory: str = "./data/chromadb"):
        super().__init__(collection_name)
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

    async def connect(self) -> bool:
        """Connect to ChromaDB"""
        try:
            if chromadb is None:
                raise ImportError("chromadb not installed")

            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": f"{self.collection_name} content embeddings"}
            )
            self.logger.info(f"Connected to ChromaDB collection: {self.collection_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to ChromaDB: {e}")
            return False

    async def disconnect(self):
        """Disconnect from ChromaDB"""
        # ChromaDB client doesn't need explicit disconnect
        self.client = None
        self.collection = None
        self.logger.info("Disconnected from ChromaDB")

    async def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict] = None,
        embedding: Optional[List[float]] = None,
    ) -> bool:
        """Add a single document to ChromaDB"""
        try:
            if not self.collection:
                await self.connect()

            # Generate embedding if not provided
            if embedding is None:
                embedding = self.encoder.encode(content).tolist()

            # Prepare metadata
            doc_metadata = metadata or {}

            # Add to collection
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                metadatas=[doc_metadata],
                documents=[content]
            )

            self.logger.info(f"Added document {doc_id} to ChromaDB")
            return True

        except Exception as e:
            self.logger.error(f"Error adding document {doc_id}: {e}")
            return False

    async def add_documents_batch(
        self,
        documents: List[Tuple[str, str, Optional[Dict], Optional[List[float]]]]
    ) -> Tuple[int, int]:
        """
        Add multiple documents in batch

        Args:
            documents: List of (doc_id, content, metadata, embedding) tuples

        Returns:
            Tuple of (successful_adds, total_documents)
        """
        try:
            if not self.collection:
                await self.connect()

            ids = []
            embeddings = []
            metadatas = []
            contents = []

            for doc_id, content, metadata, embedding in documents:
                # Generate embedding if not provided
                if embedding is None:
                    embedding = self.encoder.encode(content).tolist()

                ids.append(doc_id)
                embeddings.append(embedding)
                metadatas.append(metadata or {})
                contents.append(content)

            # Batch add
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=contents
            )

            self.logger.info(f"Added {len(ids)} documents to ChromaDB")
            return len(ids), len(ids)

        except Exception as e:
            self.logger.error(f"Error in batch add: {e}")
            return 0, len(documents)

    async def search_similar(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for similar documents"""
        try:
            if not self.collection:
                await self.connect()

            # Generate query embedding
            query_embedding = self.encoder.encode(query).tolist()

            # Perform search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
                include=['metadatas', 'documents', 'distances']
            )

            # Format results
            formatted_results = []
            for i, doc_id in enumerate(results['ids'][0]):
                formatted_results.append({
                    "id": doc_id,
                    "metadata": results['metadatas'][0][i],
                    "content": results['documents'][0][i],
                    "distance": results['distances'][0][i]
                })

            return formatted_results

        except Exception as e:
            self.logger.error(f"Error searching: {e}")
            return []

    async def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the vector store"""
        try:
            if not self.collection:
                await self.connect()

            self.collection.delete(ids=[doc_id])
            self.logger.info(f"Deleted document {doc_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting document {doc_id}: {e}")
            return False

    async def get_document_count(self) -> int:
        """Get total number of documents in collection"""
        try:
            if not self.collection:
                await self.connect()
            return self.collection.count()
        except Exception as e:
            self.logger.error(f"Error getting document count: {e}")
            return 0