"""
Cloudflare Challenge Handler
"""
import time
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class CloudflareHandler:
    """Handles Cloudflare challenges"""

    @staticmethod
    def wait_for_challenge(page, timeout: int = 30) -> bool:
        """
        Wait for Cloudflare challenge to complete.

        Args:
            page: Playwright/Selenium page object
            timeout: Maximum wait time in seconds

        Returns:
            True if challenge passed
        """
        try:
            logger.info("Cloudflare challenge detected, waiting...")

            start_time = time.time()
            check_interval = 1

            while time.time() - start_time < timeout:
                # Get page content
                if hasattr(page, 'content'):  # Playwright
                    html = page.content()
                    title = page.title()
                elif hasattr(page, 'page_source'):  # Selenium
                    html = page.page_source
                    title = page.title
                else:
                    time.sleep(check_interval)
                    continue

                html_lower = html.lower()

                # Check if challenge is still present
                cf_indicators = [
                    'cf-challenge',
                    'cf-browser-verification',
                    'checking your browser',
                    'ddos protection by cloudflare'
                ]

                challenge_present = any(ind in html_lower for ind in cf_indicators)

                if not challenge_present:
                    logger.info("Cloudflare challenge passed!")
                    time.sleep(2)  # Wait for full page load
                    return True

                # Wait before next check
                time.sleep(check_interval)

            logger.warning(f"Cloudflare challenge timeout after {timeout}s")
            return False

        except Exception as e:
            logger.error(f"Error waiting for Cloudflare challenge: {e}")
            return False

    @staticmethod
    def detect_cloudflare(html: str) -> bool:
        """
        Detect if Cloudflare protection is active.

        Args:
            html: HTML content

        Returns:
            True if Cloudflare detected
        """
        cf_indicators = [
            'cloudflare',
            'cf-ray',
            '__cf_bm',
            'cf_clearance',
            'cf-challenge',
        ]

        html_lower = html.lower()
        return any(indicator in html_lower for indicator in cf_indicators)