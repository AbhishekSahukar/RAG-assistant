from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.chat_router import chat_router
from backend.upload_router import upload_router
from backend.status_router import status_router
from backend.clear_router import clear_router

# Create FastAPI app
app = FastAPI(title="RAG Assistant API")

# Enable CORS (allow all for now — restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(status_router, prefix="/status", tags=["Status"])
app.include_router(clear_router, prefix="/maintenance", tags=["Maintenance"])

@app.get("/", tags=["Health"])
def read_root():
    """
    Health check endpoint.
    """
    return {"message": "Welcome to the RAG Assistant API"}
