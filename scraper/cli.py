from scraper.scraper import scraper
from scraper.excel import convert_to_excel

print("""
1. Guided Search
2. Custom Search""")
srch = int(input(">  "))

if srch == 1:
    niche = str(input("""\nEnter Niche of Business (ex: Denstist, Cafe, etc.)
>  """))
    
    loc = str(input("""\nEnter Search Location (ex: Delhi, Mumbai, etc.)
>  """))
    
    query = f"{niche} in {loc}"

else:
    query = str(input("""\nEnter custom query (ex: Denstist in Delhi)
>  """))

scraped = scraper(query)

if scraped["error"] == False:
    convert_to_excel(scraped["leads"])
else:
    if len(scraped["leads"]) > 0:
        convert_to_excel(scraped["leads"])
    print(scraped["error"])