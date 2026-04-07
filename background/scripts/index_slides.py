#!/usr/bin/env python3
"""Batch indexing script for slides and explanations"""
import asyncio
import sys
import os
from typing import List, Dict
import json

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from background.indexing.slide_indexer import SlideIndexer
from background.utils.logger import get_logger
from app.database.connection import get_async_session
from app.database.models import Slide, SlideExplanation

logger = get_logger(__name__)


async def load_slides_from_db() -> List[Dict]:
    """Load all slides from database"""
    async with get_async_session() as session:
        result = await session.execute(
            "SELECT id, title, content, description, is_prebuilt, version FROM slides"
        )
        slides = result.fetchall()
        return [
            {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "description": row[3],
                "is_prebuilt": row[4],
                "version": row[5]
            }
            for row in slides
        ]


async def load_explanations_from_db() -> List[Dict]:
    """Load all explanations from database"""
    async with get_async_session() as session:
        result = await session.execute(
            "SELECT id, slide_id, explanation, language FROM slide_explanations"
        )
        explanations = result.fetchall()
        return [
            {
                "id": row[0],
                "slide_id": row[1],
                "explanation": row[2],
                "language": row[3]
            }
            for row in explanations
        ]


async def index_slides_batch(indexer: SlideIndexer, slides: List[Dict], batch_size: int = 10):
    """Index slides in batches"""
    total_slides = len(slides)
    successful = 0

    for i in range(0, total_slides, batch_size):
        batch = slides[i:i + batch_size]
        batch_successful, batch_total = await indexer.index_slides_batch(batch)
        successful += batch_successful
        logger.info(f"Processed batch {i//batch_size + 1}: {batch_successful}/{batch_total} slides indexed")

    return successful, total_slides


async def index_explanations_batch(indexer: SlideIndexer, explanations: List[Dict], batch_size: int = 10):
    """Index explanations in batches"""
    total_explanations = len(explanations)
    successful = 0

    for i in range(0, total_explanations, batch_size):
        batch = explanations[i:i + batch_size]
        batch_successful, batch_total = await indexer.index_explanations_batch(batch)
        successful += batch_successful
        logger.info(f"Processed batch {i//batch_size + 1}: {batch_successful}/{batch_total} explanations indexed")

    return successful, total_explanations


async def main():
    """Main indexing function"""
    logger.info("Starting batch indexing of slides and explanations")

    # Initialize indexer
    persist_directory = os.getenv("CHROMADB_PERSIST_DIRECTORY", "./data/chromadb")
    indexer = SlideIndexer(persist_directory=persist_directory)

    try:
        # Connect to vector store
        if not await indexer.connect():
            logger.error("Failed to connect to vector store")
            return 1

        # Load data from database
        logger.info("Loading slides from database...")
        slides = await load_slides_from_db()
        logger.info(f"Loaded {len(slides)} slides")

        logger.info("Loading explanations from database...")
        explanations = await load_explanations_from_db()
        logger.info(f"Loaded {len(explanations)} explanations")

        # Index slides
        if slides:
            logger.info("Indexing slides...")
            slides_successful, slides_total = await index_slides_batch(indexer, slides)
            logger.info(f"Slides indexing complete: {slides_successful}/{slides_total} successful")
        else:
            logger.info("No slides to index")

        # Index explanations
        if explanations:
            logger.info("Indexing explanations...")
            explanations_successful, explanations_total = await index_explanations_batch(indexer, explanations)
            logger.info(f"Explanations indexing complete: {explanations_successful}/{explanations_total} successful")
        else:
            logger.info("No explanations to index")

        # Get final stats
        stats = await indexer.get_index_stats()
        logger.info(f"Indexing complete. Total documents in store: {stats['total_documents']}")

    except Exception as e:
        logger.error(f"Error during indexing: {e}")
        return 1
    finally:
        await indexer.disconnect()

    logger.info("Batch indexing completed successfully")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)