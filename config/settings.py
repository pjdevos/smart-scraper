"""
SmartScraper Configuration Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR
COOKIES_DIR = DATA_DIR / "cookies"
SESSIONS_DIR = DATA_DIR / "sessions"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
EXPORTS_DIR = DATA_DIR / "exports"
LOG_FILE = DATA_DIR / "app.log"

# Create directories
for directory in [DATA_DIR, COOKIES_DIR, SESSIONS_DIR, SCREENSHOTS_DIR, EXPORTS_DIR]:
    directory.mkdir(exist_ok=True)

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_HAIKU_MODEL = "claude-haiku-3-5-20241022"  # Future feature for simple tasks

# API Cost Estimates (per million tokens)
SONNET_INPUT_COST = 3.0  # $3 per million input tokens
SONNET_OUTPUT_COST = 15.0  # $15 per million output tokens
HAIKU_INPUT_COST = 0.8  # $0.80 per million input tokens
HAIKU_OUTPUT_COST = 4.0  # $4 per million output tokens

# Budget Configuration
DEFAULT_DAILY_BUDGET = 5.0  # €5 default budget
BUDGET_WARNING_THRESHOLD = 0.8  # Warn at 80%

# Scraping Configuration
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Selenium/Playwright Configuration
HEADLESS_MODE = True
BROWSER_WAIT_TIME = 10
PAGE_LOAD_TIMEOUT = 30

# Cache Configuration
CACHE_EXPIRY_DAYS = 7
SELECTOR_CACHE_EXPIRY_DAYS = 30

# HTML Minimization (Smart Snippet Extraction)
MAX_HTML_LENGTH = 3000  # Characters to send to LLM (reduced for cost savings)
EXTRACT_MAIN_CONTENT = True  # Extract only main content area
EXTRACT_ITEM_SAMPLES = True  # For listings, send only 2-3 sample items
REMOVE_ATTRIBUTES = True  # Remove class/id/style attributes to save tokens

# Stealth Configuration
DEFAULT_STEALTH_LEVEL = "medium"  # basic, medium, high, maximum
RESPECT_ROBOTS_TXT = True

# Rate Limiting (BASIC stealth)
MIN_REQUEST_DELAY = 2.0  # Minimum seconds between requests
MAX_REQUEST_DELAY = 5.0  # Maximum seconds between requests
REQUESTS_PER_MINUTE = 20  # Max requests per minute per domain

# Behavior Simulation (MEDIUM+ stealth)
MOUSE_MOVE_ENABLED = True
RANDOM_SCROLL_ENABLED = True
GRADUAL_PAGE_LOAD = True

# Advanced Stealth (HIGH+ stealth)
USER_AGENT_ROTATION = True
FINGERPRINT_MASKING = True
CANVAS_RANDOMIZATION = True

# Proxy Configuration (MAXIMUM stealth)
USE_PROXIES = False  # Enable in .env with PROXY_LIST
PROXY_ROTATION = True

# CAPTCHA Configuration
CAPTCHA_DETECTION_ENABLED = True
CAPTCHA_MANUAL_SOLVING_TIMEOUT = 300  # 5 minutes
CAPTCHA_AUTO_SOLVER = None  # "2captcha", "anticaptcha", None

# 2Captcha API (optional)
TWOCAPTCHA_API_KEY = os.getenv("TWOCAPTCHA_API_KEY", "")

# Anti-Captcha API (optional)
ANTICAPTCHA_API_KEY = os.getenv("ANTICAPTCHA_API_KEY", "")

# Monitoring
SUCCESS_RATE_WINDOW = 100  # Track last N requests
BLOCKING_THRESHOLD = 0.3  # Alert if success rate drops below 30%

# Export Configuration
EXPORT_CSV_ENCODING = "utf-8-sig"  # UTF-8 with BOM
EXPORT_JSON_INDENT = 2

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Crawler Configuration
DEFAULT_MAX_CRAWL_PAGES = 500
DEFAULT_MAX_CRAWL_DEPTH = 3
CRAWLER_REQUEST_DELAY = 2.0  # Seconds between requests
SITEMAP_TIMEOUT = 10  # Timeout for sitemap.xml fetch

# GUI Configuration
WINDOW_TITLE = "SmartScraper - AI-Powered Web Scraping"
WINDOW_WIDTH = 1600  # Wider for 1920px screens
WINDOW_HEIGHT = 850  # Fits 1080p with taskbar
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700
WINDOW_MAX_WIDTH = 1920  # Full HD width
WINDOW_MAX_HEIGHT = 1000  # Reduced to fit 1080p screens
DEFAULT_THEME = "dark"  # "dark" or "light"