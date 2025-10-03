"""
Regex-based Data Extractor
"""
import re
from typing import List, Dict
from utils.logger import get_logger

logger = get_logger(__name__)


class RegexExtractor:
    """Extract common data patterns using regex"""

    # Common regex patterns
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
        'url': r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)',
        'price': r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s?(?:USD|EUR|GBP|\$|€|£)',
        'date': r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',
        'number': r'\b\d+(?:,\d{3})*(?:\.\d+)?\b',
    }

    @classmethod
    def extract(cls, html: str, query: str) -> Dict[str, List[str]]:
        """
        Extract data using regex patterns.

        Args:
            html: HTML content
            query: Natural language query (used to determine what to extract)

        Returns:
            Dictionary mapping field names to extracted values
        """
        results = {}
        query_lower = query.lower()

        # Determine which patterns to use based on query
        patterns_to_use = {}

        if any(word in query_lower for word in ['email', 'mail', 'contact']):
            patterns_to_use['email'] = cls.PATTERNS['email']

        if any(word in query_lower for word in ['phone', 'tel', 'number', 'contact']):
            patterns_to_use['phone'] = cls.PATTERNS['phone']

        if any(word in query_lower for word in ['url', 'link', 'website']):
            patterns_to_use['url'] = cls.PATTERNS['url']

        if any(word in query_lower for word in ['price', 'cost', 'amount', '$', '€', '£']):
            patterns_to_use['price'] = cls.PATTERNS['price']

        if any(word in query_lower for word in ['date', 'time', 'when']):
            patterns_to_use['date'] = cls.PATTERNS['date']

        # Extract using selected patterns
        for name, pattern in patterns_to_use.items():
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                # Clean up matches (remove duplicates, limit results)
                unique_matches = list(set(matches))[:20]  # Max 20 results per pattern
                results[name] = unique_matches
                logger.info(f"Regex extracted {len(unique_matches)} {name}(s)")

        return results

    @classmethod
    def has_patterns(cls, query: str) -> bool:
        """
        Check if query matches any regex patterns.

        Args:
            query: Natural language query

        Returns:
            True if query matches known patterns
        """
        query_lower = query.lower()
        keywords = [
            'email', 'mail', 'phone', 'tel', 'contact',
            'url', 'link', 'website', 'price', 'cost',
            'amount', 'date', 'time'
        ]
        return any(keyword in query_lower for keyword in keywords)