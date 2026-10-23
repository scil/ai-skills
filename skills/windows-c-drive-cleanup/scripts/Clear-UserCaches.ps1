[CmdletBinding()]
param(
    [ValidateSet('Temp','Pip','CrashDumps','Pnpm','NuGet','Yarn')]
    [string[]]$Categories = @('Temp','Pip','CrashDumps','Pnpm','NuGet','Yarn'),
    [ValidateRange(0,36500)][int]$MinimumAgeDays = 7,
    [switch]$Apply,
    [string]$ResultDirectory
)
$ErrorActionPreference = 'Stop'
Import-Module (Join-Path $PSScriptRoot 'CacheTools.psm1') -Force
if ($Apply -and -not $ResultDirectory) { throw 'Supply -ResultDirectory outside the skill repository for actual cleanup.' }
if ($ResultDirectory) {
    $ResultDirectory = [IO.Path]::GetFullPath($ResultDirectory)
    if ($ResultDirectory.StartsWith((Split-Path $PSScriptRoot -Parent) + '\', [StringComparison]::OrdinalIgnoreCase) -or $ResultDirectory -eq (Split-Path $PSScriptRoot -Parent)) { throw 'Store results outside the skill directory.' }
    foreach ($target in Get-UserCacheTargets -Categories $Categories) {
        if ($ResultDirectory.TrimEnd('\') -eq $target.Path -or $ResultDirectory.StartsWith($target.Path + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Results cannot be inside a cleanup target.' }
    }
    New-Item -ItemType Directory -Path $ResultDirectory -Force | Out-Null
}
$before = (Get-PSDrive C).Free
$results = @()
$rejected = 0
foreach ($target in Get-UserCacheTargets -Categories $Categories) {
    try {
        $result = Invoke-CacheTree -Root $target.Path -MinimumAgeDays $MinimumAgeDays -Apply:$Apply
        $results += $result
        if ($result.ReadErrors -gt 0 -or $result.FailedFiles -gt 0 -or $result.SkippedLinks -gt 0) { $rejected++ }
    } catch {
        $rejected++
        $results += [pscustomobject]@{Root=$target.Path; Rejected=$true; Error=$_.Exception.Message}
    }
}
$after = (Get-PSDrive C).Free
$report = [pscustomobject]@{
    Mode = $(if ($Apply) {'Apply'} else {'Preview'})
    Status = $(if ($rejected) {'Partial'} elseif ($Apply) {'Completed'} else {'Preview'})
    Updated = (Get-Date).ToString('o')
    FreeBeforeGB = [math]::Round($before / 1e9, 2)
    FreeAfterGB = [math]::Round($after / 1e9, 2)
    NetGainGB = [math]::Round(($after - $before) / 1e9, 2)
    Results = $results
}
if ($ResultDirectory) { $report | ConvertTo-Json -Depth 5 | Out-File -LiteralPath (Join-Path $ResultDirectory 'UserCacheCleanup-result.json') -Encoding utf8 }
$report
