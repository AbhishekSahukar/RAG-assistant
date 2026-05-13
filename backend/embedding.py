import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


def embed_chunks(chunks: List[str]) -> np.ndarray:
    """
    Embed text chunks into dense vectors.
    """

    if not chunks:
        dim = get_model().get_sentence_embedding_dimension()
        return np.empty((0, dim), dtype="float32")

    embeddings = get_model().encode(
        chunks,
        convert_to_numpy=True,
        batch_size=8,
        show_progress_bar=False,
    )

    return np.array(embeddings, dtype="float32")