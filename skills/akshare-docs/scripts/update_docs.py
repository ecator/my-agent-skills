# /// script
# dependencies = [
#   "requests",
# ]
# ///


from pathlib import Path
import requests


LINK_LIST = [
    "https://akshare.akfamily.xyz/data/stock/stock.html",
    "https://akshare.akfamily.xyz/data/futures/futures.html",
    "https://akshare.akfamily.xyz/data/bond/bond.html",
    "https://akshare.akfamily.xyz/data/option/option.html",
    "https://akshare.akfamily.xyz/data/fx/fx.html",
    "https://akshare.akfamily.xyz/data/currency/currency.html",
    "https://akshare.akfamily.xyz/data/spot/spot.html",
    "https://akshare.akfamily.xyz/data/interest_rate/interest_rate.html",
    "https://akshare.akfamily.xyz/data/fund/fund_private.html",
    "https://akshare.akfamily.xyz/data/fund/fund_public.html",
    "https://akshare.akfamily.xyz/data/index/index.html",
    "https://akshare.akfamily.xyz/data/macro/macro.html",
    "https://akshare.akfamily.xyz/data/dc/dc.html",
    "https://akshare.akfamily.xyz/data/bank/bank.html",
    "https://akshare.akfamily.xyz/data/article/article.html",
    "https://akshare.akfamily.xyz/data/energy/energy.html",
    "https://akshare.akfamily.xyz/data/event/event.html",
    "https://akshare.akfamily.xyz/data/hf/hf.html",
    "https://akshare.akfamily.xyz/data/nlp/nlp.html",
    "https://akshare.akfamily.xyz/data/qdii/qdii.html",
    "https://akshare.akfamily.xyz/data/others/others.html",
    "https://akshare.akfamily.xyz/data/tool/tool.html",
    "https://akshare.akfamily.xyz/indicator.html",
    "https://akshare.akfamily.xyz/data_tips.html",
    "https://akshare.akfamily.xyz/answer.html",
    "https://akshare.akfamily.xyz/tutorial.html",
]


def main():
    cnt_ok = 0
    cnt_error = 0
    docs_dir = Path(__file__).parent.parent.joinpath("docs")
    for link in LINK_LIST:
        md_link = link.replace(
            "https://akshare.akfamily.xyz/", "https://akshare.akfamily.xyz/_sources/"
        ).replace(".html", ".md.txt")
        md_path = docs_dir.joinpath(
            md_link.replace("https://akshare.akfamily.xyz/_sources/", "")[:-4]
        )
        if not md_path.parent.exists():
            md_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"⏳ Fetching {md_link} to {md_path}")
        res = requests.get(md_link)
        if res.status_code == 200:
            with open(md_path, "wb") as f:
                f.write(res.content)
            cnt_ok += 1
            print(f"✅ Successfully fetched {md_link} to {md_path}")
        else:
            cnt_error += 1
            print(f"💥 Failed to fetch {md_link}")
    print(
        f"✅ Successfully fetched {cnt_ok} pages, 💥 failed to fetch {cnt_error} pages"
    )


if __name__ == "__main__":
    main()
