# Pagination Guide

## 📄 Overview

SmartScraper now supports **intelligent multi-page scraping** with automatic pagination pattern detection.

---

## ✨ Features

### 1. **Automatic Pattern Detection**

The scraper automatically detects and tries multiple pagination patterns:

- **Query Parameter**: `?page=2`, `&page=2`
- **Path-based**: `/page/2/`, `/products/page/2`
- **Hash-based**: `#page=2`

### 2. **Smart Stopping**

Pagination automatically stops when:
- Empty page is detected (no data)
- Maximum pages reached
- All patterns fail

### 3. **Cost Optimization**

Pagination benefits from all cost optimizations:
- **First page**: Learns selectors (€0.002)
- **Pages 2+**: Uses learned selectors (€0.00)
- **Cached pages**: Returns instantly (€0.00)

---

## 🎮 How to Use

### Via GUI

1. **Enter Base URL**: `https://example.com/products`
2. **Enable Pagination**: Check "Enable Pagination" checkbox
3. **Set Max Pages**: Choose 1-100 pages (default: 5)
4. **Enter Query**: "product name, price, rating"
5. **Click "Start Scraping"**

### Via Code

```python
from backend.scraper_engine import ScraperEngine, ScrapingMethod

engine = ScraperEngine(api_key="your-api-key")

result = engine.scrape_with_pagination(
    base_url="https://example.com/products",
    query="product name, price, rating",
    max_pages=10,
    method=ScrapingMethod.AUTO,
    page_delay=2.0  # Seconds between pages
)

print(f"Pages scraped: {result['pages_scraped']}")
print(f"Total items: {len(result['data'])}")
print(f"Total cost: €{result['total_cost']:.4f}")
```

---

## 📊 Example Results

### Scenario: E-commerce Product Listing

**Input:**
- URL: `https://shop.example.com/products`
- Query: "product name, price, rating"
- Max Pages: 10

**Output:**
```
✓ Scraped 8 pages, 240 total items (€0.002)

Pages scraped: 8
Total items: 240
Total cost: €0.002
Method: learned_selectors

Breakdown:
├─ Page 1: €0.002 (LLM learns selectors)
├─ Page 2: €0.00 (uses learned selectors)
├─ Page 3: €0.00 (uses learned selectors)
├─ Page 4: €0.00 (uses learned selectors)
├─ Page 5: €0.00 (uses learned selectors)
├─ Page 6: €0.00 (uses learned selectors)
├─ Page 7: €0.00 (uses learned selectors)
└─ Page 8: €0.00 (uses learned selectors)
```

**Without pagination**: Would need to manually run 8 times
**With pagination**: One click, automatic

---

## 🔧 Configuration

### Pagination Settings

In GUI:
- **Enable Pagination**: Checkbox to enable/disable
- **Max Pages**: Spinner (1-100)

In code:
```python
result = engine.scrape_with_pagination(
    base_url="...",
    query="...",
    max_pages=5,      # Maximum pages to scrape
    page_delay=2.0,   # Delay between pages (seconds)
    method=ScrapingMethod.AUTO  # Scraping method
)
```

### URL Patterns Supported

| Pattern Type | Example URL | Detected? |
|--------------|-------------|-----------|
| Query param | `site.com?page=2` | ✅ Auto |
| Query param | `site.com?cat=foo&page=2` | ✅ Auto |
| Path-based | `site.com/page/2` | ✅ Auto |
| Path-based | `site.com/products/page/2` | ✅ Auto |
| Hash-based | `site.com#page=2` | ✅ Auto |

---

## 💡 Best Practices

### 1. **Start Small**
Begin with `max_pages=3` to test the pattern detection:
```python
result = engine.scrape_with_pagination(
    base_url="https://example.com/products",
    query="product name, price",
    max_pages=3  # Test first
)
```

### 2. **Respect Rate Limits**
Use appropriate `page_delay`:
```python
# Conservative (recommended)
page_delay=2.0  # 2 seconds between pages

# Aggressive (may trigger rate limits)
page_delay=0.5  # 500ms between pages

# Very conservative (for strict sites)
page_delay=5.0  # 5 seconds between pages
```

### 3. **Use Stealth for Protected Sites**
Combine pagination with stealth settings:
```python
engine = ScraperEngine(
    api_key="...",
    stealth_level="high",  # Use stealth
    use_proxies=True,
    respect_robots=True
)

result = engine.scrape_with_pagination(
    base_url="...",
    query="...",
    max_pages=10,
    page_delay=3.0  # Longer delay with stealth
)
```

### 4. **Monitor Budget**
Set a daily budget to prevent overspending:
```python
engine = ScraperEngine(
    api_key="...",
    daily_budget=5.0  # €5/day limit
)
```

---

## 🚨 Common Issues

### Issue 1: "Failed to scrape any pages"

**Cause**: URL pattern not recognized
**Solution**: Check if URL already includes pagination:
```python
# ❌ Wrong: Already includes page number
base_url = "https://example.com/products?page=1"

# ✅ Correct: Base URL without pagination
base_url = "https://example.com/products"
```

### Issue 2: "Only scraped 1 page"

**Cause**: Pattern detection failed
**Solution**: Manually inspect the site's pagination:
1. Open the site in browser
2. Go to page 2
3. Check URL pattern
4. Ensure base_url doesn't include page number

### Issue 3: "Budget exceeded"

**Cause**: Daily budget limit reached
**Solution**:
- Increase budget in `config/settings.py`
- Or wait until next day (budget resets daily)

---

## 📈 Performance

### Speed Comparison

**Single Page Scraping:**
```
Time: 5 seconds
Cost: €0.002
Items: 30
```

**Multi-Page Scraping (10 pages):**
```
Time: 60 seconds (5s/page + 2s delay)
Cost: €0.002 (only first page uses LLM)
Items: 300
Efficiency: 99% cost savings vs individual scrapes
```

### Cost Analysis

**Without Pagination (10 separate scrapes):**
- 10 scrapes × €0.002 = **€0.02**

**With Pagination (1 scrape, 10 pages):**
- 1 LLM call (page 1): €0.002
- 9 learned selector calls (pages 2-10): €0.00
- **Total: €0.002** (90% savings)

---

## 🔮 Advanced Usage

### Custom Pagination Logic

For non-standard pagination patterns, you can modify `scraper_engine.py`:

```python
def _generate_paginated_url(self, base_url: str, page: int, pattern: str = None) -> str:
    """Add custom pattern here"""

    if pattern == "custom":
        # Your custom logic
        return f"{base_url}/list/{page}"

    # ... existing logic
```

### Parallel Pagination

For very large scrapes, consider parallel processing:

```python
from concurrent.futures import ThreadPoolExecutor

def scrape_page_range(start_page, end_page):
    """Scrape specific page range"""
    # Implement logic here
    pass

# Scrape pages 1-100 in parallel (4 threads)
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(scrape_page_range, 1, 25),
        executor.submit(scrape_page_range, 26, 50),
        executor.submit(scrape_page_range, 51, 75),
        executor.submit(scrape_page_range, 76, 100)
    ]
```

---

## ✅ Summary

SmartScraper's pagination feature:

✅ **Automatic pattern detection** (query, path, hash)
✅ **Intelligent stopping** (empty pages, max pages)
✅ **Cost optimized** (99% savings with learned selectors)
✅ **GUI integrated** (checkbox + spinner)
✅ **Rate limiting** (configurable delays)
✅ **Budget protected** (daily limits)

**Result**: Scrape hundreds of pages for the cost of one! 🚀
