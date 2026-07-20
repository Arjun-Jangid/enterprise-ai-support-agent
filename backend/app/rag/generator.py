from langchain_groq import ChatGroq
from backend.app.rag.prompts import QA_PROMPT
from config import GROQ_API_KEY, ANSWER_MODEL
from fastapi import HTTPException


answer_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=ANSWER_MODEL,
    temperature=0,
    )

chain = QA_PROMPT | answer_llm


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
