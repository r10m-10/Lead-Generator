from playwright.sync_api import sync_playwright

def scraper(query):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)

        search_box = page.locator('input[role="combobox"]')
        search_box.wait_for()
        search_box.fill(query)

        page.keyboard.press("Enter")
        page.wait_for_timeout(3000)

        businesses_loc = page.locator('div[role="article"]')
        businesses_loc.first.wait_for()

        scroller = page.locator('div[role="feed"]')
        scroller.wait_for()

        prev = businesses_loc.count()
        
        print("----------SCRAPING----------")
        while True:
            last_business = businesses_loc.nth(prev-1)
            last_business.scroll_into_view_if_needed()
            scroller.evaluate("(el) => el.scrollBy(0, 100)")
            page.wait_for_function("""(prev) => document.querySelectorAll('div[role="article"]').length > prev""", arg=prev)
            
            new = businesses_loc.count()
            print(f"Previous Count: {prev} | Current Count: {new}")

            if new == 16:
                break

            prev = new

        print(f"""
FOUND {prev} BUSINESSES
HOW MANY LEADS WOULD YOU LIKE TO GENERATE?""")
        n_leads = int(input(f"(number between 0 & {prev}):  "))

        print(f"\n----------GENERATING {n_leads} LEADS----------")

        leads = []

        for i in range(n_leads):
            card = businesses_loc.nth(i)
            d = {}
            d['name'] = card.get_attribute("aria-label")

            print(f"{i+1}. {d['name']}")

            rating_loc = card.locator('span[role="img"][aria-label*="stars"]')
            if rating_loc.count() == 0:
                d['rating'] = ""
            else:
                d['rating'] = rating_loc.get_attribute("aria-label")

            card.click()
            page.wait_for_function(
            """
            (name) => {
                const nameLoc = document.querySelector('[role="main"][aria-label]');

                if (!nameLoc) {
                    return false;
                }

                const newName = nameLoc.getAttribute("aria-label");

                return newName === name;
            }
            """,
            arg=d["name"]
            )
            
            phno_loc = page.locator('button[data-item-id^="phone"]')
            if phno_loc.count() == 0:
                d['phno'] = ""
            else:
                d['phno'] = phno_loc.get_attribute("aria-label")
            
            website_loc = page.locator('[data-item-id="authority"]')
            if website_loc.count() == 0:
                d['website'] = ""
            else:
                d['website'] = website_loc.get_attribute("href")
            
            print("GENERATED \n")
            
            leads.append(d)

        browser.close()
    return leads