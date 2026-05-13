import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

# Loaded once at startup to avoid repeated disk reads
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks: List[str]) -> np.ndarray:
    """Embed a list of text strings into dense vectors.

    Returns an ndarray of shape (len(chunks), embedding_dim).
    Returns an empty array if the input list is empty.
    """
    if not chunks:
        return np.empty((0, _model.get_sentence_embedding_dimension()), dtype="float32")
    return np.array(_model.encode(chunks, convert_to_numpy=True), dtype="float32")