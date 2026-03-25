# /// script
# dependencies = [
#   "requests",
#   "beautifulsoup4"
# ]
# ///


import requests
from bs4 import BeautifulSoup
import argparse


def escape_markdown(text: str) -> str:
    """
    转义markdown中的特殊字符
    """
    text = text.replace("\\", "\\\\")
    text = text.replace("\r\n", "<br>")
    text = text.replace("\n", "<br>")
    text = text.replace("|", "\\|")
    return text


def get_ip_location(ip):
    url = f"https://www.ipshudi.com/{ip}.htm"
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0"
            },
            timeout=10,
        )
        html_text = response.text
        soup = BeautifulSoup(html_text, "html.parser")
        location_node = soup.select_one(
            "table > tbody > tr:nth-child(2) > td:nth-child(2) > span:nth-child(1)"
        )
        location = ""
        if location_node is not None:
            location = location_node.get_text()
        provider_node = soup.select_one(
            "table > tbody > tr:nth-child(3) > td:nth-child(2) > span:nth-child(1)"
        )
        provider = ""
        if provider_node is not None:
            provider = provider_node.get_text()
        return {
            "status": "success",
            "ip": ip,
            "location": location,
            "provider": provider,
        }

    except Exception as e:
        return {"status": "error", "ip": ip, "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="IP属地查询")
    parser.add_argument("ip", nargs="+", help="IP地址（可指定多个）")
    args = parser.parse_args()

    ip_list = args.ip
    print("ip|location|provider")
    print("---|---|---")
    for ip in ip_list:
        ip_location = get_ip_location(ip)
        if ip_location.get("status") == "success":
            print(
                f"{ip}|{escape_markdown(ip_location.get('location', ''))}|{escape_markdown(ip_location.get('provider', ''))}"
            )
        else:
            print(f"{ip}|{escape_markdown(ip_location.get('message', ''))}|")


if __name__ == "__main__":
    main()
