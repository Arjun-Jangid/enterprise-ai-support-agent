import chromadb

from config import CHROMA_DB_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

collection = client.get_or_create_collection(COLLECTION_NAME)
