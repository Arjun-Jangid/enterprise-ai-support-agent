import sys
import requests
from pathlib import Path

import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/signup.py")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from config import BACKEND_URL

from frontend.utils.session import init_chat_session
from frontend.utils.headers import get_headers
from frontend.component.chat_history import render_chat_history


st.set_page_config(
    page_title="AI Enterprise Tool",
    page_icon="⚡",
    layout="centered",
)

init_chat_session()

st.title("AI Enterprise Tool")
st.markdown("Please upload your document below.")


# File upload
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"], key="uploader")

if st.button("Submit"):
    if uploaded_file:
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
                        st.write(data["answer"])
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

                print("Data in history -- ", data)

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