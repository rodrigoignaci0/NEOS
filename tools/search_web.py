"""
NEOS Tool: Web search via DuckDuckGo (no API key required)
"""
import requests
import json
import re


def search_web(query: str, max_results: int = 5) -> dict:
    """
    Search the web using DuckDuckGo Instant Answer API.
    Args:
        query: search query
        max_results: max results to return
    Returns:
        dict with search results
    """
    # DuckDuckGo Instant Answer API
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": str(e), "results": []}

    results = []

    # Abstract (direct answer)
    if data.get("AbstractText"):
        results.append({
            "title": data.get("Heading", ""),
            "snippet": data["AbstractText"][:400],
            "url": data.get("AbstractURL", ""),
            "source": "DuckDuckGo Abstract",
        })

    # Related topics
    for topic in data.get("RelatedTopics", [])[:max_results]:
        if isinstance(topic, dict) and topic.get("Text"):
            results.append({
                "title": topic.get("Text", "")[:100],
                "snippet": topic.get("Text", "")[:400],
                "url": topic.get("FirstURL", ""),
                "source": "DuckDuckGo Related",
            })

    # Fallback: HTML scrape if no results
    if not results:
        results = _scrape_ddg(query, max_results)

    return {"query": query, "results": results[:max_results]}


def _scrape_ddg(query: str, max_results: int) -> list:
    """Fallback scraper for DuckDuckGo HTML."""
    url = "https://html.duckduckgo.com/html/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.post(url, data={"q": query}, headers=headers, timeout=10)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for result in soup.select(".result")[:max_results]:
            title_el = result.select_one(".result__title")
            snippet_el = result.select_one(".result__snippet")
            url_el = result.select_one(".result__url")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True),
                    "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                    "url": url_el.get_text(strip=True) if url_el else "",
                    "source": "DuckDuckGo HTML",
                })
        return results
    except Exception:
        return []


def format_for_neos(result: dict) -> str:
    lines = [f"Web Search: '{result['query']}'\n"]
    for i, r in enumerate(result.get("results", []), 1):
        lines.append(f"[{i}] {r['title']}")
        lines.append(f"    {r['snippet'][:200]}")
        if r.get("url"):
            lines.append(f"    URL: {r['url']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    result = search_web("CVE-2021-41773 Apache exploit")
    print(format_for_neos(result))
