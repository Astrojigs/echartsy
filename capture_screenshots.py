#!/usr/bin/env python3
"""Capture PNG screenshots of every demo HTML file in ``assets/``.

Prerequisites
-------------
    pip install playwright
    playwright install chromium

Usage
-----
    python capture_screenshots.py

This opens each ``assets/demo_*.html`` file in a headless Chromium browser,
waits for ECharts to render, and saves a cropped PNG next to the HTML file.

The resulting PNGs are referenced by README.md.
"""
import asyncio
import glob
import os
import sys

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
WIDTH = 900
HEIGHT = 500


async def capture_all():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: playwright is not installed.")
        print("  pip install playwright && playwright install chromium")
        sys.exit(1)

    html_files = sorted(glob.glob(os.path.join(ASSETS, "demo_*.html")))
    if not html_files:
        print("No demo_*.html files found in assets/. Run generate_demos.py first.")
        sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})

        for html_path in html_files:
            name = os.path.splitext(os.path.basename(html_path))[0]
            png_path = os.path.join(ASSETS, f"{name}.png")

            url = f"file://{os.path.abspath(html_path)}"
            await page.goto(url, wait_until="networkidle")
            # Extra pause to let ECharts animations finish
            await page.wait_for_timeout(1500)
            await page.screenshot(path=png_path, full_page=False)
            print(f"  ✓ {png_path}")

        await browser.close()

    print(f"\nDone — {len(html_files)} screenshots saved to {ASSETS}/")


if __name__ == "__main__":
    asyncio.run(capture_all())
