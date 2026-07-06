from backend.app.rag.chunking import split_document
from backend.app.rag.retriever import store_chunks


def ingest_document(text: str, file_name: str, user_id: int, document_id: int):
    chunks = split_document(text)
    store_chunks(chunks, file_name, user_id, document_id)
