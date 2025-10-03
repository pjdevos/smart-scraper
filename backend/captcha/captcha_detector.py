"""
CAPTCHA Detector - Detects if a CAPTCHA is present on the page
"""
from typing import Optional, Dict
from utils.logger import get_logger

logger = get_logger(__name__)


class CaptchaDetector:
    """Detects various types of CAPTCHAs"""

    # Common CAPTCHA indicators
    CAPTCHA_INDICATORS = {
        'recaptcha': [
            'g-recaptcha',
            'recaptcha',
            'grecaptcha',
            'data-sitekey',
            'rc-anchor',
        ],
        'hcaptcha': [
            'h-captcha',
            'hcaptcha',
            'data-hcaptcha',
        ],
        'cloudflare': [
            'cf-challenge',
            'cf-browser-verification',
            'cf_chl_opt',
            'Checking your browser',
        ],
        'generic': [
            'captcha',
            'challenge',
            'verification',
            'prove you are human',
        ]
    }

    @staticmethod
    def detect(html: str) -> Dict[str, any]:
        """
        Detect if CAPTCHA is present in HTML.

        Args:
            html: HTML content

        Returns:
            Dictionary with detection results
        """
        html_lower = html.lower()

        detected_types = []

        # Check for each CAPTCHA type
        for captcha_type, indicators in CaptchaDetector.CAPTCHA_INDICATORS.items():
            for indicator in indicators:
                if indicator.lower() in html_lower:
                    if captcha_type not in detected_types:
                        detected_types.append(captcha_type)
                    break

        if detected_types:
            logger.warning(f"CAPTCHA detected: {', '.join(detected_types)}")
            return {
                'detected': True,
                'types': detected_types,
                'primary_type': detected_types[0] if detected_types else None
            }

        return {
            'detected': False,
            'types': [],
            'primary_type': None
        }

    @staticmethod
    def detect_in_page(page) -> Dict[str, any]:
        """
        Detect CAPTCHA in live page (Playwright/Selenium).

        Args:
            page: Page object

        Returns:
            Dictionary with detection results
        """
        try:
            # Get page content
            if hasattr(page, 'content'):  # Playwright
                html = page.content()
            elif hasattr(page, 'page_source'):  # Selenium
                html = page.page_source
            else:
                return {'detected': False, 'types': [], 'primary_type': None}

            # Use HTML detection
            result = CaptchaDetector.detect(html)

            # Additional live checks for Playwright
            if hasattr(page, 'query_selector'):
                # Check for reCAPTCHA iframe
                if page.query_selector('iframe[src*="recaptcha"]'):
                    if 'recaptcha' not in result['types']:
                        result['types'].append('recaptcha')
                        result['detected'] = True

                # Check for hCaptcha iframe
                if page.query_selector('iframe[src*="hcaptcha"]'):
                    if 'hcaptcha' not in result['types']:
                        result['types'].append('hcaptcha')
                        result['detected'] = True

            return result

        except Exception as e:
            logger.error(f"Error detecting CAPTCHA in page: {e}")
            return {'detected': False, 'types': [], 'primary_type': None}

    @staticmethod
    def is_blocked(html: str) -> bool:
        """
        Check if we're blocked (403, 429, etc.).

        Args:
            html: HTML content

        Returns:
            True if blocked
        """
        blocking_indicators = [
            '403 forbidden',
            'access denied',
            '429 too many requests',
            'rate limit exceeded',
            'temporarily blocked',
            'unusual traffic',
            'automated requests',
        ]

        html_lower = html.lower()
        for indicator in blocking_indicators:
            if indicator in html_lower:
                logger.warning(f"Blocking detected: {indicator}")
                return True

        return False