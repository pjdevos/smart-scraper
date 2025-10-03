"""
Base Scraper Abstract Class
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseScraper(ABC):
    """Abstract base class for all scrapers"""

    def __init__(self, timeout: int = 30):
        """
        Initialize base scraper.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.logger = logger

    @abstractmethod
    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from URL.

        Args:
            url: Target URL

        Returns:
            HTML content or None on error
        """
        pass

    @abstractmethod
    def close(self):
        """Clean up resources"""
        pass

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()