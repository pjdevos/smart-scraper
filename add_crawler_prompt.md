Add a Web Crawler feature to the existing SmartScraper application.

CONTEXT:
SmartScraper currently scrapes individual URLs or URL lists. I want to add a third mode where users can automatically discover URLs by crawling a website.

REQUIREMENTS:

1. ADD CRAWLER MODE TAB:
   Location: frontend/main_window.py
   
   Current tabs:
   - "📄 Single URL"
   - "📋 URL List"
   
   Add new tab:
   - "🕷️ Crawl Site"

2. CRAWLER CONFIGURATION UI:
   Create: frontend/widgets/crawler_widget.py
   
   Fields needed:
   - Start URL input field
   - "What to Extract" textarea (same as single mode)
   - Max Pages dropdown (50/100/500/1000/unlimited)
   - Max Depth dropdown (1/2/3/5/unlimited)
   - URL Pattern Filter input (regex, e.g., "/product/\d+")
   
   Checkboxes:
   ☑ Follow internal links only
   ☑ Respect robots.txt
   ☑ Parse sitemap.xml first (faster!)
   ☑ Follow pagination links
   
   Buttons:
   - "🔍 Start Crawling" (primary button)
   - "💾 Load Saved URLs" (secondary button)

3. CRAWLER PROGRESS DISPLAY:
   Show real-time stats:
   - URLs Found: 347
   - URLs Crawled: 250
   - URLs Matched: 189 (pattern matches)
   
   Progress bar with percentage
   Estimated time remaining
   
   Control buttons:
   - ⏸️ Pause
   - ⏹️ Stop
   - 📊 View Log

4. URL PREVIEW PANEL:
   Show discovered URLs in a scrollable list:
   - Checkbox for each URL (select which to scrape)
   - Display URL
   - Badge showing crawl depth/page number
   - Filter/search box
   
   Action buttons:
   - 💾 Save URL List (export to .txt)
   - 🚀 Start Scraping All (proceed to scraping)

5. BACKEND CRAWLER CLASS:
   Create: backend/crawler/web_crawler.py
```python
   class WebCrawler:
       def crawl(self, start_url, max_pages=500, max_depth=3, 
                 pattern=None, callback=None):
           """
           Discover URLs by following links
           
           Args:
               start_url: Where to start
               max_pages: Maximum pages to crawl
               max_depth: Maximum link depth
               pattern: Regex pattern for URL filtering
               callback: Function called with progress updates
           
           Returns:
               List[str]: All discovered URLs matching pattern
           """
           
       def _try_sitemap(self, start_url):
           """Try to parse sitemap.xml first (much faster!)"""
           
       def _is_internal(self, url, base_url):
           """Check if URL is internal link"""
           
       def _matches_pattern(self, url, pattern):
           """Check if URL matches regex pattern"""

Features:

Try sitemap.xml first (5 sec vs 5 min)
Follow only internal links
Respect robots.txt
Rate limiting (1-2s delay between requests)
Deduplication (track visited URLs)
Pattern matching (regex filter)
Progress callbacks for UI updates


CRAWLER WORKER THREAD:
Create: frontend/workers/crawler_worker.py

python   class CrawlerWorker(QThread):
       progress_update = pyqtSignal(dict)  # Stats update
       url_found = pyqtSignal(str)         # New URL discovered
       finished = pyqtSignal(list)         # All URLs
       error = pyqtSignal(str)             # Error occurred
       
       def run(self):
           """Run crawler in background thread"""
Must emit signals for:

Progress updates (found/crawled/matched counts)
Individual URL discoveries (for live list update)
Completion (final URL list)
Errors (with helpful messages)


INTEGRATION WITH EXISTING SCRAPER:
After crawling completes:

Show "Start Scraping All" button
When clicked, use existing ScraperWorker
Process URLs one by one
Use same 4-phase pipeline
Show progress: "Scraping 45/189..."
Use learned selectors after first URL!


COLOR SCHEME (Toggl-inspired):
Use existing colors from the app:

Primary: #E0A6D8 (soft purple)
Secondary: #F4D4A6 (soft yellow)
Accent: #B8D4A6 (soft green)
Dark: #2C1338 (aubergine)
Background: #FFF5F0 (cream)


INFO BOX:
Add helpful explanation at top of crawler mode:

   💡 Crawler Mode
   Automatically discover URLs by following links. 
   Perfect for scraping entire product catalogs, 
   blog archives, or listing sites.

ERROR HANDLING:

Invalid start URL → Show error message
No URLs found → "No matching URLs found. Try different pattern?"
Robots.txt blocks → "Site blocks crawlers. Use Single URL mode."
Network errors → Retry with exponential backoff


COST ESTIMATION:
After crawling, show:
"Ready to scrape 189 URLs
Estimated cost: €0.003 - €0.57
With caching: First page €0.003, rest €0.00
Estimated time: 2-15 minutes"

FILES TO CREATE/MODIFY:
CREATE:

backend/crawler/init.py
backend/crawler/web_crawler.py
frontend/widgets/crawler_widget.py
frontend/workers/crawler_worker.py

MODIFY:

frontend/main_window.py (add crawler tab)
config/settings.py (add crawler settings)

DEPENDENCIES (add to requirements.txt if missing):

urllib.robotparser (stdlib)
re (stdlib, for regex patterns)

TESTING:
Test with these sites:

Easy: https://books.toscrape.com/ (no protection)
Medium: https://scrapethissite.com/ (some JS)
Has sitemap: Most modern sites

EXAMPLE USAGE:

User selects "🕷️ Crawl Site" tab
Enters: https://shop.com/products
Pattern: /product/\d+
Max Pages: 500
Clicks "Start Crawling"
Crawler finds 189 matching URLs in 5 minutes
User reviews list, unchecks some URLs
Clicks "Start Scraping All"
SmartScraper scrapes all selected URLs

EXPECTED BEHAVIOR:

Crawling should not block UI (use QThread)
Progress should update in real-time
User can pause/stop crawling
URLs should appear in list as they're found
After crawling, seamlessly integrate with existing scraper

Please implement this feature following the existing code style and architecture of SmartScraper.           