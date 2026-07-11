from tavily import TavilyClient
from config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query: str) -> dict:
    try:
        response = client.search(
            query=query,
            max_results=3,
        )

        results = response["results"]

        context = "\n\n".join(
            f"Title: {result['title']}\nContent: {result['content']}"
            for result in results
        )

        sources = [
            {
                "chunk_id": None,
                "content": (
                    result["content"][:200] + "..."
                    if len(result["content"]) > 200
                    else result["content"]
                ),
                "source": result["url"],
                "similarity": round(result["score"], 3),
            }
            for result in results
        ]

        return {
            "context": context,
            "sources": sources,
        }

    except Exception:
        return {
            "context": "",
            "sources": [],
        }