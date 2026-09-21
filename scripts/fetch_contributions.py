import os
import json
import requests
from bs4 import BeautifulSoup

username = os.environ.get("GH_USERNAME", "sepansarr")
url = f"https://github.com/users/{username}/contributions"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
cells = soup.find_all(["td", "rect"], attrs={"data-date": True})

data = []
for cell in cells:
    date = cell.get("data-date")
    level = cell.get("data-level", "0")
    data.append({"date": date, "level": int(level)})

seen = set()
unique_data = []
for d in data:
    if d["date"] not in seen:
        seen.add(d["date"])
        unique_data.append(d)

unique_data.sort(key=lambda x: x["date"])

os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(unique_data, f, indent=2)
