"""
NEOS Tool Router — conecta las tools con el modelo vía system prompt
"""
import json
from typing import Callable
from search_cve import search_cve, format_for_neos as fmt_cve
from search_exploit import search_exploit_db, search_github_poc, format_for_neos as fmt_exploit
from fetch_url import fetch_url, fetch_headers
from search_web import search_web, format_for_neos as fmt_web


TOOLS_SCHEMA = [
    {
        "name": "search_cve",
        "description": "Search CVE database (NVD) for known vulnerabilities. Use when analyzing a specific product, version, or technology.",
        "parameters": {
            "query": "product name, version, or keyword (e.g. 'Apache 2.4.50', 'Log4j RCE')",
            "max_results": "number of CVEs to return (default 5)"
        }
    },
    {
        "name": "search_exploit",
        "description": "Search Exploit-DB and GitHub for public exploits and PoCs. Use after identifying a CVE or vulnerability.",
        "parameters": {
            "query": "search term (e.g. 'Apache path traversal 2021')",
            "cve_id": "optional CVE ID for GitHub PoC search (e.g. 'CVE-2021-41773')"
        }
    },
    {
        "name": "fetch_url",
        "description": "Fetch and read a web page. Use to read documentation, CVE details, or analyze a target within scope.",
        "parameters": {
            "url": "URL to fetch",
            "scope": "optional list of allowed domains for safety"
        }
    },
    {
        "name": "fetch_headers",
        "description": "Fetch HTTP headers from a URL. Use for fingerprinting server technology.",
        "parameters": {
            "url": "target URL"
        }
    },
    {
        "name": "search_web",
        "description": "Search the web for security research, writeups, or technical information.",
        "parameters": {
            "query": "search query",
            "max_results": "number of results (default 5)"
        }
    }
]


SYSTEM_PROMPT = """You are NEOS, an autonomous cybersecurity AI specialized in offensive and defensive security.

You have access to the following tools to augment your knowledge with real-time data:

{tools}

To use a tool, output a JSON block in this format:
```tool
{{"tool": "tool_name", "params": {{"param1": "value1"}}}}
```

After receiving tool output, continue your reasoning with the new information.
Always reason step by step before using a tool. Use tools when you need current CVE data, real exploits, or information about a specific target.
""".format(tools=json.dumps(TOOLS_SCHEMA, indent=2))


def execute_tool(tool_name: str, params: dict) -> str:
    """Execute a tool by name and return formatted output."""
    try:
        if tool_name == "search_cve":
            result = search_cve(params.get("query", ""), params.get("max_results", 5))
            return fmt_cve(result)
        elif tool_name == "search_exploit":
            exploit_result = search_exploit_db(params.get("query", ""))
            github_result = None
            if params.get("cve_id"):
                github_result = search_github_poc(params["cve_id"])
            return fmt_exploit(exploit_result, github_result)
        elif tool_name == "fetch_url":
            result = fetch_url(params.get("url", ""), params.get("scope"))
            return result.get("content", result.get("error", "No content"))
        elif tool_name == "fetch_headers":
            result = fetch_headers(params.get("url", ""))
            return json.dumps(result, indent=2)
        elif tool_name == "search_web":
            result = search_web(params.get("query", ""), params.get("max_results", 5))
            return fmt_web(result)
        else:
            return f"Unknown tool: {tool_name}"
    except Exception as e:
        return f"Tool error: {str(e)}"


def parse_tool_call(text: str) -> tuple:
    """Extract tool call from model output."""
    import re
    pattern = r"```tool\s*(\{.*?\})\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            call = json.loads(match.group(1))
            return call.get("tool"), call.get("params", {})
        except json.JSONDecodeError:
            return None, None
    return None, None


if __name__ == "__main__":
    # Test
    print(SYSTEM_PROMPT[:500])
    print("\n--- Test search_cve ---")
    print(execute_tool("search_cve", {"query": "Apache 2.4.50"}))
