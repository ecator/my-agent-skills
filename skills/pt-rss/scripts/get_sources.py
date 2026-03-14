# /// script
# dependencies = [
#   "requests",
#   "feedparser",
#   "markdownify",
#   "python-dotenv"
# ]
# ///


import requests
import sys
import feedparser
import json
import re
from markdownify import markdownify as md
import warnings
from bs4 import MarkupResemblesLocatorWarning
from dotenv import load_dotenv
import os

load_dotenv(override=True)


# Suppress warnings from BeautifulSoup when input looks like a URL
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# 从环境变量获取RSS订阅源
# 过滤前缀
prefix = "PTRSS_"
env_vars = {k: v for k, v in os.environ.items() if k.startswith(prefix)}
urls = []
for k, v in env_vars.items():
    urls.append(v)
if len(urls) == 0:
    print(
        "Error: No RSS sources found, please set PTRSS_* environment variables to urls."
    )
    sys.exit(1)


def remove_html_entities(text):
    text = re.sub("&amp;", "&", text)
    text = re.sub("&lt;", "<", text)
    text = re.sub("&gt;", ">", text)
    text = re.sub("&quot;", '"', text)
    text = re.sub("&apos;", "'", text)
    text = re.sub("&nbsp;", " ", text)
    text = re.sub(" +", " ", text)
    return text


def main():
    # Force stdout to use utf-8 to avoid GBK encoding errors on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    items = []
    for url in urls:
        try:
            # Fetch the URL
            feed = feedparser.parse(url)

            for entry in feed.entries:
                items.append(
                    {
                        "title": remove_html_entities(entry.title),
                        "link": entry.link,
                        "summary": md(remove_html_entities(entry.summary)),
                    }
                )
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)

    print(json.dumps(items, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
