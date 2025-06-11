from fastapi import APIRouter
from pydantic import BaseModel
from backend.llm import call_llm
from backend.retriever import retrieve_chunks
from backend.memory import add_message, get


class ChatRequest(BaseModel):
    message: str

chat_router = APIRouter()

@chat_router.post("/")
async def chat_endpoint(request: ChatRequest):
    """Handles incoming chat request and optionally augments it with retrieved chunks."""
    message = request.message

    try:
        # Step 1: Retrieve relevant document chunks (if any)
        retrieved_chunks = retrieve_chunks(message)

        if retrieved_chunks:
            context = "\n\n".join(retrieved_chunks)
            prompt = f"""Answer the question using only the information below:

{context}

Question: {message}
Answer:"""
            used_rag = True
        else:
            prompt = message
            used_rag = False

        # Step 2: Send to LLM
        response = call_llm(prompt)

        return {
            "response": response,
            "retrieved_chunks": retrieved_chunks,
            "used_rag": used_rag
        }

    except Exception as e:
        return {
            "response": f"⚠️ Error: {str(e)}",
            "retrieved_chunks": [],
            "used_rag": False
        }
