from langchain_core.prompts import PromptTemplate

ROUTER_PROMPT = """
You are an AI router.

Your task is to choose the single best route for the user's question.

Available routes:

- greeting: greetings, introductions, casual conversation.
- calculator: arithmetic calculations using numbers and operators (+, -, *, /, parentheses).
- rag: Questions about the user's uploaded documents OR questions that are not greetings or calculations.

Rules:
- Return ONLY one route.
- Do not explain your choice.
- Do not include punctuation.
- Your answer must be exactly one of:
  greeting
  calculator
  rag

Question:
{question}
"""

ROUTER_TEMPLATE = PromptTemplate(
    template=ROUTER_PROMPT,
    input_variables=["question"]
    )