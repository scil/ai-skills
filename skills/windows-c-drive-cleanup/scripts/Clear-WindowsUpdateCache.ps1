[CmdletBinding()]
param([switch]$Apply, [string]$ResultDirectory, [switch]$Elevated)
$ErrorActionPreference = 'Stop'
Import-Module (Join-Path $PSScriptRoot 'CacheTools.psm1') -Force
$root = 'C:\Windows\SoftwareDistribution\Download'
if (-not $Apply) { Invoke-CacheTree -Root $root -MinimumAgeDays 0; return }
if (-not $ResultDirectory) { throw 'Supply -ResultDirectory outside the skill repository for actual cleanup.' }
$ResultDirectory = [IO.Path]::GetFullPath($ResultDirectory).TrimEnd('\')
$skillDirectory = Split-Path $PSScriptRoot -Parent
if ($ResultDirectory -eq $skillDirectory -or $ResultDirectory.StartsWith($skillDirectory + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Store results outside the skill directory.' }
if ($ResultDirectory -eq $root -or $ResultDirectory.StartsWith($root + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Results cannot be inside the cleanup target.' }
# Reject quotes/newlines rather than attempting ambiguous command-line escaping.
foreach ($argumentPath in @($PSCommandPath,$ResultDirectory)) {
    if ($argumentPath.Contains('"') -or $argumentPath.Contains("`r") -or $argumentPath.Contains("`n")) { throw 'Unsupported characters in launch path.' }
}
$principal = [Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    if ($Elevated) { throw 'Administrator access was not granted.' }
    $arguments = '-NoProfile -ExecutionPolicy Bypass -File "{0}" -Apply -Elevated -ResultDirectory "{1}"' -f $PSCommandPath,$ResultDirectory
    try {
        $process = Start-Process -FilePath "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -ArgumentList $arguments -Verb RunAs -WindowStyle Hidden -PassThru
        [pscustomobject]@{Status='Launched';ProcessId=$process.Id;ResultPath=Join-Path $ResultDirectory 'WindowsUpdateCleanup-result.json'}
    } catch { throw "Administrator launch cancelled or failed: $($_.Exception.Message)" }
    return
}
New-Item -ItemType Directory -Path $ResultDirectory -Force | Out-Null
$resultPath = Join-Path $ResultDirectory 'WindowsUpdateCleanup-result.json'
$started = Get-Date
$freeBefore = (Get-PSDrive C).Free
$restore = [Collections.Generic.List[string]]::new()
$errors = [Collections.Generic.List[string]]::new()
$servicesBefore = [ordered]@{}
$servicesAfter = [ordered]@{}
$status = 'Running'
$summary = $null
$transcriptStarted = $false
function Save-UpdateResult {
    $freeNow = (Get-PSDrive C).Free
    $report = [ordered]@{
        Status=$script:status; Started=$script:started.ToString('o'); Updated=(Get-Date).ToString('o')
        Target='C:\Windows\SoftwareDistribution\Download'
        FreeBeforeGB=[math]::Round($script:freeBefore/1e9,2)
        FreeAfterGB=[math]::Round($freeNow/1e9,2)
        NetGainGB=[math]::Round(($freeNow-$script:freeBefore)/1e9,2)
        Summary=$script:summary; ServicesBefore=$script:servicesBefore; ServicesAfter=$script:servicesAfter
        Errors=@($script:errors.ToArray())
    }
    # Pollers see either the old complete JSON or the new complete JSON.
    $temporary = $resultPath + '.tmp'
    $report | ConvertTo-Json -Depth 6 | Out-File -LiteralPath $temporary -Encoding utf8
    Move-Item -LiteralPath $temporary -Destination $resultPath -Force
}
try {
    Start-Transcript -LiteralPath (Join-Path $ResultDirectory 'WindowsUpdateCleanup.log') -Append | Out-Null
    $transcriptStarted = $true
    Save-UpdateResult
    if (Get-Process TiWorker,TrustedInstaller -ErrorAction SilentlyContinue) { throw 'Windows component installation is active; retry after it finishes.' }
    # Validate target/ancestor links without scanning the cache twice.
    # Deletion revalidates the target after services stop.
    $null = Invoke-CacheTree -Root $root -ValidateOnly
    foreach ($name in @('bits','wuauserv')) {
        $service = Get-Service -Name $name
        $servicesBefore[$name] = $service.Status.ToString()
        if ($service.Status -ne 'Running' -and $service.Status -ne 'Stopped') { throw "Service is transitioning: $name" }
    }
    foreach ($name in @('bits','wuauserv')) {
        $service = Get-Service -Name $name
        if ($servicesBefore[$name] -eq 'Running') {
            $restore.Add($name)
            $service.Stop()
            $service.WaitForStatus([ServiceProcess.ServiceControllerStatus]::Stopped,[TimeSpan]::FromSeconds(30))
        }
    }
    if (Get-Process TiWorker,TrustedInstaller -ErrorAction SilentlyContinue) { throw 'Windows component installation started; cleanup cancelled.' }
    $guard = {
        foreach ($name in @('bits','wuauserv')) {
            if ((Get-Service -Name $name).Status -ne 'Stopped') { throw "Service restarted during cleanup: $name" }
        }
    }
    $progress = { param($current); $script:summary = $current; Save-UpdateResult }
    $summary = Invoke-CacheTree -Root $root -MinimumAgeDays 0 -Apply -BeforeDirectory $guard -OnProgress $progress
    if ($summary.ReadErrors -gt 0 -or $summary.FailedFiles -gt 0 -or $summary.SkippedLinks -gt 0) { $status='Partial' } else { $status='Completed' }
} catch {
    $status='Failed'
    $errors.Add($_.Exception.Message)
    Write-Warning $_.Exception.Message
} finally {
    foreach ($name in $restore) {
        try {
            $service = Get-Service -Name $name
            if ($service.Status -eq 'Stopped') { $service.Start() }
            $service.WaitForStatus([ServiceProcess.ServiceControllerStatus]::Running,[TimeSpan]::FromSeconds(30))
        } catch { $status='NeedsAttention'; $errors.Add("Could not restore ${name}: $($_.Exception.Message)") }
    }
    foreach ($name in @('bits','wuauserv')) {
        try { $servicesAfter[$name]=(Get-Service -Name $name).Status.ToString() }
        catch { $status='NeedsAttention'; $errors.Add($_.Exception.Message) }
    }
    try { Save-UpdateResult } finally { if ($transcriptStarted) { Stop-Transcript -ErrorAction SilentlyContinue | Out-Null } }
}
if ($status -ne 'Completed') { exit 1 }
