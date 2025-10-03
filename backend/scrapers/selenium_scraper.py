"""
Selenium-based Scraper (for JavaScript-heavy sites)
"""
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import (
    HEADLESS_MODE,
    BROWSER_WAIT_TIME,
    PAGE_LOAD_TIMEOUT,
    USER_AGENT
)
from .base_scraper import BaseScraper
from utils.logger import get_logger

logger = get_logger(__name__)


class SeleniumScraper(BaseScraper):
    """Scraper using Selenium for JavaScript-rendered pages"""

    def __init__(self, timeout: int = PAGE_LOAD_TIMEOUT, headless: bool = HEADLESS_MODE):
        """
        Initialize Selenium scraper.

        Args:
            timeout: Page load timeout in seconds
            headless: Run in headless mode
        """
        super().__init__(timeout)
        self.headless = headless
        self.driver = None
        self._init_driver()

    def _init_driver(self):
        """Initialize Chrome WebDriver"""
        try:
            chrome_options = Options()

            if self.headless:
                chrome_options.add_argument('--headless=new')

            # Common options
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument(f'user-agent={USER_AGENT}')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')

            # Disable automation flags
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Set timeouts
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.implicitly_wait(BROWSER_WAIT_TIME)

            logger.info("Selenium WebDriver initialized")

        except Exception as e:
            logger.error(f"Error initializing Selenium: {e}")
            raise

    def fetch(self, url: str) -> Optional[str]:
        """
        Fetch HTML content using Selenium.

        Args:
            url: Target URL

        Returns:
            HTML content or None on error
        """
        if not self.driver:
            logger.error("WebDriver not initialized")
            return None

        try:
            logger.info(f"Fetching {url} with Selenium")

            self.driver.get(url)

            # Wait for body to be present
            WebDriverWait(self.driver, BROWSER_WAIT_TIME).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Get page source
            html = self.driver.page_source

            logger.info(f"Successfully fetched {url} ({len(html)} chars)")
            return html

        except Exception as e:
            logger.error(f"Error fetching {url} with Selenium: {e}")
            return None

    def close(self):
        """Close WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.debug("Selenium WebDriver closed")
            except Exception as e:
                logger.error(f"Error closing Selenium: {e}")