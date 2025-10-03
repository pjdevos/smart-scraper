"""
Prompt Builder for Claude API
"""
from typing import Dict
from utils.helpers import minimize_html, get_domain


class PromptBuilder:
    """Build optimized prompts for Claude API"""

    @staticmethod
    def build_selector_prompt(html: str, query: str, url: str = "") -> str:
        """
        Build prompt for finding CSS selectors.

        Args:
            html: Minimized HTML content
            query: Natural language query
            url: Original URL (for context)

        Returns:
            Formatted prompt string
        """
        domain = get_domain(url) if url else "the website"

        prompt = f"""You are a web scraping expert. Analyze the following HTML and identify the CSS selectors needed to extract the requested data.

URL: {url}
Domain: {domain}

User wants to extract: {query}

HTML content (minimized):
```html
{html}
```

Your task:
1. Analyze the HTML structure
2. Identify the CSS selectors for each requested field
3. Return ONLY a JSON object with field names as keys and CSS selectors as values

Requirements:
- Use specific, unique CSS selectors (prefer class selectors or IDs)
- If multiple items exist (like product listings), provide selectors that will match all items
- Keep selectors as simple as possible while remaining accurate
- Field names should match the user's query (e.g., if they ask for "product name", use "product_name")

Return format (JSON only, no explanation):
{{
    "field_name_1": ".css-selector-1",
    "field_name_2": "#css-selector-2",
    ...
}}

Example:
If user asks for "product name and price", return:
{{
    "product_name": ".product-title",
    "price": ".product-price"
}}"""

        return prompt

    @staticmethod
    def build_extraction_prompt(html: str, query: str, url: str = "") -> str:
        """
        Build prompt for direct data extraction (alternative approach).

        Args:
            html: Minimized HTML content
            query: Natural language query
            url: Original URL

        Returns:
            Formatted prompt string
        """
        domain = get_domain(url) if url else "the website"

        prompt = f"""You are a web scraping expert. Extract the requested data from the following HTML.

URL: {url}
Domain: {domain}

User wants to extract: {query}

HTML content (minimized):
```html
{html}
```

Extract the requested data and return it as a JSON array of objects.

Return format (JSON only, no explanation):
[
    {{
        "field_1": "value_1",
        "field_2": "value_2"
    }},
    ...
]

If only one item is found, still return an array with one object.
If no data is found, return an empty array: []"""

        return prompt