# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv"
# ]
# ///


import asyncio
import json
import re
import uuid
from typing import Any, Dict, List, Tuple
import httpx
import os
import argparse
import sys

from dotenv import load_dotenv

load_dotenv(override=True)

EM_API_KEY = os.getenv("EM_API_KEY")

if not EM_API_KEY:
    raise RuntimeError("Please set the EM_API_KEY environment variable first")

# MCP 服务器地址
DEFAULT_URL = "https://ai-saas.eastmoney.com"
DEFAULT_PAHT = "/proxy/b/mcp/tool/searchMacroData"

# Force stdin/stdout to use utf-8 to avoid garbled code errors on Windows
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _safe_filename(s: str, max_len: int = 80) -> str:
    """将查询文本转为安全文件名片段。"""
    s = re.sub(r'[<>:"/\\|?*]', "_", s)
    s = s.strip().replace(" ", "_")[:max_len]
    return s or "query"


def _flatten_value(v: Any) -> str:
    """将单元格值转为字符串（嵌套结构转为 JSON 字符串）。"""
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _extract_frequency(entity_name: str) -> str:
    """
    从entityName中提取频率信息。
    例如："GDP（年）" -> "年", "宏观数据（周）" -> "周"
    """
    match = re.search(r"[（(]([^）)]+)[）)]", entity_name)
    if match:
        return match.group(1)
    return "unknown"


def _parse_macro_table(data_item: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], str]:
    """
    解析宏观数据的table格式。

    根据实际返回数据格式：
    {
        "table": {
            "EMM00000015": ["140.2万亿", "134.8万亿", ...],
            "headName": ["数据来源", "2025", "2024", ...]
        },
        "nameMap": {
            "EMM00000015": "中国:GDP:现价(元)",
            "headNameSub": "数据来源"
        },
        "entityName": "GDP（年）"
    }

    Returns:
        (rows, frequency) - 解析出的数据行和频率
    """
    rows = []

    table = data_item.get("table", {})
    name_map = data_item.get("nameMap", {})
    entity_name = data_item.get("entityName", "")
    description = data_item.get("description", "")

    # 提取频率
    frequency = _extract_frequency(entity_name)

    if not table or not isinstance(table, dict):
        return rows, frequency

    # 获取列名（headName）
    headers = table.get("headName", [])
    if not headers:
        # 尝试其他可能的列名键
        headers = table.get("date", [])
        if not headers:
            return rows, frequency

    # 找出所有的指标键（排除headName、date等元数据键）
    exclude_keys = {"headName", "headNameSub", "date"}
    metric_keys = [k for k in table.keys() if k not in exclude_keys]

    if not metric_keys:
        return rows, frequency

    # 对于每个指标键，创建一行数据
    for metric_key in metric_keys:
        values = table.get(metric_key, [])
        if not values:
            continue

        # 获取指标名称（从nameMap或使用键名）
        metric_name = name_map.get(metric_key, metric_key)

        # 创建一行数据
        row = {
            "entity_name": entity_name,
            "entity_description": description,
            "indicator_code": metric_key,
            "indicator_name": metric_name,
            "frequency": frequency,  # 添加频率字段
        }

        # 将每个年份/字段的值添加到行中
        for i, header in enumerate(headers):
            if i < len(values):
                value = values[i]
                # 如果值是列表，可能需要特殊处理
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value) if value else ""
                row[header] = value

        rows.append(row)

    return rows, frequency


def _build_headers() -> dict[str, str]:
    """构建请求头（与新的curl命令中的headers一致）。"""
    headers = {
        "em_api_key": EM_API_KEY,
        "Content-Type": "application/json",
    }
    return headers


def _build_request_body(query: str) -> dict[str, Any]:
    """构建 POST 请求体（与新的searchMacroData接口一致）。"""
    call_id = f"call_{uuid.uuid4().hex[:8]}"
    user_id = f"user_{uuid.uuid4().hex[:8]}"

    body = {
        "query": query,
        "toolContext": {"callId": call_id, "userInfo": {"userId": user_id}},
    }
    return body


# async def query_macro_data(
async def query_macro_data(
    query: str,
    api_base: str | None = None,
) -> dict[str, Any]:
    """
    通过文本查询宏观数据。

    Args:
        query: 自然语言查询，如「中国GDP」

    Returns:
        包含数据的字典
    """

    result: dict[str, Any] = {
        "data": [],
        "query": query,
    }

    try:
        headers = _build_headers()
        body = _build_request_body(query)
        api_base = DEFAULT_URL.rstrip("/")
        url = f"{api_base}{DEFAULT_PAHT}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url,
                json=body,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json().get("data")

    except httpx.HTTPStatusError as e:
        result["error"] = (
            f"HTTP error: {e.response.status_code} - {e.response.text[:200]}"
        )
        return result
    except Exception as e:
        result["error"] = f"Request failed: {e!s}"
        return result

    # 解析返回的数据结构 - 按频率分组
    frequency_groups: Dict[str, List[Dict[str, Any]]] = {}
    description_parts = []

    # 检查可能的返回路径
    if isinstance(data, dict):
        # 情况1：直接包含result字段（文本结果）
        if "result" in data:
            description_parts.append(f"Text result: {data['result']}")

        # 情况2：包含dataList字段（主要数据结构）
        data_list = data.get("dataTables", [])
        if data_list and isinstance(data_list, list):
            for item_list in data_list:
                # 解析table数据，同时获取频率
                rows, frequency = _parse_macro_table(item_list)

                if rows:
                    if frequency not in frequency_groups:
                        frequency_groups[frequency] = []
                    frequency_groups[frequency].extend(rows)

                    # 收集描述信息
                    entity_name = item_list.get("entityName", "")
                    description = item_list.get("description", "")
                    title = item_list.get("title", "")

                    if entity_name:
                        description_parts.append(
                            f"Entity name [{frequency}]: {entity_name}"
                        )
                    if description:
                        description_parts.append(f"Description [{frequency}]: {description}")
                    if title:
                        description_parts.append(f"Title [{frequency}]: {title}")

                    # 添加字段信息
                    field_set = item_list.get("fieldSet", [])
                    if field_set and isinstance(field_set, list) and len(field_set) > 0:
                        field = field_set[0]
                        data_source = field.get("dataSource", "")
                        unit_name = field.get("unitName", "")
                        if data_source:
                            description_parts.append(
                                f"Data source [{frequency}]: {data_source}"
                            )
                        if unit_name:
                            description_parts.append(f"Unit [{frequency}]: {unit_name}")

        # 情况3：rawDataTables
        if not frequency_groups:
            raw_data_list = data.get("rawDataTables", [])
            if raw_data_list and isinstance(raw_data_list, list):
                for item_list in raw_data_list:
                    if not isinstance(item_list, list):
                        continue

                    for data_item in item_list:
                        if not isinstance(data_item, dict):
                            continue

                        rows, frequency = _parse_macro_table(data_item)
                        if rows:
                            if frequency not in frequency_groups:
                                frequency_groups[frequency] = []
                            frequency_groups[frequency].extend(rows)

    if not frequency_groups:
        result["error"] = "Unable to parse table data"
        result["raw_preview"] = json.dumps(data, ensure_ascii=False)[:500]
        return result

    result["data"] = frequency_groups
    return result


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Query macroeconomic data via natural language")

    # 添加位置参数
    parser.add_argument(
        "query",
        type=str,
        nargs="*",
        help="Natural language query, e.g., 'China GDP in recent 5 years'",
    )

    args = parser.parse_args()
    query = " ".join(args.query).strip()
    if not query:
        query = (sys.stdin.read() or "").strip()

    if not query:
        parser.print_help()
        raise SystemExit(1)

    async def _main() -> None:
        r = await query_macro_data(query)

        print(json.dumps(r, ensure_ascii=False, indent=2))

        if "error" in r:
            sys.exit(2)

    asyncio.run(_main())


if __name__ == "__main__":
    run_cli()
