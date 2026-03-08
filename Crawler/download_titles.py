import requests
import os
import time

INPUT_FILE = "data/title_urls.txt"
OUTPUT_DIR = "data/raw_titles"

os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

with open(INPUT_FILE) as f:
    urls = [line.strip() for line in f]

for i, url in enumerate(urls):

    print("Downloading:", url)

    try:
        r = requests.get(url, headers=headers)

        file_path = f"{OUTPUT_DIR}/title_{i}.html"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(r.text)

        time.sleep(3)

    except Exception as e:
        print("Error:", e)

print("\nDownload complete")