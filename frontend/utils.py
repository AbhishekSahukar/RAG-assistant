from typing import Dict, List

import streamlit as st


def append_to_chat(
    user_input: str,
    assistant_response: str,
    used_rag: bool = False,
    chunks: List[str] = None,
) -> None:
    """Add a completed exchange to the session chat history."""
    st.session_state.chat_history.append({
        "user": user_input,
        "assistant": assistant_response,
        "used_rag": used_rag,
        "chunks": chunks or [],
    })


def display_chat_history(chat_history: List[Dict]) -> None:
    """Render the full chat history using Streamlit chat message components."""
    for entry in chat_history:
        with st.chat_message("user"):
            st.markdown(entry["user"])
        with st.chat_message("assistant"):
            st.markdown(entry["assistant"])
            if entry.get("used_rag") and entry.get("chunks"):
                with st.expander("📚 Source chunks used"):
                    for chunk in entry["chunks"]:
                        st.markdown(f"> {chunk}")