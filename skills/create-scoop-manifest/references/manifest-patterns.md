# Scoop manifest patterns

Use these patterns as starting points. Inspect the actual release asset and neighboring manifests before choosing one.

## Package selection

| Asset | Preferred handling | Required evidence |
| --- | --- | --- |
| `.zip`, `.7z`, portable archive | Direct `url` and `hash`; add `extract_dir` only when needed | Archive listing and executable path |
| Squirrel `.nupkg` | Extract the package, commonly from `lib\\net45`, but never assume that directory | Archive listing, executable path, nested root |
| Inno Setup `.exe` | Set `"innosetup": true` | Installer positively identified as Inno Setup |
| MSI or NSIS installer | Follow a proven neighboring pattern or use verified silent installer/uninstaller commands | Package inspection and tested silent behavior |
| Raw portable `.exe` | Direct `url`, `hash`, `bin`, and/or `shortcuts`; set `extract_to` only if appropriate | File is the runnable application, not an installer |

Prefer portable assets because they avoid registry and external uninstaller state. Do not invent silent flags. A URL fragment such as `#/dl.7z` changes the cached filename and can force archive handling when Scoop cannot infer it; use it only when required and keep it in `autoupdate` too.

## Portable archive

```json
{
  "version": "1.2.3",
  "description": "Short factual description",
  "homepage": "https://example.com",
  "license": "MIT",
  "architecture": {
    "64bit": {
      "url": "https://example.com/app-1.2.3-windows-x64.zip",
      "hash": "<sha256>"
    }
  },
  "extract_dir": "app-1.2.3",
  "bin": "app.exe",
  "shortcuts": [
    [
      "app.exe",
      "App"
    ]
  ],
  "checkver": {
    "github": "https://github.com/owner/repo"
  },
  "autoupdate": {
    "architecture": {
      "64bit": {
        "url": "https://example.com/app-$version-windows-x64.zip"
      }
    }
  }
}
```

Omit `extract_dir` when the executable is already at the archive root. Omit `bin` for a GUI-only application unless exposing the executable on `PATH` is useful.

## Squirrel package

```json
{
  "version": "1.2.3",
  "description": "Short factual description",
  "homepage": "https://github.com/owner/repo",
  "license": "MIT",
  "architecture": {
    "64bit": {
      "url": "https://github.com/owner/repo/releases/download/v1.2.3/App-1.2.3-full.nupkg#/dl.7z",
      "hash": "<sha256>"
    }
  },
  "extract_dir": "lib\\net45",
  "shortcuts": [
    [
      "app.exe",
      "App"
    ]
  ],
  "checkver": {
    "github": "https://github.com/owner/repo"
  },
  "autoupdate": {
    "architecture": {
      "64bit": {
        "url": "https://github.com/owner/repo/releases/download/v$version/App-$version-full.nupkg#/dl.7z"
      }
    }
  }
}
```

`lib\\net45` is a common Squirrel layout, not a rule. Verify the package. The `#/dl.7z` fragment is optional when the local Scoop extractor already recognizes `.nupkg`.

## Hash handling

- Prefer a release API's SHA-256 digest when it is attached to the exact asset URL.
- Strip an API label such as `sha256:` when the bucket convention stores bare SHA-256 values.
- Otherwise download once and run `Get-FileHash -Algorithm SHA256`.
- Use an `autoupdate.hash` checksum URL only when upstream publishes a stable, machine-readable checksum file.
- Recompute the hash whenever the selected asset URL changes. Never copy the installer hash to a portable archive or another architecture.

## Persistence and install behavior

- Persist only app-relative files or directories that the packaged app actually reads.
- If the app writes to `%APPDATA%`, `%LOCALAPPDATA%`, or another external path and has no portable mode, document that path in `notes`; do not pretend an unrelated `persist` entry redirects it.
- Keep install scripts idempotent and quote `$dir` paths.
- Add an uninstaller only when the manifest performs an external installation. Pure archive installs normally need no uninstaller.

## Failure checks

- URL and hash refer to different assets.
- `innosetup` remains after switching the URL to `.zip`, `.7z`, or `.nupkg`.
- Shortcut or `bin` points to an executable that is absent after `extract_dir` is applied.
- `autoupdate` drops a tag prefix, architecture suffix, URL fragment, or filename component.
- GitHub `checkver` selects a prerelease when the manifest is intended to track stable releases.
- Local installation is performed without explicit authorization.

