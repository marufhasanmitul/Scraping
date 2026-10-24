
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

URL = "https://www.prothomalo.com/"

async def main():
    sizes = {}
    images = []
    tasks = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS)
        )
        page = await context.new_page()

        print("Processing...")

        # Network: image response size collect
        async def add_size(response):
            if response.request.resource_type != "image":
                return

            if not 200 <= response.status < 300:
                return

            try:
                body = await response.body()
                sizes[response.url] = len(body)
            except Exception as e:
                print("Image response error:", e)

        # Track asynchronous response tasks
        def handle_response(response):
            task = asyncio.create_task(add_size(response))
            tasks.add(task)
            task.add_done_callback(tasks.discard)

        page.on("response", handle_response)

        try:
            await page.goto(
                URL,
                wait_until="load",
                timeout=60000
            )

            # DOM: image URL and dimensions
            dom_images = await page.evaluate("""
                () => Array.from(document.images).map(img => ({
                    url: img.currentSrc || img.src,
                    width: img.naturalWidth,
                    height: img.naturalHeight
                }))
            """)

            # Wait for response tasks already created
            while tasks:
                await asyncio.gather(
                    *list(tasks),
                    return_exceptions=True
                )

            # Merge DOM and Network data
            for img in dom_images:
                byte_value = sizes.get(img["url"])

                img["size_kb"] = (
                    round(byte_value / 1024, 2)
                    if byte_value is not None
                    else None
                )

                images.append(img)

            # Save JSON
            with open(
                "images.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    images,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            print(f"Done! Total images: {len(images)}")
            print("Saved to images.json")

        finally:
            await browser.close()


asyncio.run(main())
