# backend/embedding.py
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model once globally
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    """
    Embed a list of text chunks into dense vectors.
    Returns a NumPy array of shape (len(chunks), embedding_dim).
    """
    return np.array(model.encode(chunks, convert_to_numpy=True))

def get_embedding(text):
    """
    Embed a single text string and return a 1D NumPy vector.
    """
    return model.encode([text], convert_to_numpy=True)[0]
