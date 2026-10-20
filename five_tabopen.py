import asyncio
from playwright.async_api import async_playwright
WINDOWS_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=WINDOWS_UA)

        url=[
            "https://google.com",
            "https://www.youtube.com",
            "https://www.amazon.com",
            "https://www.bing.com",
            "https://www.github.com",
        ]


        pages=[]

        for _ in range(5):
            pages.append(await context.new_page())

        task=[]

        for i in range(5):
            task.append(pages[i].goto(url[i]))

        await asyncio.gather(*task)

        print("Done")

        await asyncio.sleep(20)
        await browser.close()



asyncio.run(main())