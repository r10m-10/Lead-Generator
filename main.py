from scraper import scraper
from excel import convert_to_excel

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

leads = scraper(query)

convert_to_excel(leads)