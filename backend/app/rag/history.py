from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from backend.app.rag.prompts import SYSTEM_PROMPT

def build_langchain_history(chat_history):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    for chat in chat_history:

        if chat.role == "user":
            messages.append(HumanMessage(content=chat.message))
        
        elif chat.role == "assistant":
            messages.append(AIMessage(content=chat.message))

    return messages