"""
BeautifulSoup-based Data Extractor
"""
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from utils.logger import get_logger

logger = get_logger(__name__)


class BS4Extractor:
    """Extract data using BeautifulSoup and CSS selectors"""

    @staticmethod
    def extract_with_selectors(
        html: str,
        selectors: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """
        Extract data using CSS selectors.

        Args:
            html: HTML content
            selectors: Dictionary mapping field names to CSS selectors

        Returns:
            List of dictionaries containing extracted data
        """
        soup = BeautifulSoup(html, 'lxml')
        results = []

        # Find the common parent container
        # Try to find all items (e.g., all products, all articles)
        first_selector = list(selectors.values())[0]

        try:
            # Try to find parent containers
            first_elements = soup.select(first_selector)

            if not first_elements:
                logger.warning(f"No elements found for selector: {first_selector}")
                return []

            # Determine common parent
            # For simplicity, we'll assume all selectors are at the same level
            # or we need to extract from multiple items

            # Try extracting from each potential item
            # Find common ancestor of all selectors
            max_items = len(first_elements)

            for i in range(max_items):
                item_data = {}

                for field_name, selector in selectors.items():
                    elements = soup.select(selector)

                    if i < len(elements):
                        element = elements[i]
                        # Extract text content
                        text = element.get_text(strip=True)
                        item_data[field_name] = text
                    else:
                        item_data[field_name] = ""

                # Only add if we got at least some data
                if any(item_data.values()):
                    results.append(item_data)

            logger.info(f"Extracted {len(results)} items using BeautifulSoup")
            return results

        except Exception as e:
            logger.error(f"Error extracting with selectors: {e}")
            return []

    @staticmethod
    def extract_common_selectors(html: str, query: str) -> Optional[List[Dict[str, str]]]:
        """
        Try common CSS selectors based on query.

        Args:
            html: HTML content
            query: Natural language query

        Returns:
            Extracted data or None
        """
        soup = BeautifulSoup(html, 'lxml')
        query_lower = query.lower()

        # Common selectors for different data types
        common_selectors = {
            'product': {
                'selectors': {
                    'name': ['.product-name', '.product-title', 'h2.title', '.title'],
                    'price': ['.product-price', '.price', '.cost', '[itemprop="price"]'],
                    'rating': ['.rating', '.stars', '[itemprop="ratingValue"]']
                }
            },
            'article': {
                'selectors': {
                    'title': ['h1', 'h2.title', '.article-title', '.post-title'],
                    'author': ['.author', '.by-author', '[rel="author"]'],
                    'date': ['.date', '.published', 'time', '[datetime]']
                }
            }
        }

        # Try to match query to common patterns
        if any(word in query_lower for word in ['product', 'price', 'shop', 'buy']):
            # Try product selectors
            for field, selector_list in common_selectors['product']['selectors'].items():
                for selector in selector_list:
                    elements = soup.select(selector)
                    if elements:
                        logger.info(f"Found common selector for {field}: {selector}")
                        # Found something, return partial results
                        break

        return None  # No common selectors worked