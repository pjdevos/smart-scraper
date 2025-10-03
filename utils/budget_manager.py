"""
API Budget Manager - Tracks API costs and enforces budget limits
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
from config.settings import (
    DATA_DIR,
    DEFAULT_DAILY_BUDGET,
    BUDGET_WARNING_THRESHOLD,
    SONNET_INPUT_COST,
    SONNET_OUTPUT_COST,
    HAIKU_INPUT_COST,
    HAIKU_OUTPUT_COST
)
from .logger import get_logger

logger = get_logger(__name__)


class BudgetManager:
    """Manages API usage budget and cost tracking"""

    def __init__(self, daily_budget: float = DEFAULT_DAILY_BUDGET):
        """
        Initialize budget manager.

        Args:
            daily_budget: Daily budget limit in EUR/USD
        """
        self.daily_budget = daily_budget
        self.budget_file = DATA_DIR / "budget_tracker.json"
        self.usage_data = self._load_usage_data()

    def _load_usage_data(self) -> Dict:
        """Load usage data from file"""
        if self.budget_file.exists():
            try:
                with open(self.budget_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading budget data: {e}")

        return {
            "daily_usage": {},
            "total_usage": 0.0,
            "total_requests": 0
        }

    def _save_usage_data(self):
        """Save usage data to file"""
        try:
            with open(self.budget_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving budget data: {e}")

    def _get_today_key(self) -> str:
        """Get today's date key"""
        return datetime.now().strftime("%Y-%m-%d")

    def _clean_old_data(self):
        """Remove usage data older than 30 days"""
        cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        old_keys = [k for k in self.usage_data["daily_usage"].keys() if k < cutoff_date]
        for key in old_keys:
            del self.usage_data["daily_usage"][key]

    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        model: str = "sonnet"
    ) -> float:
        """
        Calculate cost for token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model used ("sonnet" or "haiku")

        Returns:
            Cost in EUR/USD
        """
        if model.lower() == "haiku":
            input_cost = (input_tokens / 1_000_000) * HAIKU_INPUT_COST
            output_cost = (output_tokens / 1_000_000) * HAIKU_OUTPUT_COST
        else:  # sonnet
            input_cost = (input_tokens / 1_000_000) * SONNET_INPUT_COST
            output_cost = (output_tokens / 1_000_000) * SONNET_OUTPUT_COST

        return input_cost + output_cost

    def track_usage(
        self,
        input_tokens: int,
        output_tokens: int,
        model: str = "sonnet"
    ) -> float:
        """
        Track API usage and return cost.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model used

        Returns:
            Cost of this request
        """
        cost = self.calculate_cost(input_tokens, output_tokens, model)
        today = self._get_today_key()

        # Update daily usage
        if today not in self.usage_data["daily_usage"]:
            self.usage_data["daily_usage"][today] = {
                "cost": 0.0,
                "requests": 0,
                "input_tokens": 0,
                "output_tokens": 0
            }

        self.usage_data["daily_usage"][today]["cost"] += cost
        self.usage_data["daily_usage"][today]["requests"] += 1
        self.usage_data["daily_usage"][today]["input_tokens"] += input_tokens
        self.usage_data["daily_usage"][today]["output_tokens"] += output_tokens

        # Update totals
        self.usage_data["total_usage"] += cost
        self.usage_data["total_requests"] += 1

        # Clean old data and save
        self._clean_old_data()
        self._save_usage_data()

        logger.info(f"API usage tracked: €{cost:.4f} ({input_tokens} in, {output_tokens} out)")

        return cost

    def get_today_usage(self) -> Dict:
        """Get today's usage statistics"""
        today = self._get_today_key()
        return self.usage_data["daily_usage"].get(today, {
            "cost": 0.0,
            "requests": 0,
            "input_tokens": 0,
            "output_tokens": 0
        })

    def get_remaining_budget(self) -> float:
        """Get remaining budget for today"""
        today_usage = self.get_today_usage()
        return max(0, self.daily_budget - today_usage["cost"])

    def is_budget_exceeded(self) -> bool:
        """Check if daily budget is exceeded"""
        return self.get_remaining_budget() <= 0

    def should_warn(self) -> bool:
        """Check if we should warn about approaching budget limit"""
        today_usage = self.get_today_usage()
        return today_usage["cost"] >= (self.daily_budget * BUDGET_WARNING_THRESHOLD)

    def get_total_stats(self) -> Dict:
        """Get total usage statistics"""
        return {
            "total_cost": self.usage_data["total_usage"],
            "total_requests": self.usage_data["total_requests"],
            "days_tracked": len(self.usage_data["daily_usage"])
        }

    def reset_today(self):
        """Reset today's usage (for testing/debugging)"""
        today = self._get_today_key()
        if today in self.usage_data["daily_usage"]:
            del self.usage_data["daily_usage"][today]
            self._save_usage_data()
            logger.info("Today's usage reset")