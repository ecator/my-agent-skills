<#
.SYNOPSIS
生成视频的详细描述

.DESCRIPTION
压缩视频并使用antigravity-cli生成秒级别视频描述以及剪辑建议，描述文件保存为跟输入文件同级路径下的同名md文件。

.PARAMETER InputFile
输入视频文件路径

.EXAMPLE
.\gen-video-description.ps1 -InputFile "Driver:\PATH\TO\input.mp4"
#>


param (
    [Parameter(Mandatory = $true)]
    [System.IO.FileInfo]$InputFile
)

$OutputEncoding = [System.Text.UTF8Encoding]::new()
[console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
[console]::InputEncoding = [System.Text.UTF8Encoding]::new()

Push-Location $InputFile.DirectoryName
$MarkdownFile = "$($InputFile.BaseName).md"
$MediaFile = $($InputFile.Name)
$JsonSchemaFile = Join-Path $PSScriptRoot -ChildPath "markdown-output-schema.json"


$prompt = "
@$MediaFile

请按秒级别详细描述用户给你发送的音频内容，包括但不限于：
- 音频的主题
- 音频的主要内容
- 音频的结构
- 音频的鼓点
- 音频的风格
- 音频的亮点
- 音频的适用场景
- 音频的潜在用途

输出为markdown格式,注意一定要精确到秒单位,因为这个内容会作为剪辑的参考。
只用输出最终结果即可,不需要多余的解释。
输出模板参考如下：
<template>
# 音频分析报告
XXX（关于这个音频的一个整体介绍，一句话概括即可）
## 音频信息概览
### 主题
XXXXX
### 内容
XXXXX
### 结构
XXXXX
### 风格
XXXXX
### 亮点
XXXXX
### 适用场景
XXXXX
### 潜在用途
XXXXX

## 时间段详细描述

| 时间段 (MM:ss) | 音频内容描述 | 音频鼓点 |
| :--- | :--- | :--- |
| 00:00 - 00:03 | XXXX | XXXX |
| 00:04 - 00:07 | XXXX | XXXX |

## 其他补充事项
XXXX
</template>

All you need to do is to analyze the file provided to you. Do not execute any other commands.
**DO NOT USE ANY SKILLS**
**DO NOT OUTPUT FILE NAME IN YOUR RESPONSE, ONLY OUTPUT THE DESCRIPTION**


"

$result = $prompt | agy --sandbox --disable-slash-commands --output-format json --json-schema $JsonSchemaFile --add-dir $InputFile.DirectoryName | ConvertFrom-Json
#$result
$description = $result.structured_output.markdown

if ($null -eq $description -or $description.Trim() -eq "") {
    Write-Error "Generate description failed"
}
else {
    Write-Host "Generate description successfully: $MarkdownFile"
    $description | Out-File -FilePath $MarkdownFile -Encoding UTF8
}

# 清理临时文件
Remove-Item ".antigravitycli" -Force -Recurse -ErrorAction SilentlyContinue

Pop-Location