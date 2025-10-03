# SPA Category Crawler Guide

## Overview

The SPA Category Crawler is designed for **Single Page Applications** like PriceRunner that use JavaScript/API calls to load data dynamically.

## Architecture

### Two-Phase Approach

**Phase 1: Reconnaissance (Playwright)**
- Intercepts XHR/Fetch calls
- Discovers API endpoints
- Extracts required headers (locale, API keys, etc.)
- Maps URL patterns

**Phase 2: Crawling**
- **API Mode**: Uses async httpx for fast API crawling (if endpoints discovered)
- **DOM Mode**: Falls back to Playwright DOM scraping (if no API)

## Features

✅ **API Interception**: Discovers backend APIs automatically
✅ **Rate Limiting**: Configurable QPS with jitter
✅ **429 Handling**: Respects `Retry-After` header
✅ **Exponential Backoff**: 1s → 2s → 4s → 8s → 16s
✅ **Deduplication**: Tracks seen category/product IDs
✅ **Async/Concurrent**: Fast parallel crawling
✅ **CSV Export**: Hierarchical pipe-delimited format

## Usage

### 1. Reconnaissance (Optional - Discover APIs)

```bash
python recon_pricerunner_api.py
```

This will:
- Open PriceRunner in browser
- Navigate categories, products, search
- Intercept all API calls
- Save to `data/pricerunner_api_map.json`

**Output:**
```json
[
  {
    "method": "GET",
    "url": "https://api.pricerunner.com/v1/categories?locale=en-GB",
    "headers": {
      "accept": "application/json",
      "accept-language": "en-GB",
      "x-api-key": "...",
      "x-locale": "en_GB"
    }
  }
]
```

### 2. Run SPA Crawler

```bash
python crawl_pricerunner_spa.py
```

**Configuration:**
```python
crawler = SPACategoryCrawler(
    base_url="https://www.pricerunner.com",
    headless=False,          # Set True for headless
    max_depth=5,             # Category depth limit
    requests_per_second=0.5, # QPS (0.5 = 1 req every 2s)
    timeout=30
)
```

## How It Works

### Step 1: API Discovery

```python
async def _discover_api_with_playwright(self):
    # Launch browser
    # Intercept all XHR/Fetch
    # Click categories, products
    # Extract API patterns
```

Looks for:
- `/api/` endpoints
- `.json` responses
- Headers: `x-api-key`, `x-locale`, `accept-language`
- URL patterns: `/categories`, `/products`, `/search`

### Step 2: Crawling Strategy

**If API Found:**
```python
async with httpx.AsyncClient() as client:
    # Fast async API calls
    data = await client.get("/api/categories")
```

**If No API (Fallback):**
```python
async with async_playwright() as p:
    page = await p.new_page()
    # Scroll to trigger lazy loading
    # Extract <a> links from DOM
    # Follow category links
```

### Step 3: Rate Limiting

```python
async def _rate_limit(self):
    elapsed = time.time() - self.last_request_time
    sleep_time = self.min_delay - elapsed + jitter
    await asyncio.sleep(sleep_time)
```

### Step 4: 429 Handling

```python
if response.status_code == 429:
    retry_after = response.headers.get('Retry-After', '5')
    await asyncio.sleep(float(retry_after))
```

### Step 5: Deduplication

```python
self.seen_category_ids: Set[str] = set()

if cat_id not in self.seen_category_ids:
    self.seen_category_ids.add(cat_id)
    # Process category
```

## Output Format

CSV with pipe delimiter:

```
level_1|level_2|level_3|level_4|level_5|depth|full_path|url|category_id
Home & Interior|||||1|Home & Interior|https://www.pricerunner.com/t/34/Home-Interior|34
Home & Interior|Home Appliances||||2|Home & Interior > Home Appliances|https://www.pricerunner.com/t/3/Home-Appliances|3
```

## PriceRunner Specifics

### URL Patterns
- **Categories**: `/t/{id}/{name}` (e.g., `/t/34/Home-Interior`)
- **Product Categories**: `/cl/{id}/{name}` (e.g., `/cl/3/Computers-Tablets`)
- **Products**: `/p/{id}/{name}` (e.g., `/p/123/Apple-iPhone-15`)

### Selectors (DOM Fallback)
```python
selectors = [
    'a[href*="/cl/"]',      # Product category links
    'a[href*="/t/"]',       # Main category links
    '[data-category-id]',   # Elements with category ID
    '.category-link'        # Category link classes
]
```

### Headers Required
```python
headers = {
    "User-Agent": "Mozilla/5.0...",
    "Accept": "application/json",
    "Accept-Language": "en-GB,en;q=0.9",
    "X-Locale": "en_GB"  # May be required for API
}
```

## Troubleshooting

### Issue: No categories found

**Solution 1**: Check selectors
```python
# Update selectors in _crawl_with_playwright_fallback()
selectors = [
    'a.your-actual-selector',
    '[data-testid="category-link"]'
]
```

**Solution 2**: Check API endpoints
```bash
# Run recon first
python recon_pricerunner_api.py
# Check output in data/pricerunner_api_map.json
```

### Issue: Rate limited (429)

**Solution**: Lower QPS
```python
requests_per_second=0.25  # 1 request every 4 seconds
```

### Issue: Missing hierarchy

**Problem**: Breadcrumbs not extracted correctly

**Solution**: Check breadcrumb selectors
```python
selectors = [
    'nav[aria-label="breadcrumb"] a',
    '.breadcrumb a',
    '[itemtype*="BreadcrumbList"] a'
]
```

## Advanced: Custom API Integration

Once you know the API endpoints from recon:

```python
# Add to spa_category_crawler.py

async def _crawl_categories_api(self, client: httpx.AsyncClient):
    """Custom API crawling logic"""

    # Get all categories
    data = await self._fetch_json_with_retry(
        client,
        "https://api.pricerunner.com/v1/categories",
        params={"locale": "en-GB"}
    )

    for item in data.get("categories", []):
        category = Category(
            id=item["id"],
            name=item["name"],
            url=f"{self.base_url}/t/{item['id']}/{item['slug']}",
            level=1
        )
        self.categories.append(category)

        # Fetch subcategories
        if item.get("hasChildren"):
            await self._crawl_subcategories_api(client, item["id"])
```

## Performance Tips

1. **Parallel Crawling**: Use `asyncio.gather()` for concurrent requests
2. **Caching**: Store API responses to avoid re-fetching
3. **Checkpointing**: Save progress periodically
4. **Selective Crawling**: Only crawl specific category trees

## Legal & Ethics

- ✅ Respect `robots.txt`
- ✅ Use conservative rate limits
- ✅ Clear User-Agent
- ✅ No brute force
- ❌ Don't overload servers
- ❌ Don't bypass authentication

## Next Steps

1. Run reconnaissance: `python recon_pricerunner_api.py`
2. Inspect API map: `data/pricerunner_api_map.json`
3. Update crawler with real API endpoints
4. Run crawler: `python crawl_pricerunner_spa.py`
5. Analyze output: `data/exports/pricerunner_categories_spa.csv`
