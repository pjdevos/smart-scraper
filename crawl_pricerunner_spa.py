#!/usr/bin/env python
"""
PriceRunner SPA Category Crawler
Async crawler with API interception for Single Page Applications
"""
import asyncio
from pathlib import Path
from backend.crawlers.spa_category_crawler import SPACategoryCrawler

# Output
OUTPUT_DIR = Path("data/exports")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
OUTPUT_FILE = OUTPUT_DIR / "pricerunner_categories_spa.csv"


async def main():
    print("=" * 80)
    print("PriceRunner SPA Category Crawler")
    print("=" * 80)
    print()

    # Create crawler
    crawler = SPACategoryCrawler(
        base_url="https://www.pricerunner.com",
        headless=False,  # Set to True for headless mode
        max_depth=5,
        requests_per_second=0.5,  # Conservative: 2 seconds between requests
        timeout=30
    )

    # Crawl
    categories = await crawler.crawl()

    print()
    print("=" * 80)
    print("Exporting to CSV...")
    print("=" * 80)

    # Export
    crawler.export_to_csv(OUTPUT_FILE)

    print()
    print(f"[OK] Complete! Exported {len(categories)} categories to:")
    print(f"   {OUTPUT_FILE.absolute()}")
    print()

    if categories:
        print("Sample categories:")
        print("-" * 80)
        for cat in categories[:15]:
            print(f"[{cat.id}] {cat.name} - {cat.url}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
