# CCR Compliance Agent
This project implements a prototype AI system that crawls the **California Code of Regulations (CCR)** and builds a Retrieval-Augmented Generation (RAG) pipeline that can answer regulatory questions with citations.
The system extracts regulation sections, stores them in a vector database, and retrieves relevant sections when users ask questions.

---

# 1. Project Goal
The goal of this project is to build a system that:
1. Crawls the CCR website
2. Extracts regulation sections
3. Organizes the extracted data
4. Stores the sections in a vector database
5. Builds a retrieval-based AI agent that answers compliance questions with citations.

Example questions:

- What CCR regulations apply to restaurants?
- What regulations affect farms or agricultural facilities?
- What laws apply to movie theater operators?

---
# 2. System Architecture
Pipeline:
CCR Website
↓
Crawling
↓
Hierarchy extraction
↓
Section extraction
↓
Structured dataset
↓
Text chunking
↓
Embeddings
↓
Vector database
↓
RAG query system
# 3. Project Structure
CCR-Compliance-agent
Crawler/
discover_links.py
extract_hierarchy.py
extract_section_urls.py
extract_section_content.py
RAG/
chunk_sections.py
build_vector_db.py
ask_questions.py
data/
raw_hierarchy/
raw_sections/
sections_dataset.json
chunks.json
vector_db/
index.faiss
meta.json
README.md

---

# 4. Crawling Strategy

The crawler was designed in stages:
### Stage 1 — Title Discovery
The CCR homepage was parsed to extract links to titles.
Script:discover_links.py


---

### Stage 3 — Section URL Extraction
Hierarchy pages were scanned for section document URLs.
Script: extract_section_urls.py
These URLs point to pages like:
/calregs/Document/{section_id}

---

### Stage 4 — Section Content Extraction
Each section page was parsed to extract:
- section number
- section title
- regulation text
Script: extract_section_content.py

output dataset: data/sections_dataset.json

---
# 5. Dataset Structure
Each regulation section is stored as:
{
"section_number": "4001",
"title": "§ 4001. Limitations on Public Benefits for Aliens.",
"text": "Regulation content..."
}

This dataset is later used for semantic search.
---
# 6. Text Chunking
Regulation sections can be long, so they are split into smaller chunks.

Each chunk contains:
{
"section_number": "4001",
"title": "...",
"content": "text chunk"
}
---
# 7. Vector Database
The system uses **FAISS** as a local vector database.
Embeddings are generated using:
sentence-transformers/all-MiniLM-L6-v2
Script: RAG/build_vector_db.py
Output:
vector_db/index.faiss
vector_db/meta.json
---
# 8. Retrieval-Augmented Generation (RAG)
The system answers questions by:
1. Converting the question into an embedding
2. Searching the vector database
3. Retrieving the most relevant regulation sections
4. Returning them with citations
Script:RAG/ask_questions.py

Example:
Question: Who is eligible for public benefits?
Result:
CCR § 4001
CCR § 4005
---
# 9. How to Run the Project
### Install dependencies
pip install sentence-transformers
pip install faiss-cpu
pip install beautifulsoup4
---
### Step 1 — Extract section data
python Crawler/extract_section_content.py
---
### Step 2 — Chunk the text
python RAG/chunk_sections.py
---
### Step 3 — Build vector database
python RAG/build_vector_db.py
---
### Step 4 — Ask questions
python RAG/ask_questions.py
---
# 10. Example Query
Ask a question:
What regulations apply to public benefit eligibility?
Example output:
Section: 4001
Title: Limitations on Public Benefits for Aliens
Relevant regulation text...
---
# 11. Known Limitations
1. **Cloudflare Protection**
The Westlaw CCR site uses Cloudflare protection which limits automated crawling.
Because of this, section pages were downloaded manually for extraction.
---
2. **Incomplete Coverage**
The current dataset contains:

42 regulation sections
The full CCR contains thousands of sections.
The pipeline is designed to scale to full coverage if crawling access is available.
---
3. **Simplified Hierarchy**
The current dataset stores sections without fully reconstructing the canonical CCR hierarchy.
Future work could include extracting:
- title
- division
- chapter
- article
---
# 12. Future Improvements
Potential improvements include:
- Automated crawling with retry logic
- Persistent crawl checkpoints
- Coverage validation tools
- Full CCR hierarchy extraction
- LLM-powered answer generation
- Web interface for compliance queries
---
# 13. Disclaimer
This project is a **technical prototype** for regulatory information retrieval.
It is **not legal advice**.
Users should consult qualified legal professionals for regulatory compliance guidance.
---
# 14. Technologies Used
- Python
- BeautifulSoup
- Sentence Transformers
- FAISS
- Retrieval-Augmented Generation (RAG)
---
# 15. Author
Engineering Internship Assignment
CCR Compliance Agent Prototype



