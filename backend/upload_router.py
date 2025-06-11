from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import hashlib
import fitz  # PyMuPDF

from backend.document_store import chunks, hashes, index, save_vector_store
from backend.retriever import create_faiss_index
from backend.llm import clean_text_chunks

upload_router = APIRouter()


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts plain text from a PDF byte stream using PyMuPDF.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "\n".join(page.get_text("text") for page in doc)


@upload_router.post("/", tags=["Upload"])
async def upload(files: List[UploadFile] = File(...)):
    """
    Uploads and processes documents (PDF or TXT), chunks and indexes them.
    """
    try:
        all_chunks = []
        processed_files = 0
        skipped_files = 0

        for file in files:
            content = await file.read()
            file_hash = hashlib.md5(content).hexdigest()

            if file_hash in hashes:
                skipped_files += 1
                continue  # Skip duplicate file

            # Extract text
            if file.filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(content)
            else:
                text = content.decode("utf-8", errors="ignore")

            # Clean + chunk
            file_chunks = clean_text_chunks(text)

            # Append to in-memory store
            chunks.extend(file_chunks)
            hashes.add(file_hash)
            all_chunks.extend(file_chunks)
            processed_files += 1

        # Update FAISS index and persist state
        if all_chunks:
            create_faiss_index(chunks)
            save_vector_store()

        return {
            "status": "success",
            "processed_files": processed_files,
            "skipped_duplicates": skipped_files,
            "new_chunks": len(all_chunks)
        }

    except Exception as e:
        print(f"[ERROR] Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
