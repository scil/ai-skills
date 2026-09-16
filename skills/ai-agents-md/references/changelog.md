# Refresh changelog

Newest first. Each entry is written by the Refresh path (`refresh.md` §4); proposals are applied only after the user accepts them.

## 2026-09-15 — baseline

- Sources: 20 registered, fingerprints computed for the first time; 0 changed by definition.
- Verified today: 13 Claude Code claims from the Claude conversation against `code.claude.com/docs/en/memory` — 12 confirmed, 1 not found ("avoid 'always double-check'" has no official source; kept as an observed note in `harness/claude-code.md`). Codex chain, override, fallback, 32 KiB and concatenation order confirmed against `learn.chatgpt.com`.
- Exemplar reality check: `anthropics/claude-code` has no root `CLAUDE.md` (the Claude conversation named it as canonical); `supabase/supabase` carries the bridge pattern live (11-byte `CLAUDE.md`); `vercel/next.js` is 30 KB, within 2 KB of the Codex cap.
- Research: the ETH paper's exact deltas recorded in `sources.md`; the "150 lines / 20–23%" figure circulating in blogs is the paper's cost number attached to a line count the paper does not give — recorded as reported, not used.
- Proposals: none (initial build).

### 2026-09-15, second pass (user asked for more explanation and research on the six verdicts)

- Two of the six verdicts were revised against primary sources: "OpenAI ~100 lines" is true of the Harness-engineering repo (Lopopolo, 2026-02-11), not of `openai/codex`, so the claim stands; "avoid double-check" is official in the platform prompting docs for Opus 5 (over-verification, self-correction), Opus 4.5/4.6 (aggressive language) and Fable 5 (over-prescriptive older instructions), so the claim stands. Both first verdicts had searched the wrong corpus.
- A second study registered: Lulla et al. (arXiv 2601.20404), efficiency only, developer-written files, gpt-5.2-codex, −28.6% median runtime. Reconciled with Gloaguen et al. in `readme.md`; principle 1 in `rules.md` now carries both halves and the undocumented-repo qualification (+2.7% when repo docs are removed).
- `anthropics/claude-code` checked at tree level: 1,592 entries, no `CLAUDE.md`/`AGENTS.md` anywhere. The blog claim is invented, not merely stale.
- Six sources added (two papers/reports, three Anthropic prompting pages, one vendor guide). Fingerprints computed with `-Update`.
- Edits applied to `readme.md`, `rules.md` §1–2, `harness/claude-code.md`, `sources.md`.
