import asyncio
from playwright.async_api import async_playwright


async def main():

    url = "https://eyewiki.org/Category:Cataract/Anterior_Segment"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()



        await page.goto(url, wait_until="domcontentloaded")

        links = page.locator("ul.smw-format.ul-format a")

        count = await links.count()

        result=[]
        for i in range(count):
            link = links.nth(i)

            href = await link.get_attribute("href")
            text = await link.inner_text()

            full_url = "https://eyewiki.org" + href


            result.append({
                "text": text.strip(),
                "href": full_url
            })



        print(result)







asyncio.run(main())