import asyncio
import pandas as pd
from playwright.async_api import async_playwright


async def get_meta(page, selector, attr="content"):
    el = await page.query_selector(selector)
    return await el.get_attribute(attr) if el else ""




async def main():
    url="https://www.youtube.com/watch?v=lpB3nMC2iZg&t=114s"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()


        await page.goto(url,wait_until="domcontentloaded")

        video_id = url.split("v=")[-1]

        data = {
            "video_url": url,
            "video_id": video_id,

            # SEO / Meta
            "title": await get_meta(page, 'meta[name="title"]'),
            "description": await get_meta(page, 'meta[name="description"]'),
            "keywords": await get_meta(page, 'meta[name="keywords"]'),
            "og_title": await get_meta(page, 'meta[property="og:title"]'),
            "og_description": await get_meta(page, 'meta[property="og:description"]'),
            "og_tags": await get_meta(page, 'meta[property="og:video:tag"]'),

            # Thumbnails
            "thumbnail_default": f"https://img.youtube.com/vi/{video_id}/default.jpg",
            "thumbnail_medium": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
            "thumbnail_high": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            "thumbnail_max": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",

            # Channel Info
            "channel_name": await page.locator("ytd-channel-name a").inner_text(),
            "channel_url": await page.locator("ytd-channel-name a").get_attribute("href"),
        }



        print(data)











asyncio.run(main())
