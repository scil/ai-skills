[CmdletBinding()]
param(
    [Parameter(Mandatory, Position = 0)]
    [string]$Path,

    [switch]$Checkver
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-ObjectProperty {
    param(
        [Parameter(Mandatory)]
        [object]$InputObject,

        [Parameter(Mandatory)]
        [string]$Name
    )

    return $null -ne $InputObject.PSObject.Properties[$Name]
}

function Test-DownloadEntry {
    param(
        [Parameter(Mandatory)]
        [object]$Entry,

        [Parameter(Mandatory)]
        [string]$Label
    )

    foreach ($field in @('url', 'hash')) {
        if (-not (Test-ObjectProperty -InputObject $Entry -Name $field)) {
            throw "$Label is missing '$field'."
        }

        $values = @($Entry.$field)
        if ($values.Count -eq 0 -or @($values | Where-Object { $_ -is [string] -and $_.Trim() }).Count -ne $values.Count) {
            throw "$Label '$field' must contain one or more non-empty strings."
        }
    }

    $urls = @($Entry.url)
    $hashes = @($Entry.hash)
    if ($urls.Count -ne $hashes.Count) {
        throw "$Label has $($urls.Count) URL value(s) but $($hashes.Count) hash value(s)."
    }

    foreach ($url in $urls) {
        if ($url -notmatch '^https?://') {
            throw "$Label contains a non-HTTP(S) URL: $url"
        }
    }
}

$manifestPath = (Resolve-Path -LiteralPath $Path).Path
if ([IO.Path]::GetExtension($manifestPath) -ne '.json') {
    throw "Manifest must use the .json extension: $manifestPath"
}

try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
} catch {
    throw "Invalid JSON in '$manifestPath': $($_.Exception.Message)"
}

foreach ($field in @('version', 'description', 'homepage', 'license')) {
    if (-not (Test-ObjectProperty -InputObject $manifest -Name $field)) {
        throw "Manifest is missing required field '$field'."
    }

    if ($null -eq $manifest.$field -or ($manifest.$field -is [string] -and -not $manifest.$field.Trim())) {
        throw "Manifest field '$field' must not be empty."
    }
}

if ($manifest.version -match '^v\d') {
    Write-Warning "Version '$($manifest.version)' starts with 'v'; Scoop versions normally omit a release-tag prefix."
}

$downloadEntryCount = 0
if (Test-ObjectProperty -InputObject $manifest -Name 'url') {
    Test-DownloadEntry -Entry $manifest -Label 'top-level download'
    $downloadEntryCount++
}

if (Test-ObjectProperty -InputObject $manifest -Name 'architecture') {
    foreach ($architecture in $manifest.architecture.PSObject.Properties) {
        Test-DownloadEntry -Entry $architecture.Value -Label "architecture '$($architecture.Name)'"
        $downloadEntryCount++
    }
}

if ($downloadEntryCount -eq 0) {
    throw "Manifest needs a top-level download or at least one architecture download."
}

$hasCheckver = Test-ObjectProperty -InputObject $manifest -Name 'checkver'
$hasAutoupdate = Test-ObjectProperty -InputObject $manifest -Name 'autoupdate'
if ($hasCheckver -and -not $hasAutoupdate) {
    Write-Warning 'Manifest has checkver but no autoupdate block.'
} elseif ($hasAutoupdate -and -not $hasCheckver) {
    Write-Warning 'Manifest has autoupdate but no checkver block.'
}

if ((Test-ObjectProperty -InputObject $manifest -Name 'innosetup') -and $manifest.innosetup) {
    $allUrls = @()
    if (Test-ObjectProperty -InputObject $manifest -Name 'url') {
        $allUrls += @($manifest.url)
    }
    if (Test-ObjectProperty -InputObject $manifest -Name 'architecture') {
        foreach ($architecture in $manifest.architecture.PSObject.Properties) {
            $allUrls += @($architecture.Value.url)
        }
    }

    if ($allUrls | Where-Object { ($_ -split '#', 2)[0] -match '\.(zip|7z|nupkg)$' }) {
        throw 'innosetup is enabled for an archive URL. Remove innosetup or select the Inno Setup asset.'
    }
}

Write-Host "[OK] Parsed and structurally validated $manifestPath"

if ($Checkver) {
    if (-not $hasCheckver) {
        throw 'Cannot run checkver because the manifest has no checkver block.'
    }
    $scoopCommand = Get-Command scoop -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $scoopCommand) {
        throw 'Cannot run checkver because Scoop is unavailable on PATH.'
    }

    $scoopRoot = Split-Path -Parent (Split-Path -Parent $scoopCommand.Source)
    $checkverScript = Join-Path $scoopRoot 'apps\scoop\current\bin\checkver.ps1'
    if (-not (Test-Path -LiteralPath $checkverScript)) {
        throw "Scoop checkver script was not found: $checkverScript"
    }

    $app = [IO.Path]::GetFileNameWithoutExtension($manifestPath)
    $directory = Split-Path -Parent $manifestPath
    $powerShellExecutable = (Get-Process -Id $PID).Path
    & $powerShellExecutable -NoLogo -NoProfile -File $checkverScript -App $app -Dir $directory -ThrowError
    if ($LASTEXITCODE -ne 0) {
        throw "Scoop checkver failed for $app with exit code $LASTEXITCODE."
    }
    Write-Host "[OK] Scoop checkver completed for $app"
}
