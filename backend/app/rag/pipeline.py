from backend.app.rag.chunking import split_document
from backend.app.rag.generator import generate_answer
from backend.app.rag.retriever import retrieve_documents, store_chunks


def ingest_document(text: str):
    chunks = split_document(text)
    store_chunks(chunks)


def ask_question(question: str):
    result = retrieve_documents(question)
    context = "\n\n".join(
        result["documents"][0],
    )

    answer = generate_answer(
        context=context,
        question=question,
    )

    return answer
