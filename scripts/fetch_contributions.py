import os
import json
import requests
from bs4 import BeautifulSoup

username = os.environ.get("GH_USERNAME", "sepansarr")
url = f"https://github.com/users/{username}/contributions"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
days = soup.find_all("td", class_="ContributionCalendar-day")

data = []
for day in days:
    date = day.get("data-date")
    level = day.get("data-level", "0")
    if date:
        data.append({"date": date, "level": int(level)})

os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
