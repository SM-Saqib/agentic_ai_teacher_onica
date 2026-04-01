"""Configuration for background tasks"""
import os
from typing import Optional


class BackgroundConfig:
    """Configuration management for background tasks"""
    
    # Crawling settings
    CRAWL_TIMEOUT: int = int(os.getenv("CRAWL_TIMEOUT", "30"))
    CRAWL_MAX_RETRIES: int = int(os.getenv("CRAWL_MAX_RETRIES", "3"))
    CRAWL_BATCH_SIZE: int = int(os.getenv("CRAWL_BATCH_SIZE", "10"))
    
    # Indexing settings
    INDEX_BATCH_SIZE: int = int(os.getenv("INDEX_BATCH_SIZE", "100"))
    INDEX_ENABLED: bool = os.getenv("INDEX_ENABLED", "true").lower() == "true"
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Vector store settings
    VECTOR_STORE_TYPE: str = os.getenv("VECTOR_STORE_TYPE", "chromadb")
    VECTOR_STORE_HOST: str = os.getenv("VECTOR_STORE_HOST", "localhost")
    VECTOR_STORE_PORT: int = int(os.getenv("VECTOR_STORE_PORT", "8000"))
    
    # Processing settings
    PROCESS_TIMEOUT: int = int(os.getenv("PROCESS_TIMEOUT", "300"))  # 5 minutes
    PROCESS_MAX_WORKERS: int = int(os.getenv("PROCESS_MAX_WORKERS", "4"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE", None)
    
    # Data paths
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    CACHE_DIR: str = os.getenv("CACHE_DIR", "./data/cache")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./data/output")
    
    @classmethod
    def to_dict(cls) -> dict:
        """Convert configuration to dictionary"""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("Background Configuration:")
        print("-" * 50)
        for key, value in cls.to_dict().items():
            print(f"{key}: {value}")
        print("-" * 50)
