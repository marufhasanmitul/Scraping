import asyncio
from playwright.async_api import async_playwright

URL = "https://rabbil.com/"

async def run():
    data = {"bytes": 0}   # simple container

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Add size for every response
        async def add_size(res):
            try:
                body = await res.body()
                data["bytes"] += len(body)
            except:
                pass

        page.on("response", add_size)

        await page.goto(URL, wait_until="load")

        # Convert sizes
        total_kb = round(data["bytes"] / 1024, 2)
        total_mb = round(total_kb / 1024, 2)

        print("Web Page Loaded:", URL)
        print(f"Total Size: {total_kb} KB  ({total_mb} MB)")

        await page.wait_for_timeout(3000)
        await browser.close()

asyncio.run(run())
