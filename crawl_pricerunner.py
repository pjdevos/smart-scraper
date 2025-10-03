#!/usr/bin/env python
"""
PriceRunner Category Tree Crawler
Crawls the complete category hierarchy and exports to CSV
"""
from pathlib import Path
from backend.crawlers import CategoryTreeCrawler

# Configure output
OUTPUT_DIR = Path("data/exports")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_FILE = OUTPUT_DIR / "pricerunner_categories.csv"

# Create crawler
crawler = CategoryTreeCrawler(
    base_url="https://www.pricerunner.com",
    start_paths=["/", "/t/"],  # Start from homepage and /t/ hub
    path_patterns=["/t/", "/cl/"],  # Follow /t/ and /cl/ links
    max_depth=5,  # Max 5 levels deep
    requests_per_minute=15,  # Conservative rate limit (4 seconds between requests)
    timeout=30
)

# Start crawling
print("=" * 60)
print("PriceRunner Category Tree Crawler")
print("=" * 60)
print()

categories = crawler.crawl()

print()
print("=" * 60)
print("Exporting to CSV...")
print("=" * 60)

# Export to CSV
crawler.export_to_csv(OUTPUT_FILE)

print()
print(f"✅ Complete! Exported {len(categories)} categories to:")
print(f"   {OUTPUT_FILE.absolute()}")
print()

# Show sample
print("Sample categories:")
print("-" * 60)
for cat in categories[:10]:
    print(f"[Level {cat.depth}] {cat.full_path}")
print()
