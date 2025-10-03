"""
Playwright-based Scraper (for modern JavaScript frameworks)
"""
from typing import Optional
import threading
from playwright.sync_api import sync_playwright, Browser, Page
from config.settings import (
    HEADLESS_MODE,
    PAGE_LOAD_TIMEOUT,
    USER_AGENT
)
from .base_scraper import BaseScraper
from utils.logger import get_logger

logger = get_logger(__name__)


class PlaywrightScraper(BaseScraper):
    """Scraper using Playwright for modern JavaScript frameworks"""

    def __init__(self, timeout: int = PAGE_LOAD_TIMEOUT, headless: bool = HEADLESS_MODE):
        """
        Initialize Playwright scraper.

        Args:
            timeout: Page load timeout in seconds
            headless: Run in headless mode
        """
        super().__init__(timeout)
        self.headless = headless
        self.playwright = None
        self.browser = None
        self._init_lock = threading.Lock()
        self._browser_initialized = False

    def _fetch_in_thread(self, url: str, result_container: list):
        """
        Fetch HTML in a separate thread (to avoid event loop conflicts).
        Browser initialization and usage MUST happen in the same thread.

        Args:
            url: Target URL
            result_container: List to store result
        """
        playwright = None
        browser = None
        page = None

        try:
            # Initialize Playwright in THIS thread
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process'
                ]
            )

            logger.info(f"Fetching {url} with Playwright")

            # Create new page with stealth
            context = browser.new_context(
                user_agent=USER_AGENT,
                viewport={'width': 1920, 'height': 1080},
                locale='nl-BE',
                timezone_id='Europe/Brussels',
                permissions=['geolocation']
            )

            page = context.new_page()

            # Add stealth JavaScript to hide automation
            page.add_init_script("""
                // Override navigator.webdriver
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });

                // Override chrome property
                window.chrome = {
                    runtime: {}
                };

                // Override plugins
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });

                // Override permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """)

            # Set timeout
            page.set_default_timeout(self.timeout * 1000)

            # Navigate to URL
            page.goto(url, wait_until='domcontentloaded')

            # Wait for network to be idle
            page.wait_for_load_state('networkidle', timeout=self.timeout * 1000)

            # Wait a bit more for dynamic content (especially for SPAs)
            try:
                # Try to wait for common listing containers
                page.wait_for_selector('article, .card, .item, .listing, [class*="card"]', timeout=5000)
            except:
                # If specific selectors don't appear, just wait 2 seconds
                page.wait_for_timeout(2000)

            # Get HTML content
            html = page.content()

            logger.info(f"Successfully fetched {url} ({len(html)} chars)")
            result_container.append(html)

        except Exception as e:
            logger.error(f"Error fetching {url} with Playwright: {e}")
            result_container.append(None)

        finally:
            # Clean up in THIS thread
            if page:
                try:
                    page.close()
                except:
                    pass
            if browser:
                try:
                    browser.close()
                except:
                    pass
            if playwright:
                try:
                    playwright.stop()
                except:
                    pass

    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch HTML content using Playwright.

        Args:
            url: Target URL

        Returns:
            HTML content or None on error
        """
        # Use thread to avoid event loop conflicts with PyQt
        result_container = []
        thread = threading.Thread(
            target=self._fetch_in_thread,
            args=(url, result_container)
        )
        thread.start()
        thread.join(timeout=self.timeout + 10)  # Add 10s buffer

        if thread.is_alive():
            logger.error(f"Playwright fetch timeout for {url}")
            return None

        return result_container[0] if result_container else None

    def close(self):
        """Close browser and Playwright (no-op since we clean up per fetch)"""
        # Browser is now created and destroyed per fetch, so nothing to do here
        pass