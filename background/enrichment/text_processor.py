"""Text Processing Utilities for Data Enrichment"""
import re
from typing import List, Optional
from background.utils.logger import get_logger

logger = get_logger(__name__)


class TextProcessor:
    """Base text processor for cleaning and processing content"""
    
    def __init__(self):
        self.logger = logger
    
    def clean(self, text: str) -> str:
        """
        Clean text by removing extra whitespace, special characters, etc.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove control characters but keep newlines
        text = ''.join(ch if ch.isprintable() or ch in '\n\t\r' else '' for ch in text)
        
        return text
    
    def remove_html_tags(self, text: str) -> str:
        """Remove HTML tags from text"""
        return re.sub(r'<[^>]+>', '', text)
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Text to split into sentences
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting on period, question mark, exclamation
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_paragraphs(self, text: str) -> List[str]:
        """
        Extract paragraphs from text
        
        Args:
            text: Text to split into paragraphs
            
        Returns:
            List of paragraphs
        """
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    def truncate(self, text: str, max_length: int = 1000, suffix: str = "...") -> str:
        """
        Truncate text to maximum length
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text"""
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        return '\n'.join(line for line in lines if line)
    
    def lowercase(self, text: str) -> str:
        """Convert text to lowercase"""
        return text.lower()
    
    def process_pipeline(
        self,
        text: str,
        remove_html: bool = True,
        remove_urls: bool = True,
        normalize: bool = True,
        lowercase_text: bool = False,
    ) -> str:
        """
        Apply multiple processing steps in sequence
        
        Args:
            text: Text to process
            remove_html: Remove HTML tags
            remove_urls: Remove URLs
            normalize: Normalize whitespace
            lowercase_text: Convert to lowercase
            
        Returns:
            Processed text
        """
        if remove_html:
            text = self.remove_html_tags(text)
        
        if remove_urls:
            text = self.remove_urls(text)
        
        if normalize:
            text = self.normalize_whitespace(text)
        
        if lowercase_text:
            text = self.lowercase(text)
        
        text = self.clean(text)
        
        return text
