from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from config import LLM_MODEL

llm = ChatOllama(model=LLM_MODEL)


def generate_answer(context, question, chat_history):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful document Q&A assistant.
Answer only from the provided context and chat history.
If the answer is not in the uploaded documents, say:
"I could not find this information in the uploaded documents."
Keep answers short."""),
("placeholder", "{chat_history}"),
("human", """Context:

{context}

Question:

{question}""")
    ])

    chain = prompt | llm

    result = chain.invoke({
        "context": context,
        "question": question,
        "chat_history": chat_history,
    })

    return result.content
