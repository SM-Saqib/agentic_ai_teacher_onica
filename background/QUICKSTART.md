"""Quick Start Guide for Background Package

This guide shows how to quickly get started with the background package.
"""

# QUICK START EXAMPLES

# 1. LOGGING
# ==========

from background.utils.logger import get_logger, TaskLogger

logger = get_logger(__name__)

# Use in your code:
logger.info("Starting process")
logger.warning("This is a warning")
logger.error("An error occurred")

# Use with context manager:
with TaskLogger(logger, "MyTask"):
    # Your code here
    logger.info("Task is running")


# 2. TEXT PROCESSING
# ==================

from background.enrichment.text_processor import TextProcessor

processor = TextProcessor()

# Clean text
raw_text = "   Hello   world!   "
cleaned = processor.clean(raw_text)  # "Hello world!"

# Remove HTML tags
html = "<p>Hello <b>world</b></p>"
plain = processor.remove_html_tags(html)  # "Hello world"

# Extract sentences
text = "First sentence. Second sentence! Third sentence?"
sentences = processor.extract_sentences(text)

# Full processing pipeline
result = processor.process_pipeline(
    html,
    remove_html=True,
    remove_urls=True,
    normalize=True,
    lowercase_text=True
)


# 3. WEB CRAWLING
# ===============

from background.crawlers.base_crawler import BaseCrawler, CrawlResult
from bs4 import BeautifulSoup

class SimpleWebCrawler(BaseCrawler):
    """Simple concrete crawler implementation"""
    
    async def parse(self, content: str):
        """Parse HTML content"""
        soup = BeautifulSoup(content, 'html.parser')
        return {
            "title": soup.title.string if soup.title else "",
            "text": soup.get_text()[:500],
        }
    
    async def crawl(self, url: str):
        """Crawl a URL"""
        content = await self.fetch(url)
        if not content:
            return None
        
        data = await self.parse(content)
        return CrawlResult(
            url=url,
            title=data.get("title", ""),
            content=data.get("text", "")
        ).to_dict()


# Usage
import asyncio

async def crawl_example():
    crawler = SimpleWebCrawler()
    result = await crawler.crawl("https://example.com")
    print(result)

# asyncio.run(crawl_example())


# 4. VECTOR STORE INDEXING
# =========================

from background.indexing.base_indexer import BaseIndexer, IndexerConfig

# For ChromaDB-specific implementation (Phase 3):
# from background.indexing.chromadb_indexer import ChromaDBIndexer
# 
# indexer = ChromaDBIndexer()
# await indexer.connect()
# 
# # Add documents
# documents = [
#     {
#         "id": "doc1",
#         "content": "Machine learning is a subset of AI",
#         "metadata": {"source": "slides", "slide_id": 1}
#     }
# ]
# await indexer.add_documents(documents)
# 
# # Search
# results = await indexer.search("What is machine learning?", top_k=3)
# 
# await indexer.disconnect()


# 5. CONFIGURATION
# ================

from background.utils.config import BackgroundConfig

# Access config
print(BackgroundConfig.CRAWL_TIMEOUT)  # 30
print(BackgroundConfig.INDEX_BATCH_SIZE)  # 100

# Print all config
BackgroundConfig.print_config()

# Override via environment variables:
# export CRAWL_TIMEOUT=60
# export INDEX_BATCH_SIZE=200


# 6. RUNNING SCRIPTS
# ==================

# Run example script from command line:
# python -m background.scripts.example_script

# Or import and use in your code:
# from background.scripts.example_script import ExampleScript
# import asyncio
# 
# async def main():
#     script = ExampleScript()
#     success = await script.run()
#
# asyncio.run(main())


# 7. BATCH PROCESSING
# ====================

# Indexing multiple documents efficiently
# async def batch_index_slides(slides):
#     indexer = ChromaDBIndexer()
#     await indexer.connect()
#     
#     # Batch processing with progress
#     documents = [
#         {
#             "id": f"slide_{slide.id}",
#             "content": slide.content,
#             "metadata": {
#                 "slide_id": slide.id,
#                 "title": slide.title,
#                 "source": "course_slides"
#             }
#         }
#         for slide in slides
#     ]
#     
#     total = await indexer.batch_add_documents(
#         documents,
#         batch_size=100
#     )
#     
#     logger.info(f"Indexed {total} slides")
#     await indexer.disconnect()


# NEXT STEPS
# ==========
# 1. Review the README.md in the background directory
# 2. Check specific module docstrings for detailed API docs
# 3. Look at example implementations for patterns
# 4. Create your own scripts/crawlers/enrichers by extending base classes
