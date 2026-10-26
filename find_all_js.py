import asyncio
import json
import random
from playwright.async_api import async_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

URL = "https://inventory.teamrabbil.com/"

async def main():
    sizes = {}
    js_files = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = await context.new_page()

        print("Processing JS files...")

        # Capture JS file sizes
        async def add_size(res):
            if res.request.resource_type == "script":
                try:
                    body = await res.body()
                    sizes[res.url] = len(body)
                except:
                    pass

        page.on("response", add_size)
        await page.goto(URL, wait_until='load')

        # Collect JS URLs from DOM
        dom_js = await page.evaluate("""
            () => Array.from(document.scripts)
                .map(s => ({
                    url: s.src
                }))
        """)

        # Merge downloaded JS size
        for file in dom_js:
            byte_value = sizes.get(file["url"])
            file["size_kb"] = round(byte_value / 1024, 2) if byte_value else None
            js_files.append(file)

        # Save JSON output
        with open("js_files.json", "w", encoding="utf-8") as f:
            json.dump(js_files, f, indent=2, ensure_ascii=False)

        print("Done")
        await browser.close()

asyncio.run(main())
