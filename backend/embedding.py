from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# Load embedding model once globally
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str]) -> np.ndarray:
    """
    Embed a list of text chunks into dense vectors.
    Returns:
        np.ndarray of shape (len(chunks), embedding_dim)
    """
    if not chunks:
        return np.empty((0, model.get_sentence_embedding_dimension()))
    return np.array(model.encode(chunks, convert_to_numpy=True))

def get_embedding(text: str) -> np.ndarray:
    """
    Embed a single text string and return a 1D NumPy vector.
    Returns:
        np.ndarray of shape (embedding_dim,)
    """
    return model.encode([text], convert_to_numpy=True)[0]
