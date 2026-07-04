from langchain_core.prompts import ChatPromptTemplate

QA_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful document Q&A assistant.
Answer only from the provided context and chat history.
If the answer is not in the uploaded documents, say:
"I could not find this information in the uploaded documents."
Keep answers short."""
    ),
    ("placeholder", "{chat_history}"),
    (
        "human",
        """
Context:
{context}

Question:
{query}
"""
    ),
])

SYSTEM_PROMPT = (
    "You are a helpful document Question/Answer assistant "
    "that gives short answers."
)