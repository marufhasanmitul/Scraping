
import asyncio
import random
import pandas as pd

from playwright.async_api import async_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )

        page = await context.new_page()

        try:
            await page.goto(
                "https://www.bbc.com/",
                wait_until="domcontentloaded",
                timeout=30000,
            )

            card_selector = (
                'div[data-testid="card-text-wrapper"]'
            )

            await page.locator(
                'h2[data-testid="card-headline"]'
            ).first.wait_for(timeout=10000)

            cards = page.locator(card_selector)
            count = await cards.count()

            data = []

            for index in range(count):
                card = cards.nth(index)

                title_el = card.locator(
                    'h2[data-testid="card-headline"]'
                )
                desc_el = card.locator(
                    'p[data-testid="card-description"]'
                )
                time_el = card.locator(
                    '[data-testid="card-metadata-lastupdated"]'
                )
                category_el = card.locator(
                    '[data-testid="card-metadata-tag"]'
                )

                title = (
                    (await title_el.first.inner_text()).strip()
                    if await title_el.count() else ""
                )

                description = (
                    (await desc_el.first.inner_text()).strip()
                    if await desc_el.count() else ""
                )

                published_time = (
                    (await time_el.first.inner_text()).strip()
                    if await time_el.count() else ""
                )

                category = (
                    (await category_el.first.inner_text()).strip()
                    if await category_el.count() else ""
                )

                if title:
                    data.append({
                        "id": len(data) + 1,
                        "title": title,
                        "description": description,
                        "published_time": published_time,
                        "category": category,
                    })

            df = pd.DataFrame(data)

            df.to_csv(
                "news_headline.csv",
                index=False,
                encoding="utf-8-sig",
            )

            print(df.to_string(index=False))
            print(f"\nTotal news: {len(data)}")
            print("Saved to news_headline.csv")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            await browser.close()


asyncio.run(main())
