[CmdletBinding()]
param([Parameter(Mandatory)][string]$SandboxDirectory)
$ErrorActionPreference = 'Stop'
$skill = Split-Path $PSScriptRoot -Parent
Import-Module (Join-Path $skill 'scripts\CacheTools.psm1') -Force
$sandboxBase = [IO.Path]::GetFullPath($SandboxDirectory)
if (-not $sandboxBase.StartsWith('C:\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Use a scratch directory on C:.' }
if ($sandboxBase -eq $skill -or $sandboxBase.StartsWith($skill + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Keep test artifacts outside the skill directory.' }
$sandbox = Join-Path $sandboxBase ('cleanup-test-' + [guid]::NewGuid().ToString('N'))
$root = Join-Path $sandbox 'cache'
$outside = Join-Path $sandbox 'outside'
New-Item -ItemType Directory -Path $root,$outside -Force | Out-Null
function Assert-True([bool]$Value,[string]$Message) { if (-not $Value) { throw $Message } }
$old = Join-Path $root 'old.txt'
$recent = Join-Path $root 'recent.txt'
$locked = Join-Path $root 'locked.txt'
$protected = Join-Path $outside 'keep.txt'
foreach ($path in @($old,$recent,$locked,$protected)) { [IO.File]::WriteAllText($path,'test content') }
$longDirectory = '\\?\' + $root + '\' + ('a' * 100) + '\' + ('b' * 100) + '\' + ('c' * 100)
[IO.Directory]::CreateDirectory($longDirectory) | Out-Null
$longFile = $longDirectory + '\old-long.txt'
[IO.File]::WriteAllText($longFile,'long path content')
foreach ($path in @($old,$locked,$longFile)) { [IO.File]::SetLastWriteTime($path,(Get-Date).AddDays(-10)) }
New-Item -ItemType Junction -Path (Join-Path $root 'linked') -Target $outside | Out-Null
$preview = Invoke-CacheTree -Root $root -MinimumAgeDays 7
Assert-True ($preview.EligibleFiles -eq 3) 'Preview failed to count stale/long-path files.'
Assert-True ($preview.SkippedLinks -eq 1) 'Preview did not skip the junction.'
Assert-True ([IO.File]::Exists($old)) 'Preview deleted a file.'
$handle = [IO.File]::Open($locked,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::None)
try {
    $applied = Invoke-CacheTree -Root $root -MinimumAgeDays 7 -Apply
    Assert-True ($applied.RemovedFiles -eq 2) 'Cleanup failed to remove eligible files including a long path.'
    Assert-True ($applied.FailedFiles -eq 1) 'Cleanup did not report the locked file.'
    Assert-True ([IO.File]::Exists($recent)) 'Recent file was deleted.'
    Assert-True ([IO.File]::Exists($protected)) 'Cleanup followed the junction.'
    Assert-True ([IO.File]::Exists($locked)) 'Locked file was deleted.'
} finally { $handle.Dispose() }
$rejected=$false
try { Invoke-CacheTree -Root (Join-Path $root 'linked') -Apply | Out-Null } catch { $rejected=$true }
Assert-True $rejected 'Linked cleanup root was accepted.'
$rejected=$false
try { Invoke-CacheTree -Root (Join-Path $root 'linked\nested') -Apply | Out-Null } catch { $rejected=$true }
Assert-True $rejected 'Linked ancestor was accepted.'
$rejected=$false
try { Invoke-CacheTree -Root 'C:\' -Apply | Out-Null } catch { $rejected=$true }
Assert-True $rejected 'Drive-root cleanup was accepted.'
$rejected=$false
try { Invoke-CacheTree -Root $root -MinimumAgeDays 0 -Apply -BeforeDirectory { throw 'Guard stopped cleanup' } | Out-Null } catch { $rejected=$true }
Assert-True $rejected 'Guard did not abort deletion.'
Assert-True ([IO.File]::Exists($recent)) 'Guard allowed deletion.'
$progressRoot = Join-Path $sandbox 'progress'
[IO.Directory]::CreateDirectory($progressRoot) | Out-Null
for ($i=0;$i -lt 2001;$i++) { [IO.File]::WriteAllText((Join-Path $progressRoot ($i.ToString()+'.txt')),'x') }
$script:progressCount = 0
$progressResult = Invoke-CacheTree -Root $progressRoot -MinimumAgeDays 0 -OnProgress { param($current); $script:progressCount = $current.EligibleFiles }
Assert-True ($progressResult.FoundFiles -eq 2001 -and $script:progressCount -eq 2000) 'Progress callback did not receive current counts.'
try { Get-UserCacheTargets -Categories Unknown | Out-Null; throw 'Unsupported category was accepted.' } catch { if ($_.Exception.Message -eq 'Unsupported category was accepted.') { throw } }
$serviceBefore = @(Get-Service bits,wuauserv | Select-Object Name,Status)
$null = & (Join-Path $skill 'scripts\Clear-WindowsUpdateCache.ps1')
$serviceAfter = @(Get-Service bits,wuauserv | Select-Object Name,Status)
Assert-True (($serviceBefore | ConvertTo-Json -Compress) -eq ($serviceAfter | ConvertTo-Json -Compress)) 'Preview changed service states.'
$userPreview = & (Join-Path $skill 'scripts\Clear-UserCaches.ps1') -Categories Pip
Assert-True ($userPreview.Mode -eq 'Preview') 'User cleanup is not preview by default.'
'PASS: stale/recent files, long paths, junction boundaries, locked files, guard abort, category allowlist, and read-only previews.'
