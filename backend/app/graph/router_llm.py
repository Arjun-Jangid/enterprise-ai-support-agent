from langchain_ollama import ChatOllama
from config import LLM_MODEL
from backend.app.graph.prompts import ROUTER_TEMPLATE

llm = ChatOllama(model=LLM_MODEL)
router_chain = ROUTER_TEMPLATE | llm

ALLOWED_ROUTES = {
    "greeting",
    "calculator",
    "rag",
}