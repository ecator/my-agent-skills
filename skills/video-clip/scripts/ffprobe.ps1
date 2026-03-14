<#
.SYNOPSIS
包装ffprobe命令，避免乱码问题，所有参数都会透传给ffprobe
#>

$OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[System.Console]::InputEncoding = [System.Text.Encoding]::UTF8

ffprobe @args