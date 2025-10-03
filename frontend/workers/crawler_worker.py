"""
Background Crawler Worker Thread
"""
from PyQt6.QtCore import QThread, pyqtSignal
from backend.crawler import WebCrawler


class CrawlerWorker(QThread):
    """Worker thread for background URL crawling"""

    # Signals
    progress_update = pyqtSignal(dict)  # Stats update (found/crawled/matched)
    url_found = pyqtSignal(str)  # Individual URL discovered
    finished = pyqtSignal(list)  # All discovered URLs
    error = pyqtSignal(str)  # Error occurred

    def __init__(
        self,
        start_url: str,
        max_pages: int = 500,
        max_depth: int = 3,
        pattern: str = None,
        internal_only: bool = True,
        respect_robots: bool = True,
        try_sitemap: bool = True,
        follow_pagination: bool = False,
        request_delay: float = 2.0
    ):
        """
        Initialize crawler worker.

        Args:
            start_url: Starting URL
            max_pages: Maximum pages to crawl
            max_depth: Maximum link depth (-1 for unlimited)
            pattern: Regex pattern for URL filtering
            internal_only: Only follow internal links
            respect_robots: Respect robots.txt
            try_sitemap: Try sitemap.xml first
            follow_pagination: Follow pagination links
            request_delay: Delay between requests
        """
        super().__init__()
        self.start_url = start_url
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.pattern = pattern
        self.internal_only = internal_only
        self.respect_robots = respect_robots
        self.try_sitemap = try_sitemap
        self.follow_pagination = follow_pagination
        self.request_delay = request_delay

        self.crawler = None

    def run(self):
        """Run crawling in background"""
        try:
            # Create crawler with progress callback
            self.crawler = WebCrawler(
                respect_robots=self.respect_robots,
                request_delay=self.request_delay
            )

            # Run crawling with callback for UI updates
            urls = self.crawler.crawl(
                start_url=self.start_url,
                max_pages=self.max_pages,
                max_depth=self.max_depth,
                pattern=self.pattern,
                internal_only=self.internal_only,
                try_sitemap=self.try_sitemap,
                follow_pagination=self.follow_pagination,
                callback=self._progress_callback
            )

            # Emit individual URLs
            for url in urls:
                self.url_found.emit(url)

            # Emit final result
            self.finished.emit(urls)

        except Exception as e:
            self.error.emit(str(e))

    def _progress_callback(self, stats: dict):
        """Progress callback from crawler"""
        self.progress_update.emit(stats)

    def pause(self):
        """Pause crawling"""
        if self.crawler:
            self.crawler.pause()

    def resume(self):
        """Resume crawling"""
        if self.crawler:
            self.crawler.resume()

    def stop(self):
        """Stop crawling"""
        if self.crawler:
            self.crawler.stop()
