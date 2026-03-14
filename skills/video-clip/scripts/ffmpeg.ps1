<#
.SYNOPSIS
包装ffmpeg命令，避免乱码问题，所有参数都会透传给ffmpeg
#>

$OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8

ffmpeg @args