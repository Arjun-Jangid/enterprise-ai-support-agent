import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from backend.app.rag.pipeline import ask_question, ingest_document
from config import UPLOAD_DIR
from frontend.utils.file_writer import save_text_file
from frontend.utils.text_extractor import extract_docx_text, extract_pdf_text, extract_txt_text

# Streamlit Page UI configuration
st.set_page_config(
    page_title="AI Enterprise Tool",
    page_icon="⚡",
    layout="centered",
)

st.title("AI Enterprise Tool")
st.markdown("Please upload your corporate document below.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])

if uploaded_file is not None:
    # Safely generate a standardized target file name using pathlib
    base_name = Path(uploaded_file.name).stem
    file_type = Path(uploaded_file.name).suffix.lower()
    target_file_path = UPLOAD_DIR / f"{base_name}.txt"

    text: str | None = None

    # Process files based on suffix evaluations
    if file_type == ".pdf":
        with st.spinner("Processing PDF document..."):
            text = extract_pdf_text(uploaded_file)

    elif file_type == ".txt":
        with st.spinner("Processing text document..."):
            text = extract_txt_text(uploaded_file)

    elif file_type == ".docx":
        with st.spinner("Processing docx document..."):
            text = extract_docx_text(uploaded_file)


    if text is not None:
        if save_text_file(text, target_file_path):
            st.success("Document processed successfully.")

        ingest_document(text)

    user_query = st.text_input(label="Ask your question...")

    if st.button(label="Submit"):
        if user_query:
            with st.spinner("Answering..."):
                answer = ask_question(user_query)

                if answer:
                    st.write(answer)
                else:
                    st.warning("No answer found.")

        else:
            st.warning("Please ask a query.")
