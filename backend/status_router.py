# backend/status_router.py
from fastapi import APIRouter
from backend.document_store import chunks, hashes, index, save_vector_store
import faiss
import os

status_router = APIRouter()

@status_router.get("/")
def status():
    return {
        "status": "ok",
        "documents_loaded": len(chunks) > 0,
        "chunk_count": len(chunks)
    }

@status_router.post("/clear-documents")
def clear_documents():
    global chunks, hashes, index
    chunks.clear()
    hashes.clear()
    index = faiss.IndexFlatL2(384)  # Assuming embedding dim is 384
    save_vector_store()
    return {"status": "success", "message": "Documents cleared."}
    
    # Optional: clean disk files too
    try:
        os.remove("vector_store/faiss_index.idx")
        os.remove("vector_store/chunks.pkl")
        os.remove("vector_store/hashes.pkl")
    except FileNotFoundError:
        pass
    
    return {"status": "cleared", "message": "Vector store and memory cleared."}
