from uuid import uuid4

from sklearn.metrics.pairwise import cosine_similarity

from backend.app.rag.embedding import create_embeddings
from backend.app.rag.vectorstore import collection


def store_chunks(chunks, file_name):
    embeddings = create_embeddings(chunks)

    collection.add(
        ids=[str(uuid4()) for _ in chunks],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "source": file_name,
                "chunk_id": i + 1,
            }
            for i, _ in enumerate(chunks)
        ],
    )


def retrieve_documents(query: str, top_k: int = 3):
    query_embedding = create_embeddings([query])

    result = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
    )

    retrieved_chunks = result["documents"][0]
    chunk_embeddings = create_embeddings(retrieved_chunks)

    similarities = cosine_similarity(query_embedding, chunk_embeddings)
    result["similarities"] = similarities.tolist()

    return result
