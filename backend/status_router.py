from fastapi import APIRouter
from backend.document_store import chunks, hashes, index, save_vector_store
import faiss
import os

status_router = APIRouter()

@status_router.get("/", tags=["Status"])
def status():
    """
    Returns status of vector store: whether documents are loaded and count.
    """
    return {
        "status": "ok",
        "documents_loaded": len(chunks) > 0,
        "chunk_count": len(chunks)
    }

@status_router.post("/clear-documents", tags=["Maintenance"])
def clear_documents():
    """
    Clears memory + disk state of vector store.
    """
    chunks.clear()
    hashes.clear()
    index = faiss.IndexFlatL2(384)  # Assuming all-MiniLM-L6-v2 = 384 dim
    save_vector_store()

    # Attempt to clean on-disk files
    deleted = []
    for path in [
        "vector_store/faiss_index.idx",
        "vector_store/chunks.pkl",
        "vector_store/hashes.pkl"
    ]:
        try:
            os.remove(path)
            deleted.append(path)
        except FileNotFoundError:
            pass

    return {
        "status": "cleared",
        "message": "Vector store and memory cleared.",
        "files_deleted": deleted
    }
