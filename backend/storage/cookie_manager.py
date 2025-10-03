"""
Cookie Manager for CAPTCHA bypass
"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from config.settings import COOKIES_DIR
from utils.logger import get_logger
from utils.helpers import get_domain

logger = get_logger(__name__)


class CookieManager:
    """Manages browser cookies for session persistence"""

    def __init__(self, cookies_dir: Path = COOKIES_DIR):
        """
        Initialize cookie manager.

        Args:
            cookies_dir: Directory to store cookie files
        """
        self.cookies_dir = cookies_dir
        self.cookies_dir.mkdir(exist_ok=True)

    def _get_cookie_file(self, url: str) -> Path:
        """Get cookie file path for domain"""
        domain = get_domain(url).replace(".", "_")
        return self.cookies_dir / f"{domain}.json"

    def save_cookies(self, url: str, cookies: List[Dict]):
        """
        Save cookies for domain.

        Args:
            url: Target URL
            cookies: List of cookie dictionaries
        """
        cookie_file = self._get_cookie_file(url)

        try:
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            logger.info(f"Saved {len(cookies)} cookies for {get_domain(url)}")
        except Exception as e:
            logger.error(f"Error saving cookies: {e}")

    def load_cookies(self, url: str) -> Optional[List[Dict]]:
        """
        Load cookies for domain.

        Args:
            url: Target URL

        Returns:
            List of cookie dictionaries or None
        """
        cookie_file = self._get_cookie_file(url)

        if cookie_file.exists():
            try:
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                logger.info(f"Loaded {len(cookies)} cookies for {get_domain(url)}")
                return cookies
            except Exception as e:
                logger.error(f"Error loading cookies: {e}")

        return None

    def has_cookies(self, url: str) -> bool:
        """Check if we have saved cookies for domain"""
        return self._get_cookie_file(url).exists()

    def delete_cookies(self, url: str):
        """Delete saved cookies for domain"""
        cookie_file = self._get_cookie_file(url)
        if cookie_file.exists():
            cookie_file.unlink()
            logger.info(f"Deleted cookies for {get_domain(url)}")

    def list_domains(self) -> List[str]:
        """List all domains with saved cookies"""
        domains = []
        for cookie_file in self.cookies_dir.glob("*.json"):
            domain = cookie_file.stem.replace("_", ".")
            domains.append(domain)
        return domains