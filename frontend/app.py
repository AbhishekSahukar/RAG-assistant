import streamlit as st
import requests
import os
from io import BytesIO

API_URL = os.getenv("API_URL")
if not API_URL:
    raise RuntimeError("❌ API_URL environment variable is not set.")


st.set_page_config("🧠 RAG Chatbot")
st.title("📄 RAG Chatbot")
st.caption("💬 Talk to Mistral with optional document retrieval.")

# === Session State Init ===
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# === Sidebar Controls ===
st.sidebar.header("⚙️ Controls")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

if st.sidebar.button("🗑️ Clear Documents"):
    try:
        res = requests.post(f"{API_URL}/status/clear-documents")
        if res.status_code == 200:
            st.session_state.uploaded_files = []
            st.success("✅ Documents cleared.")
            st.rerun()
        else:
            st.error("⚠️ Failed to clear documents on backend.")
    except Exception as e:
        st.error(f"⚠️ Error clearing documents: {e}")

# === Display Chat Messages ===
for entry in st.session_state.chat_history:
    st.markdown(f"**🧑 You:** {entry['user']}")
    st.markdown(f"**🤖 Assistant:** {entry['assistant']}")
    if entry.get("used_rag"):
        with st.expander("📚 Source Chunks"):
            for chunk in entry.get("chunks", []):
                st.markdown(f"> {chunk}")

# === Chat Form ===
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask something...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    try:
        res = requests.post(f"{API_URL}/chat", json={"message": user_input})
        res.raise_for_status()
        data = res.json()

        st.session_state.chat_history.append({
            "user": user_input,
            "assistant": data.get("response", "⚠️ No reply."),
            "used_rag": data.get("used_rag", False),
            "chunks": data.get("retrieved_chunks", [])
        })
        st.rerun()
    except Exception as e:
        st.error(f"⚠️ Error connecting to backend: {e}")

# === Upload Section ===
st.divider()
st.subheader("📎 Upload Documents")
st.caption("Upload your PDF or TXT files to activate RAG-based responses.")

uploaded_files = st.file_uploader(
    "Upload your documents",
    type=["pdf", "txt"],
    accept_multiple_files=True,
    key="file_uploader",
    label_visibility="collapsed"
)

new_files = []
if uploaded_files:
    for f in uploaded_files:
        if f.name not in [x.name for x in st.session_state.uploaded_files]:
            new_files.append(f)

if new_files:
    with st.spinner("🔄 Uploading and processing..."):
        try:
            for f in new_files:
                file_bytes = f.read()
                files = {"file": (f.name, BytesIO(file_bytes), f.type)}
                res = requests.post(f"{API_URL}/upload", files=files)
                res.raise_for_status()

            st.session_state.uploaded_files.extend(new_files)
            st.success("✅ Files uploaded and processed.")
        except Exception as e:
            st.error(f"⚠️ Upload failed: {e}")
