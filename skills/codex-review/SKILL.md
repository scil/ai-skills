---
name: codex-review
disable-model-invocation: true
description: Review a change with the codex CLI and iterate until it reports nothing. Use whenever a change is ready for an independent review, when the user asks for a codex review, or when a change is substantial enough to warrant a second reader. Covers invoking codex safely (it can commit your tree), scoping and speeding up a round, verifying each finding before acting on it, and the default loop of review → fix → re-review until the change comes back clean.
---

# Reviewing with codex

## The default is a loop, not a single pass

**Review, fix, review again — until a round reports nothing in the change.** One pass is not a review; it is a sample. In practice each round surfaces only its top handful of findings, and fixing those exposes the next layer. A recent shelf-row change took nine rounds to converge, and rounds 6–9 were all real defects that round 1 never mentioned.

Stop when a round returns no findings **that belong to the change**. Findings about files outside the diff are reported to the user, not silently fixed (see [Findings that are not yours](#findings-that-are-not-yours)).

### A loop that will not converge is telling you about the design

Budget it: roughly **five rounds, then a confirming round**. Past that, stop reviewing and re-read the design, because a loop that keeps producing findings is rarely a change with many small faults — it is usually one wrong decision generating them.

Measured, and the reason this section exists: a confirmation-flow change took **22 rounds and ~45 findings**, of which about **30 were a single class** (state describing the current user going stale) and **two** were defects no amount of self-review would have found. The class traced to one decision made before any code was written — moving a branch that needed to know "is this reader signed in" from the server to the client. Every stale-state finding was a consequence. Nine rounds of patching instances did not touch it.

So the cheapest round is the one that reviews the **design**. When a change has a written design (an openspec `design.md`, an ADR, a plan), review that *before* implementing:

```bash
codex exec -s read-only "Review openspec/changes/<name>/design.md as a design, not as prose. What will be hard to get right, and what will keep going wrong?"
```

Ten minutes there is worth more than any later round: at that point the fix is a paragraph, not a refactor across a dozen files with tests to re-prove.

## Before the first round

Run the local gate first. A review round costs minutes of wall clock; a failing unit suite costs seconds to find yourself, and spending a round on it wastes the round *and* delays the findings only codex will catch:

```bash
pnpm -F @porch/tanstack-start typecheck && pnpm -F @porch/tanstack-start lint && pnpm -F @porch/tanstack-start test
```

**Run it unfiltered, and run it over every package the change touches.** A filter may add context; it may never drop a line. Piping the gate through `| Select-Object -Last 5` or `| Select-String "passed"` is how a lint error and a typecheck error both reached codex in one session and cost a round each — the command exits non-zero, the summary line says nothing, and a filtered tail shows only the tests that passed. If you want a summary, tee the whole output to a file and search that:

```bash
pnpm -F <pkg> typecheck 2>&1 | Tee-Object gate.log ; Select-String -Path gate.log -Pattern "error"
```

Narrowing the gate to "the package I edited" fails the same way, and more quietly: a change lands in the app, and the API package it imports from stops compiling.

## Invoking it

**Always pass a read-only sandbox.** This machine's `~/.codex/config.toml` sets `approval_policy = "never"` with `sandbox_mode = "danger-full-access"`, which gives the review agent an unrestricted shell — it has used it to **commit the working tree unprompted**. A silent commit also empties `--uncommitted`, so the next round reviews nothing and reports clean for the wrong reason.

```bash
codex review --uncommitted \
  -c model_reasoning_effort="medium" \
  -c sandbox_mode="read-only" \
  -c approval_policy="never"
```

- `sandbox_mode=read-only` is what actually blocks writes and git. Keep `approval_policy=never` rather than `on-request`: a non-interactive run auto-denies escalation instead of stalling on a prompt nobody can answer.
- **After every run, check `git log --oneline -3` and `git status`** before trusting either.
- Review a specific commit with `--commit <sha>` (works on a dangling commit, e.g. after `git reset --soft`). `--uncommitted` and a `[PROMPT]` argument are **mutually exclusive**, so custom instructions cannot be combined with either flag — use `codex exec` for a scoped review.
- An invalid `-c` value aborts at config load in about a second (`Error loading config.toml`), so trying a setting is cheap. `windows.sandbox` accepts only `elevated`/`unelevated`.
- The user's shorthand: **"sol" is the model `gpt-5.6-sol`; "Extra high" is `model_reasoning_effort=xhigh`.**
- Driving another agent "through herdr" only works from inside a Herdr pane — check `$HERDR_ENV` first. It is unset in this process, so call `codex` directly and say so.

## Making rounds faster

Effort and scope are the two levers that matter.

- **Pick the STARTING tier from what the change touches, before layering by round.** The two rules are orthogonal: this one sets where you start, the next one says where you go.
  - **Copy, a single file, no control flow** → one `medium` round. If it comes back clean, stop: there is no confirming round to schedule, because there is nothing an expensive reader could find that a cheap one could not.
  - **Ordinary feature work** → start `medium`, per the layering below.
  - **Concurrency, cache coherence, auth or permissions, migrations, money, or a cross-platform contract** → start at `high`. These carry defects a cheap pass reads straight past. Measured: two `medium` passes over an availability change missed that "newest write wins" compared `submittedAt` with `>` — a same-millisecond tie kept the OLDER write and resurrected a stale receipt. An `xhigh` round found it. A tier that cannot see the defect is not cheap, it is a wasted round.
  - **`xhigh` is an escalation, not a starting point.** Earn it: the lower tiers are repeating the same SHAPE of finding, or the change spans several of the risky surfaces above at once.
- **Cost is roughly 3× per step up** (63k / 73k / 238k / 203k output tokens across four rounds of one change). The confirming round is worth that on a risky change and is pure waste on a copy edit — which is the whole reason to pick the starting tier deliberately.
- **Leave the model alone unless the user names one.** Effort is the lever that pays; swapping models mid-loop changes what "the last round said" means.
- **Layer the reasoning effort.** `xhigh` is the slowest tier and early rounds rarely need it — the first rounds surface crashing tests, missing keys, overflow, plural forms. Run `medium` early and reserve `xhigh` for the confirming round.
- **Run narrow passes in parallel** instead of serial general ones. Three concurrent four-minute passes with distinct remits (accessibility / i18n / correctness) beat one twelve-minute general pass and surface more per round.
- **Feed the diff rather than letting it explore.** Much of a round goes into re-running `git status`, grepping locale files and dumping line ranges. `codex exec` takes a prompt, so it can be given the diff and an explicit file list:

  ```bash
  git diff --cached > review.diff
  codex exec -s read-only "Review review.diff. Read only the files it touches; do not explore the rest of the repo."
  ```

- **Middle rounds can review the increment** (`git diff <last-reviewed-sha>`) rather than the whole change, with one full pass at the end.
- `codex exec --output-schema <file>` fixes the response shape when the findings are being parsed rather than read.

## Verify each finding before acting on it

Codex is a strong reader but not an oracle. Check the claim against the code yourself — the fix is yours to justify:

- **Confirm the mechanism**, not just the conclusion. Run the failing test, open the cited spec line, measure the contrast, press the pixel. Several findings in the shelf-row review were exactly right about a defect and slightly wrong about why.
- **Where a finding cites a rule**, open the rule. Findings citing `AGENTS.md`, `brand-design-spec.md`, `plan.md` or an openspec delta were all correct there — and each was cheaper to confirm than to argue about.
- **Where you disagree, say why, in the report.** A finding that conflicts with an explicit user instruction (a named design token, a chosen layout) is a decision for the user, not something to quietly override. State the measurement, state the trade-off, and offer the revert.
- **A finding you fix needs the same proof as any other defect** — a regression test that would go red without the fix, at a layer that can observe it.

## Findings that are not yours

Codex reviews the working tree, not strictly the diff. In one session it flagged the same untracked, globally-gitignored `.vscode/launch.json` in three separate rounds.

Before acting on a finding, check it belongs to the change:

```bash
git diff --cached --name-only          # is the file even in the change?
git log --oneline -1 -- <path>         # does it have history?
git check-ignore -v <path>             # is it ignored, i.e. not shippable?
```

If the file is outside the change: **report it to the user with what you verified, and leave it alone.** Widening the diff to satisfy a review is how an unrelated regression enters a focused change. A finding on an ignored file cannot be committed at all.

Such a finding never blocks convergence — the loop ends when nothing in the change is left.

## The trap that costs the most rounds

A review names the **instance** it can see. Fixing exactly the region named, round after round, is what turns a three-round review into a nine-round one: in the shelf-row case, four consecutive rounds each reported a different dead click region, and each patch created the next one. On the **second** finding of the same shape, stop fixing the instance and find the rule that makes the whole class impossible.

Two things make this harder to obey than it reads:

- **The class wears a different costume every round**, so the shape is easier to see in your own notes than in the findings. "Stale after sign-in", "stale after navigating away", "stale across language variants", "stale after the session expires" arrive over four rounds looking like four bugs. Keep a one-line tally of what each round was ABOUT; when two lines rhyme, the next round is structural.
- **Saying "this is the class fix" is not doing one.** The tell is what the patch touches: a class fix removes the possibility (key the component so stale state cannot survive; move the value out of the shared cache; tag in-flight work with a generation), where an instance fix adds a condition at the site named. If the diff is another `if` next to the last `if`, it is an instance fix wearing the word "structural".

And when the structural move lands, **spend that round on it alone**. Mixing it with two more instance patches makes the next round's findings unattributable — you cannot tell what the structure fixed and what it did not.

