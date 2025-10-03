"""
Scraper Engine - Main Orchestrator

This is the core of SmartScraper. It orchestrates the entire scraping pipeline:
1. Cache Check
2. Learned Selectors Check
3. Simple Extraction (regex)
4. LLM Analysis (if needed)
"""
from typing import Dict, List, Optional, Callable
from enum import Enum
import time
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from utils.logger import get_logger
from utils.budget_manager import BudgetManager
from backend.storage import CacheManager, SelectorManager
from backend.scrapers import RequestsScraper, SeleniumScraper, PlaywrightScraper
from backend.scrapers.stealth_playwright_scraper import StealthPlaywrightScraper
from backend.scrapers.adaptive_scraper import AdaptiveScraper
from backend.extractors import RegexExtractor, BS4Extractor, SmartExtractor
from backend.llm import ClaudeClient

logger = get_logger(__name__)


class ScrapingMethod(Enum):
    """Scraping method options"""
    AUTO = "auto"
    REQUESTS = "requests"
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"
    STEALTH = "stealth"


class StealthLevel(Enum):
    """Stealth level options"""
    BASIC = "basic"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"


class ScraperEngine:
    """Main scraping orchestrator"""

    def __init__(
        self,
        api_key: str = None,
        daily_budget: float = 5.0,
        progress_callback: Callable[[str, int], None] = None,
        stealth_level: str = "medium",
        use_proxies: bool = False,
        respect_robots: bool = True
    ):
        """
        Initialize scraper engine.

        Args:
            api_key: Anthropic API key
            daily_budget: Daily budget limit
            progress_callback: Callback for progress updates (message, percentage)
            stealth_level: Stealth level (basic, medium, high, maximum)
            use_proxies: Use proxy rotation
            respect_robots: Respect robots.txt rules
        """
        self.cache_manager = CacheManager()
        self.selector_manager = SelectorManager()
        self.budget_manager = BudgetManager(daily_budget)
        self.stealth_level = stealth_level
        self.use_proxies = use_proxies
        self.respect_robots = respect_robots

        try:
            self.claude_client = ClaudeClient(api_key, self.budget_manager)
        except ValueError as e:
            logger.error(f"Failed to initialize Claude client: {e}")
            self.claude_client = None

        self.smart_extractor = SmartExtractor(self.claude_client) if self.claude_client else None

        self.progress_callback = progress_callback

        self.total_cost = 0.0
        self.cached_count = 0
        self.learned_count = 0
        self.llm_count = 0

    def _update_progress(self, message: str, percentage: int = 0):
        """Update progress via callback"""
        logger.info(f"Progress: {message} ({percentage}%)")
        if self.progress_callback:
            self.progress_callback(message, percentage)

    def _detect_javascript(self, html: str) -> bool:
        """
        Detect if page requires JavaScript rendering.

        Args:
            html: HTML content

        Returns:
            True if JavaScript is likely required
        """
        # Simple heuristic: check for common JS framework indicators
        js_indicators = [
            'react',
            'angular',
            'vue',
            'next.js',
            'nuxt',
            '__NEXT_DATA__',
            'ng-app',
            'v-app',
            'data-reactroot'
        ]

        html_lower = html.lower()
        return any(indicator in html_lower for indicator in js_indicators)

    def _choose_scraper(
        self,
        method: ScrapingMethod,
        html: Optional[str] = None
    ):
        """
        Choose appropriate scraper based on method and content.

        Args:
            method: Scraping method
            html: HTML content (for auto-detection)

        Returns:
            Scraper instance
        """
        if method == ScrapingMethod.REQUESTS:
            return RequestsScraper()

        elif method == ScrapingMethod.SELENIUM:
            return SeleniumScraper()

        elif method == ScrapingMethod.PLAYWRIGHT:
            return PlaywrightScraper()

        elif method == ScrapingMethod.STEALTH:
            return StealthPlaywrightScraper(
                stealth_level=self.stealth_level,
                use_proxies=self.use_proxies,
                respect_robots=self.respect_robots
            )

        elif method == ScrapingMethod.AUTO:
            # Use new AdaptiveScraper for intelligent method selection
            return AdaptiveScraper(
                stealth_level=self.stealth_level,
                use_proxies=self.use_proxies,
                respect_robots=self.respect_robots
            )

        else:
            return RequestsScraper()

    def scrape(
        self,
        url: str,
        query: str,
        method: ScrapingMethod = ScrapingMethod.AUTO
    ) -> Dict:
        """
        Main scraping method - orchestrates the entire pipeline.

        Args:
            url: Target URL
            query: Natural language query
            method: Scraping method to use

        Returns:
            Dictionary containing:
                - success: bool
                - data: List of extracted data
                - cost: API cost
                - method_used: Which method was successful
                - cached: Whether result was cached
        """
        self._update_progress("Starting scrape...", 5)

        # Phase 1: Check cache
        self._update_progress("Checking cache...", 10)
        cached_data = self.cache_manager.get(url, query)

        if cached_data:
            logger.info("✓ Cache HIT - returning cached data")
            self.cached_count += 1

            # Track cache hit
            self.cache_manager.increment_hit(url, query)

            # Get savings estimate
            savings = self.cache_manager.get_savings_estimate()

            self._update_progress("Cache hit! Returning cached data", 100)

            return {
                "success": True,
                "data": cached_data.get("data", []),
                "cost": 0.0,
                "method_used": "cache",
                "cached": True,
                "message": f"💰 Loaded from cache (€0.00) - Total saved: €{savings['total_savings_eur']}"
            }

        # Phase 2: Fetch HTML
        self._update_progress(f"Fetching HTML ({method.value})...", 20)

        scraper = None
        try:
            scraper = self._choose_scraper(method)
            html = scraper.fetch(url)

            if not html:
                return {
                    "success": False,
                    "data": [],
                    "cost": 0.0,
                    "method_used": method.value,
                    "cached": False,
                    "message": "Failed to fetch HTML"
                }

            logger.info(f"Fetched HTML successfully ({len(html)} chars)")

        finally:
            if scraper:
                scraper.close()

        # Phase 3: Check learned selectors
        self._update_progress("Checking learned selectors...", 40)
        learned_selectors = self.selector_manager.get(url, query)

        if learned_selectors:
            logger.info("✓ Found learned selectors - extracting data")
            self.learned_count += 1
            self._update_progress("Using learned selectors (free)...", 60)

            data = BS4Extractor.extract_with_selectors(html, learned_selectors)

            if data:
                # Update success count for learned selectors
                self.selector_manager.save(url, query, learned_selectors)

                # Get savings estimate
                selector_savings = self.selector_manager.get_savings_estimate()

                result = {
                    "success": True,
                    "data": data,
                    "cost": 0.0,
                    "method_used": "learned_selectors",
                    "cached": False,
                    "message": f"🎓 Extracted {len(data)} items using learned selectors (€0.00) - {selector_savings['learned_domains']} domains learned, €{selector_savings['total_savings_eur']} saved"
                }

                # Cache the result
                self.cache_manager.set(url, query, result)
                self._update_progress("Extraction complete!", 100)

                return result

        # Phase 4: Try simple extraction (regex)
        self._update_progress("Trying pattern-based extraction...", 50)

        if RegexExtractor.has_patterns(query):
            logger.info("Query matches regex patterns - trying extraction")
            regex_data = RegexExtractor.extract(html, query)

            if regex_data:
                # Convert to standard format
                data = [regex_data]  # Wrap in list

                result = {
                    "success": True,
                    "data": data,
                    "cost": 0.0,
                    "method_used": "regex",
                    "cached": False,
                    "message": f"Extracted data using patterns (free)"
                }

                # Cache the result
                self.cache_manager.set(url, query, result)
                self._update_progress("Extraction complete!", 100)

                return result

        # Phase 5: LLM Analysis (costs money!)
        if not self.smart_extractor:
            return {
                "success": False,
                "data": [],
                "cost": 0.0,
                "method_used": "none",
                "cached": False,
                "message": "LLM not available and simpler methods failed"
            }

        # Check budget
        if self.budget_manager.is_budget_exceeded():
            return {
                "success": False,
                "data": [],
                "cost": 0.0,
                "method_used": "none",
                "cached": False,
                "message": "Daily budget exceeded!"
            }

        self._update_progress("Using AI to analyze page (costs money)...", 70)
        logger.info("Using LLM for intelligent extraction")
        self.llm_count += 1

        extraction_result = self.smart_extractor.extract(html, query, url)

        if not extraction_result or not extraction_result.get("data"):
            return {
                "success": False,
                "data": [],
                "cost": extraction_result.get("cost", 0.0) if extraction_result else 0.0,
                "method_used": "llm_failed",
                "cached": False,
                "message": "LLM extraction failed"
            }

        selectors = extraction_result["selectors"]
        data = extraction_result["data"]
        cost = extraction_result["cost"]

        self.total_cost += cost

        logger.info(f"✓ LLM extraction successful: {len(data)} items (€{cost:.4f})")

        # Save learned selectors for future use
        if selectors:
            self.selector_manager.save(url, query, selectors)
            logger.info("Saved selectors for future use")

        result = {
            "success": True,
            "data": data,
            "cost": cost,
            "method_used": "llm",
            "cached": False,
            "message": f"Extracted {len(data)} items using AI (€{cost:.4f})"
        }

        # Cache the result
        self.cache_manager.set(url, query, result)

        self._update_progress("Extraction complete!", 100)

        return result

    def _generate_paginated_url(self, base_url: str, page: int, pattern: str = None) -> str:
        """
        Generate paginated URL based on detected or specified pattern.

        Args:
            base_url: Base URL
            page: Page number
            pattern: Pagination pattern (query_param, path, hash)

        Returns:
            Paginated URL
        """
        parsed = urlparse(base_url)

        if pattern == "query_param" or not pattern:
            # Try query parameter: ?page=2 or &page=2
            query_params = parse_qs(parsed.query)
            query_params['page'] = [str(page)]
            new_query = urlencode(query_params, doseq=True)
            return urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                             parsed.params, new_query, parsed.fragment))

        elif pattern == "path":
            # Try path-based: /page/2 or /2/
            path = parsed.path.rstrip('/')
            return urlunparse((parsed.scheme, parsed.netloc, f"{path}/page/{page}",
                             parsed.params, parsed.query, parsed.fragment))

        elif pattern == "hash":
            # Try hash-based: #page=2
            return urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                             parsed.params, parsed.query, f"page={page}"))

        return base_url

    def _detect_pagination_pattern(self, url: str) -> Optional[str]:
        """
        Detect pagination pattern from URL.

        Args:
            url: URL to analyze

        Returns:
            Pattern type or None
        """
        if '?page=' in url or '&page=' in url:
            return "query_param"
        elif '/page/' in url:
            return "path"
        elif '#page=' in url:
            return "hash"

        # Default to query param
        return "query_param"

    def scrape_with_pagination(
        self,
        base_url: str,
        query: str,
        max_pages: int = 5,
        method: ScrapingMethod = ScrapingMethod.AUTO,
        page_delay: float = 2.0
    ) -> Dict:
        """
        Scrape multiple pages with intelligent pagination detection.

        Args:
            base_url: Base URL (e.g., "https://example.com/products")
            query: What to extract (natural language)
            max_pages: Maximum pages to scrape
            method: Scraping method to use
            page_delay: Delay between pages in seconds

        Returns:
            Dictionary containing:
                - success: bool
                - data: Combined list of all extracted data
                - pages_scraped: Number of pages successfully scraped
                - total_cost: Total API cost
                - method_used: Scraping method
                - message: Status message
        """
        logger.info(f"Starting pagination scrape: {base_url} (max {max_pages} pages)")
        self._update_progress(f"Starting pagination (max {max_pages} pages)...", 0)

        all_data = []
        pages_scraped = 0
        total_cost = 0.0
        method_used = None

        # Detect pagination pattern
        pattern = self._detect_pagination_pattern(base_url)
        logger.info(f"Detected pagination pattern: {pattern}")

        # Try different pagination patterns
        patterns_to_try = [pattern, "query_param", "path"]

        for page in range(1, max_pages + 1):
            self._update_progress(f"Scraping page {page}/{max_pages}...",
                                int((page / max_pages) * 90))

            # Try each pattern until one works
            page_success = False

            for pattern_type in patterns_to_try:
                # Generate URL for this page
                if page == 1:
                    page_url = base_url  # First page is usually the base URL
                else:
                    page_url = self._generate_paginated_url(base_url, page, pattern_type)

                logger.info(f"Trying page {page} with pattern '{pattern_type}': {page_url}")

                try:
                    # Scrape this page
                    result = self.scrape(page_url, query, method)

                    if result.get("success") and result.get("data"):
                        # Success!
                        page_data = result["data"]
                        page_cost = result.get("cost", 0.0)

                        # Check if page has data
                        if len(page_data) > 0:
                            all_data.extend(page_data)
                            total_cost += page_cost
                            pages_scraped += 1
                            method_used = result.get("method_used")

                            logger.info(f"✓ Page {page} success: {len(page_data)} items (€{page_cost:.4f})")
                            page_success = True

                            # Remember the working pattern
                            pattern = pattern_type
                            break  # This pattern works, move to next page
                        else:
                            # Empty page = end of pagination
                            logger.info(f"Page {page} returned no data - end of pagination")
                            self._update_progress(f"Completed: reached last page at page {page-1}", 100)

                            return {
                                "success": True,
                                "data": all_data,
                                "pages_scraped": pages_scraped,
                                "total_cost": total_cost,
                                "method_used": method_used or method.value,
                                "message": f"✓ Scraped {pages_scraped} pages, {len(all_data)} total items (€{total_cost:.4f})"
                            }

                except Exception as e:
                    logger.warning(f"Page {page} with pattern '{pattern_type}' failed: {e}")
                    continue

            # If no pattern worked for this page, stop
            if not page_success:
                logger.info(f"Page {page} failed with all patterns - stopping pagination")
                break

            # Delay between pages (except after last page)
            if page < max_pages:
                logger.info(f"Waiting {page_delay}s before next page...")
                time.sleep(page_delay)

        # Final result
        self._update_progress(f"Pagination complete!", 100)

        if pages_scraped > 0:
            return {
                "success": True,
                "data": all_data,
                "pages_scraped": pages_scraped,
                "total_cost": total_cost,
                "method_used": method_used or method.value,
                "message": f"✓ Scraped {pages_scraped} pages, {len(all_data)} total items (€{total_cost:.4f})"
            }
        else:
            return {
                "success": False,
                "data": [],
                "pages_scraped": 0,
                "total_cost": 0.0,
                "method_used": method.value,
                "message": "Failed to scrape any pages"
            }

    def get_stats(self) -> Dict:
        """Get engine statistics"""
        return {
            "total_cost": self.total_cost,
            "cached_count": self.cached_count,
            "learned_count": self.learned_count,
            "llm_count": self.llm_count,
            "budget_remaining": self.budget_manager.get_remaining_budget(),
            "cache_stats": self.cache_manager.get_stats(),
            "selector_stats": self.selector_manager.get_stats()
        }