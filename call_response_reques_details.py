import asyncio
import random
from playwright.async_api import async_playwright
import json

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]


URL = "https://www.prothomalo.com/"

def is_api(url):
    clean = url.split("?", 1)[0]
    clean = clean.split("#", 1)[0]
    clean_no_slash = clean.rstrip("/")
    last = clean_no_slash.rsplit("/", 1)[-1]
    return "." not in last


async def main():

    api_logs =[]


    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = await context.new_page()



        # Response Event
        async def on_response(res):
            if is_api(res.url):
                req= res.request
                url = req.url
                method=req.method
                status=res.status

                try:
                    req_body= await req.post_data()
                except:
                    req_body=None

                try:
                    res_body= await res.json()
                except:
                    res_body=None

                api_logs.append({
                    "url": url,
                    "method": method,
                    "status": status,
                    "req_body": req_body,
                    "res_body": res_body
                })



        page.on("response", on_response)

        await page.goto(URL, wait_until="load")


        with open('api_logs.json', 'w',encoding='utf-8') as file:
            json.dump(api_logs, file, ensure_ascii=False, indent=4)



        print("Done")
        await browser.close()


asyncio.run(main())
