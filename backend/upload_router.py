# upload_router.py (Final with fixes)
from fastapi import APIRouter, UploadFile, File
from typing import List
import hashlib
from backend.document_store import chunks, hashes, index, save_vector_store
from backend.retriever import create_faiss_index
from backend.llm import clean_text_chunks
import fitz  # PyMuPDF

upload_router = APIRouter()

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join([page.get_text("text") for page in doc])  # plain text

@upload_router.post("/")
async def upload(files: List[UploadFile] = File(...)):
    try:
        all_chunks = []

        for file in files:
            content = await file.read()
            file_hash = hashlib.md5(content).hexdigest()

            if file_hash in hashes:
                continue  # Skip duplicates

            if file.filename.endswith(".pdf"):
                text = extract_text_from_pdf(content)
            else:
                text = content.decode("utf-8", errors="ignore")

            file_chunks = clean_text_chunks(text)
            chunks.extend(file_chunks)
            hashes.add(file_hash)
            all_chunks.extend(file_chunks)

        if chunks:
            create_faiss_index(chunks)
            save_vector_store()

        return {"status": "success", "message": "Files processed."}

    except Exception as e:
        print(f"Upload error: {str(e)}")
        return {"status": "error", "message": f"Upload failed: {str(e)}"}
