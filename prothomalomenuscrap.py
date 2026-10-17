from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.prothomalo.com/", wait_until="domcontentloaded")

    a_tags = page.locator("ul.navbar-list a")

    total_count = a_tags.count()
    print("Total Menu:", total_count)

    for i in range(total_count):
        element = a_tags.nth(i)

        text = element.inner_text().strip()
        href = element.get_attribute("href")

        print("Text:", text)
        print("Href:", href)
        print("-" * 40)

    browser.close()
