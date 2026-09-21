from playwright.async_api import TimeoutError as PlaywrightTimeoutError

async def scraper(browser, query, n_leads):
    result = {"leads": [], "error": False}
    context = None

    try:
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.google.com/maps", timeout=60000)

        search_box = page.locator('input[role="combobox"]')
        try:
            await search_box.wait_for()
        except PlaywrightTimeoutError:
            result["error"] = "Network Error"
            return result
        await search_box.fill(query)

        await page.keyboard.press("Enter")
        try:
            await page.wait_for_load_state(timeout=3000)
        except PlaywrightTimeoutError:
            result["error"] = "Network Error"
            return result

        main = page.locator('div[role="main"]')
        businesses_loc = page.locator('div[role="article"]')

        combined = businesses_loc.first.or_(main.get_by_text("can't find", exact=False))

        try:
            await combined.wait_for()
        except PlaywrightTimeoutError:
            result["error"] = "Network Error"
            return result

        if await businesses_loc.first.count() > 0:
            prev = await businesses_loc.count()
        elif await main.get_by_text("can't find", exact=False).count() > 0:
            result["error"] = "Invalid Input"
            return result
        
        scroller = page.locator('div[role="feed"]')
        try:
            await scroller.wait_for()
        except PlaywrightTimeoutError:
            result["error"] = "Network Error"
            return result

        unsucessful = 0

        while True:
            last_business = businesses_loc.nth(prev-1)
            await last_business.scroll_into_view_if_needed()
            await scroller.evaluate("(el) => el.scrollBy(0, 100)")
            await page.wait_for_timeout(2000)
            try:
                await page.wait_for_function("""(prev) => document.querySelectorAll('div[role="article"]').length > prev""", arg=prev, timeout=1000)
            except PlaywrightTimeoutError:
                unsucessful += 1
                if unsucessful == 3:
                    break
            finally:
                new = await businesses_loc.count()
                if new != prev:
                    unsucessful = 0
            prev = new
            if prev >= n_leads:
                break

        if prev >= n_leads:
            n_busi = n_leads
        else:
            n_busi = prev

        for i in range(n_busi):
            card = businesses_loc.nth(i)
            d = {}
            name_loc = card.locator("> a")
            d['name'] = await name_loc.get_attribute("aria-label")

            await card.click()
            try:
                await page.wait_for_function(
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
            await page.wait_for_timeout(1500)
            
            phno_loc = page.locator('button[data-item-id^="phone"]')
            if await phno_loc.count() == 0:
                d['phone_number'] = None
            else:
                d['phone_number'] = await phno_loc.get_attribute("aria-label")
            
            website_loc = page.locator('[data-item-id="authority"]')
            if await website_loc.count() == 0:
                if d['phone_number'] == None:
                    continue
                else:
                    d['website'] = None
            else:
                d['website'] = await website_loc.get_attribute("href")

            rating_loc = card.locator('span[role="img"][aria-label*="stars"]')
            if await rating_loc.count() == 0:
                d['rating'] = None
            else:
                d['rating'] = await rating_loc.get_attribute("aria-label")            
            
            result['leads'].append(d)
    except Exception as e:
        if len(result['leads']) > 0:
            result['error'] = "Error occured during runtime"
        else:
            result['error'] = str(e)
    finally:
        if context is not None:
            await context.close()
    return result