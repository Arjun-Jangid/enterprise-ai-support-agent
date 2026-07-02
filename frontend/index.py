import sys
import requests
from pathlib import Path

import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/signup.py")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.rag.pipeline import ask_question
from config import BACKEND_URL
from frontend.utils.session import (
    init_chat_session,
    get_messages,
    add_user_message,
    add_assistant_message,
)
from frontend.utils.chat_mapper import build_langchain_history
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

if uploaded_file is not None:
    try:
        token = st.session_state.get("token")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type,
            )
        }
         
        response = requests.post(f"{BACKEND_URL}/upload", files=files, headers=headers)
        data = response.json()

        if response.status_code == 200:
            st.success(data["message"])
            document_id = data.get("document_id")
            st.session_state.document_id = data["document_id"]
        elif response.status_code == 400:
            st.error(data["detail"])
        else:
            st.error(data["detail"])
    
    except Exception as e:
        print(f"Error - {e}")
        st.error(str(e))

    # User ask query
    user_query = st.chat_input("Please ask your questions...")
    if user_query:
        messages = get_messages()
        chat_history = build_langchain_history(messages)

        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Answering..."):
                try:
                    answer = ask_question(user_query, chat_history)
                    st.write(answer["answer"])
                    

                    token = st.session_state.get("token")
                    headers = {
                        "Authorization": f"Bearer {token}"
                    }
                    document_id = st.session_state.get("document_id")

                    data = {
                        "document_id": st.session_state.document_id,
                        "user_message": user_query,
                        "assistant_message": answer["answer"],
                        "sources": answer["sources"],
                    }

                    response = requests.post(f"{BACKEND_URL}/chat-history", json=data, headers=headers)

                    data = response.json()

                    if response.status_code == 200:
                        st.success(data["message"])
                    elif response.status_code == 400:
                        st.error(data["detail"])
                    else:
                        st.error(data["detail"])
                    

                    add_user_message(user_query)
                    add_assistant_message(answer)
                except Exception as e:
                    st.warning("No answer found.")
                    st.stop()


if st.session_state.get("logged_in", True):
    with st.sidebar:
        if st.button(label="Logout"):
            st.session_state.clear()
            st.switch_page("pages/login.py")
        st.subheader("Chat History")

        try:
            document_id = st.session_state.get("document_id")
            if document_id is not None:
                response = requests.get(f"{BACKEND_URL}/chat-history/{document_id}")
                data = response.json()

                if response.status_code == 200:
                    result = data["data"]
                    with st.spinner("History loading..."):
                        if result:
                            render_chat_history(messages=result)
                        else:
                            st.info("No history found.")
                elif response.status_code == 400:
                    st.error(data["message"])
                else:
                    print("Error")

        except Exception as e:
            print(e)