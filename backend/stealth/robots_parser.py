"""
Robots.txt Parser - Respects website scraping rules
"""
import requests
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from typing import Optional
from utils.logger import get_logger
from utils.helpers import get_domain

logger = get_logger(__name__)


class RobotsParser:
    """Parse and respect robots.txt rules"""

    def __init__(self, respect_robots: bool = True):
        """
        Initialize robots parser.

        Args:
            respect_robots: Whether to respect robots.txt
        """
        self.respect_robots = respect_robots
        self.parsers = {}  # Cache parsers per domain

    def can_fetch(self, url: str, user_agent: str = "*") -> bool:
        """
        Check if URL can be fetched according to robots.txt.

        Args:
            url: Target URL
            user_agent: User agent to check for

        Returns:
            True if allowed to fetch
        """
        if not self.respect_robots:
            return True

        domain = get_domain(url)

        # Get or create parser for domain
        if domain not in self.parsers:
            self._load_robots(url)

        # Check if allowed
        parser = self.parsers.get(domain)
        if parser is None:
            # No robots.txt or failed to load - allow
            return True

        allowed = parser.can_fetch(user_agent, url)

        if not allowed:
            logger.warning(f"robots.txt disallows fetching {url}")

        return allowed

    def _load_robots(self, url: str):
        """Load robots.txt for domain"""
        domain = get_domain(url)
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        try:
            logger.info(f"Loading robots.txt from {robots_url}")

            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.read()

            self.parsers[domain] = parser
            logger.info(f"Loaded robots.txt for {domain}")

        except Exception as e:
            logger.warning(f"Failed to load robots.txt for {domain}: {e}")
            # Set to None to indicate we tried and failed
            self.parsers[domain] = None

    def get_crawl_delay(self, url: str, user_agent: str = "*") -> Optional[float]:
        """
        Get crawl delay from robots.txt.

        Args:
            url: Target URL
            user_agent: User agent to check for

        Returns:
            Crawl delay in seconds or None
        """
        if not self.respect_robots:
            return None

        domain = get_domain(url)

        if domain not in self.parsers:
            self._load_robots(url)

        parser = self.parsers.get(domain)
        if parser is None:
            return None

        try:
            delay = parser.crawl_delay(user_agent)
            if delay:
                logger.info(f"robots.txt specifies crawl delay of {delay}s for {domain}")
                return float(delay)
        except Exception:
            pass

        return None