import json
from pathlib import Path

INPUT_FILE = Path("data/sections_dataset.json")
OUTPUT_FILE = Path("data/chunks.json")

CHUNK_SIZE = 500


def split_text(text, size):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size])
        chunks.append(chunk)

    return chunks


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    sections = json.load(f)

all_chunks = []

for section in sections:

    section_id = section["section_number"]
    title = section["title"]
    text = section["text"]

    chunks = split_text(text, CHUNK_SIZE)

    for chunk in chunks:

        all_chunks.append({
            "section_number": section_id,
            "title": title,
            "content": chunk
        })


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

print("Chunks created:", len(all_chunks))
print("Saved →", OUTPUT_FILE)