from langgraph.graph import StateGraph, START, END
from backend.app.graph.nodes import (
    router_node,
    greeting_node, 
    calculator_node, 
    web_search_node,
    rag_node, 
    answer_node, 
    save_history_node, 
    )
from backend.app.graph.state import State
from backend.app.graph.router import route_function, retrieval_route_function


builder = StateGraph(State)

builder.add_node("router", router_node)
builder.add_node("greeting", greeting_node)
builder.add_node("calculator", calculator_node)
builder.add_node("rag", rag_node)
builder.add_node("web_search", web_search_node)
builder.add_node("answer", answer_node)
builder.add_node("save_history", save_history_node)


builder.add_conditional_edges(
    "router",
    route_function,
    {
        "greeting": "greeting",
        "calculator": "calculator",
        "rag": "rag",
    }
)

builder.add_conditional_edges(
    "rag",
    retrieval_route_function,
    {
        "answer": "answer",
        "web_search": "web_search",
    }
)

builder.add_edge(START, "router")
builder.add_edge("greeting", "answer")
builder.add_edge("calculator", "answer")
builder.add_edge("web_search", "answer")
builder.add_edge("answer", "save_history")
builder.add_edge("save_history", END)


graph = builder.compile()