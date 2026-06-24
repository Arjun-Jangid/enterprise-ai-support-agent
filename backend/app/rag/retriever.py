from uuid import uuid4

from backend.app.rag.embedding import create_embeddings
from backend.app.rag.vectorstore import collection


def store_chunks(chunks):
    embeddings = create_embeddings(chunks)

    collection.add(
        ids=[str(uuid4()) for _ in chunks],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "chunk_id": idx,
                "source": "user",
            }
            for idx, _ in enumerate(chunks)
        ],
    )


def retrieve_documents(query: str, top_k: int = 5):
    query_embedding = create_embeddings([query])

    result = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
    )

    return result
