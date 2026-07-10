from typing import TypedDict
from sqlalchemy.orm import Session


class State(TypedDict):
    user_id: int
    document_id: int

    question: str

    retrieved_docs: list[str]
    context: str
    sources: list

    tool_result: str

    answer: str
    
    chat_history: list

    db: Session