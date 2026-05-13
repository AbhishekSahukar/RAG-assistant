import os
from io import BytesIO

import requests
import streamlit as st
from dotenv import load_dotenv

if os.getenv("ENV", "local") == "local":
    load_dotenv()

API_URL = os.getenv("API_URL", "").strip()
if not API_URL:
    st.error("API_URL environment variable is not set.")
    st.stop()

# Remove trailing slash so URL construction is consistent
API_URL = API_URL.rstrip("/")

# --- Page config ---
st.set_page_config(page_title="RAG Chatbot", page_icon="🧠", layout="centered")
st.title("🧠 RAG Chatbot")
st.caption("Ask anything — upload a document to get answers grounded in your content.")

# --- Session state defaults ---
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("uploaded_file_names", [])
st.session_state.setdefault("uploader_key", 0)

# --- Sidebar ---
with st.sidebar:
    st.header("Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🗑️ Clear Documents"):
        try:
            res = requests.post(f"{API_URL}/status/clear", timeout=10)
            if res.status_code == 200:
                st.session_state.uploaded_file_names = []
                st.session_state.uploader_key += 1
                st.success("Documents cleared.")
                st.rerun()
            else:
                st.error("Failed to clear documents.")
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.uploaded_file_names:
        st.divider()
        st.markdown("**Loaded documents:**")
        for name in st.session_state.uploaded_file_names:
            st.markdown(f"- {name}")

# --- Chat history ---
for entry in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(entry["user"])
    with st.chat_message("assistant"):
        st.markdown(entry["assistant"])
        if entry.get("used_rag") and entry.get("chunks"):
            with st.expander("📚 Source chunks used"):
                for chunk in entry["chunks"]:
                    st.markdown(f"> {chunk}")

# --- Chat input ---
user_input = st.chat_input("Ask something...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    f"{API_URL}/chat",
                    json={"message": user_input},
                    timeout=60,
                )
                res.raise_for_status()
                data = res.json()

                answer = data.get("response", "No response received.")
                used_rag = data.get("used_rag", False)
                chunks = data.get("retrieved_chunks", [])

                st.markdown(answer)
                if used_rag and chunks:
                    with st.expander("📚 Source chunks used"):
                        for chunk in chunks:
                            st.markdown(f"> {chunk}")

                st.session_state.chat_history.append({
                    "user": user_input,
                    "assistant": answer,
                    "used_rag": used_rag,
                    "chunks": chunks,
                })

            except Exception as e:
                st.error(f"Could not reach the backend: {e}")

# --- Document upload ---
st.divider()
st.subheader("📎 Upload Documents")
st.caption("Upload PDF or TXT files to enable document-grounded answers.")

uploaded_files = st.file_uploader(
    label="Choose files",
    type=["pdf", "txt"],
    accept_multiple_files=True,
    label_visibility="collapsed",
    key=f"file_uploader_{st.session_state.uploader_key}",
)

new_files = [
    f for f in (uploaded_files or [])
    if f.name not in st.session_state.uploaded_file_names
]

if new_files:
    with st.spinner(f"Processing {len(new_files)} file(s)..."):
        try:
            files_payload = [
                ("files", (f.name, BytesIO(f.read()), f.type or "application/octet-stream"))
                for f in new_files
            ]
            res = requests.post(f"{API_URL}/upload", files=files_payload, timeout=120)
            res.raise_for_status()
            data = res.json()

            st.session_state.uploaded_file_names.extend(f.name for f in new_files)
            st.success(
                f"Processed {data.get('processed_files', 0)} file(s), "
                f"{data.get('new_chunks', 0)} chunks indexed."
            )
        except Exception as e:
            st.error(f"Upload failed: {e}")