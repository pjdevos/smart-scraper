#!/usr/bin/env python
"""
PriceRunner Full Hierarchy Crawler
Recursively crawls all category levels to build complete tree
"""
import asyncio
import csv
import json
from pathlib import Path
from typing import List, Dict, Set
from playwright.async_api import async_playwright

OUTPUT_FILE = Path("data/exports/pricerunner_full_hierarchy.csv")
OUTPUT_FILE.parent.mkdir(exist_ok=True, parents=True)


class HierarchyCrawler:
    def __init__(self, max_depth: int = 5, delay: float = 2.0, checkpoint_file: Path = None):
        self.max_depth = max_depth
        self.delay = delay
        self.categories = []
        self.seen_urls: Set[str] = set()
        self.browser = None
        self.context = None
        self.checkpoint_file = checkpoint_file or Path("data/crawler_checkpoint.json")
        self.completed_seeds: Set[str] = set()
        self.output_file = None

    async def init_browser(self):
        """Initialize browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            locale="en-GB",
            viewport={"width": 1920, "height": 1080}
        )

    async def close_browser(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()

    def load_checkpoint(self):
        """Load checkpoint to resume crawling"""
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, 'r') as f:
                    data = json.load(f)
                    self.completed_seeds = set(data.get('completed_seeds', []))
                    self.seen_urls = set(data.get('seen_urls', []))
                    print(f"Loaded checkpoint: {len(self.completed_seeds)} seeds completed, {len(self.seen_urls)} URLs seen")
            except Exception as e:
                print(f"Error loading checkpoint: {e}")

    def save_checkpoint(self, seed_url: str):
        """Save checkpoint after completing a seed"""
        self.completed_seeds.add(seed_url)
        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump({
                    'completed_seeds': list(self.completed_seeds),
                    'seen_urls': list(self.seen_urls)
                }, f)
            print(f"Checkpoint saved ({len(self.completed_seeds)} seeds completed)")
        except Exception as e:
            print(f"Error saving checkpoint: {e}")

    def append_to_csv(self, categories: List[Dict]):
        """Append categories to CSV file incrementally"""
        if not categories:
            return

        # Check if file exists to determine if we need headers
        file_exists = self.output_file.exists()

        # Find max depth
        max_depth = max(cat['depth'] for cat in categories)

        # Headers
        headers = [f"level_{i}" for i in range(1, max_depth + 1)]
        headers += ['depth', 'full_path', 'url', 'category_id']

        with open(self.output_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')

            # Write header only if file is new
            if not file_exists:
                writer.writerow(headers)

            for cat in categories:
                row = []

                # Fill level columns
                path_parts = cat['parent_path'] + [cat['name']]
                for i in range(max_depth):
                    row.append(path_parts[i] if i < len(path_parts) else '')

                # Add metadata
                row.extend([
                    cat['depth'],
                    cat['full_path'],
                    cat['url'],
                    cat['id']
                ])

                writer.writerow(row)

    def extract_category_id(self, url: str) -> str:
        """Extract category ID from URL"""
        if '/cl/' in url:
            return url.split('/cl/')[1].split('/')[0].split('?')[0]
        elif '/t/' in url:
            return url.split('/t/')[1].split('/')[0].split('?')[0]
        return url

    async def extract_subcategories(self, page, parent_path: List[str], depth: int):
        """Extract subcategories from current page"""
        subcategories = []

        # Wait for page to load
        await asyncio.sleep(self.delay)

        # Try different selectors for subcategory links
        selectors = [
            'a[href*="/cl/"]',
            'a[href*="/t/"]',
            'nav a',
            '[role="navigation"] a',
            '.category-link',
            '[data-testid*="category"] a'
        ]

        for selector in selectors:
            try:
                links = await page.locator(selector).all()

                for link in links:
                    try:
                        href = await link.get_attribute('href')
                        text = await link.inner_text()

                        if not href or not text:
                            continue

                        # Make absolute URL
                        if href.startswith('/'):
                            href = f"https://www.pricerunner.com{href}"

                        # Skip if already seen
                        if href in self.seen_urls:
                            continue

                        # Only category URLs
                        if '/cl/' not in href and '/t/' not in href:
                            continue

                        cat_id = self.extract_category_id(href)
                        cat_name = text.strip()[:100]

                        # Skip empty or generic names
                        if not cat_name or cat_name.lower() in ['see all', 'view all', 'more']:
                            continue

                        subcategories.append({
                            'id': cat_id,
                            'name': cat_name,
                            'url': href,
                            'parent_path': parent_path.copy()
                        })

                    except Exception as e:
                        continue

            except Exception as e:
                continue

        # Deduplicate by ID
        seen_ids = set()
        unique_subcats = []
        for cat in subcategories:
            if cat['id'] not in seen_ids:
                seen_ids.add(cat['id'])
                unique_subcats.append(cat)

        return unique_subcats

    async def crawl_category(self, url: str, name: str, parent_path: List[str], depth: int):
        """Recursively crawl a category and its children"""
        if depth > self.max_depth:
            return

        if url in self.seen_urls:
            return

        self.seen_urls.add(url)

        # Build current path
        current_path = parent_path + [name]
        cat_id = self.extract_category_id(url)

        print(f"{'  ' * (depth - 1)}[Level {depth}] {' > '.join(current_path)}")

        # Add to results
        self.categories.append({
            'id': cat_id,
            'name': name,
            'url': url,
            'depth': depth,
            'parent_path': parent_path,
            'full_path': ' > '.join(current_path)
        })

        # Open page to find subcategories
        page = await self.context.new_page()

        try:
            print(f"{'  ' * (depth - 1)}  Loading: {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Extract subcategories
            subcategories = await self.extract_subcategories(page, current_path, depth)

            print(f"{'  ' * (depth - 1)}  Found {len(subcategories)} subcategories")

            # Recursively crawl each subcategory
            for subcat in subcategories:
                await self.crawl_category(
                    url=subcat['url'],
                    name=subcat['name'],
                    parent_path=current_path,
                    depth=depth + 1
                )

        except Exception as e:
            print(f"{'  ' * (depth - 1)}  Error: {e}")

        finally:
            await page.close()

    async def crawl_from_seeds(self, seed_file: Path, output_file: Path):
        """Start crawling from seed categories"""
        self.output_file = output_file

        # Load checkpoint
        self.load_checkpoint()

        # Load seeds
        seeds = []
        with open(seed_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                # Only start from main categories (/t/)
                if row['type'] == 'main_category':
                    # Skip if already completed
                    if row['url'] not in self.completed_seeds:
                        seeds.append(row)

        print(f"Starting crawl from {len(seeds)} main categories")
        if self.completed_seeds:
            print(f"Resuming from checkpoint ({len(self.completed_seeds)} already completed)")
        print("="*80)
        print()

        await self.init_browser()

        try:
            for i, seed in enumerate(seeds, 1):
                print(f"\n[{i}/{len(seeds)}] Starting: {seed['name']}")
                print("-"*80)

                # Reset category buffer for this seed
                seed_categories = []
                original_categories_len = len(self.categories)

                await self.crawl_category(
                    url=seed['url'],
                    name=seed['name'],
                    parent_path=[],
                    depth=1
                )

                # Get new categories from this seed
                seed_categories = self.categories[original_categories_len:]

                # Append to CSV immediately
                if seed_categories:
                    print(f"Saving {len(seed_categories)} categories from {seed['name']}...")
                    self.append_to_csv(seed_categories)

                # Save checkpoint
                self.save_checkpoint(seed['url'])

                print(f"Completed: {seed['name']} ({len(seed_categories)} categories)")
                print()

        finally:
            await self.close_browser()

    def export_to_csv(self, output_file: Path):
        """Export to hierarchical CSV"""
        if not self.categories:
            print("No categories to export")
            return

        # Find max depth
        max_depth = max(cat['depth'] for cat in self.categories)

        # Headers
        headers = [f"level_{i}" for i in range(1, max_depth + 1)]
        headers += ['depth', 'full_path', 'url', 'category_id']

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow(headers)  # Write header row

            for cat in sorted(self.categories, key=lambda c: (c['depth'], c['full_path'])):
                row = []

                # Fill level columns
                path_parts = cat['parent_path'] + [cat['name']]
                for i in range(max_depth):
                    row.append(path_parts[i] if i < len(path_parts) else '')

                # Add metadata
                row.extend([
                    cat['depth'],
                    cat['full_path'],
                    cat['url'],
                    cat['id']
                ])

                writer.writerow(row)

        print(f"\n[OK] Exported {len(self.categories)} categories to: {output_file}")


async def main():
    print("="*80)
    print("PriceRunner Full Hierarchy Crawler")
    print("="*80)
    print()

    # Check if seed file exists
    seed_file = Path("data/exports/pricerunner_categories_quick.csv")
    if not seed_file.exists():
        print(f"[ERROR] Seed file not found: {seed_file}")
        print("Please run: python extract_pricerunner_categories.py first")
        return

    # Create crawler
    crawler = HierarchyCrawler(
        max_depth=5,  # Max 5 levels deep
        delay=2.0     # 2 second delay between pages
    )

    # Crawl
    await crawler.crawl_from_seeds(seed_file, OUTPUT_FILE)

    print()
    print("="*80)
    print("Crawl Complete!")
    print("="*80)

    # Stats
    print()
    print("Statistics:")
    print("-"*80)
    for depth in range(1, 6):
        count = sum(1 for c in crawler.categories if c['depth'] == depth)
        if count > 0:
            print(f"  Level {depth}: {count} categories")

    print()
    print("Sample hierarchy:")
    print("-"*80)
    for cat in crawler.categories[:10]:
        print(f"  [Level {cat['depth']}] {cat['full_path']}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
