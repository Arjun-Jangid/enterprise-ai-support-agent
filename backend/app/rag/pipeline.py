from backend.app.rag.chunking import split_document
from backend.app.rag.generator import generate_answer
from backend.app.rag.retriever import retrieve_documents, store_chunks


def ingest_document(text: str, file_name: str):
    chunks = split_document(text)
    store_chunks(chunks, file_name)


def ask_question(question: str, chat_history):
    result = retrieve_documents(question)
    context = "\n\n".join(
        result["documents"][0],
    )

    answer = generate_answer(
        context=context,
        question=question,
        chat_history=chat_history,
    )

    docs = [doc for doc in result["documents"][0]]
    metadatas = [metadata for metadata in result["metadatas"][0]]
    similarities = [similarity for similarity in result["similarities"][0]]

    sources = [
        {
            "chunk_id": metadata["chunk_id"],
            "source": metadata["source"],
            "similarity": round(score, 3),
            "content": doc,
            }

            for metadata, doc, score in zip(metadatas, docs, similarities)
    ]

    return {"answer": answer, "sources": sources}
