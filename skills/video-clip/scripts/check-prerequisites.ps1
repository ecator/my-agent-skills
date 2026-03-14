<#
.SYNOPSIS
检查用户的环境是否满足剪辑环境

.DESCRIPTION
检查ffmpeg、mpv是否安装

#>


$OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8


$cmds = [ordered]@{
    "mpv"     = "https://mpv.io/installation/"
    "ffmpeg"  = "https://www.ffmpeg.org/download.html"
    "ffprobe" = "https://www.ffmpeg.org/download.html"
    "pwsh"    = "https://github.com/PowerShell/PowerShell"
    "gemini"  = "https://geminicli.com/docs/get-started/installation/"
}

foreach ($cmd in $cmds.GetEnumerator()) {
    Get-Command $cmd.Name -ErrorAction Ignore | Out-Null
    if (!$?) {
        Write-Error "$($cmd.Name) not installed, please see $($cmd.Value)"
        exit 1
    }
}


Write-Host "Prerequisites checking is ok"