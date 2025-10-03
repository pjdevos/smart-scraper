"""
Category Tree Crawler - Recursively crawl category hierarchies
"""
import time
import random
from typing import Dict, List, Set, Optional
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
import csv
from pathlib import Path

from bs4 import BeautifulSoup
import requests

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Category:
    """Represents a category in the tree"""
    name: str
    url: str
    level: int
    parent_path: List[str]

    @property
    def full_path(self) -> str:
        """Get full hierarchical path"""
        return " > ".join(self.parent_path + [self.name])

    @property
    def depth(self) -> int:
        """Get depth in tree"""
        return len(self.parent_path) + 1


class CategoryTreeCrawler:
    """
    Crawls website category trees with rate limiting and hierarchy extraction.

    Features:
    - Recursive link following
    - Breadcrumb extraction
    - Rate limiting with exponential backoff
    - 429 handling with Retry-After
    - CSV export with hierarchical structure
    """

    def __init__(
        self,
        base_url: str,
        start_paths: List[str] = None,
        path_patterns: List[str] = None,
        max_depth: int = 5,
        requests_per_minute: int = 20,
        timeout: int = 30
    ):
        """
        Initialize crawler.

        Args:
            base_url: Base website URL (e.g., "https://www.pricerunner.com")
            start_paths: Starting paths to crawl (e.g., ["/t/", "/"])
            path_patterns: URL patterns to follow (e.g., ["/t/", "/cl/"])
            max_depth: Maximum depth to crawl
            requests_per_minute: Rate limit
            timeout: Request timeout
        """
        self.base_url = base_url.rstrip('/')
        self.start_paths = start_paths or ["/"]
        self.path_patterns = path_patterns or ["/t/", "/cl/"]
        self.max_depth = max_depth
        self.timeout = timeout

        # Rate limiting
        self.min_delay = 60.0 / requests_per_minute  # Minimum delay between requests
        self.max_delay = 30.0  # Maximum delay
        self.last_request_time = 0

        # Tracking
        self.visited_urls: Set[str] = set()
        self.categories: List[Category] = []

        # Session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def _wait_with_rate_limit(self):
        """Wait to respect rate limiting with jitter"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed
            jitter = random.uniform(0, sleep_time * 0.1)  # Add 10% jitter
            time.sleep(sleep_time + jitter)

    def _fetch_with_retry(self, url: str, max_retries: int = 5) -> Optional[str]:
        """
        Fetch URL with exponential backoff on 429.

        Args:
            url: URL to fetch
            max_retries: Maximum retry attempts

        Returns:
            HTML content or None
        """
        retry_count = 0
        backoff = 1.0

        while retry_count < max_retries:
            self._wait_with_rate_limit()

            try:
                logger.info(f"Fetching: {url}")
                response = self.session.get(url, timeout=self.timeout)
                self.last_request_time = time.time()

                if response.status_code == 200:
                    return response.text

                elif response.status_code == 429:
                    # Rate limited - check Retry-After header
                    retry_after = response.headers.get('Retry-After')
                    if retry_after:
                        wait_time = int(retry_after)
                    else:
                        wait_time = backoff * (2 ** retry_count)  # Exponential backoff

                    logger.warning(f"Rate limited (429). Waiting {wait_time}s before retry {retry_count + 1}/{max_retries}")
                    time.sleep(wait_time)
                    retry_count += 1

                else:
                    logger.error(f"HTTP {response.status_code} for {url}")
                    return None

            except requests.RequestException as e:
                logger.error(f"Request error for {url}: {e}")
                return None

        logger.error(f"Max retries exceeded for {url}")
        return None

    def _extract_breadcrumbs(self, soup: BeautifulSoup) -> List[str]:
        """
        Extract breadcrumb path from page.

        Args:
            soup: BeautifulSoup object

        Returns:
            List of category names in hierarchy
        """
        breadcrumbs = []

        # Common breadcrumb selectors
        selectors = [
            'nav[aria-label="breadcrumb"] a',
            '.breadcrumb a',
            '[itemtype="https://schema.org/BreadcrumbList"] a',
            'ol.breadcrumb a',
            '.breadcrumbs a'
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                breadcrumbs = [elem.get_text(strip=True) for elem in elements]
                # Remove "Home" or similar
                breadcrumbs = [b for b in breadcrumbs if b.lower() not in ['home', 'start', '']]
                break

        return breadcrumbs

    def _extract_category_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """
        Extract category links from page.

        Args:
            soup: BeautifulSoup object
            current_url: Current page URL

        Returns:
            List of absolute category URLs
        """
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']

            # Check if link matches our patterns
            if any(pattern in href for pattern in self.path_patterns):
                # Convert to absolute URL
                absolute_url = urljoin(current_url, href)

                # Remove query parameters and fragments
                parsed = urlparse(absolute_url)
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

                # Only include if from same domain
                if parsed.netloc == urlparse(self.base_url).netloc:
                    links.append(clean_url)

        return list(set(links))  # Remove duplicates

    def _extract_category_name(self, soup: BeautifulSoup, url: str) -> str:
        """
        Extract category name from page.

        Args:
            soup: BeautifulSoup object
            url: Page URL

        Returns:
            Category name
        """
        # Try various selectors
        selectors = ['h1', '.page-title', '.category-title', 'title']

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                name = element.get_text(strip=True)
                # Clean up title tags
                name = name.replace(' - PriceRunner', '').replace('PriceRunner', '').strip()
                if name:
                    return name

        # Fallback: extract from URL
        path = urlparse(url).path
        parts = [p for p in path.split('/') if p]
        if parts:
            return parts[-1].replace('-', ' ').title()

        return "Unknown"

    def _crawl_url(self, url: str, parent_path: List[str], depth: int):
        """
        Recursively crawl a URL.

        Args:
            url: URL to crawl
            parent_path: Parent category path
            depth: Current depth
        """
        # Check depth limit
        if depth > self.max_depth:
            return

        # Check if already visited
        if url in self.visited_urls:
            return

        self.visited_urls.add(url)

        # Fetch page
        html = self._fetch_with_retry(url)
        if not html:
            return

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Extract category name
        category_name = self._extract_category_name(soup, url)

        # Extract breadcrumbs (more reliable than title)
        breadcrumbs = self._extract_breadcrumbs(soup)
        if breadcrumbs:
            # Use breadcrumbs to build path
            if len(breadcrumbs) > depth:
                parent_path = breadcrumbs[:-1]
                category_name = breadcrumbs[-1]

        # Create category
        category = Category(
            name=category_name,
            url=url,
            level=depth,
            parent_path=parent_path.copy()
        )
        self.categories.append(category)

        logger.info(f"[Depth {depth}] {category.full_path}")

        # Extract links
        links = self._extract_category_links(soup, url)
        logger.info(f"Found {len(links)} category links")

        # Crawl child categories
        new_parent_path = parent_path + [category_name]
        for link in links:
            self._crawl_url(link, new_parent_path, depth + 1)

    def crawl(self) -> List[Category]:
        """
        Start crawling from configured start paths.

        Returns:
            List of discovered categories
        """
        logger.info(f"Starting category tree crawl: {self.base_url}")
        logger.info(f"Start paths: {self.start_paths}")
        logger.info(f"Path patterns: {self.path_patterns}")
        logger.info(f"Max depth: {self.max_depth}")
        logger.info(f"Rate limit: {60.0/self.min_delay:.1f} requests/min")

        for start_path in self.start_paths:
            start_url = self.base_url + start_path
            logger.info(f"Crawling from: {start_url}")
            self._crawl_url(start_url, [], 1)

        logger.info(f"Crawl complete. Discovered {len(self.categories)} categories")
        return self.categories

    def export_to_csv(self, output_path: Path):
        """
        Export categories to CSV with hierarchical structure.

        Args:
            output_path: Output CSV file path
        """
        if not self.categories:
            logger.warning("No categories to export")
            return

        # Find max depth
        max_depth = max(cat.depth for cat in self.categories)

        # Prepare headers
        headers = [f"level_{i}" for i in range(1, max_depth + 1)]
        headers += ["depth", "full_path", "url"]

        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow(headers)

            for category in sorted(self.categories, key=lambda c: (c.depth, c.full_path)):
                row = []

                # Fill level columns
                path_parts = category.parent_path + [category.name]
                for i in range(max_depth):
                    if i < len(path_parts):
                        row.append(path_parts[i])
                    else:
                        row.append('')

                # Add metadata
                row.append(category.depth)
                row.append(category.full_path)
                row.append(category.url)

                writer.writerow(row)

        logger.info(f"Exported {len(self.categories)} categories to {output_path}")
