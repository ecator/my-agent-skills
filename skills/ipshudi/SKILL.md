---
name: ipshudi
description: IP属地查询
---

# IP属地查询

获取IP属地信息。

注意所有脚本调用都必须通过`uv`命令，所以如果用户没有安装`uv`，那么首先引导用户打开`https://docs.astral.sh/uv/getting-started/installation/`安装`uv`。


## IP属地查询

通过调用`scripts/ip.py`来获取IP属地信息。

调用示例：

```bash
uv run scripts/ip.py ip1 ip2 ip3 ...
```

支持ipv4和ipv6，例如：

```bash
uv run scripts/ip.py 140.82.116.3 2404:6800:4004:80e::200e
```
