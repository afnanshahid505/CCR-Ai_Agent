from bs4 import BeautifulSoup
from pathlib import Path

INPUT_DIR = Path("data/raw_titles")
OUTPUT_FILE = Path("data/hierarchy_links.txt")

BASE_URL = "https://govt.westlaw.com"

links = set()

for html_file in INPUT_DIR.glob("*.html"):

    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    container = soup.find("ul", class_="co_genericWhiteBox")

    if not container:
        continue

    for a in container.find_all("a", href=True):

        href = a["href"]

        if "/calregs/Browse/Home/" in href:
            full_url = BASE_URL + href
            links.add(full_url)

print("Hierarchy links discovered:", len(links))

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for link in sorted(links):
        f.write(link + "\n")

print("Saved to:", OUTPUT_FILE)