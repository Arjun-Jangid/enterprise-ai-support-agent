from sklearn.metrics.pairwise import cosine_similarity
import time

from backend.app.rag.embedding import embed_texts
from backend.app.rag.vectorstore import collection


def store_chunks(chunks, file_name: str, user_id: int, document_id: int):
    embeddings = embed_texts(chunks)

    collection.add(
        ids=[
            f"doc_{document_id}_chunk_{i+1}"
            for i in range(len(chunks))
            ],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {   
                "user_id": user_id,
                "document_id": document_id,
                "source": file_name,
                "chunk_id": i + 1,
            }
            for i, _ in enumerate(chunks)
        ],
    )


def retrieve_documents(query: str, user_id: int, document_id: int, top_k: int = 3):
    query_embedding = embed_texts([query])

    result = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        where={
            "$and": [
                {"user_id": user_id},
                {"document_id": document_id},
            ]
        },
    )

    if (
        not result["documents"]
        or
        not result["documents"][0]
    ):
        return None
    
    retrieved_chunks = result["documents"][0]
    chunk_embeddings = embed_texts(retrieved_chunks)

    similarities = cosine_similarity(query_embedding, chunk_embeddings)
    result["similarities"] = similarities.tolist()

    return result
