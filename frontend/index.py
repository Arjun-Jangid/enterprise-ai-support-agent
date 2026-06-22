import streamlit as st
import sys
from pathlib import Path
from utils.text_extractor import extract_pdf_text, extract_txt_text, extract_docx_text
from utils.file_writer import save_text_file

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import UPLOAD_DIR

# Streamlit Page UI configuration
st.set_page_config(
    page_title="AI Enterprise Tool",
    page_icon="⚡",
    layout="centered"
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
    
    if save_text_file(text, target_file_path):
        st.success("Document processed successfully.")

