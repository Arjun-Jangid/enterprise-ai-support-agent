from backend.app.graph.router_llm import ALLOWED_ROUTES

def validate_route(route: str) -> bool:
    return route in ALLOWED_ROUTES