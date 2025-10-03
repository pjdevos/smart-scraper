"""
Requests-based Scraper (for static HTML sites)
"""
import requests
from typing import Optional
from config.settings import DEFAULT_TIMEOUT, USER_AGENT, MAX_RETRIES
from .base_scraper import BaseScraper
from utils.logger import get_logger

logger = get_logger(__name__)


class RequestsScraper(BaseScraper):
    """Fast scraper for static HTML pages using requests library"""

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize requests scraper.

        Args:
            timeout: Request timeout in seconds
        """
        super().__init__(timeout)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch HTML content using requests.

        Args:
            url: Target URL

        Returns:
            HTML content or None on error
        """
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Fetching {url} with requests (attempt {attempt + 1}/{MAX_RETRIES})")

                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )

                response.raise_for_status()
                logger.info(f"Successfully fetched {url} ({len(response.text)} chars)")
                return response.text

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout fetching {url} (attempt {attempt + 1})")
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
                    return None

            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error fetching {url}: {e}")
                return None

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error fetching {url}: {e}")
                return None

            except Exception as e:
                logger.error(f"Unexpected error fetching {url}: {e}")
                return None

        return None

    def close(self):
        """Close session"""
        self.session.close()
        logger.debug("Requests session closed")