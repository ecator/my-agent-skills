# /// script
# dependencies = [
#   "requests",
#   "python-dotenv"
# ]
# ///


import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("EASTMONEY_APIKEY")
if not api_key:
    print("错误: 请先设置EASTMONEY_APIKEY环境变量")
    print("你可以在东方财富Skills页面获取apikey")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("请传入你需要<查询的内容>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    url = "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search"
    headers = {"Content-Type": "application/json", "apikey": api_key}
    data = {"query": query}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # 转换为 Markdown 格式
        if result.get("success") and "data" in result:
            inner_data = result["data"].get("data", {})
            search_response = inner_data.get("llmSearchResponse", {})
            news_list = search_response.get("data", [])

            if not news_list:
                print(f"未找到关于 '{query}' 的相关新闻。")
                return

            print(f"# 新闻搜索结果: {query}\n")
            for item in news_list:
                title = item.get("title", "无标题")
                
                # 智能识别来源
                source = item.get("source") or item.get("insName")
                if not source:
                    info_type = item.get("informationType", "")
                    if info_type == "NOTICE":
                        source = "上市公司公告"
                    elif info_type == "REPORT":
                        source = "研究报告"
                    else:
                        source = "未知来源"
                
                date = item.get("date", "未知日期")
                content = item.get("content", "").replace("\n", " ").strip()
                url_link = item.get("jumpUrl", "")

                if url_link:
                    print(f"## [{title}]({url_link})")
                else:
                    print(f"## {title}")
                
                print(f"**来源:** {source} | **日期:** {date}")
                print(f"\n{content}\n")
                print("---")
        else:
            print(f"查询失败: {result.get('message', '未知错误')}")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
