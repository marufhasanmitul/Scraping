import asyncio
from playwright.async_api import async_playwright
import pandas as pd





async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        print("processing.........")
        await page.goto("https://www.dse.com.bd/circuit-breaker")

        await page.wait_for_selector("table[data-cms='markets.circuit-breaker'] tbody tr",timeout=30000)

        all_rows=await page.query_selector_all("table[data-cms='markets.circuit-breaker'] tbody tr")

        result=[]
        for each_row in all_rows:
            all_columns = await each_row.query_selector_all("td")

            values=[]
            for each_column in all_columns:
                text = await each_column.text_content()
                values.append(text.strip() if text else "")

            item={
                "TREAD CODE":values[0],
                "COMPANY":values[1],
                "CLOSE PRICE":values[2],
                "BREAKER":values[3],
                "TICKSIZE":values[4],
                "OPEN ADJUSTMENT":values[5],
                "LOWER":values[6],
                "UPPER":values[7]
            }

            result.append(item)

        print(result)

        dataframe = pd.DataFrame(result)
        dataframe.to_csv(
            "share_price.csv",
            index=False,
            encoding="utf-8-sig"
        )





        await browser.close()














asyncio.run(main())