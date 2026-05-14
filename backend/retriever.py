import faiss
import numpy as np
from typing import List

import backend.document_store as ds
from backend.embedding import embed_chunks


def create_faiss_index(text_chunks: List[str]) -> None:
    """Build a new FAISS flat L2 index from the given chunks and store it globally."""
    vectors = embed_chunks(text_chunks).astype("float32")
    new_index = faiss.IndexFlatL2(vectors.shape[1])
    new_index.add(vectors)
    ds.set_index(new_index)


def retrieve_chunks(query: str, k: int = 5) -> List[str]:
    """Return the top-k most relevant chunks for a query. Returns [] if no index exists.

    k=5 instead of 3 to capture facts that may be spread across the document.
    """
    if ds.index is None or len(ds.chunks) == 0:
        return []

    # Never request more chunks than we have
    k = min(k, len(ds.chunks))

    query_vector = embed_chunks([query]).astype("float32")
    _, indices = ds.index.search(query_vector, k)
    return [ds.chunks[i] for i in indices[0] if 0 <= i < len(ds.chunks)]