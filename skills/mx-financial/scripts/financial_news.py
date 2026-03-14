# /// script
# dependencies = [
#   "python-dotenv"
# ]
# ///


from __future__ import annotations

import argparse
import asyncio
import json
import re
import uuid
from urllib import error as urllib_error
from urllib import request as urllib_request
from typing import Any
import os
from dotenv import load_dotenv
import sys

load_dotenv(override=True)

EM_API_KEY = os.getenv("EM_API_KEY")

if not EM_API_KEY:
    raise RuntimeError("Please set the EM_API_KEY environment variable first")

TIMEOUT_SECONDS = 15
MCP_URL = "https://ai-saas.eastmoney.com/proxy/b/mcp/tool/searchNews"

# Force stdin/stdout to use utf-8 to avoid garbled code errors on Windows
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _safe_filename(text: str, max_len: int = 80) -> str:
    """Convert a query string into a safe filename segment."""
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", text).strip().replace(" ", "_")
    return (cleaned[:max_len] or "query").strip("._")


def _extract_content(raw: dict[str, Any]) -> str:
    """Extract readable text from news API response payload."""
    if not isinstance(raw, dict):
        return ""

    # Common envelope format: {"data": {...}} / {"result": {...}}
    for wrapper_key in ("data", "result"):
        wrapped = raw.get(wrapper_key)
        if isinstance(wrapped, dict):
            nested = _extract_content(wrapped)
            if nested:
                return nested

    for key in ("llmSearchResponse", "searchResponse", "content", "answer", "summary"):
        value = raw.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False, indent=2)

    return json.dumps(raw, ensure_ascii=False, indent=2)


def _load_optional_tool_context() -> dict[str, Any]:
    """
    Build request context with safe defaults.

    Note:
    - No environment variables are read in this module.
    - callId is generated for traceability.
    """
    return {"callId": f"call_{uuid.uuid4().hex[:12]}"}


def _extract_error_message(body: str) -> str:
    """Return sanitized error details from response body."""
    body = (body or "").strip()
    if not body:
        return ""
    try:
        data = json.loads(body)
    except Exception:
        return body[:200]
    if isinstance(data, dict):
        for key in ("msg", "message", "error"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return body[:200]


def _http_call_search_news(query: str) -> dict[str, Any]:
    """Call `searchNews` API and return parsed JSON payload."""
    api_key = EM_API_KEY.strip()
    if not api_key:
        raise ValueError("EM_API_KEY is required.")

    timeout_raw = str(TIMEOUT_SECONDS).strip()
    try:
        timeout_seconds = max(1, int(timeout_raw))
    except ValueError as exc:
        raise ValueError(
            "FINANCIAL_SEARCH_HTTP_TIMEOUT must be an integer >= 1."
        ) from exc

    payload = {
        "query": query,
        "toolContext": _load_optional_tool_context(),
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib_request.Request(
        url=MCP_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "em_api_key": api_key,
        },
    )

    try:
        with urllib_request.urlopen(req, timeout=timeout_seconds) as resp:
            raw_body = resp.read().decode("utf-8", errors="replace")
    except urllib_error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        message = _extract_error_message(err_body) or f"http status {exc.code}"
        raise RuntimeError(f"News API request failed: {message}") from exc
    except urllib_error.URLError as exc:
        raise RuntimeError(f"News API request failed: {exc.reason}") from exc

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("News API returned invalid JSON response.") from exc
    return parsed if isinstance(parsed, dict) else {"data": parsed}


async def query_financial_news(query: str) -> dict[str, Any]:
    """
    Query time-sensitive financial information from MCP news search.

    Returns:
        dict with keys: query, content, raw, error(optional)
    """
    query = (query or "").strip()
    if not query:
        return {
            "query": "",
            "content": "",
            "raw": None,
            "error": "query is empty",
        }
    result: dict[str, Any] = {
        "query": query,
        "content": "",
        "raw": None,
    }
    try:
        raw = await asyncio.to_thread(_http_call_search_news, query)
    except Exception as exc:
        result["error"] = str(exc)
        return result

    result["raw"] = raw
    content = _extract_content(raw)
    result["content"] = content

    return result


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query financial news/reports by natural language."
    )
    parser.add_argument("query", nargs="*", help="Natural language query text.")
    return parser


def run_cli() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query:
        query = (sys.stdin.read() or "").strip()

    if not query:
        parser.print_help()
        raise SystemExit(1)

    async def _main() -> None:
        result = await query_financial_news(query=query)
        if "error" in result:
            print(f"Error: {result['error']}")
            raise SystemExit(2)
        print(result.get("content", ""))

    asyncio.run(_main())


if __name__ == "__main__":
    run_cli()
