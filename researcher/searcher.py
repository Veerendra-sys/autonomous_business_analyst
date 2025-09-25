# researcher/searcher.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def search(query: str, max_results: int = 6):
    """
    Search Google using SerpAPI and return a list of result URLs.
    """
    if not SERP_API_KEY:
        raise RuntimeError("Missing SERP_API_KEY in .env")

    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "num": max_results,
        "api_key": SERP_API_KEY,
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("organic_results", []):
        link = item.get("link")
        if link:
            results.append(link)

    return results[:max_results]
