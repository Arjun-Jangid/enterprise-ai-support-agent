from config import SUMMARIZER_MODEL, GROQ_API_KEY
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


summarizer_llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=SUMMARIZER_MODEL,
            temperature=0,
        )


SUMMARIZER_PROMPT = """
You are an expert document analyzer.

Your task is to create a concise summary that helps an AI Router decide whether a user's question should be answered from this document.

Document:

{document}

Read the document carefully and produce a summary with the following information:

1. Document Type
   (Resume, Employee Handbook, Research Paper, Invoice, Policy, Medical Report, Technical Manual, etc.)

2. Main Subject
   Explain in one or two sentences what the document is about.

3. Major Topics
   List the important topics covered in the document.

4. Named Entities
   Include important people, organizations, products, technologies, locations, and projects mentioned.

5. Key Keywords
   List the most important keywords that represent the document.

Rules:
- Do NOT include unnecessary details.
- Do NOT rewrite the document.
- Focus only on information useful for routing user questions.
- If a topic is NOT present in the document, do not invent it.
- The summary should be less than 300 words.
- Return the output in the following format.

Document Type:
...

Main Subject:
...

Major Topics:
- ...
- ...
- ...

Named Entities:
- ...
- ...
- ...

Keywords:
- ...
- ...
- ...
- ...
"""

SUMMARIZER_TEMPLATE = PromptTemplate(
    template=SUMMARIZER_PROMPT,
    input_variables=["document"]
)

summarizer_chain = SUMMARIZER_TEMPLATE | summarizer_llm

def generate_document_summary(text: str) -> str:
    try:
        result = summarizer_chain.invoke({"document": text})
        return result.content
    except Exception as e:
        print(f"Summary generation failed: {e}")
        return ""
