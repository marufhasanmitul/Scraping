import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.prothomalo.com", wait_until="networkidle")

    a_tag = page.locator("a.title-link")
    total_count = a_tag.count()

    print(total_count)

    data = []

    for i in range(total_count):
        element = a_tag.nth(i)

        text = element.inner_text().strip()
        href = element.get_attribute("href")

        data.append({
            "title": text,
            "href": href
        })

    # JSON দেখাবে
    print(json.dumps(data, ensure_ascii=False, indent=4))

    browser.close()
