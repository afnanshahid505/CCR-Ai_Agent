import json
from pathlib import Path

# Paths
HIERARCHY_DIR = Path("data/raw_hierarchy")
SECTIONS_DIR = Path("data/raw_sections")
SECTION_URL_FILE = Path("data/section_urls.txt")
DATASET_FILE = Path("data/sections_dataset.json")

report = {}

# Count hierarchy pages
if HIERARCHY_DIR.exists():
    report["hierarchy_pages_downloaded"] = len(list(HIERARCHY_DIR.glob("*.html")))
else:
    report["hierarchy_pages_downloaded"] = 0

# Count section URLs discovered
if SECTION_URL_FILE.exists():
    with open(SECTION_URL_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    report["section_urls_discovered"] = len(urls)
else:
    report["section_urls_discovered"] = 0

# Count raw section pages downloaded
if SECTIONS_DIR.exists():
    report["section_pages_downloaded"] = len(list(SECTIONS_DIR.glob("*.html")))
else:
    report["section_pages_downloaded"] = 0

# Count valid sections extracted
if DATASET_FILE.exists():
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        sections = json.load(f)
    report["valid_sections_extracted"] = len(sections)
else:
    report["valid_sections_extracted"] = 0

# Calculate extraction success rate
if report["section_pages_downloaded"] > 0:
    success_rate = report["valid_sections_extracted"] / report["section_pages_downloaded"] * 100
else:
    success_rate = 0

report["extraction_success_rate_percent"] = round(success_rate, 2)

# Save report
output_file = Path("coverage_report.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("\nCoverage Report")
print("----------------")
for k, v in report.items():
    print(f"{k}: {v}")

print("\nSaved → coverage_report.json")