"""
Claude API Response Parser
"""
import json
import re
from typing import Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


class ResponseParser:
    """Parse and validate Claude API responses"""

    @staticmethod
    def parse_json_response(response_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from Claude response.

        Args:
            response_text: Raw response text from Claude

        Returns:
            Parsed JSON dictionary or None
        """
        try:
            # Try direct JSON parsing first
            return json.loads(response_text)

        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```',
                                  response_text,
                                  re.DOTALL)

            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass

            # Try to find any JSON object or array in the response
            json_match = re.search(r'(\{.*?\}|\[.*?\])', response_text, re.DOTALL)

            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass

            logger.error(f"Could not parse JSON from response: {response_text[:200]}")
            return None

    @staticmethod
    def validate_selectors(selectors: Dict[str, str]) -> bool:
        """
        Validate CSS selectors dictionary.

        Args:
            selectors: Dictionary of field names to CSS selectors

        Returns:
            True if valid
        """
        if not isinstance(selectors, dict):
            logger.error("Selectors is not a dictionary")
            return False

        if not selectors:
            logger.error("Selectors dictionary is empty")
            return False

        for field, selector in selectors.items():
            if not isinstance(field, str) or not isinstance(selector, str):
                logger.error(f"Invalid selector format: {field} -> {selector}")
                return False

            if not selector.strip():
                logger.error(f"Empty selector for field: {field}")
                return False

        return True

    @staticmethod
    def validate_extracted_data(data: list) -> bool:
        """
        Validate extracted data array.

        Args:
            data: List of extracted data dictionaries

        Returns:
            True if valid
        """
        if not isinstance(data, list):
            logger.error("Extracted data is not a list")
            return False

        # Empty list is valid (no data found)
        if not data:
            return True

        # Check first item
        if not isinstance(data[0], dict):
            logger.error("Extracted data items are not dictionaries")
            return False

        return True