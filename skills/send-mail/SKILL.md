---
name: send-mail
description: 发送邮件
---

# 发送邮件

这个技能可以通过调用`scripts/sendmail.py`来发送邮件。

## 依赖

所有脚本都是用`uv`来执行，这样可以自动解决依赖。

## 参数

- sender: 发送者邮箱
- to: 接收者邮箱
- subject: 邮件主题
- bodyfile: 邮件正文文件路径，支持md，txt以及html文件
- attach: 附件路径，可以有多个

## 示例


**获取脚本帮助**
```bash
uv run scripts/sendmail.py --help
```

**发送纯文本邮件，并且携带附件**
```bash
uv run scripts/sendmail.py --sender test1@misaka.cool --to test2@misaka.cool --subject "test" --bodyfile "test.txt" --attach "test.mp3" "test.mp4"
```

**发送HTML邮件，并且没有携带附件**
```bash
uv run scripts/sendmail.py --sender test1@misaka.cool --to test2@misaka.cool --subject "test" --bodyfile "test.html"
```
