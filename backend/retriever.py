import numpy as np
import faiss

from typing import List
from backend.embedding import embed_chunks
from backend.document_store import chunks, index


def create_faiss_index(text_chunks: List[str]) -> None:
    """
    Creates a new FAISS index using embedded text chunks.
    Updates the global `index` object in `document_store`.
    """
    global index
    vectors = embed_chunks(text_chunks).astype('float32')  # FAISS requires float32
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)


def retrieve_chunks(query: str, k: int = 3) -> List[str]:
    """
    Returns top-k most relevant chunks from vector store given a query.
    """
    if index is None or len(chunks) == 0:
        return []

    query_vector = embed_chunks([query]).astype('float32')
    distances, indices = index.search(query_vector, k)

    # Filter out invalid or out-of-bound indices
    return [chunks[i] for i in indices[0] if 0 <= i < len(chunks)]
