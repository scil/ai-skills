# {{SUBTREE_NAME}} — rules that differ from the root

<!--
A nested AGENTS.md is loaded by Codex only when the agent starts in or below this directory, and is appended after the root file (closer wins).
Claude Code loads a nested CLAUDE.md when it reads files in this subtree.
It carries ONLY rules that differ from or add to the root. It never restates a root rule and never points sideways to another subtree.
Chain budget: root + this file (+ any file between) < 32 KiB for Codex.
-->

- {{SUBTREE_RULE}}. Instance: {{YYYY_MM_DD}}. Enforced by: {{LAYER_OR_advisory}}.
- Verification for changes here: `{{SUBTREE_CHECK_COMMAND}}`. Enforced by: CI job `{{JOB}}`.
