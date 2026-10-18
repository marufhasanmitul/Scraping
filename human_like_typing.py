import random
import time

from playwright.sync_api import sync_playwright

def human_type(element,text):
    for char in text:
        element.type(char,delay=random.randint(30,120))

        # optional tiny pause sometimes
        if random.random() < 0.05:
            time.sleep(random.uniform(0.05, 0.25))




with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://inventory.teamrabbil.com", wait_until="networkidle")

    # Locate inputs
    name_input = page.locator("input[placeholder='Name']")
    email_input = page.locator("input[placeholder='E-mail']")
    msg_input = page.locator("textarea[placeholder='Your Message...']")

    # ✅ Human typing
    human_type(name_input, "Mr Rabbil")
    human_type(email_input, "rabbil@example.com")
    human_type(msg_input, "Hello, this message is typed as human.")

    # Click submit
    page.locator("button:has-text('Action')").click()

    time.sleep(2)
    browser.close()