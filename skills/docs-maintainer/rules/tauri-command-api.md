# Tauri Command API Rule

For Tauri desktop apps, treat `#[tauri::command]` functions as a provided API boundary between frontend and backend. The facts of record are the command handlers (usually `src-tauri/src/lib.rs`), the frontend wrapper (such as `src/tauri-api.ts`), and the shared request/response types.

Prefer a generated command index under `docs/generated/api` (layer 3): command name · group by domain · payload and return type sources · whether it mutates filesystem, config, profile, shell, hardware or network state. Generate it from the handler attributes and shared types; record the generator command in the file; let CI diff it.

Write by hand only what a generator cannot know, as a short section in the security quality-attribute doc: which commands need admin or permission checks, which show a preview or confirmation before acting, which are destructive and how they are guarded. Link to config, recovery and testing owners rather than restating them.

When a Tauri command signature, payload, return type, side effect, or safety behaviour changes, update in the same change:

1. the handler, the frontend wrapper and the shared types;
2. the generated command index (regenerate);
3. the hand-written safety notes when the guard or confirmation behaviour changed;
4. the tests that prove the guard.

Do not hide Tauri commands in the architecture overview or the repo map: architecture may explain the boundary, the generated index owns the surface, the repo map owns code locations.
