import os
import re
import requests
from typing import List
from dotenv import load_dotenv

# Load .env if in local environment
if os.getenv("ENV", "local") == "local":
    load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
MODEL_ID = "mistralai/mistral-7b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY is not set!")

def call_llm(prompt: str) -> str:
    """
    Send a prompt to OpenRouter's chat completion endpoint.
    Returns the generated response as a string.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "RAG Assistant"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        raw = response.json()

        if "choices" in raw and len(raw["choices"]) > 0:
            return raw["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Unexpected response structure: {raw}"

    except requests.exceptions.HTTPError as e:
        return f"⚠️ LLM Error: {e.response.text if e.response else str(e)}"
    except Exception as ex:
        return f"⚠️ Unexpected error: {ex}"

def clean_text_chunks(text: str) -> List[str]:
    """
    Splits a long string into ~500-character chunks, cleaning extra whitespace.
    Returns a list of cleaned text chunks.
    """
    raw_chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
    cleaned = [re.sub(r'\s+', ' ', chunk).strip() for chunk in raw_chunks if chunk.strip()]
    return cleaned
