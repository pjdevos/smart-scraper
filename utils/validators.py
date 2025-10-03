"""
Input Validators
"""
import re
from urllib.parse import urlparse
from typing import Tuple


def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url or not url.strip():
        return False, "URL cannot be empty"

    url = url.strip()

    # Check if URL has a scheme
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "Invalid URL format"

        # Check for valid scheme
        if result.scheme not in ['http', 'https']:
            return False, "URL must use http or https"

        return True, url  # Return normalized URL

    except Exception as e:
        return False, f"Invalid URL: {str(e)}"


def validate_query(query: str) -> Tuple[bool, str]:
    """
    Validate natural language query.

    Args:
        query: Query to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not query or not query.strip():
        return False, "Query cannot be empty"

    query = query.strip()

    # Check minimum length
    if len(query) < 3:
        return False, "Query must be at least 3 characters"

    # Check maximum length
    if len(query) > 500:
        return False, "Query must be less than 500 characters"

    return True, ""


def validate_budget(budget: float) -> Tuple[bool, str]:
    """
    Validate budget value.

    Args:
        budget: Budget value to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        budget = float(budget)
        if budget <= 0:
            return False, "Budget must be greater than 0"
        if budget > 1000:
            return False, "Budget must be less than €1000"
        return True, ""
    except (ValueError, TypeError):
        return False, "Budget must be a valid number"