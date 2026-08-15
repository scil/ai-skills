---
name: fix-bugs
description: Fix a defect and prove it is fixed. Use when acting on a bug report, a failing test, a review finding, or anything described as broken, wrong, flaky, or "does nothing" — and whenever a change is about to be reported as working. Covers locating the real class of defect, avoiding the breakage a fix causes in untouched code, writing a test that can actually fail, choosing the layer that can observe the defect, and running the local gate before claiming the fix works.
---

# Fixing a defect, and proving it

## Scope

Not "make the symptom go away" — **make the symptom impossible, and leave behind evidence that would go red if someone undid it.**

Most of the cost in this repo has come from the second half. Fixes land quickly; what takes the time is fixes that were verified by something that could not have failed, patched one symptom at a time, or broke code the diff never touched. Work the phases in order.

## 1. Learn what governs the area before editing it

Rules already written down in this repo, discovered late, have each cost a full review round trip. Before editing a product surface, open:

1. `AGENTS.md` — repo map and standing rules (OpenSpec-first for functional decisions; degraded paths must report what happened).
2. `docs/4. Claude Design/brand-design-spec.md` — spacing scale, radii, **44×44 minimum tap target**, and the intended role of each palette token.
3. `docs/2. plan/plan.md` — the domain model, when the change touches product vocabulary. Terms are precise here: e.g. **Help is the offer side; an Ask is the separate inverse-direction broadcast** (§9), and confusing them inverts what a screen says.
4. `openspec/changes/*/specs/<capability>/spec.md` for the capability being touched — `grep` the capability name. **An unarchived change's delta is not in `openspec/specs/`**, so searching only the main specs finds nothing while the requirement still binds.

If the fix contradicts an accepted requirement, that is a real conflict: it needs its own OpenSpec change with a MODIFIED delta, not a quiet code edit.

## 2. Fix the class, not the instance

A report names the **instance** it can see. Your job is the **rule**.

On the **second** finding of the same shape, stop patching and enumerate: *what is the invariant, and where else is it violated right now?* State the invariant in one sentence; if the fix does not make that sentence true everywhere, it is still a patch.

Worked example — the owner shelf row, where "this part of the row looks pressable and does nothing" was reported four times running: the status line, then the bottom gutter, then the same gutter moved to a wrapper that still was not the opener, then the space above and below the centred `⋯` on a tall row. Each patch moved padding around and created the next dead strip. The fix that ended it was structural — one transparent pointer layer over the whole row, everything beneath it `pointer-events-none`, only the real controls re-enabled above — and it was available at the first report.

Related trigger: a third patch to one seam, or a guard that needs a paragraph to explain, means stop and look for the thing that makes the whole class impossible.

## 3. Expect the breakage in lines your diff does not contain

Two edits are correct in themselves and still leave *other, unmodified* code wrong:

- **Redefining a value** — adding a sentinel, widening a union, splitting one state in two. The type checker stays quiet: the old value is still a valid value.
- **Changing when code runs** — moving a hook or call across an early return or out of a branch. Still valid code, different mount timing.

Reading the diff cannot catch either. The check is an **enumeration**, not a re-read:

- Redefining a value: grep every producer *and* consumer, and write the list out; for each, say what it now means. Prefer making the drift impossible (one setter taking the full union) over auditing call sites.
- Moving when something runs: ask what it read at the old position that may not exist at the new one. `useState(initialValue)`, anything reading a prop or context once, and deps arrays assuming a resolved value are the classic casualties. **Prefer deriving over seeding** — a derived value cannot be stale.
- Removing or re-scoping a signal: grep the whole repo including tests, and for each hit ask "was this *asserting* the behaviour, or *leaning* on it?" Tests that leaned on it must be rerouted through the real product channel.

Two more ways a fix quietly breaks something:

- **Delete by exact text match, never by index range.** Slicing between two landmarks takes whatever sat between them, and a clean typecheck is not evidence the right lines went — what vanishes is often runtime code and a wrapper. If a block is too long to quote comfortably, delete it in named pieces.
- **Confirm a suspicious red is pre-existing** by `git stash`ing your change and re-running, before debugging your own diff.

## 4. Write a test that can fail

Two checks, applied to every regression test:

**The revert check.** Would this go red if the fix were undone? If the answer is "nothing I would plausibly write turns this red", the test asserts the implementation rather than the behaviour. A UI fix here shipped green and broken because the test reached into the DOM for the overlay just added and clicked *that*, instead of pressing where a person presses.

**The layer check.** Pick the layer that can observe the defect:

| Defect is about | Test in |
| --- | --- |
| Logic, copy, state, wiring | jsdom component test |
| Stacking, `pointer-events`, overlap, tap-target size, painted colour | Real browser (`e2e/`) |

**jsdom does no hit-testing and no stacking.** A component test cannot tell a live region from a dead one, whatever it asserts. In a browser, press **coordinates** (`page.mouse.click(x, y)` off a `boundingBox()`), not elements — and assert in both directions: the inert regions do the general thing, *and* the real controls still win their own pixels. Note a locator `.click()` correctly refuses an element with `pointer-events: none`, which is why the coordinate form is the honest one.

**Make the failure reachable.** A guard nobody can reach is indistinguishable from no guard, and both versions are green:

- *Transactions* — step order does not change correctness but decides whether atomicity is **observable**. Put the step that can abort *after* the writes you claim are all-or-nothing, or the test never reaches them and passes trivially.
- *"No-op after teardown" guards* — start the work while mounted and suspend its async seam, then tear down, then release. Firing an event at a detached node after unmount proves nothing: React removed the handler with the tree. Check the suspended path still yields a real result, or the test is vacuous a second way.
- *Boundary counts* — a test at exactly the cap cannot distinguish `>` from `>=`. Test just either side.

**E2E timing has two distinct traps.** An SSR element is visible and "actionable" before React hydration attaches its handler, so a click succeeds and does nothing — gate on something only true after hydration (`await expect(control).toBeEnabled()`), never `toBeVisible()`. Separately, a helper that triggers a server write must wait for the write to land *inside the helper*, or callers that read the database next race it; that reads as flakiness and costs a with/without run to attribute.

**Measuring painted colour** needs care: Tailwind's `/25` opacity compiles to `color-mix(in oklab, …)` and Chromium reports it as `oklab(L a b / α)` — parsing those numbers as RGB yields near-black and a wildly wrong ratio. Rows with `transition-colors` also need ~400ms to settle, or the same element reads two different values. Cross-check any contrast harness against a known pair before trusting it.

**Seed by id, not by title.** Several specs seed the same fixture names; a lookup by title finds whichever ran first, so the test passes alone and fails in the suite.

## 5. Run the gate before claiming the fix works

Typecheck, lint and e2e all passing is **not** the gate. The component tests render the real route against partial fixtures, so a newly-read field crashes them while everything else stays green:

```bash
pnpm -F @porch/tanstack-start typecheck && pnpm -F @porch/tanstack-start lint && pnpm -F @porch/tanstack-start test
```

Run the whole unit suite, not only the file you think is related — it is fast, and the suite that breaks is rarely the one you expected. Grep `src/component/*.test.tsx` for the component's name to learn which suite owns it. One e2e spec: `pnpm -F @porch/tanstack-start e2e:web <substring>`.

Before attributing a failure to your change, check whether it fails on `HEAD` too.

## 6. Report what is actually true

Never claim "full", "complete", "enforced", or "verified" for something the code or the evidence only partly meets. Either finish it, or label it partial and list the gaps. Keep the requirement, the task status and the code consistent — a self-contradiction between them is worse than an honest "partial".

Say plainly which checks ran, which failed, and what was left out and why. A pre-existing failure is reported as pre-existing, with the evidence that it is.
