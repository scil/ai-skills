# Windows Update download cleanup

Use this procedure for a confirmed large Windows Update download cache, when deleting that cache is within the requested cleanup scope. Follow [Microsoft's Windows Update guidance](https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/additional-resources-for-windows-update) for stopping the relevant services; this skill implements only download-cache deletion, not Microsoft's full reset procedure.

## Launch

From PowerShell, substitute the actual skill and task output directories:

```powershell
& '<skill-directory>\scripts\Clear-WindowsUpdateCache.ps1'
& '<skill-directory>\scripts\Clear-WindowsUpdateCache.ps1' -Apply -ResultDirectory '<task-output-directory>'
```

Preview does not request administrator access or stop services. An actual non-administrator launch uses `Start-Process -Verb RunAs -WindowStyle Hidden` with Windows PowerShell, the quoted script filename, and explicit arguments. ExecutionPolicy Bypass applies only to that subprocess, not a machine-wide policy change. UAC must be accepted by the user. Do not provide forbidden sandbox overrides in an environment that disallows them; ordinary Windows elevation is separate from tool sandbox permission.

The script records initial service states and restores only services that were running. It refuses intermediate service states or an active TiWorker/TrustedInstaller component installation. It pauses BITS and wuauserv with a bounded wait, rechecks the installer, and aborts if a paused service restarts during traversal. Do not stop or disable update watchdog/security services to force a retry.

## Observe

Poll the result file with short, bounded waits and give progress updates during long runs. A returned process ID or completed launcher only means the elevated process was launched. Result statuses are Running, Completed, Partial, Failed, or NeedsAttention. Check Started/Updated to avoid reading a previous run's result. A cancelled UAC launch does not write a new result.

Read `WindowsUpdateCleanup.log` for a failed run. A failure can occur after useful cleanup: report measured gain and incomplete status together. NeedsAttention includes service restoration failure and must be addressed before claiming completion. ReadErrors and FailedFiles produce Partial, even when traversal reaches the end. Recheck service states and actual drive free bytes independently after a terminal result.

Downloaded updates may be downloaded again. Do not clear DataStore, rename SoftwareDistribution, reset service permissions, erase update history, or run component repair merely to free disk space. Do not automatically delete pending.xml or act on a pending reboot marker; an installer process check is conservative and does not prove that every update is idle.
