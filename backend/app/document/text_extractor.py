import re
import pypdf
import docx2txt
from io import BytesIO

from tempfile import NamedTemporaryFile
from fastapi import HTTPException


def condense_whitespace(raw_text: str) -> str:
    # 1. Fix Horizontal Spacing: Replace multiple spaces/tabs with a single space
    cleaned_text = re.sub(r'[ \t]+', ' ', raw_text)
        
    # 2. Fix Vertical Spacing: Replace 3 or more consecutive newlines with exactly 2
    # This keeps distinct paragraphs separated but deletes giant empty gaps
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
    # 3. Remove leading/trailing whitespace from the entire document
    final_text = cleaned_text.strip()
    return final_text



def extract_pdf_text(file_bytes: bytes) -> str:
    """Extracts text from PDF and writes it to a file safely."""
    try:
        pdf_reader = pypdf.PdfReader(BytesIO(file_bytes))
        raw_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        
        if not raw_text.strip():
            raise HTTPException(
                    status_code=400,
                    detail="No extractable text was found in the PDF. The document may be scanned or image-based."
                )
    
        return condense_whitespace(raw_text)
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process the PDF document. Please upload a valid PDF file."
        )
    

def extract_txt_text(file_bytes: bytes) -> str:
    try:
        raw_text = file_bytes.decode("utf-8")
        return condense_whitespace(raw_text)

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the text file. Please save the file using UTF-8 encoding and try again."
        )
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process the text document. Please try again."
        )
    
    
def extract_docx_text(file_bytes: bytes) -> str:
    try:
        with NamedTemporaryFile(suffix=".docx") as temp_file:
            temp_file.write(file_bytes)
            temp_file.flush()

            raw_text = docx2txt.process(temp_file.name)

        if not raw_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No extractable text was found in the DOCX document."
            )
        return condense_whitespace(raw_text)
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process the DOCX document. Please upload a valid DOCX file."
        )
