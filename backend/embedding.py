import numpy as np
from typing import List
from fastembed import TextEmbedding

_model = None

EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output dimension


def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def embed_chunks(chunks: List[str]) -> np.ndarray:
    """Embed a list of text strings into dense vectors.

    Returns an ndarray of shape (len(chunks), 384).
    Returns an empty array if the input list is empty.
    """
    if not chunks:
        return np.empty((0, EMBEDDING_DIM), dtype="float32")
    embeddings = list(get_model().embed(chunks))
    return np.array(embeddings, dtype="float32")