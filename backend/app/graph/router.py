from backend.app.graph.state import State


def route_function(state: State) -> str:
    question = state["question"].strip().lower()

    if any(op in question for op in ['+', '-', '*', '/']):
        return "calculator"
    
    if question.lower() in {"hello", "hi", "hey", "how are you"}:
        return "greeting"
    
    else:
        return "rag"