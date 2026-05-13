from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.chat_router import chat_router
from backend.upload_router import upload_router
from backend.status_router import status_router
from fastapi import Response

app = FastAPI(title="RAG Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(status_router, prefix="/status", tags=["Status"])


@app.get("/", tags=["Health"])
@app.head("/", tags=["Health"])
def health_check():
    return {"message": "RAG Assistant API is running."}


@app.get("/health")
@app.head("/health")
def health():
    return Response(status_code=200)