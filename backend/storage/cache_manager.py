"""
LLM Response Cache Manager
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from config.settings import DATA_DIR, CACHE_EXPIRY_DAYS
from utils.logger import get_logger
from utils.helpers import create_cache_key

logger = get_logger(__name__)


class CacheManager:
    """Manages caching of LLM responses"""

    def __init__(self, cache_file: Path = None):
        """
        Initialize cache manager.

        Args:
            cache_file: Path to cache file (default: data/llm_cache.json)
        """
        self.cache_file = cache_file or DATA_DIR / "llm_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Load cache from file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading cache: {e}")
                return {}
        return {}

    def _save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")

    def _is_expired(self, timestamp: str) -> bool:
        """Check if cache entry is expired"""
        try:
            cached_time = datetime.fromisoformat(timestamp)
            expiry_time = cached_time + timedelta(days=CACHE_EXPIRY_DAYS)
            return datetime.now() > expiry_time
        except Exception:
            return True

    def get(self, url: str, query: str) -> Optional[Dict[str, Any]]:
        """
        Get cached response for URL + query.

        Args:
            url: Target URL
            query: Natural language query

        Returns:
            Cached response or None if not found/expired
        """
        key = create_cache_key(url, query)

        if key in self.cache:
            entry = self.cache[key]

            # Check expiration
            if not self._is_expired(entry.get("timestamp", "")):
                logger.info(f"Cache HIT for {url}")
                return entry.get("data")
            else:
                # Remove expired entry
                del self.cache[key]
                self._save_cache()
                logger.info(f"Cache EXPIRED for {url}")

        logger.info(f"Cache MISS for {url}")
        return None

    def set(self, url: str, query: str, data: Dict[str, Any]):
        """
        Cache response for URL + query.

        Args:
            url: Target URL
            query: Natural language query
            data: Data to cache
        """
        key = create_cache_key(url, query)

        self.cache[key] = {
            "url": url,
            "query": query,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

        self._save_cache()
        logger.info(f"Cached response for {url}")

    def clear_expired(self):
        """Remove all expired cache entries"""
        expired_keys = [
            key for key, entry in self.cache.items()
            if self._is_expired(entry.get("timestamp", ""))
        ]

        for key in expired_keys:
            del self.cache[key]

        if expired_keys:
            self._save_cache()
            logger.info(f"Removed {len(expired_keys)} expired cache entries")

    def clear_all(self):
        """Clear entire cache"""
        self.cache = {}
        self._save_cache()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = len(self.cache)
        expired = sum(1 for entry in self.cache.values()
                     if self._is_expired(entry.get("timestamp", "")))

        # Calculate total hits (if tracked)
        total_hits = sum(entry.get("hits", 0) for entry in self.cache.values())

        # Calculate cache size
        cache_size_mb = 0
        if self.cache_file.exists():
            cache_size_mb = self.cache_file.stat().st_size / (1024 * 1024)

        return {
            "total_entries": total,
            "valid_entries": total - expired,
            "expired_entries": expired,
            "total_hits": total_hits,
            "cache_size_mb": round(cache_size_mb, 2)
        }

    def get_hit_rate(self) -> float:
        """
        Get cache hit rate (if tracking enabled).

        Returns:
            Hit rate as percentage (0-100)
        """
        total_requests = sum(entry.get("total_requests", 0) for entry in self.cache.values())
        total_hits = sum(entry.get("hits", 0) for entry in self.cache.values())

        if total_requests > 0:
            return (total_hits / total_requests) * 100
        return 0.0

    def increment_hit(self, url: str, query: str):
        """
        Increment hit counter for cache entry.

        Args:
            url: Target URL
            query: Natural language query
        """
        key = create_cache_key(url, query)

        if key in self.cache:
            self.cache[key]["hits"] = self.cache[key].get("hits", 0) + 1
            self.cache[key]["last_hit"] = datetime.now().isoformat()
            self._save_cache()

    def get_savings_estimate(self) -> Dict:
        """
        Estimate cost savings from cache.

        Returns:
            Dictionary with savings statistics
        """
        total_hits = sum(entry.get("hits", 0) for entry in self.cache.values())

        # Estimate: ~800 tokens per cached request at €0.002/request
        estimated_cost_per_request = 0.002
        total_savings = total_hits * estimated_cost_per_request

        return {
            "total_cache_hits": total_hits,
            "estimated_cost_per_miss": estimated_cost_per_request,
            "total_savings_eur": round(total_savings, 2),
            "average_hit_rate": round(self.get_hit_rate(), 1)
        }