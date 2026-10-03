---
name: fix-bugs
disable-model-invocation: true
description: Fix a defect and prove it is fixed. Use on a bug report, a failing test, a review finding, anything called broken, wrong, flaky or "does nothing" — and before reporting any change as working.
---

# Fixing a defect, and proving it

Not "make the symptom go away" — **make it impossible, and leave evidence that goes red if someone undoes the fix.** Work the phases in order. Stack and tool mechanics, keyed by the same section numbers: [`references/react-web.md`](references/react-web.md), [`references/openspec.md`](references/openspec.md); the incidents behind the rules: [`references/incidents.md`](references/incidents.md).

## 1. Find the requirement that binds

- Before editing a surface, read the rule that governs it: the design spec for UI, the behaviour spec for logic — including specs still sitting in proposed or unmerged changes, which bind but are not where the accepted ones live.
- A fix that contradicts an accepted requirement is a spec change: made in the spec first, not a quiet edit.
- A fix that touches a conditional database write, two paths over the same tables, a cache after a mutation, auth or visibility, a library hook beside a hand-written listener, or state seeded from a prop writes its pseudocode paragraph first and runs `code-plan-review` on it before the first edit; the incident that named the fix is usually an instance of a question there.

## 2. Fix the class, not the instance

A report names the instance it can see; your job is the rule. On the **second** finding of the same shape, stop patching: state the invariant in one sentence and ask where else it is violated right now. If the fix does not make that sentence true everywhere, it is still a patch. (Incident: the list row.)

- **Put the fix at the one statement that decides** — the narrowest point every route passes through to produce the outcome. Guarding the callers guards a list you never finish. (Incident: a decline closes a card.)
- **A class fix names its own scope**: every route, or the routes it holds for, by name. If you cannot say which, you are still looking at instances.
- **The tell is the diff**: a new `if` beside the last `if` is an instance fix.

## 3. Expect breakage in lines the diff does not contain

Two edits that are correct in themselves still leave untouched code wrong: **redefining a value** (a sentinel, a widened union — the type checker stays quiet) and **changing when code runs** (an initialiser or hook moved across an early return). Reading the diff cannot catch either; enumerate:

- Redefined value: grep every producer *and* consumer, list them, say what each now means; prefer one setter taking the full union.
- Moved code: what did it read at the old position that may not exist at the new one (a value captured once at start-up, a context read once, a dependency list)? Derive rather than seed.
- Removed or re-scoped signal: grep including tests; each hit either *asserts* it or *leans* on it — reroute the leaners through the real channel.
- Delete by exact text, never by line range.

## 4. Write a test that can fail

- **Revert check**: would it go red with the fix undone? If not, it asserts the implementation. (Incident: the overlay that tested itself.)
- **Layer check**: test at the lowest layer that can *observe* the defect. Logic, copy, state, wiring → unit or component test. Anything the emulated runtime does not model — layout, stacking, hit-testing, painted colour, real timing, a real database — → the real runtime. There, exercise it the way the user does (press coordinates, not elements) and assert both directions: the inert part stays inert, the real control still wins.
- **Reachable failure**: a guard nobody can reach equals no guard. Put a transaction's abortable step *after* the writes claimed all-or-nothing; for a teardown guard, start, suspend the async seam, tear down, release; for a boundary, test either side of the cap, never at it.

## 5. Test what the fix touches, once

- **While fixing**: only the test that reproduces the defect. Re-run it when you believe the fix is in, not after every edit.
- **When it passes, once**: typecheck, then the suite that owns each touched unit. If §4's layer check said real runtime, one end-to-end spec.
- **The full suite only when §3 gave you a reason**: the diff redefines a value, moves when code runs, changes a shared fixture, type or hook, or reads a new field where tests render against partial fixtures. No such reason, no full run. Lint and the whole end-to-end set are for the commit, not the fix loop.
- Before debugging a red you did not expect, `git stash` and re-run it on `HEAD`; red there too means pre-existing — report it, don't fix it.

Report which checks ran, which failed, what was left out and why. "Verified", "complete", "enforced" only when the evidence meets the word; otherwise "partial" plus the gaps, with requirement, task status and code kept consistent.
