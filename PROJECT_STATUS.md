# Smart Scraper - Project Status

## Web Crawler Feature ✅ NIEUW!

**Status**: Volledig geïmplementeerd en klaar voor gebruik!

### Wat is toegevoegd:
De SmartScraper GUI heeft nu een **Crawler Mode** tab die automatisch URLs ontdekt door links te volgen.

🕷️ **3-Tab Interface**: Single URL | URL List | **Crawl Site** (NIEUW!)

### Features:
- 📊 Real-time crawl stats (URLs found/crawled/matched)
- 🎯 Regex pattern filtering voor precisie
- 🗺️ Sitemap.xml support (5x sneller dan regulier crawlen)
- ☑️ URL preview lijst met checkboxes
- ⏯️ Pause/Resume/Stop controls
- 💾 Export discovered URLs naar .txt
- 🤖 Robots.txt respect + internal links only

### Nieuwe bestanden:
```
backend/crawler/
├── __init__.py
└── web_crawler.py          # BFS crawler met sitemap support

frontend/workers/
└── crawler_worker.py       # QThread background worker

frontend/widgets/
└── crawler_widget.py       # Complete UI (600+ regels)
```

### Gebruik:
```bash
python main.py
# → Selecteer "🕷️ Crawl Site" tab
# → Start URL: https://books.toscrape.com
# → Pattern (optioneel): /catalogue/.*
# → Klik "Start Crawling"
# → Review URLs → "Start Scraping Selected"
```

**TODO**: Multi-URL scraping met learned selectors (nu alleen eerste URL als POC)

---

## Eerdere Voltooide Taken

### PriceRunner Category Crawler ✅
- 221 categorieën over 5 niveaus geëxtraheerd
- Checkpoint systeem voor crash recovery
- Output: `data/exports/pricerunner_full_hierarchy.csv`

### Playwright Threading Fix ✅
- Event loop conflicts opgelost
- Browser init in zelfde thread als gebruik

### UI Window Sizing Fix ✅  
- Venster past nu op 1920x1080 met taskbar
- 70% screen sizing met `availableGeometry()`

### Playwright MCP Server ✅
- `@playwright/mcp` geïnstalleerd
- Chromium 140.0.7339.186 beschikbaar
- **Vereist restart om te activeren**

---

## Configuratie

### `.claude.json` (MCP Server):
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

### Crawler Settings (`config/settings.py`):
```python
DEFAULT_MAX_CRAWL_PAGES = 500
DEFAULT_MAX_CRAWL_DEPTH = 3  
CRAWLER_REQUEST_DELAY = 2.0
SITEMAP_TIMEOUT = 10
```

---

## Commands

```bash
# SmartScraper GUI (met Crawler!)
python main.py

# Legacy PriceRunner crawler
python crawl_full_hierarchy.py

# Monitoring
python monitor_crawl.py
```

---

## Testing de Crawler

**Test sites**:
- ✅ Easy: `https://books.toscrape.com` (perfect voor testen)
- ⚠️ Medium: `https://scrapethissite.com`  
- 🎯 Real: Eigen catalogi met pattern filtering

**Test flow**:
1. `python main.py`
2. Tab "🕷️ Crawl Site"
3. URL: `https://books.toscrape.com`
4. Pattern: `/catalogue/.*`
5. Verify crawling werkt
6. Test scraping eerste URL

---

## Dependencies

**Python**: playwright, PyQt6, requests, beautifulsoup4, asyncio  
**Node.js**: @playwright/mcp (optioneel)

**Installatie**:
```bash
pip install -r requirements.txt
python -m playwright install chromium
npx -y @playwright/mcp  # Optioneel
```

---

*Laatst bijgewerkt: 2025-10-03*  
*Status: Web Crawler volledig functioneel ✅*  
*Volgende: Multi-URL scraping met learned selectors*
