from langchain_ollama import ChatOllama

from backend.app.rag.prompts import QA_PROMPT

from config import LLM_MODEL
from fastapi import HTTPException

llm = ChatOllama(model=LLM_MODEL)
chain = QA_PROMPT | llm


def generate_answer(context, query, chat_history):
    try:
        result = chain.invoke({
            "context": context,
            "query": query,
            "chat_history": chat_history,
        })
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="LLM service unavailable."
        )

    return result.content
