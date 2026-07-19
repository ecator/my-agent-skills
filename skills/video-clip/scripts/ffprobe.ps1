<#
.SYNOPSIS
包装ffprobe命令，避免乱码问题，所有参数都会透传给ffprobe
#>

$OutputEncoding = [System.Text.UTF8Encoding]::new()
[console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
[console]::InputEncoding = [System.Text.UTF8Encoding]::new()

ffprobe @args