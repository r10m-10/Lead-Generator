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
offset = 40
pb = f"!4m12!1m3!1d19816.27571701334!2d77.17191677375331!3d28.586875456779826!2m3!1f0!2f0!3f0!3m2!1i1600!2i543!4f13.1!7i20!8i{offset}!10b1!12m26!1m5!18b1!30b1!31m1!1b1!34e1!2m4!5m1!6e2!20e3!39b1!10b1!12b1!13b1!16b1!17m1!3e1!20m4!5e2!6b1!8b1!14b1!46m1!1b0!96b1!99b1!19m4!2m3!1i360!2i120!4i8!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0!15m16!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!22m6!1sA_viatWkIN-hseMPoeDE6Q8:2!2s1i:0,t:11886,p:A_viatWkIN-hseMPoeDE6Q8:2!7e81!12e5!17sA_viatWkIN-hseMPoeDE6Q8:205!18e15!24m109!1m27!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1!18m16!3b1!4b1!5b1!6b1!9b1!13b1!14b1!17b1!20b1!21b1!22b1!32b1!33m1!1b1!34b1!36e2!10m1!8e3!11m1!3e1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!27b1!29b1!30m1!2b1!36b1!37b1!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m1!1b1!61m2!1m1!1e1!65m5!3m4!1m3!1m2!1i224!2i298!72m22!1m8!2b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!4b1!8m10!1m6!4m1!1e1!4m1!1e3!4m1!1e4!3sother_user_google_review_posts__and__hotel_and_vr_partner_review_posts!6m1!1e1!9b1!89b1!90m2!1m1!1e2!98m3!1b1!2b1!3b1!103b1!113b1!114m3!1b1!2m1!1b1!117b1!122m1!1b1!126b1!127b1!128m1!1b1!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i530!2i543!1m6!1m2!1i1550!2i0!2m2!1i1600!2i543!1m6!1m2!1i0!2i0!2m2!1i1600!2i20!1m6!1m2!1i0!2i523!2m2!1i1600!2i543!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1!37m1!1e81!42b1!47m0!49m10!3b1!6m2!1b1!2b1!7m2!1e3!2b1!8b1!9b1!10e2!50m4!2e2!3m2!1b1!3b1!67m5!7b1!10b1!14b1!15m1!1b0!69i801!77b1"

pb0 = "!4m12!1m3!1d19816.27571701334!2d77.17191677375331!3d28.586875456779826!2m3!1f0!2f0!3f0!3m2!1i1600!2i543!4f13.1!7i20!8i0!10b1!12m26!1m5!18b1!30b1!31m1!1b1!34e1!2m4!5m1!6e2!20e3!39b1!10b1!12b1!13b1!16b1!17m1!3e1!20m4!5e2!6b1!8b1!14b1!46m1!1b0!96b1!99b1!19m4!2m3!1i360!2i120!4i8!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0!15m16!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20!22m6!1sA_viatWkIN-hseMPoeDE6Q8:2!2s1i:0,t:11886,p:A_viatWkIN-hseMPoeDE6Q8:2!7e81!12e5!17sA_viatWkIN-hseMPoeDE6Q8:205!18e15!24m109!1m27!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1!18m16!3b1!4b1!5b1!6b1!9b1!13b1!14b1!17b1!20b1!21b1!22b1!32b1!33m1!1b1!34b1!36e2!10m1!8e3!11m1!3e1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!27b1!29b1!30m1!2b1!36b1!37b1!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m1!1b1!61m2!1m1!1e1!65m5!3m4!1m3!1m2!1i224!2i298!72m22!1m8!2b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!4b1!8m10!1m6!4m1!1e1!4m1!1e3!4m1!1e4!3sother_user_google_review_posts__and__hotel_and_vr_partner_review_posts!6m1!1e1!9b1!89b1!90m2!1m1!1e2!98m3!1b1!2b1!3b1!103b1!113b1!114m3!1b1!2m1!1b1!117b1!122m1!1b1!126b1!127b1!128m1!1b1!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i530!2i543!1m6!1m2!1i1550!2i0!2m2!1i1600!2i543!1m6!1m2!1i0!2i0!2m2!1i1600!2i20!1m6!1m2!1i0!2i523!2m2!1i1600!2i543!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1!37m1!1e81!42b1!47m0!49m10!3b1!6m2!1b1!2b1!7m2!1e3!2b1!8b1!9b1!10e2!50m4!2e2!3m2!1b1!3b1!67m5!7b1!10b1!14b1!15m1!1b0!69i801!77b1"

tests = [pb0[:pb0.find("!4m12")]+pb0[pb0.find("!7i20"):],
pb0[:pb0.find("!7i20")]+pb0[pb0.find("!8i"):],
pb0[:pb0.find("!8i")]+pb0[pb0.find("!10b1!12m26"):],
pb0[:pb0.find("!10b1!12m26")]+pb0[pb0.find("!12m26"):],
pb0[:pb0.find("!12m26")]+pb0[pb0.find("!19m4"):],
pb0[:pb0.find("!19m4")]+pb0[pb0.find("!20m65"):],
pb0[:pb0.find("!20m65")]+pb0[pb0.find("!22m6"):],
pb0[:pb0.find("!22m6")]+pb0[pb0.find("!24m109"):],
pb0[:pb0.find("!24m109")]+pb0[pb0.find("!26m4"):],
pb0[:pb0.find("!26m4")]+pb0[pb0.find("!30m28"):],
pb0[:pb0.find("!30m28")]+pb0[pb0.find("!34m19"):],
pb0[:pb0.find("!34m19")]+pb0[pb0.find("!37m1"):],
pb0[:pb0.find("!37m1")]+pb0[pb0.find("!42b1"):],
pb0[:pb0.find("!42b1")]+pb0[pb0.find("!47m0"):],
pb0[:pb0.find("!47m0")]+pb0[pb0.find("!49m10"):],
pb0[:pb0.find("!49m10")]+pb0[pb0.find("!50m4"):],
pb0[:pb0.find("!50m4")]+pb0[pb0.find("!67m5"):],
pb0[:pb0.find("!67m5")]+pb0[pb0.find("!69i801"):],
pb0[:pb0.find("!69i801")]+pb0[pb0.find("!77b1"):],
pb0[:pb0.find("!77b1")]]

names = ["baseline", "4m12", "7i20", "8i", "10b1", "12m26", "19m4", "20m65",
         "22m6", "24m109", "26m4", "30m28", "34m19", "37m1", "42b1", "47m0",
         "49m10", "50m4", "67m5", "69i801", "77b1"]

base_ids = set()

for n, test in enumerate([pb0] + tests):
    leads = []
    dropped = {}
    data = None
    status_code = None
    records = 0
    note = "ok"

    try:
        params = {
            "tbm": "map",
            "authuser": 0,
            "hl": "en",
            "gl": "in",
            "q": query,
            "pb": test,
        }

        response = requests.get(url=url, params=params, impersonate="chrome")
        status_code = response.status_code

        raw_text = response.text
        if raw_text.startswith(")]}'"):
            raw_text = raw_text[4:]

        data, end = json.JSONDecoder().raw_decode(raw_text.strip())

        record_list = data[64]
        records = len(record_list)

        for j, rec in enumerate(record_list):
            d = {}
            try:
                d['place_id'] = rec[1][78]
            except (TypeError, IndexError):
                dropped[j] = "place_id"
                continue

            d['name'] = create_field('name', rec)
            d['phone_number'] = create_field('phone_number', rec)
            d['website'] = create_field('website', rec)
            if d['website'] is None and d['phone_number'] is None:
                dropped[j] = "no phone and website"
                continue
            d['stars'] = create_field('stars', rec)
            d['reviews'] = create_field('reviews', rec)
            d['address'] = create_field('address', rec)

            leads.append(d)

    except Exception as e:
        note = type(e).__name__
        if isinstance(data, list):
            note += f" len(data)={len(data)} non-None={[k for k, v in enumerate(data) if v is not None]}"

    ids = {l['place_id'] for l in leads}
    if n == 0:
        base_ids = ids

    print(f"{names[n]} | http {status_code} | records {records} | kept {len(leads)} | "
          f"dropped {len(dropped)} {dropped} | overlap with baseline {len(ids & base_ids)}/{len(base_ids)} | {note}")

    time.sleep(2)