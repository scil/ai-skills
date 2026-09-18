---
name: codex-review
disable-model-invocation: true
description: Review a change with the codex CLI and iterate until it reports nothing. Use whenever a change is ready for an independent review, when the user asks for a codex review, or when a change is substantial enough to warrant a second reader. Covers invoking codex safely (it can commit your tree), scoping and speeding up a round, verifying each finding before acting on it, and the default loop of review → fix → re-review until the change comes back clean.
---

# Reviewing with codex

## The default is a loop, not a single pass

- **Review, fix, review again — until a round reports nothing in the change.** One pass is a sample: each round surfaces its top handful of findings, and fixing those exposes the next layer.
- Stop when a round returns no findings **that belong to the change**. Findings outside the diff are reported, not fixed ([below](#findings-that-are-not-yours)).
- **Budget five rounds, then a confirming round.** Past that, stop reviewing and re-read the design: a loop that keeps producing findings is rarely many small faults — it is usually one decision generating them, and patching instances never touches it.
- **The cheapest round reviews the design.** When the change has a written design (a design doc, an ADR, a plan), review it *before* implementing; at that point the fix is a paragraph, not a refactor with tests to re-prove:

  ```bash
  codex exec -s read-only -c model="gpt-5.5" "Review <design file> as a design, not as prose. What will be hard to get right, and what will keep going wrong?"
  ```

## Before the first round

Run the project's local gate (typecheck, lint, unit tests) over **every package the change touches**, **unfiltered**. A round costs minutes; a failing suite costs seconds to find yourself. Piping the gate through a tail or a `Select-String "passed"` hides a non-zero exit behind the tests that passed — tee the whole output to a file and search that:

```bash
<gate command> 2>&1 | Tee-Object gate.log ; Select-String -Path gate.log -Pattern "error"
```
## Invoking it

**Always pass a read-only sandbox.** A full-access sandbox gives the review agent an unrestricted shell, and it has used it to **commit the working tree unprompted** — which also empties `--uncommitted`, so the next round reviews nothing and reports clean for the wrong reason.

```bash
codex review --uncommitted \
  -c model="gpt-5.5" \
  -c model_reasoning_effort="medium" \
  -c sandbox_mode="read-only" \
  -c approval_policy="never"
```

- **Always pass `-c model="gpt-5.5"`** (also on `codex exec`). The config default is `gpt-6-astra`, which is left for interactive work: a review round is a token-heavy read, and the GPT-6 tier spends far more per round for findings the 5.5 tier reaches. Since 2026-09-18 the installed CLI also rejects `gpt-6-astra` outright, so a round without the override is wasted. `codex review` has no `-m` flag; the model goes through `-c`.
- `sandbox_mode=read-only` is what blocks writes and git. Keep `approval_policy=never` rather than `on-request`: a non-interactive run auto-denies escalation instead of stalling on a prompt nobody can answer.
- **After every run, check `git log --oneline -3` and `git status`** before trusting either.
- Review a specific commit with `--commit <sha>` (works on a dangling commit, e.g. after `git reset --soft`). `--uncommitted` and a `[PROMPT]` argument are **mutually exclusive** — use `codex exec` for a scoped review with custom instructions.
- An invalid `-c` value aborts at config load in about a second, so trying a setting is cheap. `windows.sandbox` accepts only `elevated`/`unelevated`.
- Stay on `gpt-5.5` unless the user names another model; effort is the lever that pays, and swapping models mid-loop changes what "the last round said" means.

## Making rounds faster

Effort and scope are the two levers.

- **Pick the starting tier from what the change touches:**
  - Copy, a single file, no control flow → one `medium` round; clean means done, no confirming round.
  - Ordinary feature work → start `medium`.
  - Concurrency, cache coherence, auth or permissions, migrations, money, a cross-platform contract → start `high`. These carry defects a cheap pass reads straight past (a `>` where `>=` was needed on a same-millisecond tie survived two `medium` rounds and fell to `xhigh`). A tier that cannot see the defect is not cheap; it is a wasted round.
  - `xhigh` is an escalation, not a starting point: earn it when lower tiers repeat the same *shape* of finding, or the change spans several risky surfaces at once.
- **Cost is roughly 3× per step up**, so the confirming round is worth it on a risky change and pure waste on a copy edit.
- **Layer the effort**: `medium` early (crashing tests, missing keys, overflow, plural forms), `xhigh` for the confirming round.
- **Run narrow passes in parallel** (accessibility / i18n / correctness) instead of one long general pass; they surface more per round.
- **Feed the diff rather than letting it explore** — much of a round otherwise goes into `git status`, greps and line dumps:

  ```bash
  git diff --cached > review.diff
  codex exec -s read-only -c model="gpt-5.5" "Review review.diff. Read only the files it touches; do not explore the rest of the repo."
  ```

- **Middle rounds review the increment** (`git diff <last-reviewed-sha>`); one full pass at the end.
- `codex exec --output-schema <file>` fixes the response shape when findings are parsed rather than read.

## Verify each finding before acting on it

Codex is a strong reader, not an oracle; the fix is yours to justify.

- **Confirm the mechanism**, not just the conclusion: run the failing test, open the cited line, measure, press the pixel. Findings are often right about the defect and slightly wrong about why.
- **Where a finding cites a rule, open the rule.** Confirming is cheaper than arguing.
- **Where you disagree, say why, in the report.** A finding that conflicts with an explicit user instruction (a named token, a chosen layout) is the user's decision: state the measurement and the trade-off, offer the revert.
- **A finding you fix needs the same proof as any other defect** — a regression test that goes red without the fix, at a layer that can observe it.

## Findings that are not yours

Codex reviews the working tree, not strictly the diff, so it flags untracked and ignored files too. Before acting on a finding, check it belongs to the change:

```bash
git diff --cached --name-only          # is the file even in the change?
git log --oneline -1 -- <path>         # does it have history?
git check-ignore -v <path>             # is it ignored, i.e. not shippable?
```

Outside the change: **report it with what you verified, and leave it alone.** Widening the diff to satisfy a review is how an unrelated regression enters a focused change; a finding on an ignored file cannot be committed at all. Such a finding never blocks convergence.

## The trap that costs the most rounds

A review names the **instance** it can see. Fixing exactly the region named, round after round, turns three rounds into nine. The full rule is `fix-bugs` §2; what the loop adds:

- **The class wears a different costume every round** ("stale after sign-in", "stale after navigating away", "stale across variants"), so the shape is easier to see in your own notes than in the findings. Keep a one-line tally of what each round was *about*; when two lines rhyme, the next round is structural.
- **When the structural move lands, spend that round on it alone.** Mixed with two more instance patches, the next round's findings are unattributable.
