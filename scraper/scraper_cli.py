from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def get_places_id(url):
    s = url.split(sep="!")
    tmp = None
    for i in s:
        if i.startswith("19s"):
            tmp = i[3:]
            break

    if tmp is None:
        return None
    
    idx = tmp.find('?')
    if idx == -1:
        return tmp
    
    return tmp[:idx]

def scraper(query):
    result = {"leads": [], "error": False}
    browser = None

    with sync_playwright() as p:
        try:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()

            page.goto("https://www.google.com/maps", timeout=60000)

            search_box = page.locator('input[role="combobox"]')
            try:
                search_box.wait_for()
            except PlaywrightTimeoutError:
                result["error"] = "Network Error"
                return result
            search_box.fill(query)

            page.keyboard.press("Enter")
            try:
                page.wait_for_load_state(timeout=3000)
            except PlaywrightTimeoutError:
                result["error"] = "Network Error"
                return result

            main = page.locator('div[role="main"]')
            businesses_loc = page.locator('div[role="article"]')

            combined = businesses_loc.first.or_(main.get_by_text("can't find", exact=False))

            try:
                combined.wait_for()
            except PlaywrightTimeoutError:
                result["error"] = "Network Error"
                return result

            if businesses_loc.first.count() > 0:
                prev = businesses_loc.count()
            elif main.get_by_text("can't find", exact=False).count() > 0:
                result["error"] = "Invalid Input"
                return result
            
            scroller = page.locator('div[role="feed"]')
            try:
                scroller.wait_for()
            except PlaywrightTimeoutError:
                result["error"] = "Network Error"
                return result

            unsucessful = 0

            print(f"""
HOW MANY LEADS WOULD YOU LIKE TO GENERATE?""")
            n_leads = int(input(f">  "))
            
            print("\n----------SCRAPING----------")
            while True:
                last_business = businesses_loc.nth(prev-1)
                last_business.scroll_into_view_if_needed()
                scroller.evaluate("(el) => el.scrollBy(0, 100)")
                page.wait_for_timeout(2000)
                try:
                    page.wait_for_function("""(prev) => document.querySelectorAll('div[role="article"]').length > prev""", arg=prev, timeout=1000)
                except PlaywrightTimeoutError:
                    unsucessful += 1
                    if unsucessful == 3:
                        break
                finally:
                    new = businesses_loc.count()
                    print(f"Previous Count: {prev} | Current Count: {new}")
                    if new != prev:
                        unsucessful = 0
                prev = new
                if prev >= n_leads:
                    break

            if prev >= n_leads:
                n_busi = n_leads
            else:
                n_busi = prev

            print(f"\n----------GENERATING LEADS----------")

            for i in range(n_busi):
                card = businesses_loc.nth(i)
                d = {}
                name_loc = card.locator("> a")

                d['name'] = name_loc.get_attribute("aria-label")

                url = name_loc.get_attribute("href")
                d['places_id'] = get_places_id(url)

                print(f"{i+1}. {d['name']}")

                card.click()
                try:
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
                except PlaywrightTimeoutError:
                    continue
                page.wait_for_timeout(1500)
                
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

                rating_loc = card.locator('span[role="img"][aria-label*="stars"]')
                if rating_loc.count() == 0:
                    d['rating'] = ""
                else:
                    d['rating'] = rating_loc.get_attribute("aria-label")            
                
                print("GENERATED \n")
                
                result["leads"].append(d)
        except Exception as e:
            if len(result["leads"]) > 0:
                result["error"] = "Error occured during runtime"
            else:
                result["error"] = str(e)
        finally:
            if browser is not None:
                browser.close()
    return result


print(scraper('Dentist in delhi'))