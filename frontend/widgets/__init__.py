"""GUI widgets"""
from .url_input import URLInputWidget
from .query_input import QueryInputWidget
from .method_selector import MethodSelectorWidget
from .progress_widget import ProgressWidget
from .console_widget import ConsoleWidget
from .results_table import ResultsTable
from .stealth_settings import StealthSettingsWidget
from .cache_stats_widget import CacheStatsWidget
from .selector_stats_widget import SelectorStatsWidget
from .captcha_settings import CaptchaSettingsWidget
from .crawler_widget import CrawlerWidget

__all__ = [
    'URLInputWidget',
    'QueryInputWidget',
    'MethodSelectorWidget',
    'ProgressWidget',
    'ConsoleWidget',
    'ResultsTable',
    'StealthSettingsWidget',
    'CacheStatsWidget',
    'SelectorStatsWidget',
    'CaptchaSettingsWidget',
    'CrawlerWidget'
]
