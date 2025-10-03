"""
Rate Limiter - Prevents too many requests to same domain
"""
import time
import random
from datetime import datetime
from typing import Dict
from collections import defaultdict
from utils.logger import get_logger
from utils.helpers import get_domain

logger = get_logger(__name__)


class RateLimiter:
    """Rate limiter with random delays per domain"""

    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 5.0,
        requests_per_minute: int = 20
    ):
        """
        Initialize rate limiter.

        Args:
            min_delay: Minimum delay between requests (seconds)
            max_delay: Maximum delay between requests (seconds)
            requests_per_minute: Maximum requests per minute per domain
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.requests_per_minute = requests_per_minute

        # Track last request time per domain
        self.last_request: Dict[str, float] = {}

        # Track request counts per domain per minute
        self.request_counts: Dict[str, list] = defaultdict(list)

    def wait(self, url: str, stealth_level: str = "medium"):
        """
        Wait before making request based on rate limits.

        Args:
            url: Target URL
            stealth_level: Stealth level (basic, medium, high, maximum)
        """
        domain = get_domain(url)

        # Adjust delays based on stealth level
        if stealth_level == "basic":
            min_delay = self.min_delay
            max_delay = self.max_delay
        elif stealth_level == "medium":
            min_delay = 2.0
            max_delay = 5.0
        elif stealth_level == "high":
            min_delay = 5.0
            max_delay = 10.0
        elif stealth_level == "maximum":
            min_delay = 60.0  # 1 request per minute
            max_delay = 60.0
        else:
            min_delay = self.min_delay
            max_delay = self.max_delay

        # Check if we need to wait
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            required_delay = random.uniform(min_delay, max_delay)

            if elapsed < required_delay:
                wait_time = required_delay - elapsed
                logger.info(f"Rate limiting: waiting {wait_time:.2f}s for {domain}")
                time.sleep(wait_time)

        # Check requests per minute limit (except for maximum stealth)
        if stealth_level != "maximum":
            self._check_rpm_limit(domain)

        # Record this request
        self.last_request[domain] = time.time()
        self.request_counts[domain].append(time.time())

        # Add random jitter for medium+ stealth
        if stealth_level in ["medium", "high", "maximum"]:
            jitter = random.uniform(0.1, 0.5)
            time.sleep(jitter)

    def _check_rpm_limit(self, domain: str):
        """Check and enforce requests per minute limit"""
        now = time.time()
        minute_ago = now - 60

        # Remove old requests
        self.request_counts[domain] = [
            req_time for req_time in self.request_counts[domain]
            if req_time > minute_ago
        ]

        # Check if we exceeded limit
        if len(self.request_counts[domain]) >= self.requests_per_minute:
            # Wait until oldest request is > 1 minute old
            oldest_request = self.request_counts[domain][0]
            wait_time = 60 - (now - oldest_request)

            if wait_time > 0:
                logger.warning(
                    f"RPM limit reached for {domain}, waiting {wait_time:.2f}s"
                )
                time.sleep(wait_time)

    def get_stats(self) -> Dict:
        """Get rate limiting statistics"""
        return {
            "domains_tracked": len(self.last_request),
            "total_requests": sum(len(counts) for counts in self.request_counts.values())
        }