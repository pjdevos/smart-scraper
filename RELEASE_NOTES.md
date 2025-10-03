# SmartScraper v1.0.0 Release Notes

## 🎉 Initial Release

SmartScraper is an AI-powered web scraping tool with a modern PyQt6 GUI and built-in web crawler.

### ✨ Key Features

**AI-Powered Scraping**
- Natural language queries for data extraction
- Claude AI integration for intelligent parsing
- Multiple scraping methods (Playwright, Requests, BeautifulSoup)
- Automatic selector learning and caching

**Web Crawler**
- URL discovery by following links
- Regex pattern filtering
- Sitemap.xml support (5x faster)
- Real-time crawl statistics
- Pause/Resume/Stop controls

**Modern UI**
- Beautiful purple/beige color scheme
- Compact, responsive layout
- 3-tab interface (Single URL, URL List, Crawl Site)
- Real-time progress tracking
- Budget display in header

**Cost Optimization**
- Intelligent caching system
- Learned selectors reuse
- HTML minimization
- First page €0.003, rest €0.00 with caching

**Export Options**
- CSV export
- JSON export
- Excel (XLSX) export

**Stealth Features**
- User agent rotation
- Browser fingerprint masking
- Rate limiting
- Robots.txt respect
- CAPTCHA handling

### 📦 Download

**Windows (x64)**
- [SmartScraper-v1.0.0-Windows.zip](https://github.com/pjdevos/smart-scraper/releases/download/v1.0.0/SmartScraper-v1.0.0-Windows.zip) (257 MB)

### 🚀 Quick Start

1. Download and extract the ZIP file
2. Create a `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```
3. Run `SmartScraper.exe`
4. Start scraping!

### 📋 System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM (8GB recommended)
- 500MB free disk space
- Internet connection
- Anthropic API key ([get one here](https://console.anthropic.com/))

### 🐛 Known Issues

- First launch may be slow (PyInstaller unpacking)
- Large files (>10MB) may take time to load
- Anthropic API required (no offline mode)

### 🔧 Technical Details

**Built with:**
- Python 3.13
- PyQt6 for GUI
- Playwright for browser automation
- Claude AI for extraction
- PyInstaller for packaging

**Architecture:**
- Single executable (no installer needed)
- Standalone deployment
- All dependencies bundled

### 📝 License

See [LICENSE](LICENSE) for details.

---

**Full Changelog:** https://github.com/pjdevos/smart-scraper/commits/v1.0.0

🤖 Built with [Claude Code](https://claude.com/claude-code)
