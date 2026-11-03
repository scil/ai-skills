last-checked: 2026-10-28 (Claude Code docs and platform docs, fetched that day)

# Claude Code configuration facts

Sources: `code.claude.com/docs/en/model-config#set-the-auto-compact-window`, `.../settings-reference#modelsettings`, `.../settings#settings-precedence`, `.../env-vars`; `platform.claude.com/docs/en/about-claude/models/overview`, `.../pricing#long-context-pricing`.

## Context windows (current models)

| Model ID | Context window | Default compaction point in Claude Code | Long-context price |
|---|---|---|---|
| `claude-fable-5-1` | 1M | ~967K | standard rate across 1M |
| `claude-opus-5-5` | 1M | ~967K | standard rate across 1M |
| `claude-sonnet-5-5` | 1M | ~967K | standard rate across 1M |
| `claude-haiku-5-5` | 1M | ~967K | higher price for any request whose prompt exceeds 100K tokens (cache reads and writes count) |

Legacy Opus 4.6 / Sonnet 4.6 run 200K unless the ID carries `[1m]`. `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` makes native-1M models compact at 200K.

## Auto-compact window

Ways to set it, strongest first:

1. `CLAUDE_CODE_AUTO_COMPACT_WINDOW` env var, 100000–1000000 tokens (`k`/`M` suffixes need v2.1.304+; a bare `200` means 200 tokens). Beats the flag, the command and the setting; `/autocompact` then reports the override without saving.
2. `claude --autocompact <value|auto>` for one launch; not preempted by managed settings.
3. `modelSettings.<model-id>.autoCompactWindow` — what `/autocompact` writes (v2.1.288+; earlier versions wrote the top-level key). Beats the top-level key in the same file for that model. The canonical ID also matches dated, `[1m]`, Bedrock and Vertex spellings.
4. Top-level `autoCompactWindow` — every model. Scope: any file.

Range 100K–1M, or `"auto"` for the tuned window; always capped at the model's context window. `/autocompact` and the flag accept `200000`, `500k`, `1M`, or a bare `100`–`1000` meaning thousands.

Choosing a value: every turn resends the whole context, so per-turn cost scales with it even when cached (cache reads cost 5% of input on Opus 5.5 and Sonnet 5.5, 2.5% on Fable 5.1); a smaller window compacts more often and keeps less detail. The user's chosen default (2026-10-28): top-level 300000, Haiku 5.5 at 100000 (its price threshold, also the minimum).

## Precedence

- Across files: managed > `--settings` > `.claude/settings.local.json` > `.claude/settings.json` > `~/.claude/settings.json`.
- Lists such as `permissions.allow` merge across files; `modelSettings` resolves one model at a time.
- Env vars are not a level: each pairs with its key separately (see the key's settings-reference entry).
- `modelSettings` and `effortLevel` are read at session start; most other keys reload on save.

## Checks

- `/status` → `Setting sources` line: which files loaded (not which file supplied each key).
- `claude doctor` → entries Claude Code rejected.
- The published schema `https://json.schemastore.org/claude-code-settings.json` can lag the newest keys; a schema warning on a documented key is not an error.
