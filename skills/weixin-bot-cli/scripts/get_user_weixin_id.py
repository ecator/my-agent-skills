# /// script
# dependencies = [
#   "python-dotenv",
# ]
# ///


import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv(override=True)


def main():
    args = sys.argv[1:]
    weixin_bot_cli_home = Path.home().joinpath(".weixin-bot-cli")
    if os.getenv("WEIXIN_BOT_CLI_HOME"):
        weixin_bot_cli_home = Path(os.getenv("WEIXIN_BOT_CLI_HOME"))
    if len(args) > 0:
        weixin_bot_cli_home = Path(args[0])
    if not weixin_bot_cli_home.exists():
        print(
            f"Error: WEIXIN_BOT_CLI_HOME({weixin_bot_cli_home}) not exist",
            file=sys.stderr,
        )
        sys.exit(1)
    accounts_dir = weixin_bot_cli_home.joinpath("accounts")
    if not accounts_dir.exists():
        print(
            f"Error: accounts directory({accounts_dir}) not exist",
            file=sys.stderr,
        )
        sys.exit(1)
    for f in accounts_dir.glob("*-im-bot.json"):
        if f.is_file():
            with open(f, "r", encoding="utf-8") as f:
                data = json.load(f)
                id = data.get("userId", None)
                if id and id.endswith("@im.wechat"):
                    print(json.dumps({"userId": id}, ensure_ascii=False))
                    sys.exit(0)
    print("No User ID found", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
