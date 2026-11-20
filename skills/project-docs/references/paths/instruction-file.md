# Path: the instruction file (AGENTS.md, CLAUDE.md)

Read this when you create, review or grow a repository's instruction file, root or nested. The principles in [`SKILL.md`](../../SKILL.md) apply. This file adds what is specific to the instruction file.

## What earns a line

Only what the repository cannot tell the agent. Both vendors say so: Anthropic — cut any line whose removal would not cause mistakes; keep pitfalls, rationale and conventions that differ from tool defaults, not directory layouts or dependency lists. OpenAI — short and accurate beats long and vague; add a rule only after a repeated mistake. Research agrees on the direction and is mixed on details ([`../refresh/sources-instruction-file.md`](../refresh/sources-instruction-file.md)): developer-written beats generated; unconditional testing instructions raise cost; a navigational map is contested, so it is a Pointers line, not a directory listing. A line earns its place by passing the admission threshold in [`../instruction-file/rules.md`](../instruction-file/rules.md): non-inferable, costly when wrong, repeated, a team agreement, an architecture boundary, or a verification requirement.

## One canonical file, one-line bridges

`AGENTS.md` is the shared source; `CLAUDE.md`, where one exists, is `@AGENTS.md` plus Claude-only lines. Claude Code ≥ v2.1.277 reads `AGENTS.md` directly when no `CLAUDE.md` or `CLAUDE.local.md` exists, so the bridge is needed only for Claude-only lines, a personal `CLAUDE.local.md`, or older versions ([`../instruction-file/harness/claude-code.md`](../instruction-file/harness/claude-code.md)). A rule written only in the bridge is a rule the other agent never sees.

## Enforcement and budget

Each rule names its layer: a hook, a CI check, a linter rule, a test, or the explicit tag `advisory`. Destructive-action policy sits at the top, short; the real brake is the sandbox and approval config — when the config is the problem, fix the config, not the prose.

Codex cuts the whole chain at 32 KiB silently; Claude Code has no cut but a 200-line target per file. Measure before and after; the harness table lives in [`../loading/harness-loading.md`](../loading/harness-loading.md), and what each harness does with the file's content in [`../instruction-file/harness/`](../instruction-file/harness/).

Guards are model-relative — a no-op for an agent that already behaves that way, load-bearing for one that does not — so write each for the agent that failed and prune it when no agent working here trips on it.

## Create

1. Refresh gate. Confirm no instruction file exists in the chain (`AGENTS.md`, `CLAUDE.md`, nested copies, `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`); if one does, switch to Review.
2. Learn the repo the way the agent will: manifest, lockfile, CI config, lint config, test runner, generated directories, migrations. Everything found here is *inferable* and stays out of the file.
3. Collect non-inferable facts: from the user, from `git log` of past corrections, from `CONTRIBUTING`, from any hook or CI check that encodes a rule. Offer, do not insert, the candidates in [`../instruction-file/stacks/`](../instruction-file/stacks/) that match the stack.
4. Fill [`../../templates/AGENTS.md`](../../templates/AGENTS.md): delete every section whose comment says the repo already answers it; keep the file under 4 KB and under 80 lines. Write [`../../templates/CLAUDE.md`](../../templates/CLAUDE.md) as the bridge when the bridge rule above needs one. Add a nested file ([`../../templates/AGENTS.nested.md`](../../templates/AGENTS.nested.md)) only for a subtree with rules that differ from the root.
5. Done when: every remaining line passes the admission threshold, names its enforcement layer or `advisory`, the byte count is reported, and the growth loop (grow by incident, prune by review) is stated in the file's maintainer comment.

## Review

1. Refresh gate. Measure: bytes of the chain per start directory, lines per file.
2. Walk [`../instruction-file/review-checklist.md`](../instruction-file/review-checklist.md) line by line against the file; verify each claim against the tree (`Test-Path` the paths, the command in the manifest, the tool in the lockfile).
3. Report one row per finding: line, defect, disposition (delete as inferable · delete as stale · reword · move to hook/CI/linter · move to a skill or `.claude/rules/` · keep). Apply only what the user approves.
4. Done when: the file passes the checklist, or the rows the user rejected are recorded with the reason.

## Update (grow from an incident)

1. Refresh gate. State the incident: what the agent did, what it should have done, how many times it has happened.
2. Test it against the admission threshold. A first occurrence is not a rule; a one-off is a prompt. A rule the harness can enforce becomes a hook or check first, and a one-line rule second.
3. Write it in the shape from `rules.md`: positive invariant, `Instance:` with date, enforcement layer. Place it in the root, a nested file, or a `.claude/rules/` path-scoped file by scope. Then ask the three PR questions of the whole file.
4. Done when: the rule is in one file only, the bridge (if any) still reads `@AGENTS.md`, the byte count is reported.
