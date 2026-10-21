import asyncio
import random
import time

from playwright.async_api import async_playwright


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]



KEYWORDS = ["laptop", "keyboard", "router", "monitor", "ssd"]

async def search_amazon(page,keyword):
    await page.goto("https://www.google.com/",wait_until="domcontentloaded")

    box = page.locator('textarea[name="q"]')

    await box.click()
    await box.fill(keyword)
    await box.press("Enter")
    time.sleep(3)



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=random.choice(USER_AGENTS))

        # ৫টি Tab তৈরি
        pages = []

        for _ in range(len(KEYWORDS)):
            pages.append(await context.new_page())

        tasks=[]
        for i in range (len(pages)):
            tasks.append(search_amazon(pages[i],KEYWORDS[i]))
        await asyncio.gather(*tasks)

        await asyncio.sleep(5)
        await browser.close()

        print("Done")



asyncio.run(main())