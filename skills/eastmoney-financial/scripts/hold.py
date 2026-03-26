# /// script
# dependencies = [
#   "playwright",
#   "python-dotenv"
# ]
# ///


import re
from playwright.sync_api import Playwright, sync_playwright
from dotenv import load_dotenv
import os

load_dotenv(override=True)

EASTMONEY_USERNAME = os.getenv("EASTMONEY_USERNAME")
if not EASTMONEY_USERNAME:
    raise ValueError("EASTMONEY_USERNAME environment variable is not set")
EASTMONEY_PASSWORD = os.getenv("EASTMONEY_PASSWORD")
if not EASTMONEY_PASSWORD:
    raise ValueError("EASTMONEY_PASSWORD environment variable is not set")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.eastmoney.com/")
    page.locator("#topnavi_login_link").click()
    page.locator("#frame_login").content_frame.get_by_text("账号登录").click()
    page.locator("#frame_login").content_frame.get_by_role(
        "textbox", name="邮箱/手机"
    ).click()
    page.locator("#frame_login").content_frame.get_by_role(
        "textbox", name="邮箱/手机"
    ).fill(EASTMONEY_USERNAME)
    page.locator("#frame_login").content_frame.get_by_role(
        "textbox", name="请输入登录密码"
    ).click()
    page.locator("#frame_login").content_frame.get_by_role(
        "textbox", name="请输入登录密码"
    ).fill(EASTMONEY_PASSWORD)
    page.locator("#frame_login").content_frame.locator(".selectbox").first.click()
    page.locator("#frame_login").content_frame.get_by_role(
        "button", name="登录"
    ).click()
    page.locator("#frame_login").content_frame.locator("div").filter(
        has_text=re.compile(r"^点击开始验证$")
    ).first.click()
    # TODO 具体实现取出股票持仓等信息
    input()
    page.locator("#topnavi_unick").hover()
    page.locator("#hlogoutlink").click()
    page.wait_for_load_state("domcontentloaded")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
