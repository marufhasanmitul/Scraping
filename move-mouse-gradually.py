import time

import pyautogui


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://inventory.teamrabbil.com")

    # ✅ Smooth Mouse Move (Easy Version)

    for i in range(100):   #number of steps
        # gradually move
        pyautogui.moveTo(10 + i * 8, 15 + i * 4)

        # small pause (smooth)
        time.sleep(0.01)

    time.sleep(2)
    browser.close()