from langgraph.graph import StateGraph, START, END
from backend.app.graph.nodes import rag_node, answer_node, save_history_node, calculator_node, greeting_node
from backend.app.graph.state import State
from backend.app.graph.router import route_function


builder = StateGraph(State)

builder.add_node("rag", rag_node)
builder.add_node("answer", answer_node)
builder.add_node("save_history", save_history_node)
builder.add_node("calculator", calculator_node)
builder.add_node("greeting", greeting_node)


builder.add_conditional_edges(
    START,
    route_function,
    {
        "greeting": "greeting",
        "rag": "rag",
        "calculator": "calculator",
    }
)

builder.add_edge("rag", "answer")
builder.add_edge("greeting", "answer")
builder.add_edge("calculator", "answer")
builder.add_edge("answer", "save_history")
builder.add_edge("save_history", END)


graph = builder.compile()