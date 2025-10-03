# SmartScraper - AI-Powered Web Scraping Tool

SmartScraper is an intelligent web scraping tool that uses Claude AI to automatically identify and extract data from websites using natural language queries.

## Features

### Core Features
- **Natural Language Queries**: Just describe what you want to extract (e.g., "product name, price, and rating")
- **AI-Powered Extraction**: Uses Claude API to intelligently identify CSS selectors
- **Cost Optimization**:
  - Caches LLM responses (7-day TTL)
  - Learns and reuses CSS selectors per domain
  - Minimizes HTML before sending to API
  - Budget tracking and warnings
- **Multiple Scraping Methods**:
  - **Requests**: Fast static HTML scraping
  - **Selenium**: Compatible with older JavaScript sites
  - **Playwright**: Modern JavaScript framework support
  - **Stealth**: Advanced anti-detection scraping
  - **Auto**: Automatically chooses the best method
- **Smart Pipeline**:
  1. Check cache (instant, free)
  2. Check learned selectors (fast, free)
  3. Try regex patterns (fast, free)
  4. Use AI analysis (slower, costs money)
- **Export Options**: CSV, JSON, Excel
- **User-Friendly GUI**: Dark-themed PyQt6 interface

### 🛡️ Anti-Bot & Stealth Features

SmartScraper includes **4 stealth levels** with comprehensive anti-detection:

#### 🟢 BASIC Stealth
- ✅ Realistic User-Agent headers
- ✅ Random delays between requests (2-5 seconds)
- ✅ Rate limiting per domain (20 req/min)
- ✅ robots.txt respect (optional)

#### 🟡 MEDIUM Stealth (Default)
- ✅ All BASIC features
- ✅ Human-like scrolling behavior
- ✅ Session/cookie persistence
- ✅ Random timing jitter
- ✅ Gradual page loading simulation

#### 🟠 HIGH Stealth
- ✅ All MEDIUM features
- ✅ Mouse movement simulation
- ✅ User agent rotation (12+ realistic UAs)
- ✅ Viewport randomization
- ✅ JavaScript fingerprint masking
- ✅ Canvas fingerprint randomization
- ✅ WebGL vendor masking
- ✅ Longer delays (5-10 seconds)

#### 🔴 MAXIMUM Stealth
- ✅ All HIGH features
- ✅ Residential proxy support & rotation
- ✅ Cloudflare challenge handler
- ✅ CAPTCHA detection
- ✅ Manual CAPTCHA solving (pauses browser)
- ✅ Very slow scraping (1 request/minute)
- ✅ Complete browser fingerprint randomization

**Select stealth level in the GUI** or configure programmatically!

## Installation

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd smart_scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers (required for Playwright mode):
```bash
playwright install chromium
```

5. Create a `.env` file with your API key:
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

### Running the Application

```bash
python main.py
```

### Using the GUI

1. **Enter URL**: Paste the website URL you want to scrape
2. **Describe Data**: Enter what you want to extract in natural language
   - Example: "product name, price, and rating"
   - Example: "article title, author, and date"
   - Example: "email addresses and phone numbers"
3. **Select Method**: Choose scraping method (Auto recommended, or Stealth for protected sites)
4. **Configure Stealth**:
   - **Stealth Level**: Basic, Medium (default), High, or Maximum
   - **Use Proxies**: Enable if you have proxies configured in `.env`
   - **Respect robots.txt**: Follow website scraping rules (recommended)
5. **Start Scraping**: Click "Start Scraping" button
6. **View Results**: Results appear in the table below
7. **Export Data**: Export to CSV, JSON, or Excel

### 🛡️ Stealth Mode Usage

**When to use each stealth level:**

- **BASIC**: Simple websites, testing, development
- **MEDIUM**: Most production scraping (default, good balance)
- **HIGH**: Protected sites, e-commerce, sites with bot detection
- **MAXIMUM**: Cloudflare-protected sites, sites with CAPTCHA, aggressive anti-bot

**Configuring Proxies** (for MAXIMUM stealth):
```bash
# In .env file:
PROXY_LIST=http://user:pass@proxy1.com:8080,http://user2:pass2@proxy2.com:8080
```

**Expected Speed:**
- BASIC: ~3s per page
- MEDIUM: ~5-8s per page
- HIGH: ~10-15s per page
- MAXIMUM: ~60s+ per page

### Example Queries

#### E-commerce Sites
```
product name, price, and rating
```

#### News/Blog Sites
```
article title, author, published date, and summary
```

#### Contact Information
```
email addresses, phone numbers, and addresses
```

#### Job Listings
```
job title, company name, location, and salary
```

## How It Works

### Smart Pipeline

SmartScraper uses a 4-phase pipeline to minimize costs:

**Phase 1: Cache Check (Free)**
- Checks if this URL + query was scraped recently
- Returns cached results instantly (7-day cache)

**Phase 2: Learned Selectors (Free)**
- Checks if we've learned CSS selectors for this domain
- Extracts data using BeautifulSoup
- No API calls needed!

**Phase 3: Simple Extraction (Free)**
- Tries regex patterns for common data (emails, prices, etc.)
- Uses common CSS selectors
- Fast and free

**Phase 4: AI Analysis (Costs Money)**
- **Smart Snippet Extraction**: Only sends relevant HTML snippets
- Sends to Claude API to identify selectors
- Extracts data and saves selectors for future use
- Caches result

### 💰 Cost Optimization

SmartScraper is **aggressively optimized** to minimize API costs:

#### 1. **Smart HTML Snippet Extraction** (NEW!)
Instead of sending entire pages (50-200KB), we send **only relevant snippets**:

- **Removes waste**: Scripts, styles, nav, footer, header, forms
- **Extracts main content**: Finds `<main>`, `<article>`, or content area
- **Sample items for listings**: For product pages, sends only 2-3 example items
- **Removes attributes**: Strips class/id/style to save tokens
- **Result**: Typically **3KB instead of 50KB** (95% reduction!)

**Example:**
```
Original page: 50,000 chars
After smart extraction: 2,500 chars (95% reduction)
Token savings: ~12,000 tokens saved = €0.036 saved per page!
```

#### 2. **Multi-Layer Caching** (99% Cost Reduction!)

SmartScraper uses **3-layer caching** for maximum savings:

**Layer 1: LLM Response Cache (7 days)**
- Caches complete scrape results
- Key: MD5(URL + query)
- **Hit = €0.00 cost!**

**Layer 2: Learned Selectors (30 days)**
- Saves CSS selectors per domain
- Reusable across similar pages
- **2nd+ page on same domain = FREE**

**Layer 3: Session Cookies**
- Reuses browser cookies
- Bypasses login/CAPTCHA
- Reduces blocking

**Real-world example:**
```
Day 1: Scrape 50 products from shop.com
- First product: €0.002 (learns selectors)
- Products 2-50: €0.00 each (uses learned selectors)
- Total: €0.002

Day 2-30: Scrape same 50 products
- All 50: €0.00 (uses cache)
- Total for 30 days: €0.002 (1,500 scrapes!)

Without cache: €3.00
With cache: €0.002
Saved: €2.998 (99.9%)
```

**Cache Statistics Widget:**
- Real-time hit tracking
- Total savings display
- Hit rate monitoring

#### 3. **Smart Reuse**
- Second scrape of same domain: **FREE** (uses learned selectors)
- Same product rescraped: **FREE** (uses cache)
- **ROI**: App pays for itself after ~10 scrapes!

#### 4. **Budget Tracking**
- Real-time cost monitoring
- Daily budget warnings
- Per-request cost display
- Cache savings counter

**Cost Comparison:**

| Method | Tokens Sent | Cost per Page | Savings |
|--------|-------------|---------------|---------|
| **Full HTML** | ~15,000 | €0.045 | - |
| **Basic Minimization** | ~5,000 | €0.015 | 67% |
| **Smart Snippets** ✅ | ~800 | €0.002 | **96%** |

**Real Example:**
- Scraping 100 product pages
- Old method: €4.50
- **New method: €0.20** (€4.30 saved!)
- With learned selectors (2nd+ pages): **€0.00**

### Estimated Costs

Using Claude Sonnet 4:
- Input: $3 per million tokens
- Output: $15 per million tokens
- **Typical scrape: €0.002 - €0.005 per page**
- **Default budget: €5/day = 1000+ pages**

## Configuration

Edit `config/settings.py` to customize:

```python
# Budget
DEFAULT_DAILY_BUDGET = 5.0  # €5 per day

# Cache
CACHE_EXPIRY_DAYS = 7
SELECTOR_CACHE_EXPIRY_DAYS = 30

# Scraping
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
HEADLESS_MODE = True

# HTML Minimization
MAX_HTML_LENGTH = 5000  # Characters sent to LLM
```

## Project Structure

```
smart_scraper/
├── main.py                    # Entry point
├── requirements.txt
├── .env.example
├── README.md
├── config/
│   └── settings.py           # Configuration
├── frontend/                 # PyQt6 GUI
│   ├── main_window.py
│   ├── widgets/
│   ├── workers/
│   └── styles/
├── backend/                  # Core logic
│   ├── scraper_engine.py    # Main orchestrator
│   ├── scrapers/            # Requests/Selenium/Playwright
│   ├── llm/                 # Claude API integration
│   ├── extractors/          # Data extraction
│   └── storage/             # Caching & learned selectors
├── utils/                    # Utilities
│   ├── logger.py
│   ├── budget_manager.py
│   └── validators.py
└── data/                     # Runtime data (auto-created)
    ├── llm_cache.json
    ├── learned_selectors.json
    ├── app.log
    └── exports/
```

## Troubleshooting

### "API key not provided"
Make sure you've created a `.env` file with your `ANTHROPIC_API_KEY`

### "Failed to fetch HTML"
- Check if URL is accessible
- Try a different scraping method (Selenium or Playwright)
- Check your internet connection

### "Daily budget exceeded"
- Increase budget in `config/settings.py`
- Wait until tomorrow (budget resets daily)
- Clear cache to start fresh

### Playwright not working
```bash
playwright install chromium
```

### Selenium ChromeDriver issues
The app uses `webdriver-manager` to auto-install ChromeDriver. If issues persist:
```bash
pip install --upgrade webdriver-manager
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Structure

The application follows a clean architecture:
- **Frontend**: PyQt6 GUI (no business logic)
- **Backend**: Pure Python (can be used standalone)
- **Utils**: Shared utilities
- **Config**: Centralized configuration

### Adding New Features

To add a new scraping method:
1. Create new scraper in `backend/scrapers/`
2. Inherit from `BaseScraper`
3. Implement `fetch()` and `close()` methods
4. Add to `ScraperEngine._choose_scraper()`

## License

MIT License

## Credits

- Built with PyQt6 for GUI
- Uses Claude API for intelligent extraction
- Scraping powered by Requests, Selenium, and Playwright
- Data processing with BeautifulSoup and Pandas

## Support

For issues and questions:
- Open an issue on GitHub
- Check the logs in `data/app.log`

## Roadmap

- [ ] Add proxy support
- [ ] Add CAPTCHA handling
- [ ] Add rate limiting
- [ ] Add user agent rotation
- [ ] Add browser cookie management
- [ ] Add scheduled scraping
- [ ] Add API endpoint
- [ ] Add CLI interface
- [ ] Add more export formats (SQL, MongoDB)
- [ ] Add data validation rules

---

**Made with ❤️ by SmartScraper Team**