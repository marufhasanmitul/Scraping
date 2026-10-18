import random
import time

from playwright.sync_api import sync_playwright


def human_pause(min_s=0.3, max_s=1.2):
    time.sleep(random.uniform(min_s, max_s))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://inventory.teamrabbil.com", wait_until="networkidle")

    # Scroll Down slowly with random timing

    for _ in range(40):
        page.mouse.wheel(0,40)
        human_pause(min_s=0.02, max_s=0.08)
    human_pause(0.5, 1.5)  # pause before scrolling back up

    # Scroll Up slowly with random timing
    for _ in range(40):
        page.mouse.wheel(0, -40)
        human_pause(0.02, 0.08)

    browser.close()