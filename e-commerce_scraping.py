import asyncio
import pandas as pd
from playwright.async_api import async_playwright




async def main():
    url="https://www.daraz.com.bd"
    keyword="laptop"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context=await browser.new_context()

        page = await context.new_page()

        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector("input#q", timeout=3000)
        await page.fill("input#q", keyword)
        await page.wait_for_timeout(2000)
        await page.keyboard.press("Enter")
        await page.wait_for_selector("div[data-qa-locator='product-item']", timeout=3000)
        product_elements = await page.query_selector_all('div[data-qa-locator="product-item"]')

        result = []
        for each_element in product_elements:
            title_el = await each_element.query_selector("div.RfADt a")
            title = await title_el.inner_text() if title_el else ""

            price_el = await each_element.query_selector("span.ooOxS")
            price = await price_el.inner_text() if price_el else ""

            img_el = await each_element.query_selector("img[type='product']")
            img = await img_el.get_attribute("src") if img_el else ""

            location_el = await each_element.query_selector("span.oa6ri")
            location = await location_el.inner_text() if location_el else ""

            result.append({
                "title": title,
                "price": price,
                "img": img,
                "location": location,
            })



        await browser.close()

        df = pd.DataFrame(result)
        df.to_csv("result.csv")

        print("Done")



asyncio.run(main())