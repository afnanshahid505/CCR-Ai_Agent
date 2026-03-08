import streamlit as st
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

st.title("CCR Compliance Agent")
st.write("Ask questions about the California Code of Regulations")

# Load vector DB
index = faiss.read_index("vector_db/index.faiss")

with open("vector_db/meta.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

question = st.text_input("Ask a question")

if question:

    query_embedding = model.encode([question])
    distances, indices = index.search(np.array(query_embedding), 3)

    st.subheader("Relevant CCR Sections")

    seen_sections = set()

    for idx in indices[0]:

        chunk = meta[idx]

        if chunk["section_number"] in seen_sections:
            continue

        seen_sections.add(chunk["section_number"])

        st.markdown(f"### CCR § {chunk['section_number']}")
        st.write(chunk["title"])
        st.write(chunk["content"][:500])
        st.write("---")

st.caption("Disclaimer: This tool is a prototype and does not provide legal advice.")