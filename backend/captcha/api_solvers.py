"""
API CAPTCHA Solvers
Integration with 2Captcha and Anti-Captcha services
"""
import time
import requests
import logging
from typing import Optional, Dict
from config.settings import TWOCAPTCHA_API_KEY, ANTICAPTCHA_API_KEY

logger = logging.getLogger(__name__)


class CaptchaSolver:
    """Base class for CAPTCHA solving services"""

    def solve(self, site_key: str, page_url: str, captcha_type: str = "recaptcha_v2") -> Optional[str]:
        """
        Solve CAPTCHA.

        Args:
            site_key: CAPTCHA site key
            page_url: Page URL where CAPTCHA appears
            captcha_type: Type of CAPTCHA (recaptcha_v2, recaptcha_v3, hcaptcha)

        Returns:
            CAPTCHA solution token or None
        """
        raise NotImplementedError


class TwoCaptchaSolver(CaptchaSolver):
    """2Captcha API solver"""

    API_URL = "https://2captcha.com"

    def __init__(self, api_key: str = None):
        """
        Initialize 2Captcha solver.

        Args:
            api_key: 2Captcha API key
        """
        self.api_key = api_key or TWOCAPTCHA_API_KEY
        if not self.api_key:
            raise ValueError("2Captcha API key not provided")

        logger.info("TwoCaptcha solver initialized")

    def solve(self, site_key: str, page_url: str, captcha_type: str = "recaptcha_v2") -> Optional[str]:
        """
        Solve CAPTCHA using 2Captcha API.

        Args:
            site_key: CAPTCHA site key
            page_url: Page URL
            captcha_type: CAPTCHA type

        Returns:
            Solution token or None
        """
        logger.info(f"Solving {captcha_type} via 2Captcha...")

        try:
            # Submit CAPTCHA
            captcha_id = self._submit_captcha(site_key, page_url, captcha_type)
            if not captcha_id:
                return None

            logger.info(f"CAPTCHA submitted, ID: {captcha_id}")

            # Poll for result
            solution = self._get_result(captcha_id)

            if solution:
                logger.info("✓ CAPTCHA solved successfully")
            else:
                logger.error("✗ CAPTCHA solving failed")

            return solution

        except Exception as e:
            logger.error(f"2Captcha error: {e}")
            return None

    def _submit_captcha(self, site_key: str, page_url: str, captcha_type: str) -> Optional[str]:
        """Submit CAPTCHA to 2Captcha"""

        # Map captcha types to 2Captcha methods
        method_map = {
            "recaptcha_v2": "userrecaptcha",
            "recaptcha_v3": "userrecaptcha",
            "hcaptcha": "hcaptcha"
        }

        method = method_map.get(captcha_type, "userrecaptcha")

        params = {
            "key": self.api_key,
            "method": method,
            "googlekey": site_key,
            "pageurl": page_url,
            "json": 1
        }

        # Additional params for v3
        if captcha_type == "recaptcha_v3":
            params["version"] = "v3"
            params["action"] = "verify"
            params["min_score"] = 0.3

        response = requests.post(f"{self.API_URL}/in.php", data=params, timeout=30)
        result = response.json()

        if result.get("status") == 1:
            return result.get("request")
        else:
            logger.error(f"2Captcha submit error: {result.get('request')}")
            return None

    def _get_result(self, captcha_id: str, timeout: int = 120) -> Optional[str]:
        """Poll for CAPTCHA result"""

        params = {
            "key": self.api_key,
            "action": "get",
            "id": captcha_id,
            "json": 1
        }

        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(5)  # Wait 5 seconds between polls

            response = requests.get(f"{self.API_URL}/res.php", params=params, timeout=30)
            result = response.json()

            if result.get("status") == 1:
                return result.get("request")
            elif result.get("request") == "CAPCHA_NOT_READY":
                continue
            else:
                logger.error(f"2Captcha result error: {result.get('request')}")
                return None

        logger.error("2Captcha timeout")
        return None

    def get_balance(self) -> Optional[float]:
        """Get account balance"""
        try:
            params = {
                "key": self.api_key,
                "action": "getbalance",
                "json": 1
            }

            response = requests.get(f"{self.API_URL}/res.php", params=params, timeout=30)
            result = response.json()

            if result.get("status") == 1:
                balance = float(result.get("request", 0))
                logger.info(f"2Captcha balance: ${balance:.2f}")
                return balance
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None


class AntiCaptchaSolver(CaptchaSolver):
    """Anti-Captcha API solver"""

    API_URL = "https://api.anti-captcha.com"

    def __init__(self, api_key: str = None):
        """
        Initialize Anti-Captcha solver.

        Args:
            api_key: Anti-Captcha API key
        """
        self.api_key = api_key or ANTICAPTCHA_API_KEY
        if not self.api_key:
            raise ValueError("Anti-Captcha API key not provided")

        logger.info("Anti-Captcha solver initialized")

    def solve(self, site_key: str, page_url: str, captcha_type: str = "recaptcha_v2") -> Optional[str]:
        """
        Solve CAPTCHA using Anti-Captcha API.

        Args:
            site_key: CAPTCHA site key
            page_url: Page URL
            captcha_type: CAPTCHA type

        Returns:
            Solution token or None
        """
        logger.info(f"Solving {captcha_type} via Anti-Captcha...")

        try:
            # Submit CAPTCHA
            task_id = self._submit_captcha(site_key, page_url, captcha_type)
            if not task_id:
                return None

            logger.info(f"CAPTCHA submitted, Task ID: {task_id}")

            # Poll for result
            solution = self._get_result(task_id)

            if solution:
                logger.info("✓ CAPTCHA solved successfully")
            else:
                logger.error("✗ CAPTCHA solving failed")

            return solution

        except Exception as e:
            logger.error(f"Anti-Captcha error: {e}")
            return None

    def _submit_captcha(self, site_key: str, page_url: str, captcha_type: str) -> Optional[int]:
        """Submit CAPTCHA to Anti-Captcha"""

        # Map captcha types to Anti-Captcha task types
        type_map = {
            "recaptcha_v2": "RecaptchaV2TaskProxyless",
            "recaptcha_v3": "RecaptchaV3TaskProxyless",
            "hcaptcha": "HCaptchaTaskProxyless"
        }

        task_type = type_map.get(captcha_type, "RecaptchaV2TaskProxyless")

        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": task_type,
                "websiteURL": page_url,
                "websiteKey": site_key
            }
        }

        # Additional params for v3
        if captcha_type == "recaptcha_v3":
            payload["task"]["minScore"] = 0.3
            payload["task"]["pageAction"] = "verify"

        response = requests.post(
            f"{self.API_URL}/createTask",
            json=payload,
            timeout=30
        )
        result = response.json()

        if result.get("errorId") == 0:
            return result.get("taskId")
        else:
            logger.error(f"Anti-Captcha submit error: {result.get('errorDescription')}")
            return None

    def _get_result(self, task_id: int, timeout: int = 120) -> Optional[str]:
        """Poll for CAPTCHA result"""

        payload = {
            "clientKey": self.api_key,
            "taskId": task_id
        }

        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(5)  # Wait 5 seconds between polls

            response = requests.post(
                f"{self.API_URL}/getTaskResult",
                json=payload,
                timeout=30
            )
            result = response.json()

            if result.get("errorId") == 0:
                if result.get("status") == "ready":
                    solution = result.get("solution", {})
                    return solution.get("gRecaptchaResponse")
                elif result.get("status") == "processing":
                    continue
            else:
                logger.error(f"Anti-Captcha result error: {result.get('errorDescription')}")
                return None

        logger.error("Anti-Captcha timeout")
        return None

    def get_balance(self) -> Optional[float]:
        """Get account balance"""
        try:
            payload = {
                "clientKey": self.api_key
            }

            response = requests.post(
                f"{self.API_URL}/getBalance",
                json=payload,
                timeout=30
            )
            result = response.json()

            if result.get("errorId") == 0:
                balance = float(result.get("balance", 0))
                logger.info(f"Anti-Captcha balance: ${balance:.2f}")
                return balance
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None


def get_solver(service: str = "2captcha") -> Optional[CaptchaSolver]:
    """
    Get CAPTCHA solver instance.

    Args:
        service: Service name ("2captcha" or "anticaptcha")

    Returns:
        Solver instance or None
    """
    try:
        if service == "2captcha":
            if TWOCAPTCHA_API_KEY:
                return TwoCaptchaSolver()
            else:
                logger.warning("2Captcha API key not configured")
                return None

        elif service == "anticaptcha":
            if ANTICAPTCHA_API_KEY:
                return AntiCaptchaSolver()
            else:
                logger.warning("Anti-Captcha API key not configured")
                return None

        else:
            logger.error(f"Unknown CAPTCHA service: {service}")
            return None

    except Exception as e:
        logger.error(f"Error initializing solver: {e}")
        return None
