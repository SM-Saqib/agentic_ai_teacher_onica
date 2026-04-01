"""Base Crawler - Foundation for web crawling utilities"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import httpx
from datetime import datetime
from background.utils.logger import get_logger

logger = get_logger(__name__)


class BaseCrawler(ABC):
    """Abstract base class for web crawlers"""
    
    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize crawler
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            headers: Custom HTTP headers
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = headers or self._default_headers()
        self.logger = logger
    
    def _default_headers(self) -> Dict[str, str]:
        """Get default HTTP headers"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def fetch(self, url: str) -> Optional[str]:
        """
        Fetch content from URL with retries
        
        Args:
            url: URL to fetch
            
        Returns:
            Response content or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, headers=self.headers)
                    response.raise_for_status()
                    return response.text
            except httpx.HTTPError as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == self.max_retries - 1:
                    self.logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
                    return None
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {e}")
                return None
    
    @abstractmethod
    async def parse(self, content: str) -> Dict:
        """
        Parse fetched content
        
        Args:
            content: Raw content to parse
            
        Returns:
            Parsed data
        """
        pass
    
    @abstractmethod
    async def crawl(self, url: str) -> Optional[Dict]:
        """
        Crawl a single URL and extract data
        
        Args:
            url: URL to crawl
            
        Returns:
            Extracted data or None if failed
        """
        pass
    
    async def crawl_batch(self, urls: List[str]) -> List[Dict]:
        """
        Crawl multiple URLs
        
        Args:
            urls: List of URLs to crawl
            
        Returns:
            List of extracted data
        """
        results = []
        for url in urls:
            self.logger.info(f"Crawling: {url}")
            try:
                data = await self.crawl(url)
                if data:
                    results.append(data)
            except Exception as e:
                self.logger.error(f"Error crawling {url}: {e}")
                continue
        
        return results
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc


class CrawlResult:
    """Result of a crawl operation"""
    
    def __init__(self, url: str, title: str = "", content: str = "", metadata: Dict = None):
        self.url = url
        self.title = title
        self.content = content
        self.metadata = metadata or {}
        self.crawled_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata,
            "crawled_at": self.crawled_at,
        }
