# /// script
# dependencies = [
#   "requests",
#   "python-dotenv"
# ]
# ///


import os
import sys
import requests
from dotenv import load_dotenv
import argparse

load_dotenv(override=True)
api_key = os.getenv("EASTMONEY_APIKEY")
if not api_key:
    print("错误: 请先设置EASTMONEY_APIKEY环境变量")
    print("你可以在东方财富Skills页面获取apikey")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="妙想智能选股")
    parser.add_argument("-k", "--keyword", required=True, help="需要查询的关键字")
    parser.add_argument("-p", "--page-no", type=int, default=1, help="页码")
    parser.add_argument("-s", "--page-size", type=int, default=20, help="每页数量")
    args = parser.parse_args()

    url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen"
    headers = {"Content-Type": "application/json", "apikey": api_key}
    data = {"keyword": args.keyword, "pageNo": args.page_no, "pageSize": args.page_size}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # 检查是否有数据返回
        if not result.get("data"):
            print("查询结果为空，建议到东方财富妙想AI查询更详细的信息。")
            sys.exit(0)

        # 格式化输出友好的 Markdown 表格
        data_node = result.get("data", {})
        # JSON 结构嵌套了两次 data
        inner_data = (
            data_node.get("data", {})
            if isinstance(data_node, dict) and "data" in data_node
            else data_node
        )

        all_results_data = inner_data.get("allResults", {}).get("result", {})
        columns = all_results_data.get("columns", [])
        data_list = all_results_data.get("dataList", [])

        if not columns or not data_list:
            print("没有查到相关的表格数据。")
            sys.exit(0)

        # 过滤掉 hide 为 True 的列，只保留核心数据，使表格更精简友好
        display_columns = [col for col in columns if not col.get("hide")]

        headers = []
        for col in display_columns:
            headers.append(col.get("title", ""))

        print("| " + " | ".join(headers) + " |")
        print("|" + "|".join(["---"] * len(headers)) + "|")

        for row in data_list:
            row_data = [str(row.get(col.get("key"), "")) for col in display_columns]
            print("| " + " | ".join(row_data) + " |")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
