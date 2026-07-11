import regex as re
from backend.app.graph.state import State


def extract_expression(question: str) -> str:
    pattern = r"[^0-9+\-*/(). ]"
    expression = re.sub(pattern, "", question)

    return expression.strip()


def validate_expression(expression: str) -> bool:
    if not expression:
        return False
    
    pattern = r"^[0-9+\-*/(). ]+$"
    return bool(re.fullmatch(pattern, expression))


def has_valid_expression(expression: str) -> bool:
    pattern = r"[+\-*/]"

    return bool(re.search(pattern, expression))
    

def calculate_expression(expression: str) -> int | float | None:
    if not expression:
        return None

    try:
        return eval(expression)
    except Exception:
        return None
    

def invalid_expression(state: State) -> State:
    state["tool_result"] = "Invalid mathematical expression."
    state["sources"] = []
    return state