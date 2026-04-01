# Background Tasks and Data Enrichment

This package contains background scripts, tasks, and utilities for data preparation, processing, and enrichment in the AI Teacher platform.

## Directory Structure

```
background/
├── __init__.py
├── README.md
├── scripts/                      # Standalone executable scripts
│   ├── __init__.py
│   ├── initialize_db.py         # Database initialization
│   ├── seed_data.py             # Populate initial data
│   ├── migrate_data.py           # Data migration utilities
│   └── ...
├── enrichment/                   # Data enrichment and transformation
│   ├── __init__.py
│   ├── text_processor.py        # Text cleaning and preprocessing
│   ├── metadata_extractor.py    # Extract metadata from content
│   ├── transformer.py           # Transform data between formats
│   └── ...
├── crawlers/                     # Web crawling utilities
│   ├── __init__.py
│   ├── base_crawler.py          # Base crawler class
│   ├── website_crawler.py       # General website crawler
│   ├── documentation_crawler.py # Documentation crawler
│   └── ...
├── indexing/                     # Vector store indexing
│   ├── __init__.py
│   ├── indexer.py               # Base indexer interface
│   ├── chromadb_indexer.py      # ChromaDB integration
│   ├── batch_processor.py       # Batch indexing processor
│   └── ...
└── utils/                        # Shared utilities
    ├── __init__.py
    ├── logger.py                # Logging utilities
    ├── config.py                # Configuration management
    ├── decorators.py            # Common decorators
    └── ...
```

## Use Cases

### 1. Data Preparation (`scripts/`)
- Database initialization
- Seeding initial data
- Data migrations
- Bulk data imports

### 2. Data Enrichment (`enrichment/`)
- Text preprocessing and cleaning
- Metadata extraction (titles, summaries, tagging)
- Content transformation (Markdown → HTML, PDF → text, etc.)
- Semantic enrichment (adding embeddings, keywords, etc.)

### 3. Web Crawling (`crawlers/`)
- Website crawling for content extraction
- Documentation site scraping
- API data collection
- Automatic content discovery

### 4. Vector Store Indexing (`indexing/`)
- Populate ChromaDB with course content
- Batch embedding generation
- Index management and updates
- Similarity search optimization

## Example: Using Background Tasks

### Running a Script
```bash
# From project root
python -m background.scripts.initialize_db
python -m background.scripts.seed_data
```

### Using Enrichment Utilities
```python
from background.enrichment.text_processor import TextProcessor
from background.enrichment.metadata_extractor import MetadataExtractor

processor = TextProcessor()
cleaned_text = processor.clean(raw_text)

extractor = MetadataExtractor()
metadata = extractor.extract(content)
```

### Web Crawling
```python
from background.crawlers.website_crawler import WebsiteCrawler

crawler = WebsiteCrawler()
content = await crawler.crawl("https://example.com")
```

### Vector Store Indexing
```python
from background.indexing.chromadb_indexer import ChromaDBIndexer

indexer = ChromaDBIndexer()
await indexer.index_slides(slides_data)
await indexer.search("machine learning", top_k=5)
```

## Running Tasks Asynchronously

For long-running tasks, use background job queues (e.g., Celery):

```python
from celery import Celery
from background.indexing.batch_processor import BatchProcessor

app = Celery('ai_teacher')

@app.task
def index_batch_of_slides(slides_ids):
    processor = BatchProcessor()
    return processor.index_batch(slides_ids)
```

## Dependencies

Install additional dependencies as needed:

```bash
# Web crawling
pip install beautifulsoup4 selenium requests

# Data processing
pip install pandas numpy

# Vector stores
pip install chromadb

# Task queuing
pip install celery redis
```

## Configuration

Configuration for background tasks can be managed through:
- Environment variables
- `background/utils/config.py`
- Task-specific config files

Example `.env`:
```
BATCH_SIZE=100
CRAWL_TIMEOUT=30
INDEX_BATCH_ENABLED=true
LOG_LEVEL=INFO
```

## Contributing

When adding new background tasks:
1. Choose the appropriate directory based on the task type
2. Create a new module with clear, documented functions/classes
3. Add unit tests in a `tests/` subdirectory
4. Update this README with new functionality

## Testing

```bash
# Run tests for background tasks
python -m pytest background/

# Run specific module tests
python -m pytest background/scripts/test_initialize_db.py

# With coverage
python -m pytest background/ --cov=background
```
