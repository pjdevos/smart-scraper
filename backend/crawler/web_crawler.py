"""
Web Crawler - Automatic URL Discovery
Discovers URLs by following links with sitemap support
"""
import re
import time
import requests
from typing import List, Optional, Callable, Set, Dict
from urllib.parse import urljoin, urlparse, urlunparse
from collections import deque
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from utils.logger import get_logger
from utils.helpers import get_domain
from backend.stealth.robots_parser import RobotsParser

logger = get_logger(__name__)


class WebCrawler:
    """Discovers URLs by following links with sitemap support"""

    def __init__(
        self,
        respect_robots: bool = True,
        request_delay: float = 2.0,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ):
        """
        Initialize web crawler.

        Args:
            respect_robots: Respect robots.txt rules
            request_delay: Delay between requests (seconds)
            user_agent: User agent string
        """
        self.respect_robots = respect_robots
        self.request_delay = request_delay
        self.user_agent = user_agent
        self.robots_parser = RobotsParser(respect_robots)
        self.session = requests.Session()
        self.session.headers['User-Agent'] = user_agent

        # State
        self.seen_urls: Set[str] = set()
        self.matched_urls: List[str] = []
        self.paused = False
        self.stopped = False

    def crawl(
        self,
        start_url: str,
        max_pages: int = 500,
        max_depth: int = 3,
        pattern: Optional[str] = None,
        internal_only: bool = True,
        try_sitemap: bool = True,
        follow_pagination: bool = False,
        callback: Optional[Callable[[Dict], None]] = None
    ) -> List[str]:
        """
        Crawl website to discover URLs.

        Args:
            start_url: Starting URL
            max_pages: Maximum pages to crawl
            max_depth: Maximum link depth
            pattern: Regex pattern for URL filtering (None = all URLs)
            internal_only: Only follow internal links
            try_sitemap: Try sitemap.xml first
            follow_pagination: Follow pagination links
            callback: Progress callback (receives stats dict)

        Returns:
            List of discovered URLs matching pattern
        """
        logger.info(f"Starting crawl from {start_url}")
        logger.info(f"Max pages: {max_pages}, Max depth: {max_depth}, Pattern: {pattern}")

        # Reset state
        self.seen_urls.clear()
        self.matched_urls.clear()
        self.paused = False
        self.stopped = False

        # Try sitemap first (much faster!)
        if try_sitemap:
            sitemap_urls = self._try_sitemap(start_url, pattern)
            if sitemap_urls:
                logger.info(f"Found {len(sitemap_urls)} URLs from sitemap.xml")
                self.matched_urls = sitemap_urls[:max_pages]
                if callback:
                    callback({
                        'found': len(sitemap_urls),
                        'crawled': 0,
                        'matched': len(self.matched_urls),
                        'source': 'sitemap'
                    })
                return self.matched_urls

        # Compile pattern if provided
        pattern_regex = re.compile(pattern) if pattern else None

        # BFS queue: (url, depth)
        queue = deque([(start_url, 0)])
        self.seen_urls.add(start_url)
        crawled_count = 0
        base_domain = get_domain(start_url)

        while queue and crawled_count < max_pages and not self.stopped:
            # Handle pause
            while self.paused and not self.stopped:
                time.sleep(0.1)

            if self.stopped:
                break

            current_url, depth = queue.popleft()

            # Check if allowed by robots.txt
            if not self.robots_parser.can_fetch(current_url, self.user_agent):
                logger.warning(f"Robots.txt blocks {current_url}")
                continue

            # Check depth limit
            if max_depth != -1 and depth > max_depth:
                continue

            try:
                # Fetch page
                logger.debug(f"Crawling {current_url} (depth {depth})")
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                crawled_count += 1

                # Extract links
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)

                for link in links:
                    href = link['href']
                    absolute_url = urljoin(current_url, href)
                    absolute_url = self._normalize_url(absolute_url)

                    # Skip if already seen
                    if absolute_url in self.seen_urls:
                        continue

                    # Check internal only
                    if internal_only and not self._is_internal(absolute_url, base_domain):
                        continue

                    # Check pagination
                    if not follow_pagination and self._is_pagination(href):
                        continue

                    # Mark as seen
                    self.seen_urls.add(absolute_url)

                    # Check pattern match
                    if pattern_regex is None or pattern_regex.search(absolute_url):
                        if absolute_url not in self.matched_urls:
                            self.matched_urls.append(absolute_url)
                            logger.debug(f"Matched: {absolute_url}")

                    # Add to queue for further crawling
                    if depth < max_depth or max_depth == -1:
                        queue.append((absolute_url, depth + 1))

                # Progress callback
                if callback:
                    callback({
                        'found': len(self.seen_urls),
                        'crawled': crawled_count,
                        'matched': len(self.matched_urls),
                        'queue_size': len(queue)
                    })

                # Rate limiting
                time.sleep(self.request_delay)

            except Exception as e:
                logger.warning(f"Failed to crawl {current_url}: {e}")
                continue

        logger.info(f"Crawl complete. Found {len(self.matched_urls)} matching URLs")
        return self.matched_urls

    def _try_sitemap(self, start_url: str, pattern: Optional[str] = None) -> List[str]:
        """
        Try to parse sitemap.xml.

        Args:
            start_url: Starting URL
            pattern: Regex pattern for filtering

        Returns:
            List of URLs from sitemap
        """
        parsed = urlparse(start_url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"

        try:
            logger.info(f"Trying sitemap at {sitemap_url}")
            response = self.session.get(sitemap_url, timeout=10)
            response.raise_for_status()

            # Parse XML
            root = ET.fromstring(response.content)

            # Handle different sitemap formats
            urls = []

            # Standard sitemap
            for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                url = url_elem.text
                if url:
                    urls.append(url)

            # Sitemap index (contains other sitemaps)
            if not urls:
                for sitemap_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
                    loc = sitemap_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc is not None and loc.text:
                        # Recursively fetch sub-sitemap
                        sub_urls = self._fetch_sitemap_urls(loc.text)
                        urls.extend(sub_urls)

            # Apply pattern filter
            if pattern:
                pattern_regex = re.compile(pattern)
                urls = [url for url in urls if pattern_regex.search(url)]

            logger.info(f"Extracted {len(urls)} URLs from sitemap")
            return urls

        except Exception as e:
            logger.debug(f"Failed to parse sitemap: {e}")
            return []

    def _fetch_sitemap_urls(self, sitemap_url: str) -> List[str]:
        """Fetch URLs from a specific sitemap"""
        try:
            response = self.session.get(sitemap_url, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)

            urls = []
            for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                if url_elem.text:
                    urls.append(url_elem.text)

            return urls
        except Exception as e:
            logger.warning(f"Failed to fetch sitemap {sitemap_url}: {e}")
            return []

    def _is_internal(self, url: str, base_domain: str) -> bool:
        """Check if URL is internal to base domain"""
        url_domain = get_domain(url)
        return url_domain == base_domain

    def _is_pagination(self, href: str) -> bool:
        """Detect pagination links"""
        pagination_patterns = [
            r'page=\d+',
            r'/page/\d+',
            r'\?p=\d+',
            r'/p\d+',
            r'offset=\d+',
            r'start=\d+'
        ]
        return any(re.search(pattern, href, re.IGNORECASE) for pattern in pagination_patterns)

    def _normalize_url(self, url: str) -> str:
        """
        Normalize URL (remove fragments, sort query params).

        Args:
            url: URL to normalize

        Returns:
            Normalized URL
        """
        parsed = urlparse(url)

        # Remove fragment
        parsed = parsed._replace(fragment='')

        # Rebuild URL
        normalized = urlunparse(parsed)

        return normalized

    def _matches_pattern(self, url: str, pattern: str) -> bool:
        """
        Check if URL matches regex pattern.

        Args:
            url: URL to check
            pattern: Regex pattern

        Returns:
            True if matches
        """
        try:
            return bool(re.search(pattern, url))
        except re.error:
            logger.error(f"Invalid regex pattern: {pattern}")
            return False

    def pause(self):
        """Pause crawling"""
        self.paused = True
        logger.info("Crawler paused")

    def resume(self):
        """Resume crawling"""
        self.paused = False
        logger.info("Crawler resumed")

    def stop(self):
        """Stop crawling"""
        self.stopped = True
        logger.info("Crawler stopped")
