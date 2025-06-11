from fastapi import APIRouter
from backend.document_store import chunks, hashes, index, save_vector_store

clear_router = APIRouter()

@clear_router.post("/clear_docs", tags=["Maintenance"])
async def clear_documents():
    """
    Clears all loaded documents, vector index, and metadata cache.
    """
    chunks.clear()
    hashes.clear()

    if index is not None:
        try:
            index.reset()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to reset vector index: {e}"
            }

    save_vector_store()
    return {
        "status": "success",
        "message": "✅ Vector store and memory cleared."
    }
