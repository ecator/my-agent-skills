# /// script
# dependencies = [
#   "playwright",
#   "python-dotenv"
# ]
# ///

import json
import re
from playwright.sync_api import Playwright, sync_playwright, Page, BrowserContext
from datetime import datetime, timedelta
import platform
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
    text = text.replace("\r\n", "<br>")
    text = text.replace("\n", "<br>")
    text = text.replace("|", "\\|")
    return text


def dict_get(d: dict, key: str, default: str = "") -> str:
    """提取字典值，如果取到None则返回默认字符串"""
    val = d.get(key, default)
    return default if val is None else str(val)


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
            md += f"\n{dict_get(asset, 'fundCode')}|{escape_markdown(dict_get(asset, 'fundName'))}|{dict_get(asset, 'fundTypeName')}|{dict_get(asset, 'nav')}|{dict_get(asset, 'navdate')}|{dict_get(asset, 'assetValue')}|{dict_get(asset, 'profitValue')}|{dict_get(asset, 'profitPercent')}"
    else:
        md += "\n还没有购买任何基金"
    return md


def get_hold_data(page: Page) -> dict:
    """获取持仓信息"""
    page.goto("https://trade.1234567.com.cn/myAssets/hold")
    data = page.evaluate("""
        async () => {
            const response = await fetch("https://trade.1234567.com.cn/request/hold", {
                "method": "POST",
                "headers": {
                    "sort": "5",
                    "type": "0"
                }
            })
            const json = await response.json();
            return json.result;
        }
    """)
    # print(json.dumps(data, ensure_ascii=False, indent=2))
    return data


def delegate2md(data: dict) -> str:
    """
    将交易数据转换为markdown格式
    """
    total_count = data["totalCount"]
    delegate_list = data["list"]
    md = "# 基金交易记录"
    md += "\n- 查询周期：近3个月"
    md += f"\n- 交易次数：{total_count}"
    md += "\n\n"
    md += "## 交易明细"
    if delegate_list and len(delegate_list) > 0:
        md += "\n交易发起时间|产品名称|业务类型|申请数额|确认数额|状态"
        md += "\n---|---|---|---|---|---"
        for delegate in delegate_list:
            md += f"\n{dict_get(delegate, 'strikeStartDate')}|{escape_markdown(dict_get(delegate, 'productName'))}({dict_get(delegate, 'productCode')})|{dict_get(delegate, 'businessTypeText1')}|{dict_get(delegate, 'applyCount')}{dict_get(delegate, 'applyCountUnit')}|{dict_get(delegate, 'confirmCount')}{dict_get(delegate, 'confirmCountUnit')}|{dict_get(delegate, 'appStateText')}"
    else:
        md += "\n没有查询到任何交易记录"
    return md


def get_delegate_data(page: Page, context: BrowserContext):
    page.goto("https://query.1234567.com.cn")
    fund_trade_token = ""
    for cookie in context.cookies():
        # print(cookie)
        if cookie["name"] == "fund_trade_token":
            fund_trade_token = cookie["value"]
            break
    if fund_trade_token == "":
        raise ValueError("fund_trade_token is not set")
    now = datetime.now()
    end_date_str = now.strftime("%Y-%m-%d 00:00:00")
    start_date = now - timedelta(days=90)
    start_date_str = start_date.strftime("%Y-%m-%d 00:00:00")

    def get_data(
        fund_trade_token: str,
        start_date_str: str,
        end_date_str: str,
        page_num: int,
        page_size: int,
    ) -> dict:
        data = page.evaluate(
            """
            async ([fund_trade_token,start_date_str,end_date_str,page_num,page_size]) => {
                const response = await fetch("https://query.1234567.com.cn/queryapi/trading/Query/DelegateList", {
                    "method": "POST",
                    "headers": {
                        "type": "0",
                        "sort": "5",
                        "ACCESS-TOKEN": fund_trade_token,
                        "Content-Type": "application/json"
                    },
                    "body": JSON.stringify({
                        "dataType": 1,
                        "startDate": start_date_str,
                        "endDate": end_date_str,
                        "timeType": "1",
                        "busType": "0",
                        "status": "0",
                        "account": "",
                        "fundType": "0",
                        "pageSize": page_size,
                        "pageNum": page_num,
                        "container": "tb_delegate",
                        "fundCode": "",
                        "isHistory": false,
                    }),
                })
                const json = await response.json();
                return json.data;
            }
        """,
            [fund_trade_token, start_date_str, end_date_str, page_num, page_size],
        )
        return data

    data_list = []
    data = {"totalCount": 0, "list": []}
    page_num = 1
    page_size = 20
    while True:
        data = get_data(
            fund_trade_token, start_date_str, end_date_str, page_num, page_size
        )
        # print(json.dumps(data, ensure_ascii=False, indent=2))
        data_list.extend(data["list"])
        page_num += 1
        if data["totalCount"] == len(data_list):
            break
    data["list"] = data_list
    return data


def get_yingkui_table_md(page: Page, fund_code: str) -> str:
    """
    获取基金盈亏数据
    """
    url = f"https://trade.1234567.com.cn/myassets/single?iv=false&fc={fund_code}"
    page.goto(url)
    page.wait_for_load_state("networkidle")
    page.locator("li[data-prop=yingkui]").click()
    page.wait_for_load_state("networkidle")
    table = page.locator("table.yingkui").inner_html()
    # print(table)
    tr_matches = re.findall(
        r"<tr><td>(\d{4}-\d{2}-\d{2})</td><td>(\S+)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td></tr>",
        table,
    )
    md = "日期|单位净值|日涨跌幅|当日持仓份额(份)|日盈亏"
    md += "\n---|---|---|---|---"
    if tr_matches is not None and len(tr_matches) > 0:
        for match in tr_matches:
            md += f"\n{match[0]} | {match[1]} | {match[2]} | {match[3]} | {match[4]}"
    else:
        md = "没有查询到任何盈亏数据"
    return md


def get_yingkui_tables_md(page: Page, hold_data: dict) -> str:
    """
    获取所有基金盈亏数据表格
    """
    md = "# 基金每日盈亏"
    asset_list = hold_data["assetList"]
    if asset_list and len(asset_list) > 0:
        for asset in asset_list:
            fund_code = dict_get(asset, "fundCode")
            fund_name = escape_markdown(dict_get(asset, "fundName"))
            md += f"\n\n## {fund_name}({fund_code})"
            md += f"\n{get_yingkui_table_md(page, fund_code)}"
    else:
        md += "\n还没有购买任何基金"
    return md


def run(playwright: Playwright) -> None:
    # 启动浏览器
    browser = playwright.chromium.launch(
        headless=(platform.system().lower() == "linux")
    )
    context = browser.new_context()
    page = context.new_page()
    # 登录
    page.goto("https://login.1234567.com.cn/login")
    page.locator("#tbname").click()
    page.locator("#tbname").fill(DAY_DAY_FUND_USERNAME)
    page.locator("#tbpwd").click()
    page.locator("#tbpwd").fill(DAY_DAY_FUND_PASSWORD)
    page.locator("#protocolCheckbox").check()
    page.locator("#btn_login").click()
    page.wait_for_load_state("networkidle")

    # 获取持仓数据
    hold_data = get_hold_data(page)
    print(hold2md(hold_data))

    print("\n")

    # 获取交易数据
    print(delegate2md(get_delegate_data(page, context)))

    print("\n")

    # 获取每个基金的盈亏数据
    print(get_yingkui_tables_md(page, hold_data))
    # 登出
    page.goto("https://trade.1234567.com.cn/MyAssets/Default")
    page.locator(".logout").first.click()
    page.wait_for_load_state("networkidle")

    # 关闭浏览器
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
