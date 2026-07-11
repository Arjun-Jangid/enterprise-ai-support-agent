from backend.app.graph.state import State
from config import SIMILARITY_THRESHOLD


def route_function(state: State) -> str:
    return state["route"]

def retrieval_route_function(state: State) -> str:
    if state["max_similarity"] >= SIMILARITY_THRESHOLD:
        return "answer"

    return "web_search"