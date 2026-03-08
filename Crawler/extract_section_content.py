from bs4 import BeautifulSoup
from pathlib import Path
import json
import re

# ----------------------------------
# Paths
# ----------------------------------

INPUT_DIR = Path("data/raw_sections")
OUTPUT_FILE = Path("data/sections_dataset.json")

records = []

# ----------------------------------
# Process HTML files
# ----------------------------------

for file in sorted(INPUT_DIR.glob("*.html")):

    print(f"Processing {file.name}...")

    html = file.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    # ----------------------------------
    # Extract title
    # ----------------------------------

    title_tag = soup.find("span", id="title")

    if not title_tag:
        print("Skipping (no title found)")
        continue

    title = title_tag.get_text(strip=True)

    # ----------------------------------
    # Extract section number
    # ----------------------------------

    section_number = ""
    match = re.search(r'§\s*(\d+)', title)

    if match:
        section_number = match.group(1)

    # ----------------------------------
    # Extract regulation text
    # ----------------------------------

    paragraphs = soup.select("div.co_paragraphText")

    text_parts = []

    for p in paragraphs:

        text = p.get_text(strip=True)

        # stop when metadata begins
        if text.startswith("Note:") or text.startswith("History") or text.startswith("Credits"):
            break

        if text:
            text_parts.append(text)

    section_text = "\n".join(text_parts)

    # ----------------------------------
    # Skip empty pages
    # ----------------------------------

    if section_text.strip() == "":
        print("Skipping empty section:", file.name)
        continue

    # ----------------------------------
    # Save record
    # ----------------------------------

    record = {
        "source_file": file.name,
        "section_number": section_number,
        "title": title,
        "text": section_text
    }

    records.append(record)

# ----------------------------------
# Save dataset
# ----------------------------------

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print("\nExtraction complete")
print("Valid sections extracted:", len(records))
print("Dataset saved →", OUTPUT_FILE)