from fastapi import APIRouter
from backend.document_store import chunks, hashes, index, save_vector_store

clear_router = APIRouter()

@clear_router.post("/clear_docs")
async def clear_documents():
    chunks.clear()
    hashes.clear()
    if index:
        index.reset()
    save_vector_store()
    return {"status": "success", "message": "Vector store and memory cleared."}

