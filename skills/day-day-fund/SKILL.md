---
name: day-day-fund
description: 天天基金相关数据获取，目前只支持持仓数据获取
---

# 天天基金数据

获取天天基金相关数据。

注意所有脚本调用都必须通过`uv`命令，所以如果用户没有安装`uv`，那么首先引导用户打开`https://docs.astral.sh/uv/getting-started/installation/`安装`uv`。


## 持仓数据

通过调用`scripts/hold.py`来获取持仓数据。

调用示例：

```bash
uv run scripts/hold.py
```