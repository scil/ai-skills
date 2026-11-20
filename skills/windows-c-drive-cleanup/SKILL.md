---
name: windows-c-drive-cleanup
disable-model-invocation: true
description: Inspect and free space on the Windows C drive by removing verified temporary files and rebuildable caches, including administrator-assisted Windows Update download cleanup. Use for a full or nearly full C drive; preserve personal files, installed applications, and development environments.
---

# Windows C Drive Cleanup

A cache contains files an application can download or generate again. A Windows reparse point is a filesystem link, including junctions and symbolic links; following it can cross into unrelated folders or drives. UAC (User Account Control) is the Windows prompt used to grant administrator access.

## Inspect and select

1. Record C: free bytes before cleanup. Report GB as bytes / 1e9; GiB means bytes / 2^30. Keep units consistent.
2. Run `scripts/Inspect-CDrive.ps1`. It measures specific cache directories without following reparse points, reports age-eligible files, and identifies administrator access. It does not scan the whole drive. Missing directories are normal; read errors make estimates incomplete.
3. Inspect the largest candidates before deleting. Preserve Documents, Downloads, Desktop, source trees, installed programs, package stores, Windows Installer, WinSxS, recovery files, pagefile, and virtual disks. Emptying the Recycle Bin, uninstalling software, or moving personal files needs specific user authorization. A broad cleanup request supports removing verified stale temporary files and rebuildable caches.
4. Prefer the candidate with the largest useful gain and lowest disruption. Avoid scanning hundreds of thousands of unrelated files when targeted cache measurements already identify enough space.

## Clean user caches

Run `scripts/Clear-UserCaches.ps1` first without `-Apply`; its default is a read-only preview. Select categories with `-Categories Temp,Pip,CrashDumps,Pnpm,NuGet,Yarn`. These are a fixed allowlist under the current user's LOCALAPPDATA, not arbitrary paths. Supply `-Apply` for actual cleanup and `-ResultDirectory` pointing to the task's output directory.

The default `-MinimumAgeDays 7` preserves recent files. If it finds little eligible data, inspect dates and contents. For confirmed abandoned installer staging, one day can be appropriate after checking setup/installer processes. Do not automatically lower the age threshold or assume a running application's temporary data is expendable. Locked files are skipped; do not kill applications merely to delete them. Pnpm's `pnpm-cache` is a download/metadata cache, distinct from its package store; do not target stores or project node_modules without a separate reason.

## Clean Windows Update downloads

Read [references/windows-update.md](references/windows-update.md) before administrator cleanup. `scripts/Clear-WindowsUpdateCache.ps1` defaults to preview. With `-Apply -ResultDirectory <task-output-directory>`, it requests UAC access if necessary and runs hidden. The launching process exits before elevated cleanup finishes: a process ID is not proof of completion.

The script validates the fixed `C:\Windows\SoftwareDistribution\Download` target and all ancestors, rejects filesystem links, refuses an active component installer, pauses BITS (Background Intelligent Transfer Service, which transfers files in the background) and `wuauserv` (the Windows Update service), deletes only cache contents, and restores previously running services in `finally`. It does not reset update databases, permissions, or service configuration. Windows may download removed updates again.

Poll `WindowsUpdateCleanup-result.json` in the specified result directory. Check its timestamp belongs to this launch, its status is terminal, its errors/skipped counts, and service restoration. If UAC is rejected, stop this operation and report the rejection. If an update installer is active or a service cannot stop, do not force it; wait for the relevant state to change. Retry a failed run only after addressing its cause. An explicit request to write/request/run an administrator cleanup script authorizes that launch; do not seek redundant chat approval.

## Verify and report

Re-read C: free bytes after completion. The actual gain is free-after minus free-before, not the sum of file lengths. Hard links (multiple filenames sharing the same stored file), compression, and concurrent disk activity can make those figures differ. Distinguish a partial run from successful completion and confirm restored service states. Preserve logs and JSON results outside the skill repository; do not create UAC prompts merely to validate the skill.

For implementation details and the observed incident, read [references/operations-and-lessons.md](references/operations-and-lessons.md). Use PowerShell end to end for deletion; never pass enumerated paths to another shell. Scripts use .NET filesystem APIs with extended-length paths (`\\?\`) to handle names beyond 260 characters, validate containment, skip links, and remove only empty directories after deleting files.
