import os
import json
import pickle
import faiss
import numpy as np

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# ==========================================
# LOAD JSON
# ==========================================

JSON_FILE = "ChatBot.json"

with open(JSON_FILE, "r", encoding="utf-8") as f: 
    data = json.load(f)

# ==========================================
# EXTRACT CONTENT
# ==========================================

documents = []

# ==========================================
# FAQS
# ==========================================

for faq in data.get("faqs", []):

    question = faq.get("question", "")
    answer = faq.get("answer", "")

    text = f"""
Question: {question}

Answer: {answer}
"""

    documents.append(
        Document(
            page_content=text,
            metadata={
                "type": "faq",
                "id": faq.get("id")
            }
        )
    )

# ==========================================
# FACILITIES
# ==========================================

facilities = data.get("facilities", {})

documents.append(
    Document(
        page_content=f"""
Facilities Available:

{json.dumps(facilities, indent=2)}
""",
        metadata={"type": "facilities"}
    )
)

# ==========================================
# VENUE DETAILS
# ==========================================

venue = data.get("venue", {})

documents.append(
    Document(
        page_content=f"""
Venue Details:

{json.dumps(venue, indent=2)}
""",
        metadata={"type": "venue"}
    )
)

# ==========================================
# SLOT DETAILS
# ==========================================

slots = data.get("slots", {})

documents.append(
    Document(
        page_content=f"""
Slot Information:

{json.dumps(slots, indent=2)}
""",
        metadata={"type": "slots"}
    )
)

# ==========================================
# PRICING
# ==========================================

pricing = data.get("pricing", {})

documents.append(
    Document(
        page_content=f"""
Pricing Information:

{json.dumps(pricing, indent=2)}
""",
        metadata={"type": "pricing"}
    )
)

print(f"\nTotal Documents Extracted: {len(documents)}")

print(f"\nTotal Documents Extracted: {len(documents)}")

# ==========================================
# SPLIT DOCUMENTS
# ==========================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"Total Chunks Created: {len(chunks)}")

# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# CREATE EMBEDDINGS
# ==========================================

texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_model.embed_documents(texts)

embeddings = np.array(embeddings, dtype="float32")

print(f"Embedding Shape: {embeddings.shape}")

# ==========================================
# CREATE FAISS INDEX
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# ==========================================
# CREATE DIRECTORY
# ==========================================

os.makedirs("faiss_index", exist_ok=True)

# ==========================================
# SAVE INDEX
# ==========================================

faiss.write_index(
    index,
    "faiss_index/index.faiss"
)

with open(
    "faiss_index/index.pkl",
    "wb"
) as f:
    pickle.dump(chunks, f)

print("\nFAISS Index Saved Successfully!")
print("Location: faiss_index/")
print(f"Total Indexed Chunks: {len(chunks)}")

# ==========================================
# OPTIONAL TEST
# ==========================================

print("\nSample Indexed Chunk:\n")

if len(chunks) > 0:
    print(chunks[0].page_content[:500])