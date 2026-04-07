"""ChromaDB Vector Store Client"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """ChromaDB client for vector storage and retrieval"""

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMADB_PERSIST_DIRECTORY,
            settings=Settings(anonymized_telemetry=False)
        )
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(
            name="slides",
            metadata={"description": "Slide content embeddings"}
        )

    async def add_slide(self, slide_id: int, title: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a slide to the vector store"""
        try:
            # Generate embedding
            text_to_embed = f"{title} {content}"
            embedding = self.encoder.encode(text_to_embed).tolist()

            # Prepare metadata
            doc_metadata = metadata or {}
            doc_metadata.update({
                "slide_id": str(slide_id),
                "title": title,
                "content_length": len(content)
            })

            # Add to collection
            doc_id = f"slide_{slide_id}"
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                metadatas=[doc_metadata],
                documents=[content]
            )

            logger.info(f"Added slide {slide_id} to vector store")
            return doc_id

        except Exception as e:
            logger.error(f"Error adding slide {slide_id}: {e}")
            raise

    async def add_slide_explanation(self, explanation_id: int, slide_id: int, explanation: str, language: str = "en") -> str:
        """Add a slide explanation to the vector store"""
        try:
            # Generate embedding
            embedding = self.encoder.encode(explanation).tolist()

            # Prepare metadata
            doc_metadata = {
                "explanation_id": str(explanation_id),
                "slide_id": str(slide_id),
                "language": language,
                "type": "explanation"
            }

            # Add to collection
            doc_id = f"explanation_{explanation_id}"
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                metadatas=[doc_metadata],
                documents=[explanation]
            )

            logger.info(f"Added explanation {explanation_id} to vector store")
            return doc_id

        except Exception as e:
            logger.error(f"Error adding explanation {explanation_id}: {e}")
            raise

    async def search_similar(self, query: str, n_results: int = 5, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar content"""
        try:
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
            logger.error(f"Error searching vector store: {e}")
            raise

    async def delete_slide(self, slide_id: int) -> bool:
        """Delete a slide from vector store"""
        try:
            doc_id = f"slide_{slide_id}"
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted slide {slide_id} from vector store")
            return True
        except Exception as e:
            logger.error(f"Error deleting slide {slide_id}: {e}")
            return False

    async def delete_explanation(self, explanation_id: int) -> bool:
        """Delete an explanation from vector store"""
        try:
            doc_id = f"explanation_{explanation_id}"
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted explanation {explanation_id} from vector store")
            return True
        except Exception as e:
            logger.error(f"Error deleting explanation {explanation_id}: {e}")
            return False

    async def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": "slides",
                "document_count": count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise


# Global instance
chroma_store = ChromaVectorStore()