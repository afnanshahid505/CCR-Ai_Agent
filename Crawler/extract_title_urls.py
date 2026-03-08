from bs4 import BeautifulSoup
from pathlib import Path

INPUT_FILE = Path("data/root_page.html")
OUTPUT_FILE = Path("data/title_urls.txt")

BASE_URL = "https://govt.westlaw.com"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

title_links = []

for a in soup.find_all("a", href=True):
    href = a["href"]

    if "/calregs/Browse/Home/California/CaliforniaCodeofRegulations?guid=" in href:
        full_url = BASE_URL + href

        title = a.get_text(strip=True)

        title_links.append((title, full_url))

print("Titles discovered:", len(title_links))

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for title, url in title_links:
        f.write(f"{title} | {url}\n")

print("Saved to:", OUTPUT_FILE)