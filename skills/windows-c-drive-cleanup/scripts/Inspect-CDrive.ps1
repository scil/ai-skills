[CmdletBinding()]
param([ValidateRange(0,36500)][int]$MinimumAgeDays = 7)
$ErrorActionPreference = 'Stop'
Import-Module (Join-Path $PSScriptRoot 'CacheTools.psm1') -Force
$drive = Get-PSDrive C
$principal = [Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent())
[pscustomobject]@{
    Kind = 'Drive'; FreeGB = [math]::Round($drive.Free / 1e9, 2)
    UsedGB = [math]::Round($drive.Used / 1e9, 2)
    Administrator = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}
$targets = @(Get-UserCacheTargets) + @(
    [pscustomobject]@{Category='WindowsTemp'; Path='C:\Windows\Temp'},
    [pscustomobject]@{Category='WindowsUpdate'; Path='C:\Windows\SoftwareDistribution\Download'}
)
foreach ($target in $targets) {
    try {
        $age = $MinimumAgeDays
        if ($target.Category -eq 'WindowsUpdate') { $age = 0 }
        $result = Invoke-CacheTree -Root $target.Path -MinimumAgeDays $age
        [pscustomobject]@{
            Kind='Candidate'; Category=$target.Category; Path=$target.Path; Exists=$result.Exists
            Files=$result.FoundFiles; EligibleGB=[math]::Round($result.EligibleBytes / 1e9, 3)
            MinimumAgeDays=$age; SkippedLinks=$result.SkippedLinks; ReadErrors=$result.ReadErrors
        }
    } catch { [pscustomobject]@{Kind='Rejected'; Path=$target.Path; Reason=$_.Exception.Message} }
}
