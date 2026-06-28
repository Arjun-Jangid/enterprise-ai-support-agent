from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80

COLLECTION_NAME = "my_docs"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

LLM_MODEL = "qwen2.5:3b"

DATABASE_URL = f"sqlite:///{DATA_DIR / 'enterprise.db'}"

BACKEND_URL = "http://127.0.0.1:8000"