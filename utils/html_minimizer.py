"""
Smart HTML Minimizer - Extracts only relevant snippets for LLM
"""
from bs4 import BeautifulSoup
import re
from typing import List, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class HTMLMinimizer:
    """Intelligently minimizes HTML to save LLM costs"""

    # Elements to remove (waste tokens)
    REMOVE_TAGS = [
        'script', 'style', 'noscript', 'iframe', 'svg',
        'nav', 'header', 'footer', 'aside',
        'form', 'button', 'input', 'textarea', 'select'
    ]

    # Main content selectors (in order of priority)
    MAIN_CONTENT_SELECTORS = [
        'main',
        'article',
        '[role="main"]',
        '.main-content',
        '#main-content',
        '.content',
        '#content',
        '.post-content',
        '.article-content',
        '.product-list',
        '.products',
        '.items',
        '.listings'
    ]

    # Repeated item patterns (for listings)
    ITEM_PATTERNS = [
        '.product',
        '.item',
        '.card',
        '.listing',
        '[class*="product"]',
        '[class*="item"]',
        'article',
        'li'
    ]

    @staticmethod
    def minimize(html: str, max_chars: int = 3000, query: str = "") -> str:
        """
        Minimize HTML intelligently for LLM processing.

        Args:
            html: Raw HTML content
            max_chars: Maximum characters to send to LLM
            query: User query (helps identify relevant content)

        Returns:
            Minimized HTML snippet
        """
        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception:
            # Fallback to html.parser
            soup = BeautifulSoup(html, 'html.parser')

        # Step 1: Remove unwanted elements
        for tag in HTMLMinimizer.REMOVE_TAGS:
            for element in soup.find_all(tag):
                element.decompose()

        # Remove comments
        for comment in soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in text):
            comment.extract()

        # Step 2: Find main content area
        main_content = HTMLMinimizer._find_main_content(soup)

        if main_content:
            logger.info(f"Found main content: {main_content.name}")
            content_html = str(main_content)
        else:
            # Fallback to body
            body = soup.find('body')
            content_html = str(body) if body else str(soup)

        # Step 3: If query suggests repeated items (listing), extract sample
        if HTMLMinimizer._is_listing_query(query):
            sample_html = HTMLMinimizer._extract_item_samples(main_content or soup, max_chars)
            if sample_html:
                logger.info("Extracted item samples for listing query")
                return sample_html

        # Step 4: Clean up and minimize
        minimized = HTMLMinimizer._clean_html(content_html)

        # Step 5: Truncate if still too long
        if len(minimized) > max_chars:
            logger.warning(f"HTML still too long ({len(minimized)} chars), truncating to {max_chars}")
            minimized = minimized[:max_chars] + "..."

        logger.info(f"Minimized HTML: {len(html)} → {len(minimized)} chars ({100 - int(len(minimized)/len(html)*100)}% reduction)")

        return minimized

    @staticmethod
    def _find_main_content(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """Find the main content area"""
        for selector in HTMLMinimizer.MAIN_CONTENT_SELECTORS:
            element = soup.select_one(selector)
            if element:
                return element
        return None

    @staticmethod
    def _is_listing_query(query: str) -> bool:
        """Check if query suggests a listing/repeated items"""
        if not query:
            return False

        listing_keywords = [
            'product', 'item', 'listing', 'article', 'post',
            'job', 'result', 'card', 'entry', 'all', 'list'
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in listing_keywords)

    @staticmethod
    def _extract_item_samples(soup: BeautifulSoup, max_chars: int = 3000) -> Optional[str]:
        """
        Extract sample items for listing queries.

        Instead of sending entire page, send 2-3 example items.
        """
        for pattern in HTMLMinimizer.ITEM_PATTERNS:
            items = soup.select(pattern)

            if len(items) >= 2:
                # Found repeated items!
                # Take first 2-3 items as samples
                sample_count = min(3, len(items))
                samples = items[:sample_count]

                # Build sample HTML
                sample_html = f"<!-- Found {len(items)} items, showing {sample_count} samples -->\n"

                for i, item in enumerate(samples, 1):
                    sample_html += f"<!-- Sample {i}/{sample_count} -->\n"
                    sample_html += str(item) + "\n\n"

                # Check if within limit
                if len(sample_html) <= max_chars:
                    logger.info(f"Extracted {sample_count} item samples using pattern: {pattern}")
                    return HTMLMinimizer._clean_html(sample_html)

        return None

    @staticmethod
    def _clean_html(html: str) -> str:
        """Final HTML cleanup"""
        # Remove attributes that waste tokens
        html = re.sub(r'\s+class="[^"]*"', '', html)
        html = re.sub(r'\s+id="[^"]*"', '', html)
        html = re.sub(r'\s+style="[^"]*"', '', html)
        html = re.sub(r'\s+data-[a-z-]+="[^"]*"', '', html)

        # Collapse whitespace
        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r'>\s+<', '><', html)

        return html.strip()

    @staticmethod
    def extract_with_context(html: str, query: str, max_chars: int = 3000) -> str:
        """
        Extract HTML with query context awareness.

        Args:
            html: Raw HTML
            query: User query (e.g., "product name and price")
            max_chars: Maximum characters

        Returns:
            Relevant HTML snippet
        """
        # Parse query for keywords
        query_lower = query.lower()
        keywords = []

        # Extract potential field names
        common_fields = [
            'name', 'title', 'price', 'cost', 'rating', 'review',
            'description', 'author', 'date', 'email', 'phone',
            'address', 'company', 'job', 'salary', 'location'
        ]

        for field in common_fields:
            if field in query_lower:
                keywords.append(field)

        logger.debug(f"Query keywords: {keywords}")

        # Use smart minimization with query context
        minimized = HTMLMinimizer.minimize(html, max_chars, query)

        return minimized