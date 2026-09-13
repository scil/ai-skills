# What each harness loads — and where it stops

Verified 2026-09-13 on Windows 11 with Claude Code (desktop app, Opus 5) and Codex CLI 0.147. Re-verify with the probes below when a harness updates; the numbers are the part most likely to move.

| Dimension | Claude Code | Codex |
|---|---|---|
| Instruction file | `CLAUDE.md` at the repo root, `~/.claude/CLAUDE.md` user-level, nested `CLAUDE.md` in subdirectories; supports `@path` imports (absolute paths allowed) | `AGENTS.md` chain: global `~/.codex/AGENTS.md` (or `AGENTS.override.md`), then the repo root, then only the nested `AGENTS.md` files on the path from root to the working directory. No import syntax. `CLAUDE.md` means nothing to it. |
| Silent limit | none observed on file size (attention still thins) | `project_doc_max_bytes`, **32 KiB by default, combined across the chain, cut mid-sentence with no notice**. Set in `~/.codex/config.toml`; raising it restores text, not attention. |
| Skills | `.claude/skills/` (a symlink to `.agents/skills/` keeps one source), `~/.claude/skills/`, plugins; invocable as `/<name>`; descriptions always in context | `.agents/skills/` natively, `~/.codex/skills/`, `~/.agents/skills/`, plugin skills (e.g. the Expo plugin's `expo-upgrade`). Prints *"Skill descriptions were shortened to fit the skills context budget"* when the roster is too large — that line is a measurement. |
| Slash commands | `.claude/commands/<ns>/<name>.md` → `/ns:name` | none from the repo |
| Durable memory | auto-memory per project (`~/.claude/projects/<slug>/memory/`, index always loaded) | none — the repo must carry every project fact |
| Hooks | `.claude/settings.json` (`SessionStart`, `Stop`, …; `$CLAUDE_PROJECT_DIR`) | `.codex/hooks.json`, same event names and JSON decision protocol (`{"decision":"block","reason":…}`); `$(git rev-parse --show-toplevel)` for the path |
| Approval / sandbox | the harness prompts per tool by default | user config: `approval_policy`, `sandbox_mode` (`read-only` / `workspace-write` / `danger-full-access`); `[projects.<path>] trust_level` only — `sandbox_mode` is not a project-table key. A per-run `-s read-only` overrides. With `never` + `danger-full-access` nothing prompts and nothing is sandboxed: instructions are then the only behavioural layer. |
| Model selection | `~/.claude/settings.json` `model` | `~/.codex/config.toml` `model`; a model newer than the CLI fails with "requires a newer version of Codex" — override for one run with `-m <model>` rather than upgrading mid-task |
| Shell on Windows | PowerShell; the Bash tool may return empty output | PowerShell desktop shell |

## Probes

**What did the agent actually receive?** (no file reads allowed, so it can only answer from context)

```bash
codex exec -s read-only -c approval_policy="never" -c model_reasoning_effort="low" \
  "Do NOT read any files and do NOT run any commands. Answer only from the instructions already in your context. \
   (1) Name the LAST markdown heading in the project AGENTS.md text you received and quote its final sentence verbatim. \
   (2) Which of these headings are present: <list the file's sections>. \
   (3) Did you also receive a global AGENTS.md? Quote its first heading. \
   (4) Did the text end mid-sentence anywhere?"
```

For Claude Code, `/memory` in an interactive terminal lists the loaded instruction files; a session's injected instruction block is the other evidence.

**Where does the cut fall?** Measure, don't guess:

```powershell
$bytes = [IO.File]::ReadAllBytes('AGENTS.md'); $bytes.Length
$text = [Text.Encoding]::UTF8.GetString($bytes, 0, 32768); ($text -split "`n").Count   # line of the cut
```

**Is the skill roster over budget?** Run any `codex exec` and read stderr for the "shortened to fit" warning.

## Budgeting

- Budget the whole effective chain, not one file: `global ≤ 4 KiB` + `repo chain (root + nested on the cwd path) ≤ 28 KiB` = under the 32 KiB cap, for every directory an agent is started in.
- Guard it in the unit suite the project already runs on every change, with a self-test proving the measurer reads the real files (a guard that reads the wrong path passes forever). Pre-commit hooks are skippable and only fire when the file is staged.
- A one-line bridge for the other harness (`CLAUDE.md` = `@AGENTS.md`) stays one line: a rule written there is a rule the other agent never sees; let the guard assert that too.
