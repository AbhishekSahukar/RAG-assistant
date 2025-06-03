# frontend/utils.py

import streamlit as st
from typing import Dict, List

def initialize_session() -> None:
    st.session_state.setdefault("chat_history", [])

def append_to_chat(user_input: str, assistant_response: str, used_rag: bool = False, chunks: List[str] = []) -> None:
    st.session_state.chat_history.append({
        "user": user_input,
        "assistant": assistant_response,
        "used_rag": used_rag,
        "chunks": chunks
    })

def display_chat_history(chat_history: List[Dict[str, str]]) -> None:
    for entry in chat_history:
        st.markdown(f"**🧑 You:** {entry['user']}**")
        st.markdown(f"**🤖 Assistant:** {entry['assistant']}**")
        if entry.get("used_rag"):
            with st.expander("📚 Source Chunks"):
                for chunk in entry.get("chunks", []):
                    st.markdown(f"> {chunk}")
