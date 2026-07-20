from backend.app.graph.state import State
from backend.app.rag.generator import generate_answer
from backend.app.rag.retriever import retrieve_documents
from backend.app.models.models import ChatHistory
from backend.app.graph.tools.calculator import (
    extract_expression, 
    validate_expression, 
    calculate_expression, 
    has_valid_expression,
    invalid_expression
    )
from backend.app.graph.tools.router import validate_route
from backend.app.graph.tools.web_search import search_web
from backend.app.graph.router_llm import router_chain

from datetime import datetime, timezone


def router_node(state: State):
    question = state["question"]
    try:
        response = router_chain.invoke({"question": question})

        route = response.content.strip().lower()
        if validate_route(route):
            state["route"] = route
        else:
            state["route"] = "rag"

        return state

    except Exception as e:
        print(e)
        state["route"] = "rag"

        return state
    


def greeting_node(state: State) -> State:
    state["tool_result"] = "Hello! How can I assist you today?"
    state["sources"] = []

    return state


def calculator_node(state: State) -> State:
    question = state["question"]

    expression = extract_expression(question)

    if not validate_expression(expression):
        return invalid_expression(state)
    
    if not has_valid_expression(expression):
        return invalid_expression(state)
    
    result = calculate_expression(expression)
    state["tool_result"] = str(result)
    state["sources"] = []

    return state


def rag_node(state: State) -> State:
    result = retrieve_documents(
        query=state["question"],
        user_id=state["user_id"],
        document_id=state["document_id"],
    )

    if result is None:
        state["retrieved_docs"] = []
        state["context"] = ""
        state["sources"] = []
        state["max_similarity"] = 0.0

        return state

    retrieved_docs = result["documents"][0]
    metadatas = [metadata for metadata in result["metadatas"][0]]
    similarities = [similarity for similarity in result["similarities"][0]]
    
    context = "\n\n".join(retrieved_docs)

    sources = [
        {
            "chunk_id": metadata["chunk_id"],
            "source": metadata["source"],
            "similarity": round(score, 3),
            "content": doc[:200] + "..." if len(doc) > 200 else doc,
            }

            for metadata, doc, score in zip(metadatas, retrieved_docs, similarities)
    ]
    
    state["retrieved_docs"] = retrieved_docs
    state["context"] = context
    state["sources"] = sources
    state["max_similarity"] = max(similarities) if similarities else 0.0

    return state


def web_search_node(state: State) -> State:
    result = search_web(state["question"])

    state["context"] = result["context"]
    state["sources"] = result["sources"]

    return state


def answer_node(state: State) -> State:
    if state.get("tool_result"):
        state["answer"] = state["tool_result"]
        return state
    else:
        context = state.get("context", "")


    if not context:
        state["answer"] = (
            "Sorry, I could not find this information in the uploaded documents."
        )
        return state

    answer = generate_answer(
        context=context,
        query=state["question"],
        chat_history=state["chat_history"],
    )
    state["answer"] = answer
    
    return state


def save_history_node(state: State) -> State:
    user_id = state["user_id"]
    document_id = state["document_id"]
    db = state["db"]

    user_message = state["question"]
    assistant_message = state["answer"]
    sources = state["sources"]

    # User row
    db_user_message = ChatHistory(
        user_id=user_id,
        document_id=document_id,
        role="user",
        message=user_message,
        sources=None,
        created_at=datetime.now(timezone.utc),
    )
    # Assistant row
    db_assistant_message = ChatHistory(
        user_id=user_id,
        document_id=document_id,
        role="assistant",
        message=assistant_message,
        sources=sources,
        created_at=datetime.now(timezone.utc),
    )
    
    try:
        db.add_all([db_user_message, db_assistant_message])
        db.commit()
    except Exception:
        db.rollback()
        raise

    return state