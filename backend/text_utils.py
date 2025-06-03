import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        raw = page.get_text()
        clean = re.sub(r"[^\x20-\x7E]+", " ", raw)  # keep only printable ASCII
        text += clean + "\n"
    return text.strip()

def clean_text_chunks(chunks):
    return [c.strip() for c in chunks if len(c.strip()) > 30 and re.search(r"[a-zA-Z]", c)]
