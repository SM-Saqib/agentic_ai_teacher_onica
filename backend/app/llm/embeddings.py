"""Embeddings Service - Convert text to vectors using sentence-transformers"""
import logging
from typing import List
import numpy as np

from app.config.settings import settings
from app.config.constants import EMBEDDING_DIMENSION
from app.core.exceptions import VectorStoreError

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("sentence-transformers not installed. Embeddings will be simulated.")


class EmbeddingsService:
    """Service for generating text embeddings"""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = None
        self.dimension = EMBEDDING_DIMENSION

        if EMBEDDINGS_AVAILABLE:
            try:
                logger.info(f"Loading embedding model: {self.model_name}")
                self.model = SentenceTransformer(self.model_name)
                logger.info(f"Embedding model loaded. Dimension: {self.model.get_sentence_embedding_dimension()}")
                self.dimension = self.model.get_sentence_embedding_dimension()
            except Exception as e:
                logger.error(f"Error loading embedding model: {e}")
                raise VectorStoreError(f"Failed to load embedding model: {e}")

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string"""
        try:
            if not EMBEDDINGS_AVAILABLE or self.model is None:
                # Return simulated embedding for development
                return self._simulate_embedding(text)

            embedding = self.model.encode([text], normalize_embeddings=True)[0]
            return embedding.tolist()

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise VectorStoreError(f"Failed to generate embedding: {e}")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts"""
        try:
            if not EMBEDDINGS_AVAILABLE or self.model is None:
                # Return simulated embeddings for development
                return [self._simulate_embedding(text) for text in texts]

            embeddings = self.model.encode(texts, normalize_embeddings=True)
            return embeddings.tolist()

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise VectorStoreError(f"Failed to generate embeddings: {e}")

    def _simulate_embedding(self, text: str) -> List[float]:
        """Generate a simulated embedding for development/testing"""
        # Simple hash-based simulation for development
        hash_val = hash(text) % 2147483647
        np.random.seed(hash_val)
        embedding = np.random.randn(self.dimension).astype(np.float32)
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        return embedding.tolist()

    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)

            # Cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            return float(dot_product / (norm1 * norm2))

        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0


# Global embeddings service instance
embeddings_service = EmbeddingsService()
