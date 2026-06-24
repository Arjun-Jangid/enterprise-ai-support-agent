from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from config import LLM_MODEL

llm = ChatOllama(model=LLM_MODEL)

PROMPT = """
You are a document QA assistant.

Context:

{context}
Question:

{question}
Instructions:

- Answer only from the context.
- Combine information from multiple sections if needed.
- Do not use outside knowledge.
- If the answer is not available, reply:
"I could not find this information in the uploaded documents."
"""


def generate_answer(context, question):
    prompt = PromptTemplate(
        template=PROMPT,
        input_variables=["context", "question"],
    )

    chain = prompt | llm

    result = chain.invoke({
        "context": context,
        "question": question,
    })

    return result.content
