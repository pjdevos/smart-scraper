"""
Proxy Configuration
"""
import os
from typing import Optional, Dict, List
from utils.logger import get_logger

logger = get_logger(__name__)


class ProxyConfig:
    """Proxy configuration and rotation"""

    def __init__(self):
        """Initialize proxy configuration"""
        self.proxies: List[Dict[str, str]] = []
        self.current_index = 0
        self._load_proxies()

    def _load_proxies(self):
        """Load proxies from environment or config"""
        # Load from environment variable (format: http://user:pass@host:port)
        proxy_list = os.getenv('PROXY_LIST', '').split(',')

        for proxy_url in proxy_list:
            proxy_url = proxy_url.strip()
            if proxy_url:
                self.proxies.append({
                    'http': proxy_url,
                    'https': proxy_url
                })

        if self.proxies:
            logger.info(f"Loaded {len(self.proxies)} proxies")
        else:
            logger.debug("No proxies configured")

    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get next proxy in rotation.

        Returns:
            Proxy dict or None if no proxies configured
        """
        if not self.proxies:
            return None

        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)

        logger.debug(f"Using proxy: {proxy['http']}")
        return proxy

    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """Get random proxy"""
        if not self.proxies:
            return None

        import random
        return random.choice(self.proxies)

    def add_proxy(self, proxy_url: str):
        """
        Add a proxy to the pool.

        Args:
            proxy_url: Proxy URL (http://user:pass@host:port)
        """
        self.proxies.append({
            'http': proxy_url,
            'https': proxy_url
        })
        logger.info(f"Added proxy: {proxy_url}")

    def get_playwright_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get proxy config for Playwright.

        Returns:
            Playwright proxy dict or None
        """
        if not self.proxies:
            return None

        proxy = self.get_next_proxy()
        if not proxy:
            return None

        # Parse proxy URL
        proxy_url = proxy['http']

        # Format: http://user:pass@host:port or http://host:port
        if '@' in proxy_url:
            # Has authentication
            protocol, rest = proxy_url.split('://')
            auth, server = rest.split('@')
            username, password = auth.split(':')

            return {
                'server': f'http://{server}',
                'username': username,
                'password': password
            }
        else:
            # No authentication
            return {
                'server': proxy_url
            }

    def has_proxies(self) -> bool:
        """Check if proxies are configured"""
        return len(self.proxies) > 0