import asyncio
from playwright.async_api import async_playwright
WINDOWS_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=WINDOWS_UA)
        page = await context.new_page()

        await page.goto("https://www.prothomalo.com/")

        await page.wait_for_timeout(2000)
        title=await page.title()

        print("Page title:", title)

        await browser.close()


asyncio.run(run())
