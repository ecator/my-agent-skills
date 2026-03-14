# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv"
# ]
# ///

import argparse
import asyncio
import json
import os
import re
import sys
import uuid
from typing import Any
import httpx
from dotenv import load_dotenv

load_dotenv(override=True)

EM_API_KEY = os.getenv("EM_API_KEY")

if not EM_API_KEY:
    raise RuntimeError("Please set the EM_API_KEY environment variable first")


DEFAULT_SEARCH_API_URL = "https://ai-saas.eastmoney.com/proxy/b/mcp/tool/searchData"

# Force stdin/stdout to use utf-8 to avoid garbled code errors on Windows
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _flatten_value(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _ordered_keys(table: dict[str, Any], indicator_order: list[Any]) -> list[Any]:
    data_keys = [k for k in table.keys() if k != "headName"]
    key_map = {str(k): k for k in data_keys}
    preferred: list[Any] = []
    seen: set[str] = set()
    for key in indicator_order:
        key_str = str(key)
        if key_str in key_map and key_str not in seen:
            preferred.append(key_map[key_str])
            seen.add(key_str)
    for key in data_keys:
        key_str = str(key)
        if key_str not in seen:
            preferred.append(key)
            seen.add(key_str)
    return preferred


def _normalize_values(raw_values: list[Any], expected_len: int) -> list[str]:
    values = [_flatten_value(v) for v in raw_values]
    if len(values) < expected_len:
        values.extend([""] * (expected_len - len(values)))
    return values[:expected_len]


def _return_code_map(block: dict[str, Any]) -> dict[str, str]:
    for key in ("returnCodeMap", "returnCodeNameMap", "codeMap"):
        data = block.get(key)
        if isinstance(data, dict):
            return {str(k): _flatten_value(v) for k, v in data.items()}
    return {}


def _format_indicator_label(
    key: str, name_map: dict[str, Any], code_map: dict[str, str]
) -> str:
    mapped = name_map.get(key)
    if mapped is None and key.isdigit():
        mapped = name_map.get(int(key))
    if mapped not in (None, ""):
        return _flatten_value(mapped)
    mapped_code = code_map.get(key)
    if mapped_code not in (None, ""):
        return _flatten_value(mapped_code)
    if key.isdigit():
        return ""
    return key


def _table_to_rows_generic(
    table: Any, name_map: dict[str, str] | None
) -> list[dict[str, Any]]:
    name_map = name_map or {}
    if isinstance(table, list):
        if not table:
            return []
        if isinstance(table[0], dict):
            rows = table
        else:
            rows = [
                dict(zip([f"column_{i}" for i in range(len(table[0]))], row))
                for row in table
            ]
    elif isinstance(table, dict):
        vals = [v for v in table.values() if isinstance(v, list)]
        if vals and all(isinstance(v, list) for v in table.values()):
            n = len(vals[0])
            if all(len(v) == n for v in vals):
                cols = list(table.keys())
                rows = [
                    dict(zip(cols, [v[i] for v in table.values()])) for i in range(n)
                ]
            else:
                rows = []
        else:
            cols = table.get("columns") or table.get("fields") or []
            rows_data = table.get("rows") or table.get("data") or []
            if not cols and rows_data:
                cols = [f"column_{i}" for i in range(len(rows_data[0]))]
            rows = [dict(zip(cols, r)) for r in rows_data]
    else:
        return []

    return [
        {name_map.get(k, k): _flatten_value(v) for k, v in row.items()} for row in rows
    ]


def _table_to_rows(block: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    table = block.get("table") or {}
    name_map = block.get("nameMap") or {}
    if isinstance(name_map, list):
        name_map = {str(i): v for i, v in enumerate(name_map)}
    elif not isinstance(name_map, dict):
        name_map = {}

    if not isinstance(table, dict):
        rows = _table_to_rows_generic(table, name_map)
        fieldnames = list(rows[0].keys()) if rows else []
        return rows, fieldnames

    headers = table.get("headName") or []
    if not isinstance(headers, list):
        headers = []
    order = _ordered_keys(table, block.get("indicatorOrder") or [])
    entity_name = _flatten_value(block.get("entityName") or "") or "Indicator"
    code_map = _return_code_map(block)

    rows: list[dict[str, Any]] = []
    data_key_count = len([key for key in table.keys() if key != "headName"])

    if len(headers) > 1 and data_key_count >= 1:
        fieldnames = [entity_name] + [_flatten_value(h) for h in headers]
        for key in order:
            raw_values = table.get(key, [])
            if not isinstance(raw_values, list):
                raw_values = [raw_values]
            values = _normalize_values(raw_values, len(headers))
            label = _format_indicator_label(str(key), name_map, code_map)
            rows.append(dict(zip(fieldnames, [label] + values)))
        return rows, fieldnames

    if len(headers) == 1 and data_key_count >= 1:
        fieldnames = [entity_name, _flatten_value(headers[0])]
        for key in order:
            raw_values = table.get(key, [])
            value = (
                raw_values[0]
                if isinstance(raw_values, list) and raw_values
                else raw_values
            )
            label = _format_indicator_label(str(key), name_map, code_map)
            rows.append({fieldnames[0]: label, fieldnames[1]: _flatten_value(value)})
        return rows, fieldnames

    fallback_rows = _table_to_rows_generic(table, name_map)
    if fallback_rows:
        return fallback_rows, list(fallback_rows[0].keys())
    return [], []


def _build_request_body(query: str) -> dict[str, Any]:
    call_id = str(uuid.uuid4())
    return {
        "query": query,
        "toolContext": {
            "callId": call_id,
            "userInfo": {
                "userId": EM_API_KEY,
            },
        },
    }


def _safe_sheet_name(raw_name: Any, used_names: set[str]) -> str:
    name = _flatten_value(raw_name).strip() or "Table"
    name = re.sub(r"[:\\/?*\[\]]", "_", name)
    if len(name) > 31:
        name = name[:31]

    base = name or "Table"
    candidate = base
    idx = 2
    while candidate in used_names:
        suffix = f"_{idx}"
        if len(base) + len(suffix) > 31:
            candidate = base[: 31 - len(suffix)] + suffix
        else:
            candidate = base + suffix
        idx += 1
    used_names.add(candidate)
    return candidate


def _extract_data_table_dto_list(
    api_result: Any,
) -> tuple[list[Any] | None, str | None]:
    """
    从接口返回中提取 dataTableDTOList。
    兼容新结构：
      data.searchDataResultDTO.dataTableDTOList
    同时兼容旧结构：
      dataTableDTOList 或 data.dataTableDTOList
    """
    if not isinstance(api_result, dict):
        return None, "API response is not a JSON object"

    dto_list = api_result.get("dataTableDTOList")
    if isinstance(dto_list, list):
        return dto_list, None

    data_node = api_result.get("data")
    if isinstance(data_node, dict):
        search_result = data_node.get("searchDataResultDTO")
        if isinstance(search_result, dict):
            dto_list = search_result.get("dataTableDTOList")
            if isinstance(dto_list, list):
                return dto_list, None

        dto_list = data_node.get("dataTableDTOList")
        if isinstance(dto_list, list):
            return dto_list, None

    return None, "API response missing data.searchDataResultDTO.dataTableDTOList"


def _check_business_status(api_result: Any) -> str | None:
    """
    校验新接口业务状态字段：
    - code == 0
    - status == 0
    若字段缺失则不拦截，保持兼容。
    """
    if not isinstance(api_result, dict):
        return "API response is not a JSON object"

    code = api_result.get("code")
    status = api_result.get("status")
    if code not in (None, 200) or status not in (None, 200):
        message = _flatten_value(api_result.get("message") or "Business status unsuccessful")
        return f"API business error: code={code}, status={status}, message={message}"
    return None


def _parse_data_table_response(
    api_result: Any,
) -> tuple[list[dict[str, Any]], list[str], int, str | None]:
    dto_list, extract_err = _extract_data_table_dto_list(api_result)
    if extract_err:
        return [], [], 0, extract_err
    if not dto_list:
        return [], [], 0, "API response dataTableDTOList is empty"

    condition_parts: list[str] = []
    tables: list[dict[str, Any]] = []
    total_rows = 0
    used_sheet_names: set[str] = set()

    for i, dto in enumerate(dto_list):
        if not isinstance(dto, dict):
            continue

        sheet_name = _safe_sheet_name(
            dto.get("title")
            or dto.get("inputTitle")
            or dto.get("entityName")
            or f"Table {i + 1}",
            used_sheet_names,
        )
        condition = dto.get("condition")
        if condition is not None and condition != "":
            entity = dto.get("entityName") or sheet_name
            condition_parts.append(f"[{entity}]\n{condition}")

        rows, fieldnames = _table_to_rows(dto)
        if not rows:
            continue
        tables.append({"title": sheet_name, "rows": rows, "fieldnames": fieldnames})
        total_rows += len(rows)

    if not tables:
        return [], condition_parts, 0, "No valid table data in dataTableDTOList"
    return tables, condition_parts, total_rows, None


async def query_financial_data(
    query: str,
    api_base: str | None = None,
) -> dict[str, Any]:
    url = api_base or DEFAULT_SEARCH_API_URL
    result = {}
    try:
        body = _build_request_body(query)
        api_key = EM_API_KEY
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url,
                json=body,
                headers={
                    "Content-Type": "application/json",
                    "em_api_key": api_key,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as exc:
        return {
            "error": f"HTTP error: {exc.response.status_code} - {exc.response.text[:200]}"
        }
    except Exception as exc:
        return {"error": f"Request failed: {exc!s}"}

    status_err = _check_business_status(data)
    if status_err:
        return {"error": status_err}

    tables, condition_parts, total_rows, err = _parse_data_table_response(data)
    if err:
        result["error"] = err
        result["raw_preview"] = json.dumps(data, ensure_ascii=False)[:500]
        return result

    result["data"] = tables
    return result


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Direct query of financial data")
    # 添加位置参数
    parser.add_argument(
        "query",
        type=str,
        nargs="*",
        help="Natural language query, e.g., 'How is Kweichow Moutai performing recently'",
    )

    args = parser.parse_args()
    query = " ".join(args.query).strip()
    if not query:
        query = (sys.stdin.read() or "").strip()

    if not query:
        parser.print_help()
        raise SystemExit(1)

    async def _main() -> None:
        try:
            result = await query_financial_data(query=query)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        if "error" in result:
            sys.exit(2)

    asyncio.run(_main())


if __name__ == "__main__":
    run_cli()
