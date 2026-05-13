from fastapi import APIRouter
from pydantic import BaseModel

from backend.llm import call_llm
from backend.retriever import retrieve_chunks

chat_router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@chat_router.post("/")
async def chat(request: ChatRequest):
    """Handle a chat message. Uses retrieved document chunks as context when available,
    otherwise falls back to a direct LLM call."""
    message = request.message

    try:
        retrieved_chunks = retrieve_chunks(message)

        if retrieved_chunks:
            context = "\n\n".join(retrieved_chunks)
            prompt = (
                f"Answer the question using only the information provided below.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {message}\n"
                f"Answer:"
            )
            used_rag = True
        else:
            prompt = message
            used_rag = False

        response = call_llm(prompt)

        return {
            "response": response,
            "retrieved_chunks": retrieved_chunks,
            "used_rag": used_rag,
        }

    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "retrieved_chunks": [],
            "used_rag": False,
        }