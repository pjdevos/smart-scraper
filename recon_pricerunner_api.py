#!/usr/bin/env python
"""
PriceRunner API Reconnaissance
Intercepts XHR/Fetch calls to discover API endpoints
"""
import asyncio
import json
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Route, Request

# Output file for discovered endpoints
OUTPUT_FILE = Path("data/pricerunner_api_map.json")
OUTPUT_FILE.parent.mkdir(exist_ok=True, parents=True)

# Tracked API calls
api_calls = []
seen_urls = set()


def safe_post_data(request: Request) -> Optional[str]:
    """Safely extract POST data, handling binary/gzip payloads"""
    if request.method != "POST":
        return None

    try:
        buf = request.post_data_buffer
        if not buf:
            return None

        # Check for GZIP
        if buf[:2] == b"\x1f\x8b":
            import gzip
            buf = gzip.decompress(buf)

        # Try to decode as UTF-8
        try:
            return buf.decode("utf-8")
        except UnicodeDecodeError:
            return f"<{len(buf)} bytes binary>"

    except Exception as e:
        return f"<error: {e}>"


async def intercept_handler(route: Route, request: Request):
    """Intercept and log API calls"""
    # Block analytics/tracking to speed up
    BLOCK_DOMAINS = (
        "taboola.com", "doubleclick.net", "google-analytics.com",
        "googletagmanager.com", "facebook.net", "adservice.google"
    )

    if any(blocked in request.url for blocked in BLOCK_DOMAINS):
        await route.abort()
        return

    # Only log XHR/Fetch
    if request.resource_type in ("xhr", "fetch"):
        url = request.url

        if url not in seen_urls:
            seen_urls.add(url)

            # Extract relevant info
            call_info = {
                "method": request.method,
                "url": url,
                "headers": {
                    k: v for k, v in request.headers.items()
                    if k.lower() in (
                        "accept", "authorization", "content-type",
                        "cookie", "accept-language", "x-api-key",
                        "x-client-id", "x-locale", "x-country"
                    )
                },
                "post_data": safe_post_data(request)
            }

            api_calls.append(call_info)

            print(f"\n{'='*80}")
            print(f"[{request.method}] {url}")
            print(f"Resource Type: {request.resource_type}")
            if call_info["headers"]:
                print("Headers:")
                for k, v in call_info["headers"].items():
                    print(f"  {k}: {v}")
            if call_info["post_data"]:
                print(f"POST Data: {call_info['post_data']}")
            print('='*80)

    # Continue with request (use fallback() for modern Playwright)
    await route.fallback()


async def explore_site():
    """Explore PriceRunner with Playwright and intercept API calls"""
    print("Starting PriceRunner API reconnaissance...")
    print("This will take 2-3 minutes to explore the site\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True for headless
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            locale="en-GB",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        # Setup route interception
        await page.route("**/*", intercept_handler)

        print("Step 1: Loading homepage...")
        await page.goto("https://www.pricerunner.com/", wait_until="networkidle")
        await asyncio.sleep(3)

        print("Step 2: Navigating to categories...")
        # Try to find and click a category
        try:
            # Look for category links (try multiple selectors)
            print("  Looking for category links...")

            # Try different URL patterns
            for pattern in ["/cl/", "/t/", "categories"]:
                category_links = await page.locator(f'a[href*="{pattern}"]').all()
                if category_links:
                    print(f"  Found {len(category_links)} links with '{pattern}'")
                    # Click first category
                    href = await category_links[0].get_attribute('href')
                    print(f"  Clicking: {href}")
                    await category_links[0].click()
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(3)
                    break

                print("Step 3: Scrolling to trigger pagination...")
                # Scroll to trigger lazy loading
                for i in range(5):
                    await page.mouse.wheel(0, 4000)
                    await asyncio.sleep(1.5)
                    print(f"  Scroll {i+1}/5...")

                print("Step 4: Clicking on a product...")
                # Try to click a product
                product_links = await page.locator('a[href*="/p/"]').all()
                if product_links and len(product_links) > 0:
                    await product_links[0].click()
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(3)
        except Exception as e:
            print(f"Navigation error (expected): {e}")

        print("\nStep 5: Exploring menu/navigation...")
        # Go back to homepage
        await page.goto("https://www.pricerunner.com/", wait_until="networkidle")
        await asyncio.sleep(2)

        # Try to interact with search
        try:
            search_input = page.locator('input[type="search"], input[placeholder*="Search"]').first
            if await search_input.count() > 0:
                await search_input.fill("laptop")
                await asyncio.sleep(2)
                await search_input.press("Enter")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(3)
        except Exception as e:
            print(f"Search error (expected): {e}")

        await browser.close()

    # Save results
    print(f"\n{'='*80}")
    print(f"Reconnaissance complete!")
    print(f"Discovered {len(api_calls)} unique API calls")
    print(f"{'='*80}\n")

    # Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(api_calls, f, indent=2)

    print(f"✅ API map saved to: {OUTPUT_FILE}\n")

    # Print summary
    print("API Endpoints Summary:")
    print("-" * 80)
    for call in api_calls:
        print(f"[{call['method']}] {call['url']}")
    print()


if __name__ == "__main__":
    asyncio.run(explore_site())
