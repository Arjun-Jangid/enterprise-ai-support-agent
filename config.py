from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(".env")

# Paths
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

# Collection name
COLLECTION_NAME = "enterprise_documents"

# URLs
DATABASE_URL = f"sqlite:///{DATA_DIR / 'enterprise.db'}"
BACKEND_URL = "http://backend:8000"

# API keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LLMs
ROUTER_MODEL = "llama-3.1-8b-instant"
ANSWER_MODEL = "llama-3.3-70b-versatile"

# Router
SIMILARITY_THRESHOLD = 0.40

# RAG
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80