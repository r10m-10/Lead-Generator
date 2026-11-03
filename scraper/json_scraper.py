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

query = "dentists in delhi"
url = "https://www.google.com/search"
offset = 0
n_leads = 999
pb = f"!4m12!1m3!1d19816.27571701334!2d77.17191677375331!3d28.586875456779826!2m3!1f0!2f0!3f0!3m2!1i1600!2i543!4f13.1!7i{n_leads}!8i{offset}!10b1!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1"

params = {
    "tbm": "map",
    "hl": "en",
    "gl": "in",
    "q": query,
    "pb": pb,
}

place_ids = []
inter = set()

for n in range(10):
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

    place_ids.append(place_id)

    if n == 0:
        prev = place_id
    else:
        inter = place_id & prev
        prev = place_id

    print(f"Run: {n} | found Leads: {len(data)} | Kept: {len(leads)} | Dropped: {len(dropped)} | Dropped data: {dropped} | Colliding with prev: {len(inter)}")
    time.sleep(2)

union = place_ids[0]
for i in place_ids[1:]:
    union = union | i

print(f"Final Union: {len(union)}")