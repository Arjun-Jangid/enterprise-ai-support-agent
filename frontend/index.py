import sys
import time
from pathlib import Path

import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/signup.py")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from backend.app.rag.pipeline import ask_question, ingest_document
from config import UPLOAD_DIR
from frontend.utils.file_writer import save_text_file
from frontend.utils.text_extractor import extract_docx_text, extract_pdf_text, extract_txt_text
from frontend.utils.session import (
    init_chat_session,
    get_messages,
    add_user_message,
    add_assistant_message,
)
from frontend.utils.chat_mapper import build_langchain_history
from frontend.component.chat_history import render_chat_history

# Streamlit Page UI configuration
st.set_page_config(
    page_title="AI Enterprise Tool",
    page_icon="⚡",
    layout="centered",
)

init_chat_session()

if "doc_processed" not in st.session_state:
    st.session_state.doc_processed = False

if "current_file_id" not in st.session_state:
    st.session_state.current_file_id = None


st.title("AI Enterprise Tool")
st.markdown("Please upload your corporate document below.")

def reset_for_new_file():
    st.session_state.doc_processed = False
    st.session_state.current_file_id = None
    st.session_state.messages = []

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"], key="uploader")

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_size = uploaded_file.size
    file_id = f"{file_name}_{file_size}"

    st.write(f"Current file - {uploaded_file.name}_{uploaded_file.size}")
    print()
    print(st.session_state.get("current_file_id"), "and", file_id)
    print()

    if st.session_state.get("current_file_id") != file_id:
        reset_for_new_file()
        st.session_state.current_file_id = file_id
        try:
            text: str | None = None
            file_type = Path(file_name).suffix.lower()

            # Process files based on suffix
            if file_type == ".pdf":
                with st.spinner("Processing PDF document..."):
                    text = extract_pdf_text(uploaded_file)
            elif file_type == ".txt":
                with st.spinner("Processing text document..."):
                    text = extract_txt_text(uploaded_file)
            elif file_type == ".docx":
                with st.spinner("Processing docx document..."):
                    text = extract_docx_text(uploaded_file)

            if not text or not text.strip():
                st.error("Could not extract any text from the file.")
                st.stop()

            base_name = f"{Path(file_name).stem}_{int(time.time())}.txt"
            target_file_path = UPLOAD_DIR / base_name

            status = st.empty()

            if not save_text_file(text, target_file_path):
                st.error("Failed to save document.")
                st.stop()

            ingest_document(text, file_name)
            st.session_state.doc_processed = True
            status.success("Document ready.")
            status.empty()
        
        except Exception as e:
            st.error(f"Document processing failed: {e}")
            st.stop()
    
    else:
        st.write(f"This document {uploaded_file.name}_{uploaded_file.size} has already uploaded!")
        print(f"This document {uploaded_file.name}_{uploaded_file.size} has already uploaded!")

if st.session_state.doc_processed:
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
            
        render_chat_history(messages=get_messages())