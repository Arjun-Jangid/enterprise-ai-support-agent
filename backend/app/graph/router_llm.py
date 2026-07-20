from langchain_groq import ChatGroq
from config import GROQ_API_KEY, ROUTER_MODEL
from backend.app.graph.prompts import ROUTER_TEMPLATE


router_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=ROUTER_MODEL,
    temperature=0,
)

router_chain = ROUTER_TEMPLATE | router_llm

ALLOWED_ROUTES = {
    "greeting",
    "calculator",
    "rag",
}