# researcher/fetcher.py
import requests
import trafilatura
from bs4 import BeautifulSoup
from .utils import is_allowed_by_robots, polite_wait, logger

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

def fetch_url(url, timeout=15):
    if not is_allowed_by_robots(url):
        logger.warning("Blocked by robots.txt: %s", url)
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        html = r.text
        # try trafilatura extraction
        text = trafilatura.extract(html, include_comments=False, include_tables=False)
        if text and len(text) > 200:
            return text.strip()
        # fallback: join <p> tags
        soup = BeautifulSoup(html, "lxml")
        p_texts = [p.get_text(strip=True) for p in soup.find_all("p")]
        return "\n\n".join(p_texts).strip()
    except Exception as e:
        logger.exception("Error fetching %s: %s", url, e)
        return None

def fetch_many(urls, pause=1.0):
    results = {}
    for u in urls:
        polite_wait(pause)
        txt = fetch_url(u)
        if txt:
            results[u] = txt
    return results
