"""
NEOS Tool: Fetch and parse web pages within authorized scope
"""
import requests
from urllib.parse import urlparse
from typing import Optional


def fetch_url(url: str, scope: Optional[list] = None, max_chars: int = 4000) -> dict:
    """
    Fetch a URL and return cleaned text content.
    Args:
        url: URL to fetch
        scope: list of allowed domains (None = unrestricted)
        max_chars: max characters to return (fits in NEOS context)
    Returns:
        dict with content and metadata
    """
    if scope:
        domain = urlparse(url).netloc
        if not any(domain.endswith(s) for s in scope):
            return {"error": f"URL out of scope. Allowed: {scope}", "content": ""}

    headers = {"User-Agent": "Mozilla/5.0 (Security Research)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "")

        # Extract text — skip binary
        if "text" not in content_type and "json" not in content_type:
            return {"error": f"Non-text content: {content_type}", "content": ""}

        # Parse HTML if needed
        if "html" in content_type:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer"]):
                    tag.decompose()
                text = soup.get_text(separator="\n", strip=True)
            except ImportError:
                text = resp.text
        else:
            text = resp.text

        # Truncate to fit NEOS context window
        text = "\n".join(line for line in text.splitlines() if line.strip())
        text = text[:max_chars]

        return {
            "url": url,
            "status": resp.status_code,
            "content_type": content_type,
            "content": text,
            "truncated": len(resp.text) > max_chars,
        }

    except Exception as e:
        return {"error": str(e), "content": ""}


def fetch_headers(url: str) -> dict:
    """Fetch only HTTP headers — useful for fingerprinting."""
    try:
        resp = requests.head(url, timeout=10, allow_redirects=True)
        return {
            "url": url,
            "status": resp.status_code,
            "headers": dict(resp.headers),
            "server": resp.headers.get("Server", ""),
            "x_powered_by": resp.headers.get("X-Powered-By", ""),
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    result = fetch_headers("https://httpbin.org")
    print(result)
