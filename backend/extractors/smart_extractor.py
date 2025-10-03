"""
LLM-based Smart Data Extractor
"""
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from utils.logger import get_logger

logger = get_logger(__name__)


class SmartExtractor:
    """
    LLM-powered intelligent data extractor.

    This extractor uses Claude API to:
    1. Analyze HTML structure
    2. Identify appropriate CSS selectors
    3. Extract data intelligently
    """

    def __init__(self, claude_client):
        """
        Initialize smart extractor.

        Args:
            claude_client: ClaudeClient instance
        """
        self.claude = claude_client

    def extract(
        self,
        html: str,
        query: str,
        url: str = ""
    ) -> Dict[str, any]:
        """
        Extract data using LLM intelligence.

        Args:
            html: HTML content
            query: Natural language query
            url: Original URL (for context)

        Returns:
            Dictionary containing:
                - selectors: Dict mapping field names to CSS selectors
                - data: List of extracted data dictionaries
                - cost: API cost for this extraction
        """
        try:
            # Get selectors from LLM
            response = self.claude.find_selectors(html, query, url)

            if not response or 'selectors' not in response:
                logger.error("LLM did not return selectors")
                return {
                    'selectors': {},
                    'data': [],
                    'cost': 0.0
                }

            selectors = response['selectors']
            cost = response.get('cost', 0.0)

            logger.info(f"LLM found selectors: {selectors}")

            # Extract data using the identified selectors
            data = self._extract_with_selectors(html, selectors)

            return {
                'selectors': selectors,
                'data': data,
                'cost': cost
            }

        except Exception as e:
            logger.error(f"Error in smart extraction: {e}")
            return {
                'selectors': {},
                'data': [],
                'cost': 0.0
            }

    def _extract_with_selectors(
        self,
        html: str,
        selectors: Dict[str, str]
    ) -> List[Dict[str, str]]:
        """
        Extract data using provided selectors.

        Args:
            html: HTML content
            selectors: Dictionary mapping field names to CSS selectors

        Returns:
            List of extracted data dictionaries
        """
        from .bs4_extractor import BS4Extractor
        return BS4Extractor.extract_with_selectors(html, selectors)