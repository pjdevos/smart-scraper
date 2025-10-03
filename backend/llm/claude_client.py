"""
Claude API Client
"""
import requests
import json
from typing import Dict, Optional, Any
from config.settings import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    DEFAULT_TIMEOUT
)
from utils.logger import get_logger
from utils.budget_manager import BudgetManager
from utils.helpers import minimize_html
from .prompt_builder import PromptBuilder
from .response_parser import ResponseParser

logger = get_logger(__name__)


class ClaudeClient:
    """Client for interacting with Claude API"""

    API_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def __init__(self, api_key: str = None, budget_manager: BudgetManager = None):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key (defaults to config)
            budget_manager: Budget manager instance
        """
        self.api_key = api_key or ANTHROPIC_API_KEY

        if not self.api_key:
            raise ValueError("Anthropic API key not provided")

        self.budget_manager = budget_manager or BudgetManager()
        self.prompt_builder = PromptBuilder()
        self.parser = ResponseParser()

    def _make_request(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.0
    ) -> Optional[Dict[str, Any]]:
        """
        Make request to Claude API.

        Args:
            prompt: Prompt text
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation

        Returns:
            API response dictionary or None
        """
        # Check budget first
        if self.budget_manager.is_budget_exceeded():
            logger.error("Daily budget exceeded!")
            return None

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "content-type": "application/json"
        }

        data = {
            "model": CLAUDE_MODEL,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            logger.info(f"Sending request to Claude API ({len(prompt)} chars)")

            response = requests.post(
                self.API_URL,
                headers=headers,
                json=data,
                timeout=DEFAULT_TIMEOUT
            )

            response.raise_for_status()
            result = response.json()

            # Track usage
            usage = result.get("usage", {})
            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)

            cost = self.budget_manager.track_usage(input_tokens, output_tokens, "sonnet")

            logger.info(f"Claude API response received (cost: €{cost:.4f})")

            return {
                "content": result.get("content", [{}])[0].get("text", ""),
                "cost": cost,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }

        except requests.exceptions.Timeout:
            logger.error("Claude API request timed out")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"Claude API HTTP error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            return None

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return None

    def find_selectors(
        self,
        html: str,
        query: str,
        url: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Find CSS selectors for extracting data.

        Args:
            html: HTML content
            query: Natural language query
            url: Original URL

        Returns:
            Dictionary with selectors and cost, or None
        """
        # Minimize HTML with query context
        minimized_html = minimize_html(html, max_length=3000, query=query)
        logger.info(f"Minimized HTML: {len(html)} -> {len(minimized_html)} chars ({100 - int(len(minimized_html)/len(html)*100)}% reduction)")

        # Build prompt
        prompt = self.prompt_builder.build_selector_prompt(
            minimized_html,
            query,
            url
        )

        # Make API request
        response = self._make_request(prompt, max_tokens=1024, temperature=0.0)

        if not response:
            return None

        # Parse response
        content = response["content"]
        selectors = self.parser.parse_json_response(content)

        if not selectors or not self.parser.validate_selectors(selectors):
            logger.error("Invalid selectors from Claude API")
            return None

        return {
            "selectors": selectors,
            "cost": response["cost"],
            "input_tokens": response["input_tokens"],
            "output_tokens": response["output_tokens"]
        }

    def extract_data(
        self,
        html: str,
        query: str,
        url: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Extract data directly using Claude (alternative to selector approach).

        Args:
            html: HTML content
            query: Natural language query
            url: Original URL

        Returns:
            Dictionary with extracted data and cost, or None
        """
        # Minimize HTML with query context
        minimized_html = minimize_html(html, max_length=3000, query=query)

        # Build prompt
        prompt = self.prompt_builder.build_extraction_prompt(
            minimized_html,
            query,
            url
        )

        # Make API request
        response = self._make_request(prompt, max_tokens=2048, temperature=0.0)

        if not response:
            return None

        # Parse response
        content = response["content"]
        data = self.parser.parse_json_response(content)

        if not data or not self.parser.validate_extracted_data(data):
            logger.error("Invalid data from Claude API")
            return None

        return {
            "data": data,
            "cost": response["cost"],
            "input_tokens": response["input_tokens"],
            "output_tokens": response["output_tokens"]
        }