<#
.SYNOPSIS
    Update the docs references.
#>



$RootFolder = Join-Path -Path $PSScriptRoot -ChildPath ".."
$RootFolder = Resolve-Path $RootFolder
$DocFile = Join-Path $RootFolder "scripts/urls.txt"

$SuccessCount = 0
$ErrorCount = 0
$SkippedCount = 0

# 文档页面控制台执行(doc和api两个tab需要全部展开)
# copy(Array.from(document.querySelectorAll("nav .menu__link")).map(i=>i.href.replace("#","")).filter(i=>i.startsWith("https://www.remotion.dev/docs/")).map(i=>i.endsWith("/")? i+"index.md":i+".md").join("\n"))
$DocLinks = Get-Content $DocFile

$jobs = @()
for ($i = 0; $i -lt $DocLinks.Count; $i++) {
    $link = $DocLinks[$i]
    $urls = $link -split "/"
    $paths = $urls | Select-Object -Skip 3
    $name = $paths -join "/"
    if ($paths.Length -gt 1) {
        $folder = $paths[0..$($paths.Length - 2)]
        $folder = Join-Path $RootFolder $folder
        if (-not (Test-Path $folder)) {
            New-Item -Path $folder -ItemType Directory | Out-Null
        }
    }
    $path = Join-Path $RootFolder $name
    Write-Host -ForegroundColor Yellow "[$($i+1)/$($DocLinks.Count)] Downloading $link to $path"
    $job = Start-ThreadJob -ScriptBlock {
        param(
            $link,
            $path
        )
        if ((Test-Path $path) -and ((Get-Item $path).Length -gt 0)) {
            return [PSCustomObject]@{ Status = 'Skipped'; Message = "File $path already exists, skipping download." }
        }
        try {
            $response = Invoke-WebRequest -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" -Uri $link -ErrorAction Stop
            $response.Content -split "`r?`n" | Select-Object -Skip 0 | Set-Content -Path $path -Encoding UTF8
            return [PSCustomObject]@{ Status = 'Success'; Message = "Downloaded $link to $path" }
        }
        catch {
            return [PSCustomObject]@{ Status = 'Error'; Message = "Failed to download $link to $path : $_" }
        }

    } -ArgumentList $link, $path -Name $name -ErrorAction Stop
    $jobs += $job
}

Write-Host -ForegroundColor Green "Waiting for all jobs to complete."
$jobs | ForEach-Object {
    $_ | Wait-Job | Out-Null
    if ($_.State -ne 'Completed') {
        Write-Host -ForegroundColor Red "Job $($_.Name) failed with state $($_.State)"
    }
    
    $results = $_ | Receive-Job
    foreach ($res in $results) {
        if ($res -is [System.Management.Automation.PSCustomObject] -and $res.Status) {
            switch ($res.Status) {
                'Skipped' {
                    $SkippedCount++
                    Write-Host -ForegroundColor Cyan $res.Message
                }
                'Success' {
                    $SuccessCount++
                    Write-Host -ForegroundColor Green $res.Message
                }
                'Error' {
                    $ErrorCount++
                    Write-Host -ForegroundColor Red $res.Message
                }
            }
        }
        else {
            # Handle any unexpected output
            Write-Output $res
        }
    }
}
$jobs | Remove-Job

Write-Host -ForegroundColor Green "Success Count: $SuccessCount"
Write-Host -ForegroundColor Cyan "Skipped Count: $SkippedCount"
Write-Host -ForegroundColor Red "Error Count: $ErrorCount"
Write-Host -ForegroundColor Green "Done."