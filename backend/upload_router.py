import hashlib
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

import backend.document_store as ds
from backend.retriever import create_faiss_index
from backend.text_utils import extract_text_from_pdf, split_into_chunks

upload_router = APIRouter()


@upload_router.post("/")
async def upload(files: List[UploadFile] = File(...)):
    """Upload one or more PDF or TXT files. Extracts text, splits into chunks,
    embeds them, and updates the FAISS index."""
    new_chunks: List[str] = []
    processed = 0
    skipped = 0

    try:
        for file in files:
            content = await file.read()
            file_hash = hashlib.md5(content).hexdigest()

            if file_hash in ds.hashes:
                skipped += 1
                continue

            if file.filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(content)
            else:
                text = content.decode("utf-8", errors="ignore")

            chunks = split_into_chunks(text)
            ds.chunks.extend(chunks)
            ds.hashes.add(file_hash)
            new_chunks.extend(chunks)
            processed += 1

        if new_chunks:
            create_faiss_index(ds.chunks)
            ds.save_vector_store()

        return {
            "status": "success",
            "processed_files": processed,
            "skipped_duplicates": skipped,
            "new_chunks": len(new_chunks),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")