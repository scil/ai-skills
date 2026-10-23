Set-StrictMode -Version 2

function Get-UserCacheTargets {
    param([string[]]$Categories = @('Temp','Pip','CrashDumps','Pnpm','NuGet','Yarn'))
    $base = [Environment]::GetFolderPath('LocalApplicationData')
    $paths = [ordered]@{
        Temp = 'Temp'; Pip = 'pip\Cache'; CrashDumps = 'CrashDumps'
        Pnpm = 'pnpm-cache'; NuGet = 'NuGet\v3-cache'; Yarn = 'Yarn\Cache'
    }
    foreach ($category in $Categories) {
        if (-not $paths.Contains($category)) { throw "Unsupported category: $category" }
        [pscustomobject]@{ Category = $category; Path = Join-Path $base $paths[$category] }
    }
}

function Invoke-CacheTree {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Root,
        [ValidateRange(0,36500)][int]$MinimumAgeDays = 7,
        [switch]$Apply,
        [switch]$ValidateOnly,
        [scriptblock]$BeforeDirectory,
        [scriptblock]$OnProgress
    )
    $rootPath = [IO.Path]::GetFullPath($Root).TrimEnd('\')
    if ($rootPath -eq [IO.Path]::GetPathRoot($rootPath).TrimEnd('\')) { throw 'A drive root cannot be a cleanup target.' }
    if (-not $rootPath.StartsWith('C:\', [StringComparison]::OrdinalIgnoreCase)) { throw 'This helper only handles C: targets.' }
    $summary = [pscustomobject]@{
        Root = $rootPath; Exists = $false; Apply = [bool]$Apply
        FoundFiles = 0; EligibleFiles = 0; EligibleBytes = 0L
        RemovedFiles = 0; RemovedBytes = 0L; SkippedLinks = 0
        FailedFiles = 0; ReadErrors = 0
    }
    # Check all ancestors so an apparently ordinary child cannot hide a junction.
    $ancestor = $rootPath
    while ($ancestor) {
        if (Test-Path -LiteralPath $ancestor) {
            $item = Get-Item -LiteralPath $ancestor -Force -ErrorAction Stop
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked target or ancestor rejected: $ancestor" }
            if (-not $item.PSIsContainer) { throw "Not a directory: $ancestor" }
        }
        $parent = [IO.Directory]::GetParent($ancestor)
        if ($null -eq $parent) { break }
        $ancestor = $parent.FullName
    }
    if (-not (Test-Path -LiteralPath $rootPath -PathType Container)) { return $summary }
    if ((Resolve-Path -LiteralPath $rootPath).Path.TrimEnd('\') -ne $rootPath) { throw 'Unexpected resolved target.' }
    $summary.Exists = $true
    if ($ValidateOnly) { return $summary }
    $ioRoot = '\\?\' + $rootPath
    $cutoff = (Get-Date).AddDays(-$MinimumAgeDays)
    $pending = [Collections.Generic.Stack[string]]::new()
    $directories = [Collections.Generic.List[string]]::new()
    $pending.Push($ioRoot)
    while ($pending.Count) {
        if ($BeforeDirectory) { & $BeforeDirectory | Out-Null }
        $directory = $pending.Pop()
        if ($directory -ne $ioRoot -and -not $directory.StartsWith($ioRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Directory outside target.' }
        try {
            if ([IO.File]::GetAttributes($directory) -band [IO.FileAttributes]::ReparsePoint) { $summary.SkippedLinks++; continue }
            $entries = [IO.Directory]::GetFileSystemEntries($directory)
        } catch { $summary.ReadErrors++; continue }
        $directories.Add($directory)
        foreach ($entry in $entries) {
            if (-not $entry.StartsWith($ioRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Entry outside target.' }
            try {
                $attributes = [IO.File]::GetAttributes($entry)
                if ($attributes -band [IO.FileAttributes]::ReparsePoint) { $summary.SkippedLinks++; continue }
                if ($attributes -band [IO.FileAttributes]::Directory) { $pending.Push($entry); continue }
                $file = [IO.FileInfo]::new($entry)
                $length = $file.Length
                $modified = $file.LastWriteTime
            } catch { $summary.ReadErrors++; continue }
            $summary.FoundFiles++
            if ($MinimumAgeDays -gt 0 -and $modified -ge $cutoff) { continue }
            $summary.EligibleFiles++
            $summary.EligibleBytes += $length
            if ($Apply) {
                try {
                    [IO.File]::Delete($entry)
                    $summary.RemovedFiles++
                    $summary.RemovedBytes += $length
                } catch { $summary.FailedFiles++ }
            }
            if ($OnProgress -and $summary.EligibleFiles % 2000 -eq 0) { & $OnProgress $summary | Out-Null }
        }
    }
    if ($Apply) {
        for ($index = $directories.Count - 1; $index -ge 0; $index--) {
            $directory = $directories[$index]
            if ($directory -eq $ioRoot) { continue }
            if (-not $directory.StartsWith($ioRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Directory outside target.' }
            try {
                if ([IO.File]::GetAttributes($directory) -band [IO.FileAttributes]::ReparsePoint) { continue }
                [IO.Directory]::Delete($directory, $false)
            } catch { }
        }
    }
    return $summary
}
Export-ModuleMember -Function Get-UserCacheTargets,Invoke-CacheTree
