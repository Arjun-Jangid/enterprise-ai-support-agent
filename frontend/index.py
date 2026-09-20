import sys
import requests
from pathlib import Path

from frontend.component.source_badges import render_sources

import streamlit as st

st.set_page_config(
    page_title="Enterprise AI Agent",
    page_icon="⚡",
    layout="centered",
)

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/signup.py")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from config import BACKEND_URL

from frontend.utils.session import init_chat_session
from frontend.utils.headers import get_headers
from frontend.component.chat_history import render_chat_history

init_chat_session()

st.title("⚡ Enterprise AI Agent")

st.markdown(
    """
    <div style="font-size:18px; color:#B0B3B8; margin-bottom:20px;">
        AI-powered assistant for <b>Document Q&A</b>,
        <b>Mathematical Calculations</b>, and
        <b>Web Search</b> in one place.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.subheader("📄 Upload Document")

st.caption(
    "Upload a PDF, DOCX, or TXT file to chat with your documents."
)

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["pdf", "txt", "docx"],
    key="uploader",
)

st.divider()

if st.button("Submit", disabled=uploaded_file is None):
    if uploaded_file:
        with st.spinner("Uploading document..."):
            try:
                headers = get_headers()
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                    )
                }
                response = requests.post(f"{BACKEND_URL}/upload", files=files, headers=headers)
                data = response.json()
                if response.status_code == 200:
                    st.success(data["message"])
                    st.session_state.document_id = data["document_id"]
                else:
                    st.error(data.get("detail", "Upload failed."))
            
            except Exception as e:
                print(e)
                st.error("Something went wrong.")
    else:
        st.warning("Please upload a file!")


# User ask query
document_id = st.session_state.get("document_id")
if document_id:

    user_query = st.chat_input("Please ask your questions...")

    if user_query:
        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Answering..."):
                try:
                    headers = get_headers()

                    data = {
                        "document_id": document_id,
                        "query": user_query,
                    }

                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        json=data,
                        headers=headers,
                    )
                    data = response.json()

                    if response.status_code == 200:
                        answer = data["answer"]
                        sources = [source["source"] for source in data["sources"]]

                        print("Sources: ", data["sources"])

                        st.write(answer)
                        
                        if sources:
                            render_sources(sources)
                            
                    else:
                        st.error(data.get("detail", "Something went wrong."))
                        st.stop()

                except Exception as e:
                    print(e)
                    st.error("Something went wrong.")
                    st.stop()
                    

if st.session_state.get("logged_in", False):
    with st.sidebar:
        if st.button(label="Logout"):
            st.session_state.clear()
            st.switch_page("pages/login.py")
        st.subheader("Chat History")

        try:
            if document_id:
                response = requests.get(f"{BACKEND_URL}/chat-history/{document_id}")
                data = response.json()

                if response.status_code == 200:
                    result = data["data"]
                    with st.spinner("History loading..."):
                        if result:
                            render_chat_history(messages=result)
                        else:
                            st.info("No history found.")
                else:
                    st.error(data.get("detail", "Failed to load chat history."))

        except Exception as e:
            print(e)
            st.error("Failed to load chat history.")