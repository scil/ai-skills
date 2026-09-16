---
name: scil:create-scoop-manifest
disable-model-invocation: true
description: Create, update, and validate Scoop package manifests (`.json`) for Windows applications. Use when Codex needs to add an app to a Scoop bucket, package a GitHub release or other Windows download for Scoop, repair a manifest's URL/hash/extraction rules, add `checkver` and `autoupdate`, or locally verify a manifest when explicitly requested.
---

# Create Scoop Manifest

Create a maintainable manifest from verified release facts, then validate the JSON, package layout, hash, and update rules.

## Workflow

1. Inspect the target.
   - Read repository instructions and inspect neighboring manifests before editing.
   - Check Git status and preserve unrelated worktree changes.
   - Derive the app ID and filename from bucket conventions; use lowercase unless the bucket consistently does otherwise.
   - Treat manifest creation as authorization to research releases, download assets for inspection or hashing, and write the requested JSON. Do not install, uninstall, launch, or replace an existing app unless the user also requests it.

2. Resolve release facts from primary sources.
   - Prefer the vendor's release page, API, checksums, license, and source repository.
   - Select the latest stable release unless the user requests a prerelease, nightly, or pinned version.
   - Record the exact version, tag, asset name, architecture, download URL, size, and upstream digest.
   - Map `x64`, `x86_64`, and `amd64` to Scoop `64bit`; map `x86` and `ia32` to `32bit`; map `aarch64` and `arm64` to `arm64`.

3. Choose and inspect the package.
   - Prefer a portable archive when upstream provides one.
   - Otherwise inspect `.nupkg`, Inno Setup, MSI, NSIS, or other installers instead of guessing their internal layout or silent flags.
   - List archive contents and confirm the executable, `extract_dir`, shortcut target, CLI entry points, and portable data directory.
   - Load [references/manifest-patterns.md](references/manifest-patterns.md) when selecting an installer pattern, handling persistence, or writing nontrivial extraction steps.

4. Build the manifest.
   - Match the target bucket's indentation, field ordering, and architecture structure.
   - Use the version without a leading release-tag `v` unless the upstream version genuinely includes it.
   - Use the upstream SHA-256 digest only when it belongs to the exact selected asset; otherwise download the asset and compute its hash.
   - Include accurate `description`, `homepage`, and SPDX `license` data.
   - Add only verified `bin`, `shortcuts`, `persist`, extraction, and install/uninstall behavior.
   - Add `checkver` and `autoupdate` whenever releases are discoverable. Ensure the autoupdate URL reproduces the selected asset name for a different version.
   - Never retain a hash, `innosetup`, `extract_dir`, or install script after changing to an incompatible asset type.

5. Validate before reporting completion.
   - Parse the JSON and run the bundled validator:

     ```powershell
     pwsh -File <skill-dir>/scripts/validate_manifest.ps1 -Path <manifest-path> -Checkver
     ```

   - Omit `-Checkver` only when the manifest intentionally has no version check or Scoop is unavailable.
   - Confirm archive paths against the real extracted package, especially for nested `.nupkg` layouts.
   - If the user explicitly requested local installation, run `scoop install <absolute-manifest-path>` and verify the installed version, executable, and shortcut. Do not launch the GUI unless asked.
   - Review the final Git diff and ensure only intended files changed.

## Completion report

Report the manifest path, packaged version and architecture, selected upstream asset, validation performed, and installation state. Call out any upstream limitation, unverified silent installer behavior, external application-data path, or pre-existing dirty bucket state.


