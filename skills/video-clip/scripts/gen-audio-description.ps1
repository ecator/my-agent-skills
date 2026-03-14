<#
.SYNOPSIS
生成音频的详细描述

.DESCRIPTION
使用gemini-cli生成秒级别音频描述以及剪辑建议，描述文件保存为输入文件同级路径下的同名md文件

.PARAMETER InputFile
输入音频文件路径

.EXAMPLE
.\gen-audio-description.ps1 -InputFile "Driver:\PATH\TO\input.mp3"

#>


param (
    [Parameter(Mandatory = $true)]
    [System.IO.FileInfo]$InputFile
)


$OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8

Push-Location $InputFile.DirectoryName
$MarkdownFile = "$($InputFile.BaseName).md"


$prompt = "
@$($InputFile.Name)

请按秒级别详细描述这个音频的内容，包括但不限于：
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

**DO NOT USE ANY SKILLS**
**DO NOT OUTPUT FILE NAME**
"

$Description = $prompt | gemini
if ($LASTEXITCODE -ne 0) {
    Write-Error "Audio Description generation failed"
    Pop-Location
    exit $LASTEXITCODE
}

# 4. 将总结结果写入 .md 文件
$Description | Out-File -FilePath $MarkdownFile -Encoding utf8 -Force

Write-Host "Audio Description file saved: $MarkdownFile"
Pop-Location