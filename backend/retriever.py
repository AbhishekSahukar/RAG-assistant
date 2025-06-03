# backend/retriever.py
import numpy as np
import faiss
from backend.embedding import embed_chunks
from backend.document_store import chunks, index

def create_faiss_index(text_chunks):
    global index
    vectors = embed_chunks(text_chunks).astype('float32')
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

def retrieve_chunks(query, k=3):
    if index is None or len(chunks) == 0:
        return []

    query_vector = embed_chunks([query]).astype('float32')
    distances, indices = index.search(query_vector, k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]
