<#
.SYNOPSIS
生成视频的详细描述

.DESCRIPTION
压缩视频并使用gemini-cli生成秒级别视频描述以及剪辑建议，描述文件保存为跟输入文件同级路径下的同名md文件。

.PARAMETER InputFile
输入视频文件路径

.EXAMPLE
.\gen-video-description.ps1 -InputFile "Driver:\PATH\TO\input.mp4"
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
$TempCompressedFile = "$($InputFile.BaseName)_compressed.mp4"


# 2. 调用 ffmpeg 进行压缩
ffmpeg -loglevel quiet -hwaccel cuda -hwaccel_output_format cuda -i "$($InputFile.FullName)"  -vf scale_cuda=-1:480 -c:v hevc_nvenc -rc vbr -cq 35 -preset p6 -y "$TempCompressedFile"

if ($LASTEXITCODE -ne 0) {
    Write-Error "ffmpeg compression failed"
    Pop-Location
    exit $LASTEXITCODE
}


$prompt = "
@$tempCompressedFile

请按秒级别详细描述这个视频的内容，包括但不限于：
- 视频的主题
- 视频的主要内容
- 视频的结构
- 视频的风格
- 视频的亮点
- 视频的适用场景
- 视频的潜在用途

输出为markdown格式,注意一定要精确到秒单位,因为这个内容会作为剪辑的参考。
只用输出最终结果即可,不需要多余的解释。
输出模板参考如下：
``````md
# 视频分析报告
XXX（关于这个视频的一个整体介绍，一句话概括即可）
## 视频信息概览
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

| 时间段 (MM:ss) | 画面内容描述 | 镜头语言/运动 |
| :--- | :--- | :--- |
| 00:00 - 00:03 | XXXX | XXXX |
| 00:04 - 00:07 | XXXX | XXXX |

## 其他补充事项
XXXX

``````

**DO NOT USE ANY SKILLS**
**DO NOT OUTPUT FILE NAME**

"

$Description = $prompt | gemini
if ($LASTEXITCODE -ne 0) {
    Write-Error "Video Description generation failed"
    Remove-Item "$TempCompressedFile" -ErrorAction SilentlyContinue
    Pop-Location
    exit $LASTEXITCODE
}

# 4. 将总结结果写入 .md 文件
$Description | Out-File -FilePath $MarkdownFile -Encoding utf8 -Force

# 5. 清理临时压缩文件
Remove-Item "$TempCompressedFile" -ErrorAction SilentlyContinue

Write-Host "Video Description file saved: $MarkdownFile"
Pop-Location