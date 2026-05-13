import os
import requests
from dotenv import load_dotenv

if os.getenv("ENV", "local") == "local":
    load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
MODEL_ID = "minimax/minimax-m2.5"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Add it to your .env file.")


def call_llm(prompt: str) -> str:
    """Send a prompt to Mistral 7B via OpenRouter and return the response text."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "RAG Assistant",
    }
    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        choices = data.get("choices", [])
        if choices:
            return choices[0]["message"]["content"]
        return f"Unexpected response structure: {data}"
    except requests.exceptions.HTTPError as e:
        detail = e.response.text if e.response else str(e)
        return f"LLM request failed: {detail}"
    except Exception as e:
        return f"Unexpected error calling LLM: {e}"