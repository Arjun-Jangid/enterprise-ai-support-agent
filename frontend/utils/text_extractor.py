import re
import pypdf
import docx2txt
import logging
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def condense_whitespace(raw_text: str) -> str:
    # 1. Fix Horizontal Spacing: Replace multiple spaces/tabs with a single space
    cleaned_text = re.sub(r'[ \t]+', ' ', raw_text)
        
    # 2. Fix Vertical Spacing: Replace 3 or more consecutive newlines with exactly 2
    # This keeps distinct paragraphs separated but deletes giant empty gaps
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
    # 3. Remove leading/trailing whitespace from the entire document
    final_text = cleaned_text.strip()
    return final_text



def extract_pdf_text(uploaded_file) -> str | None:
    """Extracts text from PDF and writes it to a file safely."""
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        raw_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        
        if not raw_text.strip():
            st.warning("No extractable text was found in the PDF. The document may be scanned or image-based.")
            return None
        
        return condense_whitespace(raw_text)
    
    except Exception as e:
        logger.error(f"Failed to process PDF {uploaded_file.name}: {str(e)}")
        st.error("Unable to process the PDF document. Please upload a valid PDF file.")
        return None
    

def extract_txt_text(uploaded_file) -> str | None:
    """Decodes and writes raw text file safely."""
    try:
        raw_text = uploaded_file.read().decode("utf-8")
        return condense_whitespace(raw_text)
    
    except UnicodeDecodeError:
        logger.error(f"Encoding mismatch for file {uploaded_file.name}")
        st.error("Unable to read the text file. Please save the file using UTF-8 encoding and try again.")
        return None
    
    except Exception as e:
        logger.error(f"Failed to save text file {uploaded_file.name}: {str(e)}")
        st.error("Unable to process the text document. Please try again.")
        return None
    

def extract_docx_text(uploaded_file) -> str | None:

    try:
        raw_text = docx2txt.process(uploaded_file)
        return condense_whitespace(raw_text)

    except Exception as e:
        logger.error(f"Failed to save docx file {uploaded_file.name}: {str(e)}")
        st.error("Unable to process the docx document. Please try again.")
        return None
