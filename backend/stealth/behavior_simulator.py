"""
Human Behavior Simulator - Mouse movements, scrolling, typing
"""
import time
import random
from typing import Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class BehaviorSimulator:
    """Simulates human-like browser behavior"""

    @staticmethod
    def random_sleep(min_seconds: float = 0.5, max_seconds: float = 2.0):
        """Random sleep to simulate human thinking time"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    @staticmethod
    def human_like_scroll(page, scroll_count: int = None):
        """
        Simulate human-like scrolling on a page.

        Args:
            page: Playwright or Selenium page object
            scroll_count: Number of scrolls (random if None)
        """
        if scroll_count is None:
            scroll_count = random.randint(3, 7)

        try:
            # Check if it's Playwright or Selenium
            if hasattr(page, 'evaluate'):  # Playwright
                for _ in range(scroll_count):
                    # Random scroll amount
                    scroll_amount = random.randint(200, 600)

                    # Scroll down
                    page.evaluate(f"window.scrollBy(0, {scroll_amount})")

                    # Random delay
                    time.sleep(random.uniform(0.3, 1.0))

                # Scroll back to top sometimes
                if random.random() > 0.7:
                    page.evaluate("window.scrollTo(0, 0)")
                    time.sleep(random.uniform(0.5, 1.5))

            elif hasattr(page, 'execute_script'):  # Selenium
                for _ in range(scroll_count):
                    scroll_amount = random.randint(200, 600)
                    page.execute_script(f"window.scrollBy(0, {scroll_amount})")
                    time.sleep(random.uniform(0.3, 1.0))

                if random.random() > 0.7:
                    page.execute_script("window.scrollTo(0, 0)")
                    time.sleep(random.uniform(0.5, 1.5))

            logger.debug(f"Performed {scroll_count} human-like scrolls")

        except Exception as e:
            logger.warning(f"Error during scrolling: {e}")

    @staticmethod
    def simulate_mouse_movement(page, movements: int = None):
        """
        Simulate random mouse movements (Playwright only).

        Args:
            page: Playwright page object
            movements: Number of movements (random if None)
        """
        if movements is None:
            movements = random.randint(2, 5)

        try:
            if hasattr(page, 'mouse'):  # Playwright
                viewport = page.viewport_size
                width = viewport['width']
                height = viewport['height']

                for _ in range(movements):
                    # Random position
                    x = random.randint(50, width - 50)
                    y = random.randint(50, height - 50)

                    # Move mouse with random steps
                    steps = random.randint(10, 30)
                    page.mouse.move(x, y, steps=steps)

                    # Random delay
                    time.sleep(random.uniform(0.1, 0.5))

                logger.debug(f"Simulated {movements} mouse movements")

        except Exception as e:
            logger.warning(f"Error during mouse movement: {e}")

    @staticmethod
    def random_mouse_click(page):
        """
        Randomly click on safe elements (Playwright only).

        Args:
            page: Playwright page object
        """
        try:
            if hasattr(page, 'mouse'):  # Playwright
                viewport = page.viewport_size

                # Click somewhere safe (avoid edges)
                x = random.randint(100, viewport['width'] - 100)
                y = random.randint(100, viewport['height'] - 100)

                page.mouse.click(x, y)
                time.sleep(random.uniform(0.2, 0.8))

                logger.debug(f"Random click at ({x}, {y})")

        except Exception as e:
            logger.warning(f"Error during random click: {e}")

    @staticmethod
    def gradual_page_load(page, wait_time: float = 3.0):
        """
        Wait for page to load gradually with random checks.

        Args:
            page: Page object
            wait_time: Total wait time in seconds
        """
        steps = random.randint(3, 6)
        step_time = wait_time / steps

        for i in range(steps):
            time.sleep(step_time + random.uniform(-0.2, 0.5))

            # Random action during load
            action = random.choice(['scroll', 'wait', 'check'])

            if action == 'scroll' and i > 0:
                try:
                    if hasattr(page, 'evaluate'):  # Playwright
                        page.evaluate(f"window.scrollBy(0, {random.randint(50, 200)})")
                    elif hasattr(page, 'execute_script'):  # Selenium
                        page.execute_script(f"window.scrollBy(0, {random.randint(50, 200)})")
                except Exception:
                    pass

        logger.debug("Gradual page load complete")

    @staticmethod
    def simulate_reading(duration: float = None):
        """
        Simulate human reading time.

        Args:
            duration: Reading duration in seconds (random if None)
        """
        if duration is None:
            duration = random.uniform(2.0, 8.0)

        logger.debug(f"Simulating reading for {duration:.1f}s")
        time.sleep(duration)