"""
Learned CSS Selectors Manager
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List
from config.settings import DATA_DIR, SELECTOR_CACHE_EXPIRY_DAYS
from utils.logger import get_logger
from utils.helpers import get_domain

logger = get_logger(__name__)


class SelectorManager:
    """Manages learned CSS selectors per domain"""

    def __init__(self, selectors_file: Path = None):
        """
        Initialize selector manager.

        Args:
            selectors_file: Path to selectors file (default: data/learned_selectors.json)
        """
        self.selectors_file = selectors_file or DATA_DIR / "learned_selectors.json"
        self.selectors = self._load_selectors()

    def _load_selectors(self) -> Dict:
        """Load selectors from file"""
        if self.selectors_file.exists():
            try:
                with open(self.selectors_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading selectors: {e}")
                return {}
        return {}

    def _save_selectors(self):
        """Save selectors to file"""
        try:
            with open(self.selectors_file, 'w', encoding='utf-8') as f:
                json.dump(self.selectors, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving selectors: {e}")

    def _is_expired(self, timestamp: str) -> bool:
        """Check if selector entry is expired"""
        try:
            learned_time = datetime.fromisoformat(timestamp)
            expiry_time = learned_time + timedelta(days=SELECTOR_CACHE_EXPIRY_DAYS)
            return datetime.now() > expiry_time
        except Exception:
            return True

    def get(self, url: str, query: str) -> Optional[Dict[str, str]]:
        """
        Get learned selectors for domain + query.

        Args:
            url: Target URL
            query: Natural language query (e.g., "product name, price")

        Returns:
            Dictionary mapping field names to CSS selectors, or None
        """
        domain = get_domain(url)

        if domain in self.selectors:
            domain_data = self.selectors[domain]

            # Find matching query
            for entry in domain_data.get("queries", []):
                if entry["query"].lower() == query.lower():
                    # Check expiration
                    if not self._is_expired(entry.get("timestamp", "")):
                        logger.info(f"Found learned selectors for {domain}: {query}")
                        return entry["selectors"]
                    else:
                        logger.info(f"Selectors expired for {domain}: {query}")

        logger.info(f"No learned selectors for {domain}: {query}")
        return None

    def save(self, url: str, query: str, selectors: Dict[str, str]):
        """
        Save learned selectors for domain + query.

        Args:
            url: Target URL
            query: Natural language query
            selectors: Dictionary mapping field names to CSS selectors
        """
        domain = get_domain(url)

        if domain not in self.selectors:
            self.selectors[domain] = {
                "domain": domain,
                "queries": []
            }

        # Check if query already exists and update it
        query_found = False
        for entry in self.selectors[domain]["queries"]:
            if entry["query"].lower() == query.lower():
                entry["selectors"] = selectors
                entry["timestamp"] = datetime.now().isoformat()
                entry["success_count"] = entry.get("success_count", 0) + 1
                query_found = True
                break

        # Add new query if not found
        if not query_found:
            self.selectors[domain]["queries"].append({
                "query": query,
                "selectors": selectors,
                "timestamp": datetime.now().isoformat(),
                "success_count": 1
            })

        self._save_selectors()
        logger.info(f"Saved selectors for {domain}: {query}")

    def get_domain_queries(self, url: str) -> List[str]:
        """
        Get all queries we've learned for a domain.

        Args:
            url: Target URL

        Returns:
            List of query strings
        """
        domain = get_domain(url)
        if domain in self.selectors:
            return [entry["query"] for entry in self.selectors[domain]["queries"]]
        return []

    def clear_expired(self):
        """Remove all expired selector entries"""
        removed_count = 0

        for domain in list(self.selectors.keys()):
            queries = self.selectors[domain]["queries"]
            valid_queries = [
                q for q in queries
                if not self._is_expired(q.get("timestamp", ""))
            ]

            removed_count += len(queries) - len(valid_queries)
            self.selectors[domain]["queries"] = valid_queries

            # Remove domain if no queries left
            if not valid_queries:
                del self.selectors[domain]

        if removed_count > 0:
            self._save_selectors()
            logger.info(f"Removed {removed_count} expired selector entries")

    def get_stats(self) -> Dict:
        """Get selector statistics"""
        total_domains = len(self.selectors)
        total_queries = sum(len(d["queries"]) for d in self.selectors.values())

        # Calculate total uses
        total_uses = sum(
            entry.get("success_count", 0)
            for domain_data in self.selectors.values()
            for entry in domain_data.get("queries", [])
        )

        # Calculate total reuses (success_count - 1 for each query)
        total_reuses = sum(
            max(0, entry.get("success_count", 1) - 1)
            for domain_data in self.selectors.values()
            for entry in domain_data.get("queries", [])
        )

        return {
            "total_domains": total_domains,
            "total_queries": total_queries,
            "total_uses": total_uses,
            "total_reuses": total_reuses
        }

    def get_savings_estimate(self) -> Dict:
        """
        Estimate cost savings from learned selectors.

        Returns:
            Dictionary with savings statistics
        """
        stats = self.get_stats()

        # Each reuse saves €0.002 (cost of LLM call)
        cost_per_llm_call = 0.002
        total_savings = stats["total_reuses"] * cost_per_llm_call

        # Calculate efficiency
        if stats["total_uses"] > 0:
            reuse_rate = (stats["total_reuses"] / stats["total_uses"]) * 100
        else:
            reuse_rate = 0.0

        return {
            "learned_domains": stats["total_domains"],
            "learned_queries": stats["total_queries"],
            "total_reuses": stats["total_reuses"],
            "total_savings_eur": round(total_savings, 2),
            "reuse_rate": round(reuse_rate, 1),
            "cost_per_llm_call": cost_per_llm_call
        }

    def get_top_domains(self, limit: int = 5) -> List[Dict]:
        """
        Get top domains by usage.

        Args:
            limit: Maximum number of domains to return

        Returns:
            List of domain statistics
        """
        domain_stats = []

        for domain, domain_data in self.selectors.items():
            total_uses = sum(
                entry.get("success_count", 0)
                for entry in domain_data.get("queries", [])
            )

            domain_stats.append({
                "domain": domain,
                "queries": len(domain_data.get("queries", [])),
                "uses": total_uses
            })

        # Sort by uses
        domain_stats.sort(key=lambda x: x["uses"], reverse=True)

        return domain_stats[:limit]