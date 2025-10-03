"""
Adaptive Scraper
Automatically selects the best scraping method based on page characteristics
"""
import logging
from typing import Optional, Dict
from urllib.parse import urlparse
from .base_scraper import BaseScraper
from .requests_scraper import RequestsScraper
from .selenium_scraper import SeleniumScraper
from .playwright_scraper import PlaywrightScraper
from .stealth_playwright_scraper import StealthPlaywrightScraper

logger = logging.getLogger(__name__)


class AdaptiveScraper(BaseScraper):
    """
    Intelligent scraper that automatically selects the best method.

    Decision tree:
    1. Try Requests first (fastest)
    2. If page has JS indicators -> try Playwright
    3. If anti-bot detected -> try Stealth
    4. Fallback to Selenium if needed
    """

    # Known JS-heavy domains
    JS_HEAVY_DOMAINS = [
        'angular',
        'react',
        'vue',
        'next',
        'nuxt',
        'gatsby',
        'svelte'
    ]

    # Known anti-bot domains
    PROTECTED_DOMAINS = [
        'cloudflare',
        'datadome',
        'perimeter',
        'imperva',
        'akamai'
    ]

    # Fast static sites
    STATIC_DOMAINS = [
        'wikipedia',
        'github',
        'stackoverflow',
        'reddit'
    ]

    def __init__(
        self,
        timeout: int = 30,
        stealth_level: str = "medium",
        use_proxies: bool = False,
        respect_robots: bool = True
    ):
        """
        Initialize adaptive scraper.

        Args:
            timeout: Request timeout
            stealth_level: Stealth level for protected sites
            use_proxies: Use proxy rotation
            respect_robots: Respect robots.txt
        """
        super().__init__(timeout)
        self.stealth_level = stealth_level
        self.use_proxies = use_proxies
        self.respect_robots = respect_robots

        # Initialize all scrapers
        self.scrapers = {
            'requests': RequestsScraper(timeout),
            'playwright': PlaywrightScraper(timeout),
            'selenium': SeleniumScraper(timeout),
            'stealth': StealthPlaywrightScraper(
                timeout=timeout,
                stealth_level=stealth_level,
                use_proxies=use_proxies,
                respect_robots=respect_robots
            )
        }

        self.current_scraper = None
        logger.info("AdaptiveScraper initialized")

    def _analyze_domain(self, url: str) -> Dict[str, bool]:
        """
        Analyze domain to determine characteristics.

        Args:
            url: Target URL

        Returns:
            Dictionary with domain characteristics
        """
        domain = urlparse(url).netloc.lower()

        analysis = {
            'is_static': any(d in domain for d in self.STATIC_DOMAINS),
            'is_js_heavy': any(d in domain for d in self.JS_HEAVY_DOMAINS),
            'is_protected': any(d in domain for d in self.PROTECTED_DOMAINS),
            'needs_stealth': False
        }

        # Determine if stealth is needed
        analysis['needs_stealth'] = analysis['is_protected'] or self.stealth_level in ['high', 'maximum']

        logger.debug(f"Domain analysis for {domain}: {analysis}")

        return analysis

    def _detect_javascript(self, html: str) -> bool:
        """
        Detect if page requires JavaScript rendering.

        Args:
            html: HTML content

        Returns:
            True if JavaScript is likely required
        """
        if not html:
            return False

        js_indicators = [
            '<script',
            'react',
            'angular',
            'vue',
            'next.js',
            'nuxt',
            '__NEXT_DATA__',
            'ng-app',
            'v-app',
            'data-reactroot',
            'data-react-helmet',
            'gatsby'
        ]

        html_lower = html[:5000].lower()  # Check first 5KB
        js_count = sum(1 for indicator in js_indicators if indicator in html_lower)

        # If 3+ indicators, likely needs JS
        return js_count >= 3

    def _detect_anti_bot(self, html: str) -> bool:
        """
        Detect anti-bot protection.

        Args:
            html: HTML content

        Returns:
            True if anti-bot detected
        """
        if not html:
            return False

        anti_bot_indicators = [
            'cloudflare',
            'captcha',
            'recaptcha',
            'hcaptcha',
            'datadome',
            'perimeter',
            'imperva',
            'blocked',
            'access denied',
            'challenge',
            'bot detection'
        ]

        html_lower = html[:3000].lower()  # Check first 3KB
        return any(indicator in html_lower for indicator in anti_bot_indicators)

    def _has_sufficient_content(self, html: str) -> bool:
        """
        Check if HTML has sufficient content.

        Args:
            html: HTML content

        Returns:
            True if content seems sufficient
        """
        if not html:
            return False

        # Check length
        if len(html) < 500:
            return False

        # Check for common content indicators
        content_indicators = ['<p', '<div', '<article', '<section', '<main']
        content_count = sum(1 for indicator in content_indicators if indicator in html.lower())

        return content_count >= 3

    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch HTML with adaptive method selection.

        Args:
            url: Target URL

        Returns:
            HTML content or None
        """
        logger.info(f"🧠 Adaptive scraping: {url}")

        # Analyze domain
        domain_info = self._analyze_domain(url)

        # Strategy 1: Known static site -> Use Requests
        if domain_info['is_static']:
            logger.info("→ Using Requests (known static site)")
            self.current_scraper = self.scrapers['requests']
            html = self.current_scraper.fetch(url)

            if html and self._has_sufficient_content(html):
                return html

        # Strategy 2: Protected site -> Use Stealth
        if domain_info['needs_stealth']:
            logger.info("→ Using Stealth (protected site or high stealth level)")
            self.current_scraper = self.scrapers['stealth']
            return self.current_scraper.fetch(url)

        # Strategy 3: Try Requests first (fastest)
        logger.info("→ Trying Requests first...")
        self.current_scraper = self.scrapers['requests']
        html = self.current_scraper.fetch(url)

        if html:
            # Check for anti-bot
            if self._detect_anti_bot(html):
                logger.info("  ⚠️ Anti-bot detected, switching to Stealth")
                self.scrapers['requests'].close()
                self.current_scraper = self.scrapers['stealth']
                return self.current_scraper.fetch(url)

            # Check if JS is needed
            if self._detect_javascript(html):
                logger.info("  ⚠️ JavaScript detected, switching to Playwright")
                self.scrapers['requests'].close()
                self.current_scraper = self.scrapers['playwright']
                return self.current_scraper.fetch(url)

            # Check content sufficiency
            if self._has_sufficient_content(html):
                logger.info("  ✓ Success with Requests")
                return html

        # Strategy 4: Fallback to Playwright
        logger.info("→ Falling back to Playwright...")
        self.scrapers['requests'].close()
        self.current_scraper = self.scrapers['playwright']
        html = self.current_scraper.fetch(url)

        if html and self._has_sufficient_content(html):
            return html

        # Strategy 5: Last resort - Selenium
        logger.info("→ Last resort: Selenium...")
        self.current_scraper.close()
        self.current_scraper = self.scrapers['selenium']
        return self.current_scraper.fetch(url)

    def get_method_used(self) -> str:
        """Get the method that was actually used"""
        if self.current_scraper == self.scrapers['requests']:
            return "adaptive_requests"
        elif self.current_scraper == self.scrapers['playwright']:
            return "adaptive_playwright"
        elif self.current_scraper == self.scrapers['selenium']:
            return "adaptive_selenium"
        elif self.current_scraper == self.scrapers['stealth']:
            return "adaptive_stealth"
        else:
            return "adaptive_unknown"

    def close(self):
        """Close all scrapers"""
        for scraper in self.scrapers.values():
            try:
                scraper.close()
            except:
                pass

        logger.info("AdaptiveScraper closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
