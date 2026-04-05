---
name: weixin-bot-cli
description: 使用命令行工具给微信用户发送文本或者文件
---

# Weixin Bot CLI

使用命令行工具给微信用户发送文本或者文件。

注意所有脚本调用都必须通过`uv`命令，所以如果用户没有安装`uv`，那么首先引导用户打开`https://docs.astral.sh/uv/getting-started/installation/`安装`uv`。

另外还需要有node环境，如果用户没有按照node，那么引导用户打开`https://nodejs.org/en/download/`安装node，建议安装最LTS版本即可。

## 获取用户微信ID


如果用户没有指定ID的情况下请调用下面的脚本获取用户ID，这样才能发送消息。

```bash
uv run scripts/get_user_weixin_id.py
```

原理是从`weixin-bot-cli`的配置路径里面获取，当然还可以手动指定这个路径：
```bash
uv run scripts/get_user_weixin_id.py /path/to/weixin-bot-cli
```

## 发送文本消息

```bash
npx -y @ecat/weixin-bot-cli send user_id text
```

`user_id`是用户微信ID，如果用户没有明确说明那么使用`scripts/get_user_weixin_id.py`脚本获取。
`text`是发送的文本消息，如果包含空格，那么需要使用引号括起来，如果有大段文件中的文本需要发送可以通过标准输入传入：
```bash
cat message.txt | npx -y @ecat/weixin-bot-cli send user_id
```

## 发送文件

除了单纯发送文本消息，还可以发送文件，只需要通过`--files`参数指定文件即可，可以指定多个，会自动根据文件类型发送不同的消息类型。

```bash
npx -y @ecat/weixin-bot-cli send user_id optional_text --files file1 file2
```

`user_id`是用户微信ID，如果用户没有明确说明那么使用`scripts/get_user_weixin_id.py`脚本获取。
`optional_text`是可选的文本消息，会在所有文件最开始发送一条文本消息，当然也可以不指定，那么就是只发送文件。
> 注意发送文件的时候文本消息只能通过位置参数指定，不能通过标准输入传入。
`--files`是发送的文件路径，可以指定多个，注意如果文件里面有空格或者特殊字符，那么需要使用引号括起来。
