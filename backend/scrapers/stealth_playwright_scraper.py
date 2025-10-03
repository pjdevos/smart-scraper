"""
Stealth Playwright Scraper - Maximum anti-detection
"""
from typing import Optional
import threading
from playwright.sync_api import sync_playwright, Browser, Page, Error as PlaywrightError
from config.settings import PAGE_LOAD_TIMEOUT
from config.proxy_config import ProxyConfig
from .base_scraper import BaseScraper
from backend.stealth.user_agent_rotator import UserAgentRotator
from backend.stealth.fingerprint_mask import FingerprintMask
from backend.stealth.behavior_simulator import BehaviorSimulator
from backend.stealth.rate_limiter import RateLimiter
from backend.stealth.robots_parser import RobotsParser
from backend.captcha.captcha_detector import CaptchaDetector
from backend.captcha.manual_solver import ManualCaptchaSolver
from backend.captcha.cloudflare_handler import CloudflareHandler
from backend.storage import CookieManager
from utils.logger import get_logger

logger = get_logger(__name__)


class StealthPlaywrightScraper(BaseScraper):
    """
    Advanced Playwright scraper with full stealth features.

    Stealth Levels:
    - basic: User agent, basic delays
    - medium: + scrolling, cookies, jitter
    - high: + mouse movement, UA rotation, fingerprinting
    - maximum: + proxies, CAPTCHA handling, very slow
    """

    def __init__(
        self,
        timeout: int = PAGE_LOAD_TIMEOUT,
        headless: bool = True,
        stealth_level: str = "medium",
        use_proxies: bool = False,
        respect_robots: bool = True
    ):
        """
        Initialize stealth scraper.

        Args:
            timeout: Page load timeout
            headless: Run in headless mode
            stealth_level: Stealth level (basic, medium, high, maximum)
            use_proxies: Use proxy rotation
            respect_robots: Respect robots.txt
        """
        super().__init__(timeout)
        self.headless = headless
        self.stealth_level = stealth_level
        self.use_proxies = use_proxies

        # Initialize components
        self.ua_rotator = UserAgentRotator()
        self.rate_limiter = RateLimiter()
        self.robots_parser = RobotsParser(respect_robots)
        self.cookie_manager = CookieManager()
        self.proxy_config = ProxyConfig() if use_proxies else None

        # These are no longer needed since we create browser per fetch
        # self.playwright = None
        # self.browser = None

    def _fetch_in_thread(self, url: str, result_container: list):
        """
        Fetch HTML in a separate thread (to avoid event loop conflicts).
        Browser initialization and usage MUST happen in the same thread.

        Args:
            url: Target URL
            result_container: List to store result
        """
        # Check robots.txt
        user_agent = self.ua_rotator.get_random()
        if not self.robots_parser.can_fetch(url, user_agent):
            logger.error(f"robots.txt disallows fetching {url}")
            result_container.append(None)
            return

        # Rate limiting
        self.rate_limiter.wait(url, self.stealth_level)

        # Check for crawl delay in robots.txt
        crawl_delay = self.robots_parser.get_crawl_delay(url, user_agent)
        if crawl_delay:
            import time
            logger.info(f"robots.txt crawl delay: {crawl_delay}s")
            time.sleep(crawl_delay)

        playwright = None
        browser = None
        page = None
        context = None

        try:
            # Initialize Playwright in THIS thread
            playwright = sync_playwright().start()

            # Get proxy if enabled
            proxy = None
            if self.use_proxies and self.proxy_config and self.proxy_config.has_proxies():
                proxy = self.proxy_config.get_playwright_proxy()
                logger.info(f"Using proxy: {proxy['server']}")

            # Browser args for stealth
            args = [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
            ]

            # Launch browser
            launch_options = {
                'headless': self.headless,
                'args': args
            }

            if proxy:
                launch_options['proxy'] = proxy

            browser = playwright.chromium.launch(**launch_options)

            logger.info(f"Fetching {url} with Stealth Playwright (level: {self.stealth_level})")

            # Create context with stealth settings
            viewport = FingerprintMask.get_random_viewport()
            locale = FingerprintMask.get_random_languages()[0]
            timezone = FingerprintMask.get_random_timezone()

            context = browser.new_context(
                user_agent=user_agent,
                viewport=viewport,
                locale=locale,
                timezone_id=timezone,
                permissions=[],
                geolocation=None,
                color_scheme='light',
            )

            # Create page
            page = context.new_page()

            # Apply stealth scripts
            if self.stealth_level in ['high', 'maximum']:
                FingerprintMask.apply_stealth_scripts(page)
                FingerprintMask.randomize_canvas_fingerprint(page)

            # Load cookies if available
            saved_cookies = self.cookie_manager.load_cookies(url)
            if saved_cookies:
                context.add_cookies(saved_cookies)
                logger.info("Loaded saved cookies")

            # Set timeout
            page.set_default_timeout(self.timeout * 1000)

            # Navigate to URL
            page.goto(url, wait_until='domcontentloaded')

            # MEDIUM+ stealth: Gradual loading
            if self.stealth_level in ['medium', 'high', 'maximum']:
                BehaviorSimulator.gradual_page_load(page, wait_time=3.0)

            # Wait for network idle
            try:
                page.wait_for_load_state('networkidle', timeout=self.timeout * 1000)
            except PlaywrightError:
                logger.warning("Network idle timeout, continuing anyway")

            # Check for Cloudflare
            html = page.content()
            if CloudflareHandler.detect_cloudflare(html):
                logger.warning("Cloudflare detected, waiting for challenge...")
                if CloudflareHandler.wait_for_challenge(page, timeout=30):
                    html = page.content()
                else:
                    logger.error("Failed to pass Cloudflare challenge")
                    return None

            # Check for CAPTCHA
            captcha_result = CaptchaDetector.detect_in_page(page)
            if captcha_result['detected']:
                logger.warning(f"CAPTCHA detected: {captcha_result['types']}")

                if self.stealth_level == 'maximum':
                    # Allow manual solving
                    logger.info("Attempting manual CAPTCHA solving...")
                    if ManualCaptchaSolver.solve_with_browser(page, timeout=300):
                        html = page.content()
                    else:
                        logger.error("CAPTCHA not solved")
                        return None
                else:
                    logger.error("CAPTCHA detected but not in maximum stealth mode")
                    return None

            # HIGH+ stealth: Human behavior simulation
            if self.stealth_level in ['high', 'maximum']:
                # Mouse movements
                BehaviorSimulator.simulate_mouse_movement(page, movements=3)

                # Scrolling
                BehaviorSimulator.human_like_scroll(page, scroll_count=4)

                # Reading time
                BehaviorSimulator.simulate_reading(duration=2.0)

            elif self.stealth_level == 'medium':
                # Just scrolling
                BehaviorSimulator.human_like_scroll(page, scroll_count=2)

            # Get final HTML
            html = page.content()

            # Save cookies for future use
            cookies = context.cookies()
            if cookies:
                self.cookie_manager.save_cookies(url, cookies)

            logger.info(f"Successfully fetched {url} ({len(html)} chars)")
            result_container.append(html)

        except PlaywrightError as e:
            logger.error(f"Playwright error fetching {url}: {e}")
            result_container.append(None)

        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            result_container.append(None)

        finally:
            # Clean up in THIS thread
            if page:
                page.close()
            if context:
                context.close()
            if browser:
                browser.close()
            if playwright:
                playwright.stop()

    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch HTML with full stealth features.

        Args:
            url: Target URL

        Returns:
            HTML content or None
        """
        # Use thread to avoid event loop conflicts with PyQt
        result_container = []
        thread = threading.Thread(
            target=self._fetch_in_thread,
            args=(url, result_container)
        )
        thread.start()
        thread.join(timeout=self.timeout + 60)  # Add 60s buffer for stealth delays

        if thread.is_alive():
            logger.error(f"Stealth Playwright fetch timeout for {url}")
            return None

        return result_container[0] if result_container else None

    def close(self):
        """Close browser and Playwright (no-op since we clean up per fetch)"""
        # Browser is now created and destroyed per fetch, so nothing to do here
        pass