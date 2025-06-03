# llm.py
import os
import re
import requests
from dotenv import load_dotenv

if os.getenv("ENV","local") == "local":
    load_dotenv()

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY is not set!")

def call_llm(prompt):
    if not OPENROUTER_API_KEY:
        return "⚠️ Error: Missing OpenRouter API key in environment variables"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # Adjust if hosted
        "X-Title": "RAG Assistant"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        raw = response.json()

        if "choices" in raw and len(raw["choices"]) > 0:
            return raw["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Unexpected response structure: {raw}"

    except requests.exceptions.HTTPError as e:
        return f"⚠️ LLM Error: {e}"
    except Exception as ex:
        return f"⚠️ Unexpected error: {ex}"

def clean_text_chunks(text):
    """
    Splits text into ~500-character chunks and cleans whitespace.
    """
    raw_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    cleaned = [re.sub(r'\s+', ' ', chunk).strip() for chunk in raw_chunks if chunk.strip()]
    return cleaned
