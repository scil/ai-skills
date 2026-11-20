---
name: ai-harness
disable-model-invocation: true
description: Set or review a coding harness's own configuration — Claude Code settings.json (model, modelSettings, autoCompactWindow, effort, env, permissions) and the equivalent Codex config — so each key sits in the right scope, wins where intended, and matches the vendor docs.
---

# Harness configuration: set and review

Hand-offs: which instruction files and skills a harness loads, their byte budgets, and the content of `AGENTS.md` / `CLAUDE.md` → project-docs; a permission rule that encodes a project rule → project-docs decides whether it belongs in the file or the config.

A **harness** is the program that runs the model (Claude Code, Codex CLI). Its **configuration** is the settings it reads from files, flags and environment variables. A **scope** is the file a key lives in (user, project, project-local, managed), which decides who it reaches and what overrides it.

## Principles

1. **Vendor docs decide; the binary is the last resort.** Read the official page for the key before setting it: Claude Code at `code.claude.com/docs/en/settings-reference`, `.../settings`, `.../model-config`, `.../env-vars`. Grep the installed binary (`grep -aoE '.{0,200}<key>.{0,200}'`) only when the docs are silent, and label such a claim `[binary]` with what it does not prove. A text editor shows a binary as noise; never save one from an editor.
2. **A slash command may save narrower than you think.** Commands write to a scope of their own choosing: `/autocompact` and `/effort` save per model under `modelSettings`, not for every model. After any command that saves a setting, read the file it wrote and say which key and scope it used.
3. **Facts are dated.** [`references/claude-code.md`](references/claude-code.md) carries `last-checked`. If it is more than 30 days old, re-fetch the pages it cites before relying on a number (context windows, ranges, prices change with each release).

## Paths

### Set a key

1. Find the user scope file: `~/.claude/settings.json`, or the directory in `CLAUDE_CONFIG_DIR` if that one variable is set. Read the file in full; never dump or list environment variables.
2. Look the key up (principle 1). Record its scope column, range, and what overrides it.
3. Edit with the editor tool; keep strict JSON (no comments, no trailing commas). Apply principle 4 to existing copies.
4. Validate: `node -e "JSON.parse(require('fs').readFileSync(process.argv[1],'utf8'))" <file>` exits 0.
5. Done when: the file parses, the report names the key, the scope, the value per model it now resolves to, and anything that still overrides it (another scope, an env var, a flag), and tells the user to confirm with `/status` (sources loaded) and `claude doctor` (rejected entries).

### Review a configuration

1. Read every scope file that exists: user, the project's `.claude/settings.json` and `.claude/settings.local.json`, and check `/status` for a managed source.
2. For every key: is it documented (principle 1)? Is its value in range? Is it in a scope that can set it (the settings index's Scope column)? Is it shadowed by a narrower or higher scope (principles 3–4)?
3. Check the model-dependent keys against [`references/claude-code.md`](references/claude-code.md): compaction window versus each model's context window and pricing threshold, effort level versus the model's supported levels.
4. Report one row per finding: key, file, defect (undocumented · out of range · wrong scope · shadowed · duplicate · stale), proposed change. Apply only what the user approves.
5. Done when: every key in every scope file has a row or is listed as checked-clean.

### Codex

Codex reads its own config (`~/.codex/config.toml` and per-project files). No Codex facts are recorded here yet: before setting a Codex key, fetch the Codex configuration docs, then add the verified, dated facts to a new `references/codex.md` in the same shape as the Claude Code file.
