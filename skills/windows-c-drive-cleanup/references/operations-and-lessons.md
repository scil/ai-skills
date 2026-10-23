# Tools and observed lessons

## Inspection and deletion

- Use `Get-PSDrive C` or `[IO.DriveInfo]::new('C:\').AvailableFreeSpace` for actual free space. `Get-PSDrive` exposes byte counts; divide by 1e9 for GB. PowerShell's `1GB` constant means 2^30 bytes, so label that calculation GiB.
- Prefer targeted traversal of known cache directories. `Get-ChildItem -Recurse` can conceal permission problems and encounter filesystem links; the helper explicitly checks every ancestor and skips linked entries. A zero estimate with read errors is not proof of an empty directory.
- Use `Get-Service`, `Get-Process`, and the current Windows principal to inspect services, installers, and administrator status. Inspect large temporary entries' names, timestamps, and related processes before shortening retention.
- Use .NET filesystem APIs on extended-length absolute paths for large trees. `\\?\C:\...` avoids the traditional 260-character limitation on this Windows PowerShell/.NET runtime. Check each deletion stays below the validated target; never recursively delete the computed root. Remove only empty subdirectories afterward. Do not follow reparse points or clear read-only attributes to force removal.
- PowerShell `Get-ChildItem`, `[IO.FileInfo]`, and logs can report logical file sizes. Those are selection estimates, not guaranteed reclaimed bytes. Hard links, compression, and concurrent writes affect actual gain. Never assume sparse virtual disks can be reclaimed by deleting their contents from Windows.
- Run operations in one shell. Do not enumerate in PowerShell and construct cmd.exe or Bash deletion commands. Quote arguments for the actual target process; JSON string escaping is not shell argument escaping. Use editor tools for script edits and PowerShell parsing for syntax checks.

## Validate changes without another live cleanup

Use the skill-creator frontmatter validator when available and parse every `.ps1`/`.psm1` with `System.Management.Automation.Language.Parser.ParseFile`. Then run:

```powershell
& '<skill-directory>\scripts\Test-CacheTools.ps1' -SandboxDirectory '<scratch-directory-on-C>'
```

The test creates a uniquely named scratch tree. It checks preview preservation, stale versus recent files, a path longer than 260 characters, locked-file handling, a junction whose target must survive, rejection of linked ancestors and drive roots, guard aborts, progress callbacks, the category allowlist, and read-only wrapper behavior. Test artifacts remain in the supplied scratch directory for inspection; no real cache is deleted and no UAC request is made. This does not test the complete elevated service-stop/restore workflow. The original administrator script was run successfully in the recorded incident; its reusable version should not be described as newly proven by a privileged run unless that run actually occurred.

## Case recorded on 2026-10-07

The inspected Windows C: volume had about 0.56 GB free. Temporary data, package caches, and crash logs yielded about 8.01 GB, taking free space to 8.57 GB. Most temporary files were newer than seven days, including abandoned Visual Studio installer files from three days earlier. After inspecting the staging files and confirming no setup process, cleanup used a one-day threshold. This does not justify using one day everywhere.

The Windows Update download cache's logical size was approximately 17.65 GB. Administrator cleanup initially stopped on a path over 260 characters and restored the original service states. The file still existed; testing `GetAttributes` with the extended-path prefix confirmed the diagnosis. The corrected run completed. Free space reached 21.29 GB, a measured total gain of 20.73 GB. The administrator phase's net gain was approximately 12.73 GB, smaller than the sum of removed file lengths; the specific storage cause was not measured.

Reusable lessons: implement long-path support before deletion, preserve service restoration on every exit, retain partial progress, wait for elevated work to finish, and report measured free-space gain rather than equating cache size with reclaimed space. These figures are an observed example, not a promise for another machine.
