from playwright.sync_api import sync_playwright
import time, random

# Human pause thinking
def human_think(min_s=0.3, max_s=1.4):
    time.sleep(random.uniform(min_s, max_s))

# Human typing character by character
def human_type(element, text):
    for char in text:
        element.type(char, delay=random.randint(30,120))  # random typing speed
        if random.random() < 0.05:                        # 5% chance small thinking pause
            human_think(0.1, 0.4)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://inventory.teamrabbil.com", wait_until="networkidle")

    # Get input fields
    name_input = page.locator("input[placeholder='Name']")
    email_input = page.locator("input[placeholder='E-mail']")
    msg_input = page.locator("textarea[placeholder='Your Message...']")

    # ✅ Human actions
    human_think()                        # thinking before typing
    human_type(name_input, "Mr Rabbil")

    human_think()                        # thinking again
    human_type(email_input, "rabbil@example.com")

    human_think(1, 2)                    # longer thinking before writing message
    human_type(msg_input, "Hello, I am testing human-like typing behavior.")




    human_think(1, 2)
    browser.close()