import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

INPUT_FILE = Path("data/chunks.json")
VECTOR_DB_PATH = Path("vector_db/index.faiss")
META_PATH = Path("vector_db/meta.json")

VECTOR_DB_PATH.parent.mkdir(exist_ok=True)

print("Loading chunks...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["content"] for chunk in chunks]

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")

embeddings = model.encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, str(VECTOR_DB_PATH))

with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print("Vector DB built successfully")
print("Vectors stored:", len(chunks))