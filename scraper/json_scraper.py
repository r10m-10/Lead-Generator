from curl_cffi import requests
import json

query = "dentists in delhi"
url = "https://www.google.com/search"
pb = "!4m8!1m3!1d28027.459775185278!2d77.1719168!3d28.5868001!3m2!1i1024!2i768!4f13.1!7i20!8i0!10b1!12m62!1m5!18b1!30b1!31m1!1b1!34e1!2m4!5m1!6e2!20e3!39b1!6m32!32i1!49b1!63m0!66b1!85b1!114b1!149b1!206b1!209b1!212b1!215b1!216b1!222b1!223b1!234b1!235b1!239b1!246b1!253b1!260b1!262b1!266b1!267b1!270b1!271b1!273b1!281b1!294b1!300b1!301b1!302i300!303i100!10b1!12b1!13b1!14b1!16b1!17m1!3e1!20m4!5e2!6b1!8b1!14b1!46m1!1b0!96b1!97m1!2b1!99b1!19m4!2m3!1i360!2i120!4i8!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0!15m16!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!22m5!1se-Xmao6EGfWbseMP0LSS-Qg:124!2s1i:0,t:246204,p:e-Xmao6EGfWbseMP0LSS-Qg:124!7e81!12e22!17se-Xmao6EGfWbseMP0LSS-Qg:125!24m107!1m25!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1!18m14!3b1!4b1!5b1!6b1!13b1!14b1!17b1!21b1!22b1!32b1!33m1!1b1!34b1!36e2!10m1!8e3!11m1!3e1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!27b1!29b1!30m1!2b1!36b1!37b1!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m1!1b1!61m2!1m1!1e1!65m5!3m4!1m3!1m2!1i224!2i298!72m22!1m8!2b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!4b1!8m10!1m6!4m1!1e1!4m1!1e3!4m1!1e4!3sother_user_google_review_posts__and__hotel_and_vr_partner_review_posts!6m1!1e1!9b1!89b1!90m2!1m1!1e2!98m3!1b1!2b1!3b1!103b1!113b1!114m3!1b1!2m1!1b1!117b1!122m1!1b1!126b1!127b1!128m1!1b1!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i530!2i768!1m6!1m2!1i974!2i0!2m2!1i1024!2i768!1m6!1m2!1i0!2i0!2m2!1i1024!2i20!1m6!1m2!1i0!2i748!2m2!1i1024!2i768!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1!37m1!1e81!42b1!46m1!1e2!47m0!49m10!3b1!6m2!1b1!2b1!7m2!1e3!2b1!8b1!9b1!10e2!50m25!1m21!2m7!1u3!4sOpen now!5e1!9s2ahUKEwiNm5iZm-aXAxVvaHADHf7nFtsQ_KkBKAJ6BAgaEAY!10m2!3m1!1e1!2m7!1u2!4sTop-rated!5e1!9s2ahUKEwiNm5iZm-aXAxVvaHADHf7nFtsQ_KkBKAN6BAgaEAc!10m2!2m1!1e1!3m1!1u2!3m1!1u3!4BIAE!2e2!3m1!3b1!59BQ2dBd0Fn!61b1!67m5!7b1!10b1!14b1!15m1!1b0!69i801!77b1"
params = {
    "tbm": "map",
    "authuser": 0,
    "hl": "en",
    "gl": "in",
    "q": query,
    "pb": pb,
    "ech": 1,
    "psi": "e-Xmao6EGfWbseMP0LSS-Qg.1793516925076.1"
}

response = requests.get(url=url, params=params, impersonate="chrome")

raw_text = response.text

if raw_text.startswith(")]}'"):
    raw_text = raw_text[4:]

decoder = json.JSONDecoder()
data, idx = decoder.raw_decode(raw_text.strip())

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

data = data[64]
leads = []

for i in data:
    d = {}

    try:
        d['place_id'] = i[1][78]
    except (TypeError, IndexError):
        continue

    d['name'] = create_field('name', i)
    d['phone_number'] = create_field('phone_number', i)
    d['website'] = create_field('website', i)
    if d['website'] is None and d['phone_number'] is None:
        continue
    d['stars'] = create_field('stars', i)
    d['reviews'] = create_field('reviews', i)
    d['address'] = create_field('address', i)

    leads.append(d)

with open("gmaps_debug.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(leads, len(leads))