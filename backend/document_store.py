import os
import pickle
import faiss

VECTOR_STORE_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_index.idx")
CHUNKS_PATH = os.path.join(VECTOR_STORE_DIR, "chunks.pkl")
HASHES_PATH = os.path.join(VECTOR_STORE_DIR, "hashes.pkl")

os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# Shared in-memory state
chunks: list = []
hashes: set = set()
index = None

# Load persisted state on startup
if os.path.exists(CHUNKS_PATH):
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

if os.path.exists(HASHES_PATH):
    with open(HASHES_PATH, "rb") as f:
        hashes = pickle.load(f)

if os.path.exists(INDEX_PATH):
    try:
        index = faiss.read_index(INDEX_PATH)
    except Exception as e:
        print(f"Warning: could not load FAISS index: {e}")
        index = None


def set_index(new_index) -> None:
    """Update the global FAISS index. Use this instead of direct assignment
    to avoid Python's import rebinding issue."""
    global index
    index = new_index


def save_vector_store() -> None:
    """Persist FAISS index, chunks, and hashes to disk."""
    if index is not None:
        faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    with open(HASHES_PATH, "wb") as f:
        pickle.dump(hashes, f)


def clear_vector_store() -> None:
    """Wipe in-memory state and delete persisted files."""
    global index
    chunks.clear()
    hashes.clear()
    index = None
    for path in [INDEX_PATH, CHUNKS_PATH, HASHES_PATH]:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass