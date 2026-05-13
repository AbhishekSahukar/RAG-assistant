from fastapi import APIRouter

import backend.document_store as ds

status_router = APIRouter()


@status_router.get("/")
def get_status():
    """Return the current state of the vector store."""
    return {
        "status": "ok",
        "documents_loaded": len(ds.chunks) > 0,
        "chunk_count": len(ds.chunks),
    }


@status_router.post("/clear")
def clear_documents():
    """Clear all loaded documents and reset the vector store."""
    ds.clear_vector_store()
    return {"status": "success", "message": "Vector store cleared."}