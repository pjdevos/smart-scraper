# Cache Optimization Guide

## 💰 Maximale Kostenbesparing met Caching

SmartScraper gebruikt **intelligent caching** om LLM kosten tot **100% te reduceren** voor herhaalde scrapes.

## Hoe Werkt de Cache?

### 3-Laags Caching Systeem

```
1. LLM Response Cache (7 dagen)
   └─ Volledige scrape resultaten
   └─ Key: MD5(URL + query)

2. Learned Selectors Cache (30 dagen)
   └─ CSS selectors per domain
   └─ Herbruikbaar voor vergelijkbare queries

3. Session Cookies (per domain)
   └─ Browser cookies voor hergebruik
   └─ Bypass login/CAPTCHA
```

## Cost Savings Voorbeelden

### Scenario 1: E-commerce Product Scraping

```python
# Eerste scrape
URL: "https://shop.com/product/123"
Query: "product name, price, rating"
Cost: €0.002 (met smart snippets)
Cache: MISS → Scrape + Cache

# Tweede scrape (zelfde product)
Cost: €0.00 → Cache HIT!
Saving: €0.002 per request

# 100 herhaalde scrapes
Total saved: €0.20
```

### Scenario 2: Multiple Products Same Site

```python
# Product 1
URL: "https://shop.com/product/1"
Cost: €0.002 → Learns selectors for shop.com

# Product 2
URL: "https://shop.com/product/2"
Cost: €0.00 → Uses learned selectors!

# Product 3-100
Cost: €0.00 each → All use learned selectors

Total cost: €0.002 (first product only)
Without cache: €0.20 (100 × €0.002)
Saved: €0.198 (99%)
```

### Scenario 3: Daily Monitoring

```python
# Monitor 50 products daily for 30 days

Day 1:
- 50 products × €0.002 = €0.10
- Learns selectors

Day 2-30:
- 50 products × €0.00 = €0.00 (uses learned selectors)

Total cost: €0.10 for 30 days (1,500 scrapes)
Without cache: €3.00
Saved: €2.90 (97%)
```

## Cache Statistics in GUI

De GUI toont real-time cache statistieken:

- **Cached entries**: Aantal gecachte responses
- **Cache hits**: Aantal keer cache gebruikt
- **Total saved**: Totale kostenbesparing
- **Hit rate**: Cache effectiviteit percentage

## Best Practices

### 1. Consistente Queries

✅ **Goed:**
```python
query = "product name, price, rating"  # Altijd zelfde formulering
```

❌ **Slecht:**
```python
query1 = "product name, price, rating"
query2 = "name, price and rating of product"  # Andere formulering
# → Twee verschillende cache entries!
```

### 2. URL Normalisatie

De cache normaliseert URLs automatisch:
```python
"example.com/product?id=1"
→ Same cache key as:
"https://example.com/product?id=1"
```

### 3. Learned Selectors Benutten

Voor **dezelfde domain** met **vergelijkbare structuur**:

```python
# Eerste product
scrape("shop.com/product/1", "name, price")  # Leert selectors

# Volgende producten - gebruik exact dezelfde query!
scrape("shop.com/product/2", "name, price")  # FREE
scrape("shop.com/product/3", "name, price")  # FREE
```

### 4. Cache Warm-Up

Voor productie gebruik:

```python
# Scrape 1 sample van elke domein type
domains = ["shop1.com", "shop2.com", "news.com"]
for domain in domains:
    scrape(f"{domain}/sample", "your query")
    # Leert selectors voor elk domein

# Daarna: alle scrapes zijn FREE!
```

### 5. Cache Expiry Beheer

**Default settings:**
- LLM responses: 7 dagen
- Learned selectors: 30 dagen

**Aanpassen in `config/settings.py`:**
```python
CACHE_EXPIRY_DAYS = 14  # LLM response cache
SELECTOR_CACHE_EXPIRY_DAYS = 60  # Selector cache
```

## Cache Maintenance

### Clean Expired Entries

```python
from backend.storage import CacheManager

cache = CacheManager()
cache.clear_expired()  # Verwijdert verlopen entries
```

### View Cache Stats

```python
stats = cache.get_stats()
print(f"Total entries: {stats['total_entries']}")
print(f"Valid entries: {stats['valid_entries']}")
print(f"Cache size: {stats['cache_size_mb']} MB")

savings = cache.get_savings_estimate()
print(f"Total saved: €{savings['total_savings_eur']}")
print(f"Hit rate: {savings['average_hit_rate']}%")
```

### Reset Cache

Via GUI: Click "Clear Cache" button

Via code:
```python
cache.clear_all()  # Removes everything
```

## ROI Calculation

### Small Scale (100 pages/month)

| Without Cache | With Cache | Savings |
|---------------|------------|---------|
| €0.20 | €0.002 | €0.198 (99%) |

### Medium Scale (1,000 pages/month)

| Without Cache | With Cache | Savings |
|---------------|------------|---------|
| €2.00 | €0.02 | €1.98 (99%) |

### Large Scale (10,000 pages/month)

| Without Cache | With Cache | Savings |
|---------------|------------|---------|
| €20.00 | €0.20 | €19.80 (99%) |

## Tips voor Maximum Savings

1. **✅ Scrape dezelfde sites regelmatig**
   - Learned selectors blijven cached

2. **✅ Gebruik consistente queries**
   - Verhoogt cache hit rate

3. **✅ Batch vergelijkbare scrapes**
   - Eerste leert, rest is free

4. **✅ Monitor cache statistics**
   - Optimaliseer op basis van hit rate

5. **✅ Laat cache expiry lang staan**
   - Selectors veranderen zelden

6. **❌ Vermijd random URL parameters**
   - Cache per unieke URL

7. **❌ Don't clear cache unnecessarily**
   - Elke clear = fresh start = costs

## Conclusie

Met **intelligente caching** kan SmartScraper:

- 📉 **99% kostenreductie** voor herhaalde scrapes
- 💰 **€0.00** voor 2e+ scrapes van zelfde domain
- 🚀 **Instant results** voor gecachte queries
- 📊 **Transparante savings** tracking

**Smart Scraper betaalt zichzelf terug na ~10 scrapes!** 🎉