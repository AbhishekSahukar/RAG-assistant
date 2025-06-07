# backend/main.py
from backend.chat_router import chat_router
from backend.upload_router import upload_router
from backend.status_router import status_router
from backend.clear_router import clear_router

from fastapi import FastAPI

app = FastAPI()

# Include routers
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(status_router, prefix="/status", tags=["Status"])
app.include_router(clear_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Assistant API"}
