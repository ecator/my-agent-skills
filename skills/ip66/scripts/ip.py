# /// script
# dependencies = [
#   "requests",
#   "maxminddb",
#   "pyyaml"
# ]
# ///


import os
import requests
import maxminddb
import argparse
import yaml


def main():
    parser = argparse.ArgumentParser(description="IP Geolocation Lookup")
    parser.add_argument("ip", nargs="+", help="IP address (one or more)")
    args = parser.parse_args()

    ip_list = args.ip

    # 拼接当前脚本文件夹下 ip66.mmdb 的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "ip66.mmdb")

    # 检查数据库文件是否存在或是否超过1天没有更新
    import time
    should_download = False
    if not os.path.exists(db_path):
        should_download = True
    else:
        mtime = os.path.getmtime(db_path)
        if time.time() - mtime > 86400:  # 1天 = 86400秒
            should_download = True

    if should_download:
        url = "https://downloads.ip66.dev/db/ip66.mmdb"
        print(f"Downloading database from {url}...")
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            temp_db_path = db_path + ".tmp"
            with open(temp_db_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            if os.path.exists(db_path):
                os.remove(db_path)
            os.rename(temp_db_path, db_path)
            print("Download completed successfully.")
        except Exception as e:
            print(f"Warning: Failed to download database ({e}).")
            if not os.path.exists(db_path):
                print("Error: Local database file not found and download failed. Cannot proceed.")
                return

    try:
        with maxminddb.open_database(db_path) as reader:
            for ip in ip_list:
                try:
                    result = reader.get(ip)
                    yaml_result = yaml.dump(result, allow_unicode=True, sort_keys=False)
                    print(f"---\nIP: {ip} -> Result:\n{yaml_result}")
                except Exception as e:
                    print(f"Error reading {ip}: {e}")
    except Exception as e:
        print(f"Error opening or reading database: {e}")


if __name__ == "__main__":
    main()
