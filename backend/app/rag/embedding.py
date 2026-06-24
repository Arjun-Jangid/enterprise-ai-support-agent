from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)


def create_embeddings(texts):
    return model.encode(
        texts,
        normalize_embeddings=True,
    ).tolist()
