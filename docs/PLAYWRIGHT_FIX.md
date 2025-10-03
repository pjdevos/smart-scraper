# Playwright Event Loop Fix

## Problem

When running SmartScraper with PyQt6, Playwright throws this error:

```
It looks like you are using Playwright Sync API inside the asyncio loop.
Please use the Async API instead.
```

## Root Cause

- PyQt6 runs its own event loop
- Playwright's sync API conflicts with PyQt's event loop
- Both try to control async operations

## Solution

Wrap Playwright operations in a **separate thread** to isolate it from PyQt's event loop.

### Files Modified:

**1. `backend/scrapers/playwright_scraper.py`**

```python
import threading

def _fetch_in_thread(self, url: str, result_container: list):
    """Fetch HTML in separate thread"""
    # All Playwright operations here
    page = self.browser.new_page()
    page.goto(url)
    html = page.content()
    result_container.append(html)
    page.close()

def fetch(self, url: str) -> Optional[str]:
    """Main fetch method using thread"""
    result_container = []
    thread = threading.Thread(
        target=self._fetch_in_thread,
        args=(url, result_container)
    )
    thread.start()
    thread.join(timeout=self.timeout + 10)

    return result_container[0] if result_container else None
```

**2. `backend/scrapers/stealth_playwright_scraper.py`**

Same approach - wrapped entire fetch logic in `_fetch_in_thread()` method.

## Benefits

✅ **No event loop conflicts**
✅ **Works with PyQt6**
✅ **No code changes needed in rest of app**
✅ **Thread-safe result passing**
✅ **Timeout protection**

## Testing

```bash
python main.py
```

Try scraping with:
- Method: Auto (will use AdaptiveScraper)
- Method: Playwright
- Method: Stealth

All should work without event loop errors.

## Alternative Solutions Considered

❌ **Use Playwright Async API** - Would require async/await everywhere
❌ **Run PyQt in thread** - Too invasive, breaks Qt patterns
❌ **Use subprocess** - Too slow, overhead
✅ **Thread wrapper** - Minimal changes, clean isolation

## Notes

- Thread timeout = scraper timeout + buffer (10s for Playwright, 60s for Stealth)
- Result passed via list container (thread-safe)
- Thread cleanup automatic (join ensures completion)
