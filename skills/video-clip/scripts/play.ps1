<#
.SYNOPSIS
播放视频或者音频

.DESCRIPTION
可以指定开始时间使用mpv播放指定视频或者音频

.PARAMETER Path
要播放的视频或者音频文件

.PARAMETER StartTime
开始播放的时间（百分比，秒，hh:mm:ss）

.EXAMPLE
# 从头开始播放input.mp4
.\play.ps1 -Path input.mp4

.EXAMPLE
# 从第10秒开始播放input.mp3
.\play.ps1 -Path input.mp3 -StartTime "10"
#>

param(
    [Parameter(Mandatory = $true)]
    [System.IO.FileInfo]$Path,
    [Parameter(Mandatory = $false)]
    [string]$StartTime
)

$OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8

if ($null -eq $StartTime -or $StartTime.Length -eq 0) {
    $StartTime = "0"
}

if ($Path.Exists) {
    mpv $Path --start=$StartTime 2> $null
}
else {
    Write-Error "File Not Exists: $Path"
    exit 1
}