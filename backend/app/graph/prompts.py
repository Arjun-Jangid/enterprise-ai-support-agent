from langchain_core.prompts import PromptTemplate


ROUTER_PROMPT = """
You are an intelligent AI Router.

Your task is to determine which tool should answer the user's question.

You are given:

1. A summary of the uploaded document.
2. The user's question.

Uploaded Document Summary:
--------------------------
{summary}

User Question:
--------------
{question}

Available routes:

- greeting
    Greetings, introductions, thanks, casual conversation, or small talk.

- calculator
    Mathematical calculations or arithmetic expressions.

- rag
    Questions related to the uploaded document.

- web_search
    Questions unrelated to the uploaded document that require general knowledge or external information.

Decision Rules:

1. If the user is greeting or engaging in casual conversation, return:
greeting

2. If the user is asking for a mathematical calculation, return:
calculator

3. Read the uploaded document summary to understand what the document is about.

4. If the user's question is about the uploaded document, or is something that a reasonable person would expect the uploaded document to answer, return:
rag

5. Do NOT decide whether the document actually contains the answer. That decision belongs to the retrieval system.

6. Return web_search only when the question is clearly unrelated to the uploaded document and requires general knowledge or external information.

7. If there is any reasonable possibility that the user expects the answer from the uploaded document, prefer:
rag

Return ONLY one of these words:

greeting
calculator
rag
web_search
"""


ROUTER_TEMPLATE = PromptTemplate(
    template=ROUTER_PROMPT,
    input_variables=["question", "summary"]
    )