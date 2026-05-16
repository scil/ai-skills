# Tauri Command API Rule

For Tauri desktop apps, treat `#[tauri::command]` functions as a provided API boundary between frontend and backend.

Document Tauri Commands under `docs/api.md` for compact projects or `docs/api/tauri-commands.md` when the app has more than a few commands or when commands mutate files, config, profiles, shell state, hardware, network state, or other local resources.

The Tauri command API doc should include:

- API direction: Provided API.
- Transport: Tauri `invoke`.
- frontend wrapper file, such as `src/tauri-api.ts`;
- backend handler file, usually `src-tauri/src/lib.rs`;
- payload/return type sources, such as frontend shared types and Rust request structs;
- command groups by domain;
- whether each command mutates filesystem/config/state;
- admin, permission, preview/confirmation, and safety notes;
- links to config, security, runbook, or testing docs instead of duplicating those details.

When a Tauri command signature, payload, return type, side effect, or safety behavior changes, update:

1. `docs/api.md`, `docs/api/tauri-commands.md`, or the nearest API section;
2. frontend wrappers;
3. shared frontend types;
4. relevant security, config, testing, or runbook docs when behavior changes.

Do not hide Tauri Commands only in architecture or repo-map docs. Architecture may explain the boundary; `docs/api/` owns the interface contract; repo-map owns code locations.
