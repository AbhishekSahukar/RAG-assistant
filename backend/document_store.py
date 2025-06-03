# backend/document_store.py
import os
import pickle
import faiss

VECTOR_STORE_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_index.idx")
CHUNKS_PATH = os.path.join(VECTOR_STORE_DIR, "chunks.pkl")
HASHES_PATH = os.path.join(VECTOR_STORE_DIR, "hashes.pkl")

# Ensure vector store directory exists
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Global shared state
chunks = []
hashes = set()
index = None

# Load persisted data if available
if os.path.exists(CHUNKS_PATH):
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

if os.path.exists(HASHES_PATH):
    with open(HASHES_PATH, "rb") as f:
        hashes = pickle.load(f)

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)


def save_vector_store():
    """Persist FAISS index, chunks, and hashes."""
    if index is not None:
        faiss.write_index(index, INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    with open(HASHES_PATH, "wb") as f:
        pickle.dump(hashes, f)


def clear_vector_store():
    """Clear in-memory and persisted vector data."""
    global chunks, hashes, index
    chunks = []
    hashes = set()
    index = None

    # Remove files if they exist
    for path in [CHUNKS_PATH, HASHES_PATH, INDEX_PATH]:
        if os.path.exists(path):
            os.remove(path)
