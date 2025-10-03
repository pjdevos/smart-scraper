"""
Background Scraper Worker Thread
"""
from PyQt6.QtCore import QThread, pyqtSignal
from backend.scraper_engine import ScraperEngine, ScrapingMethod


class ScraperWorker(QThread):
    """Worker thread for background scraping"""

    # Signals
    progress = pyqtSignal(str, int)  # message, percentage
    finished = pyqtSignal(dict)  # result dictionary
    error = pyqtSignal(str)  # error message

    def __init__(
        self,
        url: str,
        query: str,
        method: ScrapingMethod,
        api_key: str = None,
        daily_budget: float = 5.0,
        stealth_level: str = "medium",
        use_proxies: bool = False,
        respect_robots: bool = True,
        enable_pagination: bool = False,
        max_pages: int = 5
    ):
        """
        Initialize worker.

        Args:
            url: Target URL
            query: Natural language query
            method: Scraping method
            api_key: Anthropic API key
            daily_budget: Daily budget limit
            stealth_level: Stealth level (basic, medium, high, maximum)
            use_proxies: Use proxy rotation
            respect_robots: Respect robots.txt
            enable_pagination: Enable multi-page scraping
            max_pages: Maximum pages to scrape
        """
        super().__init__()
        self.url = url
        self.query = query
        self.method = method
        self.api_key = api_key
        self.daily_budget = daily_budget
        self.stealth_level = stealth_level
        self.use_proxies = use_proxies
        self.respect_robots = respect_robots
        self.enable_pagination = enable_pagination
        self.max_pages = max_pages

    def run(self):
        """Run scraping in background"""
        try:
            # Create engine with progress callback
            engine = ScraperEngine(
                api_key=self.api_key,
                daily_budget=self.daily_budget,
                progress_callback=self._progress_callback,
                stealth_level=self.stealth_level,
                use_proxies=self.use_proxies,
                respect_robots=self.respect_robots
            )

            # Run scraping (with or without pagination)
            if self.enable_pagination:
                result = engine.scrape_with_pagination(
                    base_url=self.url,
                    query=self.query,
                    max_pages=self.max_pages,
                    method=self.method,
                    page_delay=2.0
                )
            else:
                result = engine.scrape(self.url, self.query, self.method)

            # Emit result
            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))

    def _progress_callback(self, message: str, percentage: int):
        """Progress callback from engine"""
        self.progress.emit(message, percentage)