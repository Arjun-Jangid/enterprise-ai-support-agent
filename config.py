from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
SIMILARITY_THRESHOLD = 0.40

COLLECTION_NAME = "enterprise_documents"

EMBEDDING_MODEL = "BAAI/bge-m3"

LLM_MODEL = "qwen2.5:3b"

DATABASE_URL = f"sqlite:///{DATA_DIR / 'enterprise.db'}"

BACKEND_URL = "http://127.0.0.1:8000"