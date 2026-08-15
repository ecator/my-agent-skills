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

$OutputEncoding = [System.Text.UTF8Encoding]::new()
[console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
[console]::InputEncoding = [System.Text.UTF8Encoding]::new()

Push-Location $InputFile.DirectoryName
$MarkdownFile = "$($InputFile.BaseName).md"
$TempCompressedFile = "$($InputFile.BaseName)_compressed.mp4"
$JsonSchemaFile = Join-Path $PSScriptRoot -ChildPath "gen-video-description-output-schema.json"

# 调用 ffmpeg 进行压缩
ffmpeg -loglevel quiet -hwaccel cuda -hwaccel_output_format cuda -i "$($InputFile.FullName)"  -vf scale_cuda=-1:480 -c:v hevc_nvenc -rc vbr -cq 35 -preset p6 -y "$TempCompressedFile"

if ($LASTEXITCODE -ne 0) {
    Write-Error "ffmpeg compression failed"
    Pop-Location
    exit $LASTEXITCODE
}


$prompt = "
@$TempCompressedFile

请按秒级别详细描述这个视频的内容，包括但不限于：
- 视频的主题
- 视频的主要内容
- 视频的结构
- 视频的风格
- 视频的亮点
- 视频的适用场景
- 视频的潜在用途

输出为markdown格式,注意一定要精确到秒单位,因为这个内容会作为剪辑的参考。
把结果输出到``markdown``属性中。
输出模板参考如下：
<template>
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

</template>

**DO NOT USE ANY SKILLS**
**DO NOT OUTPUT VIDEO FILE NAME IN YOUR RESPONSE, ONLY OUTPUT THE DESCRIPTION**

"

$result = $prompt | agy --mode plan --disable-slash-commands --output-format json --json-schema $JsonSchemaFile --add-dir $InputFile.DirectoryName | ConvertFrom-Json
#$result
$description = $result.structured_output.markdown

if ($null -eq $description -or $description.Trim() -eq "") {
    Write-Error "Generate description failed"
}
else {
    Write-Host "Generate description successfully: $MarkdownFile"
    $description | Out-File -FilePath $MarkdownFile -Encoding UTF8
}

# 清理临时压缩文件
Remove-Item "$TempCompressedFile" -ErrorAction SilentlyContinue
Remove-Item ".antigravitycli" -Force -Recurse -ErrorAction SilentlyContinue

Pop-Location