"""Logging Utilities for Background Tasks"""
import logging
import sys
from typing import Optional
import os

# Get log level from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name (usually __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level or LOG_LEVEL)
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level or LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler if not already present
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger


class TaskLogger:
    """Context manager for logging tasks"""
    
    def __init__(self, logger: logging.Logger, task_name: str):
        self.logger = logger
        self.task_name = task_name
    
    def __enter__(self):
        self.logger.info(f"Starting task: {self.task_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.logger.info(f"Completed task: {self.task_name}")
        else:
            self.logger.error(f"Failed task: {self.task_name} - {exc_val}")
        return False
