import re
import fitz  # PyMuPDF
from typing import List


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from a PDF byte stream using PyMuPDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = [page.get_text("text") for page in doc]
    return "\n".join(pages)


def split_into_chunks(text: str, chunk_size: int = 500) -> List[str]:
    """Split text into fixed-size character chunks and clean each one.

    Chunks shorter than 30 characters or lacking alphabetic content are dropped.
    """
    raw = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    cleaned = []
    for chunk in raw:
        chunk = re.sub(r"\s+", " ", chunk).strip()
        if len(chunk) >= 30 and re.search(r"[a-zA-Z]", chunk):
            cleaned.append(chunk)
    return cleaned