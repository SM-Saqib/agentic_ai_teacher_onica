"""Slide Indexer - Indexes slide content into vector store"""
import asyncio
from typing import List, Dict, Optional, Tuple
from background.indexing.chroma_indexer import ChromaIndexer
from background.utils.logger import get_logger

logger = get_logger(__name__)


class SlideIndexer:
    """Handles indexing of slides and their explanations"""

    def __init__(self, persist_directory: str = "./data/chromadb"):
        self.indexer = ChromaIndexer(collection_name="slides", persist_directory=persist_directory)
        self.logger = logger

    async def connect(self) -> bool:
        """Connect to vector store"""
        return await self.indexer.connect()

    async def disconnect(self):
        """Disconnect from vector store"""
        await self.indexer.disconnect()

    async def index_slide(self, slide_data: Dict) -> bool:
        """
        Index a single slide

        Args:
            slide_data: Dict with keys: id, title, content, description, is_prebuilt, version
        """
        try:
            slide_id = slide_data['id']
            title = slide_data['title']
            content = slide_data['content']
            description = slide_data.get('description', '')

            # Combine title and content for embedding
            text_to_embed = f"{title} {description} {content}"

            # Prepare metadata
            metadata = {
                "slide_id": str(slide_id),
                "title": title,
                "description": description,
                "is_prebuilt": slide_data.get('is_prebuilt', True),
                "version": slide_data.get('version', 1),
                "type": "slide"
            }

            # Add to vector store
            doc_id = f"slide_{slide_id}"
            success = await self.indexer.add_document(
                doc_id=doc_id,
                content=text_to_embed,
                metadata=metadata
            )

            if success:
                self.logger.info(f"Indexed slide {slide_id}: {title}")
            return success

        except Exception as e:
            self.logger.error(f"Error indexing slide {slide_data.get('id')}: {e}")
            return False

    async def index_slide_explanation(self, explanation_data: Dict) -> bool:
        """
        Index a single slide explanation

        Args:
            explanation_data: Dict with keys: id, slide_id, explanation, language
        """
        try:
            explanation_id = explanation_data['id']
            slide_id = explanation_data['slide_id']
            explanation = explanation_data['explanation']
            language = explanation_data.get('language', 'en')

            # Prepare metadata
            metadata = {
                "explanation_id": str(explanation_id),
                "slide_id": str(slide_id),
                "language": language,
                "type": "explanation"
            }

            # Add to vector store
            doc_id = f"explanation_{explanation_id}"
            success = await self.indexer.add_document(
                doc_id=doc_id,
                content=explanation,
                metadata=metadata
            )

            if success:
                self.logger.info(f"Indexed explanation {explanation_id} for slide {slide_id}")
            return success

        except Exception as e:
            self.logger.error(f"Error indexing explanation {explanation_data.get('id')}: {e}")
            return False

    async def index_slides_batch(self, slides_data: List[Dict]) -> Tuple[int, int]:
        """
        Index multiple slides in batch

        Args:
            slides_data: List of slide dictionaries

        Returns:
            Tuple of (successful_indexes, total_slides)
        """
        try:
            documents = []
            for slide in slides_data:
                slide_id = slide['id']
                title = slide['title']
                content = slide['content']
                description = slide.get('description', '')

                text_to_embed = f"{title} {description} {content}"
                metadata = {
                    "slide_id": str(slide_id),
                    "title": title,
                    "description": description,
                    "is_prebuilt": slide.get('is_prebuilt', True),
                    "version": slide.get('version', 1),
                    "type": "slide"
                }

                doc_id = f"slide_{slide_id}"
                documents.append((doc_id, text_to_embed, metadata, None))

            successful, total = await self.indexer.add_documents_batch(documents)
            self.logger.info(f"Batch indexed {successful}/{total} slides")
            return successful, total

        except Exception as e:
            self.logger.error(f"Error in batch slide indexing: {e}")
            return 0, len(slides_data)

    async def index_explanations_batch(self, explanations_data: List[Dict]) -> Tuple[int, int]:
        """
        Index multiple explanations in batch

        Args:
            explanations_data: List of explanation dictionaries

        Returns:
            Tuple of (successful_indexes, total_explanations)
        """
        try:
            documents = []
            for exp in explanations_data:
                explanation_id = exp['id']
                slide_id = exp['slide_id']
                explanation = exp['explanation']
                language = exp.get('language', 'en')

                metadata = {
                    "explanation_id": str(explanation_id),
                    "slide_id": str(slide_id),
                    "language": language,
                    "type": "explanation"
                }

                doc_id = f"explanation_{explanation_id}"
                documents.append((doc_id, explanation, metadata, None))

            successful, total = await self.indexer.add_documents_batch(documents)
            self.logger.info(f"Batch indexed {successful}/{total} explanations")
            return successful, total

        except Exception as e:
            self.logger.error(f"Error in batch explanation indexing: {e}")
            return 0, len(explanations_data)

    async def search_slide_content(self, query: str, n_results: int = 5, slide_id: Optional[int] = None) -> List[Dict]:
        """
        Search for similar slide content

        Args:
            query: Search query
            n_results: Number of results to return
            slide_id: Optional filter by specific slide

        Returns:
            List of search results
        """
        where = {"type": "slide"}
        if slide_id:
            where["slide_id"] = str(slide_id)

        return await self.indexer.search_similar(query, n_results, where)

    async def search_explanations(self, query: str, n_results: int = 5, slide_id: Optional[int] = None) -> List[Dict]:
        """
        Search for similar explanations

        Args:
            query: Search query
            n_results: Number of results to return
            slide_id: Optional filter by specific slide

        Returns:
            List of search results
        """
        where = {"type": "explanation"}
        if slide_id:
            where["slide_id"] = str(slide_id)

        return await self.indexer.search_similar(query, n_results, where)

    async def delete_slide(self, slide_id: int) -> bool:
        """Delete a slide from vector store"""
        doc_id = f"slide_{slide_id}"
        return await self.indexer.delete_document(doc_id)

    async def delete_explanation(self, explanation_id: int) -> bool:
        """Delete an explanation from vector store"""
        doc_id = f"explanation_{explanation_id}"
        return await self.indexer.delete_document(doc_id)

    async def get_index_stats(self) -> Dict:
        """Get indexing statistics"""
        total_docs = await self.indexer.get_document_count()
        return {
            "total_documents": total_docs,
            "collection_name": "slides"
        }