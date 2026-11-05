from curl_cffi import requests
import json
import time

field_idx = {
    'name': lambda l: l[1][11],
    'phone_number': lambda l: l[1][178][0][1][1][0],
    'website': lambda l: l[1][7][0],
    'stars': lambda l: str(l[1][4][7]),
    'reviews': lambda l: str(l[1][4][8]),
    'address': lambda l: l[1][18]
    }

def create_field(field, business):
    try:
        return field_idx[field](business)
    except (TypeError, IndexError):
        return None

query = "dentists"
url = "https://www.google.com/search"
offset = 0
n_leads = 999
lng = 77.17191677375331
lat = 28.586875456779826
view_size = 19816.27571701334
pb = f"!4m12!1m3!1d{view_size}!2d{lng}!3d{lat}!2m3!1f0!2f0!3f0!3m2!1i1600!2i543!4f13.1!7i{n_leads}!8i{offset}!10b1!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1"

inter = set()

t = {1: 0.05, 2: 0.1, 3: 0.2}

for n in range(5):

    if n in t:
        new_lng = lng + t[n]
        pb = f"!4m12!1m3!1d{view_size}!2d{new_lng}!3d{lat}!2m3!1f0!2f0!3f0!3m2!1i1600!2i543!4f13.1!7i{n_leads}!8i{offset}!10b1!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1"
    elif n == 4:
        new_view_size = 9908.13785850667
        pb = f"!4m12!1m3!1d{new_view_size}!2d{lng}!3d{lat}!2m3!1f0!2f0!3f0!3m2!1i1600!2i543!4f13.1!7i{n_leads}!8i{offset}!10b1!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1"
    params = {
    "tbm": "map",
    "hl": "en",
    "gl": "in",
    "q": query,
    "pb": pb,
    }
    response = requests.get(url=url, params=params, impersonate="chrome")
    status_code = response.status_code

    raw_text = response.text

    if raw_text.startswith(")]}'"):
        raw_text = raw_text[4:]

    decoder = json.JSONDecoder()
    data, idx = decoder.raw_decode(raw_text.strip())

    data = data[64]

    leads = []
    dropped = {}
    union = set()

    for i in data:
        d = {}

        try:
            d['place_id'] = i[1][78]
        except (TypeError, IndexError):
            dropped[data.index(i)] = "place_id"
            continue

        d['name'] = create_field('name', i)
        d['phone_number'] = create_field('phone_number', i)
        d['website'] = create_field('website', i)
        if d['website'] is None and d['phone_number'] is None:
            dropped[data.index(i)] = "no phone and website"
            continue
        d['stars'] = create_field('stars', i)
        d['reviews'] = create_field('reviews', i)
        d['address'] = create_field('address', i)

        leads.append(d)

    place_id = set()
    for i in leads:
        place_id.add(i["place_id"])

    if n == 0:
        baseline = place_id
    else:
        inter = place_id & baseline

    print(f"Run: {n} | found Leads: {len(data)} | Kept: {len(leads)} | Dropped: {len(dropped)} | Overlap with baseline: {len(inter)}")
    time.sleep(2)