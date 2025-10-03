"""
Helper utilities
"""
import hashlib
from typing import Any
from urllib.parse import urlparse


def get_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: Full URL

    Returns:
        Domain name (e.g., "example.com")
    """
    parsed = urlparse(url)
    return parsed.netloc or parsed.path


def create_cache_key(url: str, query: str) -> str:
    """
    Create a unique cache key for URL + query combination.

    Args:
        url: Target URL
        query: Natural language query

    Returns:
        MD5 hash key
    """
    combined = f"{url}::{query}"
    return hashlib.md5(combined.encode()).hexdigest()


def minimize_html(html: str, max_length: int = 3000, query: str = "") -> str:
    """
    Minimize HTML for LLM processing using intelligent snippet extraction.

    Args:
        html: Raw HTML content
        max_length: Maximum length to keep
        query: User query (helps identify relevant content)

    Returns:
        Minimized HTML snippet
    """
    # Use smart minimizer for better results
    from utils.html_minimizer import HTMLMinimizer
    return HTMLMinimizer.minimize(html, max_length, query)


def format_currency(amount: float) -> str:
    """
    Format amount as currency.

    Args:
        amount: Amount to format

    Returns:
        Formatted string (e.g., "€2.35")
    """
    return f"€{amount:.4f}"