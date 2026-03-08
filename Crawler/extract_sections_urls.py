from bs4 import BeautifulSoup
from pathlib import Path

INPUT_DIR = Path("data/raw_hierarchy")
SECTION_OUTPUT = Path("data/section_urls.txt")
MORE_HIERARCHY_OUTPUT = Path("data/more_hierarchy_links.txt")

BASE = "https://govt.westlaw.com"

section_links = set()
hierarchy_links = set()

for file in INPUT_DIR.glob("*.html"):

    print("Scanning:", file.name)

    html = file.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):

        href = a["href"]

        # Normalize relative links
        if href.startswith("/"):
            href = BASE + href

        # SECTION PAGE
        if "/calregs/Document/" in href:
            section_links.add(href)

        # MORE HIERARCHY
        elif "/calregs/Browse/" in href:
            hierarchy_links.add(href)

print("\nSections discovered:", len(section_links))
print("More hierarchy discovered:", len(hierarchy_links))

SECTION_OUTPUT.parent.mkdir(exist_ok=True)

with open(SECTION_OUTPUT, "w", encoding="utf-8") as f:
    for link in sorted(section_links):
        f.write(link + "\n")

with open(MORE_HIERARCHY_OUTPUT, "w", encoding="utf-8") as f:
    for link in sorted(hierarchy_links):
        f.write(link + "\n")

print("\nSaved section URLs →", SECTION_OUTPUT)
print("Saved next hierarchy →", MORE_HIERARCHY_OUTPUT)