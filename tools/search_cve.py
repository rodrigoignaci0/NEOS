"""
NEOS Tool: CVE Search via NVD API (public, no key required)
"""
import requests
import json
from datetime import datetime


def search_cve(query: str, max_results: int = 5) -> dict:
    """
    Search CVEs from NVD database.
    Args:
        query: product name, vendor, or keyword (e.g. "Apache 2.4.50")
        max_results: max CVEs to return
    Returns:
        dict with CVE list and metadata
    """
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {"keywordSearch": query, "resultsPerPage": max_results}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": str(e), "results": []}

    results = []
    for item in data.get("vulnerabilities", []):
        cve = item.get("cve", {})
        cve_id = cve.get("id", "")
        descriptions = cve.get("descriptions", [])
        desc = next((d["value"] for d in descriptions if d["lang"] == "en"), "")
        metrics = cve.get("metrics", {})
        cvss = None
        if "cvssMetricV31" in metrics:
            cvss = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
        elif "cvssMetricV30" in metrics:
            cvss = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
        elif "cvssMetricV2" in metrics:
            cvss = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]

        results.append({
            "cve_id": cve_id,
            "description": desc[:500],
            "cvss_score": cvss,
            "published": cve.get("published", "")[:10],
            "references": [r["url"] for r in cve.get("references", [])[:3]],
        })

    return {
        "query": query,
        "total_found": data.get("totalResults", 0),
        "results": results,
    }


def format_for_neos(result: dict) -> str:
    """Format CVE results as text for NEOS context."""
    if "error" in result:
        return f"[CVE Search Error] {result['error']}"

    lines = [f"CVE Search: '{result['query']}' — {result['total_found']} found\n"]
    for cve in result["results"]:
        lines.append(f"[{cve['cve_id']}] CVSS: {cve['cvss_score']} | {cve['published']}")
        lines.append(f"  {cve['description'][:200]}")
        if cve["references"]:
            lines.append(f"  Ref: {cve['references'][0]}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    result = search_cve("Apache 2.4.50")
    print(format_for_neos(result))
