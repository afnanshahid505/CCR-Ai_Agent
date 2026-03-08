import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading vector database...")

index = faiss.read_index("vector_db/index.faiss")

with open("vector_db/meta.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

print("RAG system ready!")

while True:

    query = input("\nAsk a question (type 'exit'): ")

    if query == "exit":
        break

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), 3)

    print("\nRelevant Sections:\n")

    for idx in indices[0]:

        chunk = meta[idx]

        print("Section:", chunk["section_number"])
        print("Title:", chunk["title"])
        print("Content:", chunk["content"][:300])
        print("-" * 50)