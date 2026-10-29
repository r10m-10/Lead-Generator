from curl_cffi import requests
import json

query = "dentist in delhi"
url = "https://www.google.com/search"
params = {
    "tbm": "map",
    "hl": "en",
    "gl": "in",
    "q": query,
    "pb": "!4m9!1m3!1d19816!2d77.1719!3d28.5868!2m0!3m2!1i1920!2i1080!4f13.1"
}

response = requests.get(url=url, params=params, impersonate="chrome")

raw_text = response.text

if raw_text.startswith(")]}'"):
    raw_text = raw_text[4:]

data = json.loads(raw_text)

print(data)