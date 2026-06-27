from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False, slow_mo=100000)
    page = browser.new_page()
    query = "cats"    
    page.goto(f"http://www.google.com/search?client=firefox-b-d&q={query}")
    browser.close()