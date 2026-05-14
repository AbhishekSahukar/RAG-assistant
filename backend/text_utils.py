import re
import fitz  # PyMuPDF
from typing import List


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from a PDF byte stream using PyMuPDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = [page.get_text("text") for page in doc]
    return "\n".join(pages)


def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks.

    Overlap ensures that facts sitting near a chunk boundary are not cut in half
    and lost. A 200-character overlap means each chunk shares its last 200
    characters with the start of the next one.

    Chunks under 50 characters or with no alphabetic content are dropped.
    """
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]
        chunk = re.sub(r"\s+", " ", chunk).strip()
        if len(chunk) >= 50 and re.search(r"[a-zA-Z]", chunk):
            chunks.append(chunk)
        start += chunk_size - overlap  # slide forward by (chunk_size - overlap)

    return chunks