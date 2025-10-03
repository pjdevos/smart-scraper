"""
Manual CAPTCHA Solver - Opens browser for user to solve
"""
import time
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class ManualCaptchaSolver:
    """Allows user to manually solve CAPTCHAs"""

    @staticmethod
    def solve_with_browser(page, timeout: int = 300) -> bool:
        """
        Open browser for user to solve CAPTCHA manually.

        Args:
            page: Playwright/Selenium page object
            timeout: Maximum wait time in seconds (default 5 minutes)

        Returns:
            True if likely solved
        """
        try:
            logger.info("CAPTCHA detected - waiting for manual solving...")
            logger.info(f"Please solve the CAPTCHA in the browser window (timeout: {timeout}s)")

            # Make browser visible if it's Playwright
            if hasattr(page, 'context'):
                try:
                    # Cannot change headless mode after creation
                    # Just wait for user
                    pass
                except Exception:
                    pass

            start_time = time.time()
            check_interval = 2  # Check every 2 seconds

            while time.time() - start_time < timeout:
                # Check if CAPTCHA is still present
                if hasattr(page, 'content'):  # Playwright
                    html = page.content()
                elif hasattr(page, 'page_source'):  # Selenium
                    html = page.page_source
                else:
                    time.sleep(check_interval)
                    continue

                # Check if CAPTCHA is gone
                from .captcha_detector import CaptchaDetector
                result = CaptchaDetector.detect(html)

                if not result['detected']:
                    logger.info("CAPTCHA appears to be solved!")
                    time.sleep(2)  # Wait a bit more to ensure page loads
                    return True

                # Wait before next check
                time.sleep(check_interval)

            logger.warning(f"CAPTCHA solving timed out after {timeout}s")
            return False

        except Exception as e:
            logger.error(f"Error during manual CAPTCHA solving: {e}")
            return False

    @staticmethod
    def wait_for_user_action(page, message: str = "Press Enter when ready...", timeout: int = 300) -> bool:
        """
        Pause and wait for user to take action.

        Args:
            page: Page object
            message: Message to display
            timeout: Maximum wait time

        Returns:
            True if user pressed Enter
        """
        logger.info(message)
        logger.info("Waiting for user input...")

        try:
            # In a GUI application, this would show a dialog
            # For now, just wait with periodic checks
            start_time = time.time()

            while time.time() - start_time < timeout:
                time.sleep(1)

                # Check if CAPTCHA is solved
                if hasattr(page, 'content'):
                    html = page.content()
                elif hasattr(page, 'page_source'):
                    html = page.page_source
                else:
                    continue

                from .captcha_detector import CaptchaDetector
                if not CaptchaDetector.detect(html)['detected']:
                    return True

            return False

        except Exception as e:
            logger.error(f"Error waiting for user action: {e}")
            return False