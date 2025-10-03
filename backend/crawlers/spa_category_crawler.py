"""
SPA Category Tree Crawler
Async crawler for Single Page Applications with API interception
"""
import asyncio
import json
import time
import random
from typing import Dict, List, Set, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse, parse_qs
import csv

try:
    import httpx
except ImportError:
    raise ImportError("httpx required: pip install httpx")

from playwright.async_api import async_playwright, Route, Request, Page
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Category:
    """Category with hierarchy"""
    id: str
    name: str
    url: str
    level: int
    parent_ids: List[str] = field(default_factory=list)
    parent_names: List[str] = field(default_factory=list)

    @property
    def full_path(self) -> str:
        return " > ".join(self.parent_names + [self.name])

    @property
    def depth(self) -> int:
        return len(self.parent_ids) + 1


class SPACategoryCrawler:
    """
    Crawls SPA category trees via API interception.

    Strategy:
    1. Use Playwright to navigate and intercept XHR/Fetch
    2. Extract API endpoints and patterns
    3. Switch to async httpx for fast API crawling
    4. Fallback to Playwright for JS-rendered pages
    """

    def __init__(
        self,
        base_url: str,
        headless: bool = True,
        max_depth: int = 5,
        requests_per_second: float = 0.5,
        timeout: int = 30
    ):
        """
        Initialize crawler.

        Args:
            base_url: Base website URL
            headless: Run browser headless
            max_depth: Maximum category depth
            requests_per_second: Rate limit (QPS)
            timeout: Request timeout
        """
        self.base_url = base_url.rstrip('/')
        self.headless = headless
        self.max_depth = max_depth
        self.timeout = timeout

        # Rate limiting
        self.min_delay = 1.0 / requests_per_second
        self.last_request_time = 0

        # Tracking
        self.categories: List[Category] = []
        self.seen_category_ids: Set[str] = set()
        self.seen_product_ids: Set[str] = set()

        # API patterns discovered during recon
        self.api_endpoints: Dict[str, str] = {}
        self.api_headers: Dict[str, str] = {}

    async def _rate_limit(self):
        """Async rate limiting with jitter"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            sleep_time = self.min_delay - elapsed
            jitter = random.uniform(0, sleep_time * 0.1)
            await asyncio.sleep(sleep_time + jitter)
        self.last_request_time = time.time()

    async def _fetch_json_with_retry(
        self,
        client: httpx.AsyncClient,
        url: str,
        params: Dict = None,
        max_retries: int = 5
    ) -> Optional[Dict]:
        """
        Fetch JSON with exponential backoff.

        Args:
            client: HTTP client
            url: URL to fetch
            params: Query parameters
            max_retries: Max retry attempts

        Returns:
            JSON response or None
        """
        retry_count = 0

        while retry_count < max_retries:
            await self._rate_limit()

            try:
                response = await client.get(
                    url,
                    params=params,
                    headers=self.api_headers,
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    return response.json()

                elif response.status_code == 429:
                    retry_after = response.headers.get('Retry-After', '5')
                    wait_time = float(retry_after)
                    logger.warning(f"Rate limited (429). Waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                    retry_count += 1

                elif response.status_code == 503:
                    backoff = 2 ** retry_count
                    logger.warning(f"Service unavailable (503). Backoff {backoff}s")
                    await asyncio.sleep(backoff)
                    retry_count += 1

                else:
                    logger.error(f"HTTP {response.status_code} for {url}")
                    return None

            except Exception as e:
                logger.error(f"Request error: {e}")
                retry_count += 1
                await asyncio.sleep(2 ** retry_count)

        logger.error(f"Max retries exceeded for {url}")
        return None

    async def _intercept_api_calls(self, route: Route, request: Request):
        """Intercept XHR/Fetch to discover API patterns"""
        # Block analytics/tracking to speed up
        BLOCK_DOMAINS = (
            "taboola.com", "doubleclick.net", "google-analytics.com",
            "googletagmanager.com", "facebook.net", "adservice.google"
        )

        if any(blocked in request.url for blocked in BLOCK_DOMAINS):
            await route.abort()
            return

        if request.resource_type in ("xhr", "fetch"):
            url = request.url

            # Log API call
            logger.debug(f"API: [{request.method}] {url}")

            # Extract patterns
            if "/api/" in url or ".json" in url:
                parsed = urlparse(url)

                # Store base patterns
                if "category" in url.lower() or "/cat" in url:
                    self.api_endpoints["categories"] = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

                if "product" in url.lower():
                    self.api_endpoints["products"] = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

                # Store headers
                for key in ["accept", "accept-language", "x-api-key", "x-locale"]:
                    if key in request.headers:
                        self.api_headers[key] = request.headers[key]

        await route.fallback()

    async def _discover_api_with_playwright(self) -> Dict[str, Any]:
        """
        Use Playwright to discover API endpoints.

        Returns:
            Dictionary with API patterns and headers
        """
        logger.info("Starting API reconnaissance with Playwright...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                locale="en-GB",
                viewport={"width": 1920, "height": 1080}
            )
            page = await context.new_page()

            # Setup interception
            await page.route("**/*", self._intercept_api_calls)

            # Navigate and explore
            logger.info(f"Loading {self.base_url}...")
            await page.goto(self.base_url, wait_until="networkidle")
            await asyncio.sleep(2)

            # Click on categories
            try:
                category_links = await page.locator('a[href*="/cl/"], a[href*="/t/"]').all()
                if category_links:
                    logger.info(f"Found {len(category_links)} category links, clicking first...")
                    await category_links[0].click()
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(2)
            except Exception as e:
                logger.warning(f"Category click failed: {e}")

            await browser.close()

        logger.info(f"Discovered {len(self.api_endpoints)} API endpoints")
        logger.info(f"Endpoints: {list(self.api_endpoints.keys())}")

        return {
            "endpoints": self.api_endpoints,
            "headers": self.api_headers
        }

    async def _crawl_with_playwright_fallback(self, url: str) -> List[Category]:
        """
        Fallback: crawl via DOM rendering when API unavailable.

        Args:
            url: URL to crawl

        Returns:
            List of categories extracted from DOM
        """
        logger.info(f"Using Playwright fallback for {url}")

        categories = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            page = await browser.new_page()

            await page.goto(url, wait_until="networkidle")

            # Scroll to trigger lazy loading
            for i in range(5):
                await page.mouse.wheel(0, 4000)
                await asyncio.sleep(1.5)

            # Extract category elements
            # Adjust selectors based on actual PriceRunner DOM structure
            selectors = [
                'a[href*="/cl/"]',
                'a[href*="/t/"]',
                '[data-category-id]',
                '.category-link'
            ]

            for selector in selectors:
                elements = await page.locator(selector).all()
                if elements:
                    logger.info(f"Found {len(elements)} elements with selector: {selector}")

                    for elem in elements[:50]:  # Limit to prevent overload
                        try:
                            href = await elem.get_attribute('href')
                            text = await elem.inner_text()
                            cat_id = await elem.get_attribute('data-category-id')

                            if not cat_id:
                                # Extract ID from URL
                                if href and '/cl/' in href:
                                    cat_id = href.split('/cl/')[-1].split('/')[0]
                                elif href and '/t/' in href:
                                    cat_id = href.split('/t/')[-1].split('/')[0]

                            if cat_id and cat_id not in self.seen_category_ids:
                                self.seen_category_ids.add(cat_id)
                                category = Category(
                                    id=cat_id,
                                    name=text.strip(),
                                    url=urljoin(self.base_url, href) if href else url,
                                    level=1
                                )
                                categories.append(category)

                        except Exception as e:
                            logger.warning(f"Element extraction error: {e}")

                    break  # Stop after first working selector

            await browser.close()

        return categories

    async def crawl(self) -> List[Category]:
        """
        Start crawling.

        Returns:
            List of discovered categories
        """
        logger.info(f"Starting SPA category crawl: {self.base_url}")
        logger.info(f"Max depth: {self.max_depth}, QPS: {1/self.min_delay:.2f}")

        # Step 1: Discover API endpoints
        await self._discover_api_with_playwright()

        # Step 2: If API endpoints found, use httpx; else fallback to Playwright
        if self.api_endpoints:
            logger.info("Using API-based crawling...")
            # TODO: Implement API crawling once endpoints are known
            # For now, this would require specific API endpoint knowledge
            logger.warning("API crawling not yet implemented - falling back to DOM")
            self.categories = await self._crawl_with_playwright_fallback(self.base_url)
        else:
            logger.info("No API endpoints found - using DOM rendering fallback")
            self.categories = await self._crawl_with_playwright_fallback(self.base_url)

        logger.info(f"Crawl complete. Discovered {len(self.categories)} categories")
        return self.categories

    def export_to_csv(self, output_path: Path):
        """
        Export to CSV with hierarchical structure.

        Args:
            output_path: Output file path
        """
        if not self.categories:
            logger.warning("No categories to export")
            return

        max_depth = max((cat.depth for cat in self.categories), default=1)

        headers = [f"level_{i}" for i in range(1, max_depth + 1)]
        headers += ["depth", "full_path", "url", "category_id"]

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow(headers)

            for category in sorted(self.categories, key=lambda c: (c.depth, c.full_path)):
                row = []

                # Fill level columns
                path_parts = category.parent_names + [category.name]
                for i in range(max_depth):
                    row.append(path_parts[i] if i < len(path_parts) else '')

                row.extend([
                    category.depth,
                    category.full_path,
                    category.url,
                    category.id
                ])

                writer.writerow(row)

        logger.info(f"Exported {len(self.categories)} categories to {output_path}")
