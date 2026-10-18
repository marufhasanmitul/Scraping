from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://inventory.teamrabbil.com", wait_until="networkidle")

    for _ in range(50):
        page.mouse.wheel(0,50)
        time.sleep(1)

    time.sleep(1)


    for _ in range(50):
        page.mouse.wheel(0,-50)
        time.sleep(1)


    browser.close()