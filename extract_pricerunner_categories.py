#!/usr/bin/env python
"""
Quick PriceRunner Category Extractor
Extracts all visible category links from homepage
"""
import asyncio
import csv
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_FILE = Path("data/exports/pricerunner_categories_quick.csv")
OUTPUT_FILE.parent.mkdir(exist_ok=True, parents=True)


async def extract_categories():
    """Extract all category links from PriceRunner"""
    categories = []
    seen_urls = set()

    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            locale="en-GB",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        print("Loading PriceRunner homepage...")
        await page.goto("https://www.pricerunner.com/", wait_until="networkidle")
        await asyncio.sleep(3)

        print("Extracting category links...")

        # Try multiple selectors
        selectors = [
            'a[href*="/cl/"]',
            'a[href*="/t/"]',
            '[data-testid*="category"]',
            'nav a',
            'header a'
        ]

        for selector in selectors:
            print(f"\n  Trying selector: {selector}")
            links = await page.locator(selector).all()
            print(f"  Found {len(links)} links")

            for link in links:
                try:
                    href = await link.get_attribute('href')
                    text = await link.inner_text()

                    if not href or href in seen_urls:
                        continue

                    # Filter for category URLs
                    if '/cl/' in href or '/t/' in href:
                        seen_urls.add(href)

                        # Extract category ID
                        cat_id = None
                        if '/cl/' in href:
                            parts = href.split('/cl/')
                            if len(parts) > 1:
                                cat_id = parts[1].split('/')[0]
                        elif '/t/' in href:
                            parts = href.split('/t/')
                            if len(parts) > 1:
                                cat_id = parts[1].split('/')[0]

                        if cat_id:
                            # Make absolute URL
                            if href.startswith('/'):
                                href = f"https://www.pricerunner.com{href}"

                            categories.append({
                                'id': cat_id,
                                'name': text.strip()[:100],
                                'url': href,
                                'type': 'product_category' if '/cl/' in href else 'main_category'
                            })
                            print(f"    [{cat_id}] {text.strip()[:50]}")

                except Exception as e:
                    pass  # Skip errors

        # Also try scrolling and clicking menu
        print("\n  Checking navigation menu...")
        try:
            # Look for menu button
            menu_buttons = await page.locator('button:has-text("Menu"), button:has-text("Categories")').all()
            if menu_buttons:
                await menu_buttons[0].click()
                await asyncio.sleep(2)

                # Extract from opened menu
                menu_links = await page.locator('a[href*="/cl/"], a[href*="/t/"]').all()
                print(f"  Found {len(menu_links)} links in menu")

                for link in menu_links[:50]:  # Limit to prevent overload
                    try:
                        href = await link.get_attribute('href')
                        text = await link.inner_text()

                        if href and href not in seen_urls:
                            if '/cl/' in href or '/t/' in href:
                                seen_urls.add(href)

                                cat_id = None
                                if '/cl/' in href:
                                    cat_id = href.split('/cl/')[1].split('/')[0]
                                elif '/t/' in href:
                                    cat_id = href.split('/t/')[1].split('/')[0]

                                if cat_id:
                                    if href.startswith('/'):
                                        href = f"https://www.pricerunner.com{href}"

                                    categories.append({
                                        'id': cat_id,
                                        'name': text.strip()[:100],
                                        'url': href,
                                        'type': 'product_category' if '/cl/' in href else 'main_category'
                                    })
                                    print(f"    [{cat_id}] {text.strip()[:50]}")
                    except:
                        pass
        except Exception as e:
            print(f"  Menu interaction failed: {e}")

        await browser.close()

    return categories


async def main():
    print("="*80)
    print("PriceRunner Quick Category Extractor")
    print("="*80)
    print()

    categories = await extract_categories()

    print()
    print("="*80)
    print(f"Found {len(categories)} unique categories")
    print("="*80)

    # Export to CSV
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'url', 'type'], delimiter='|')
        writer.writeheader()
        writer.writerows(categories)

    print()
    print(f"[OK] Exported to: {OUTPUT_FILE.absolute()}")
    print()

    # Show stats
    main_cats = sum(1 for c in categories if c['type'] == 'main_category')
    prod_cats = sum(1 for c in categories if c['type'] == 'product_category')

    print("Category breakdown:")
    print(f"  Main categories (/t/): {main_cats}")
    print(f"  Product categories (/cl/): {prod_cats}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
