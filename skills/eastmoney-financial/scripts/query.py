# /// script
# dependencies = [
#   "requests",
#   "python-dotenv"
# ]
# ///


import os
import sys
import json
import argparse
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("EASTMONEY_APIKEY")
if not api_key:
    print("错误: 请先设置EASTMONEY_APIKEY环境变量")
    print("你可以在东方财富Skills页面获取apikey")
    sys.exit(1)


def format_as_markdown(result):
    if not result or not result.get("success"):
        return "查询失败或返回结果为空。"

    try:
        data_wrapper = result.get("data", {}).get("data", {})
        if not data_wrapper:
            return "未找到相关数据。"

        search_result = data_wrapper.get("searchDataResultDTO", {})
        table_list = search_result.get("dataTableDTOList", [])

        if not table_list:
            # 如果没有结构化表格，尝试返回一些描述性文字
            message = data_wrapper.get("message")
            if message:
                # 转义消息中的换行，使其更适合在某些环境下显示
                return message.replace("\n", "\\n")
            return "未找到结构化数据表格。"

        markdown_outputs = []

        for item in table_list:
            title = item.get("title") or item.get("inputTitle") or "数据表格"
            title = title.replace("\n", " ")  # 标题中的换行转为空格
            table_data = item.get("table", {})
            name_map = item.get("nameMap", {})
            indicator_order = item.get("indicatorOrder", [])

            if not table_data:
                continue

            # 确定表头
            headers = []
            # headName 通常是第一列（时间/名称等）
            if "headName" in table_data:
                headers.append("headName")
            
            # 添加其他列，优先按 indicator_order
            for key in indicator_order:
                if key in table_data and key not in headers:
                    headers.append(key)
            
            # 添加剩下的在 table_data 中但不在 headers 中的列
            for key in table_data.keys():
                if key not in headers and key != "headName":
                    headers.append(key)

            # 转换为友好名称并转义
            display_headers = []
            for h in headers:
                name = name_map.get(h)
                if not name:
                    if h == "headName":
                        name = name_map.get("headNameSub") or "日期/名称"
                        if name == "数据来源":
                             name = "时间/名称"
                    else:
                        name = h
                display_headers.append(str(name).replace("\n", " ").replace("|", "\\|"))
            
            # 准备行数据
            rows = []
            # 获取数据长度
            max_len = 0
            for h in headers:
                max_len = max(max_len, len(table_data[h]))
            
            for i in range(max_len):
                row = []
                for h in headers:
                    val_list = table_data[h]
                    if i < len(val_list):
                        # 替换换行符为 <br> 以保持 Markdown 表格结构，并转义 |
                        val = str(val_list[i]).replace("\n", "<br>").replace("|", "\\|")
                        row.append(val)
                    else:
                        row.append("-")
                rows.append(row)

            # 构建 Markdown 表格
            if rows:
                md = f"### {title}\n\n"
                md += "| " + " | ".join(display_headers) + " |\n"
                md += "| " + " | ".join(["---"] * len(display_headers)) + " |\n"
                for row in rows:
                    md += "| " + " | ".join(row) + " |\n"
                markdown_outputs.append(md)

        if not markdown_outputs:
            return "未找到有效数据进行表格展示。"

        return "\n\n".join(markdown_outputs)

    except Exception as e:
        return f"解析数据时出错: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="东方财富数据查询")
    parser.add_argument("query", nargs="+", help="需要查询的内容")
    args = parser.parse_args()

    query = " ".join(args.query)

    url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/query"
    headers = {"Content-Type": "application/json", "apikey": api_key}
    data = {"toolQuery": query}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        with open("debug_output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 格式化为 Markdown 输出
        print(format_as_markdown(result))

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
