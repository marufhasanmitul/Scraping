import asyncio

import pandas as pd

from playwright.async_api import async_playwright

async def scroll_full_page(page):
    last_height=await page.evaluate('document.body.scrollHeight')
    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await  page.wait_for_timeout(5000)
        new_height = await page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height




async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()

        await page.goto("https://www.coingecko.com",wait_until="domcontentloaded")
        await page.wait_for_selector("table tbody tr")

        print("Scrolling Page...........")

        await scroll_full_page(page)

        rows=await page.query_selector_all("table tbody tr")

        result = []

        for row in rows:
            #Coin Name
            name_element=await row.query_selector("td:nth-child(3) a div div")
            name= (await name_element.text_content()).strip() if name_element else ""

            # Symbol
            symbol_element = await row.query_selector("td:nth-child(3) a div div div")
            symbol = (await symbol_element.text_content()).strip() if symbol_element else ""

            # Price
            price_element = await row.query_selector("td:nth-child(5) span")
            price = (await price_element.text_content()).strip() if price_element else ""

            # 1h %
            h1_element = await row.query_selector("td:nth-child(6) span")
            h1 = (await h1_element.text_content()).strip() if h1_element else ""

            # 24h %
            h24_element = await row.query_selector("td:nth-child(7) span")
            h24 = (await h1_element.text_content()).strip() if h24_element else ""

            # 7d %
            h7d_element = await row.query_selector("td:nth-child(8) span")
            h7d = (await h1_element.text_content()).strip() if h7d_element else ""

            item = {
                "name": name,
                "symbol": symbol,
                "price": price,
                "1h": h1,
                "24h": h24,
                "7d": h7d,
            }

            result.append(item)

        dataframe = pd.DataFrame(result)
        dataframe.to_csv("result.csv", index=False)







        print("Done....")
        await browser.close()











asyncio.run(main())