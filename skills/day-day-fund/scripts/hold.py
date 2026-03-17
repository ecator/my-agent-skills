# /// script
# dependencies = [
#   "playwright",
#   "python-dotenv"
# ]
# ///


from playwright.sync_api import Playwright, sync_playwright
import json

import os
import sys
from dotenv import load_dotenv

load_dotenv(override=True)

DAY_DAY_FUND_USERNAME = os.getenv("DAY_DAY_FUND_USERNAME")
if not DAY_DAY_FUND_USERNAME:
    raise ValueError("DAY_DAY_FUND_USERNAME environment variable is not set")
DAY_DAY_FUND_PASSWORD = os.getenv("DAY_DAY_FUND_PASSWORD")
if not DAY_DAY_FUND_PASSWORD:
    raise ValueError("DAY_DAY_FUND_PASSWORD environment variable is not set")


# Force stdin/stdout to use utf-8 to avoid garbled code errors on Windows
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def escape_markdown(text: str) -> str:
    """
    转义markdown中的特殊字符
    """
    text = text.replace("\\", "\\\\")
    text = text.replace("|", "\\|")
    return text


def hold2md(data: dict) -> str:
    """
    将持仓数据转换为markdown格式
    """
    asset_total = data["assetTotal"]
    asset_list = data["assetList"]
    md = "# 基金产品"
    md += f"\n- 总额（元）：{asset_total[0]['strValue']}"
    md += f"\n- 持仓收益（元）：{asset_total[1]['strValue']}"
    md += f"\n- 累计收益（元）：{asset_total[2]['strValue']}"
    md += "\n\n"
    md += "## 持仓明细"
    if asset_list and len(asset_list) > 0:
        md += "\n产品代码|产品名称|产品类型|最新净值|净值日期|金额（元）|持仓收益（元）|持仓收益（%）"
        md += "\n---|---|---|---|---|---|---|---"
        for asset in asset_list:
            md += f"\n{asset['fundCode']}|{escape_markdown(asset['fundName'])}|{asset['fundTypeName']}|{asset['nav']}|{asset['navdate']}|{asset['assetValue']}|{asset['profitValue']}|{asset['profitPercent']}"
    else:
        md += "\n还没有购买任何基金"
    return md


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://login.1234567.com.cn/login")
    page.locator("#tbname").click()
    page.locator("#tbname").fill(DAY_DAY_FUND_USERNAME)
    page.locator("#tbpwd").click()
    page.locator("#tbpwd").fill(DAY_DAY_FUND_PASSWORD)
    page.locator("#protocolCheckbox").check()
    page.locator("#btn_login").click()
    page.wait_for_load_state("networkidle")

    hold_data = page.evaluate("""
        async () => {
            const response = await fetch("/request/hold", {
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5",
                    "type": "0",
                    "sort": "5",
                    "X-Requested-With": "XMLHttpRequest"
                },
                "referrer": "https://trade.1234567.com.cn/myAssets/hold",
                "method": "POST"
            })
            const json = await response.json();
            return json.result;
        }
    """)
    # print(json.dumps(hold_data, ensure_ascii=False, indent=2))
    print(hold2md(hold_data))

    page.locator(".logout").first.click()
    page.wait_for_load_state("networkidle")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
