---
name: scil:scil-testing
description: Test a guard in both directions and at the layer where the real library runs. Use when testing anything that prompts, blocks, or warns — a leave guard, a confirm, a validation gate — when a component suite stubs a library hook, when the test harness bypasses the browser behaviour under test, or before claiming a guard is verified. Owns how the proof is built; scil-coding owns the code and scil-review owns reading it.
---

# A guard has two sides, and stubs hide the library

The lesson of 2026-09-11: a leave-prompt guard was tested only as "prompts when a draft is open" and prompted on every clean refresh for months. Nothing could have caught it: every component suite stubbed `useBlocker` to `{ status: "idle" }`, so the router's own `beforeunload` listener never existed where a test could see it, and the e2e harness's `reload()` skips `beforeunload` entirely. Each rule below is one thing that would have caught it.

## Test both directions

- **Arms when dirty AND silent when clean.** A guard verified in one direction is half verified. The silence assertion is the one people skip, and it is the one that catches over-blocking — which is what a wrong library default produces.
- **Silent after the thing that saves itself.** If part of the screen autosaves (a photo picked → stored), assert no prompt *after its confirmation* — that is the moment a user notices a false prompt.
- **Silent again after resolution.** Arm it, resolve it (Cancel / Save), assert it stood down. Three states, three assertions.

## Put one test where the library actually runs

- **A stubbed hook is an absent library.** `vi.mock("@tanstack/react-router", () => ({ useBlocker: () => ({ status: "idle" }) }))` is fine for the screen's own logic — but then nothing in that suite can observe what the hook does. Keep **one** test at the layer where the real hook mounts (browser e2e), asserting the *outcome*, not any one handler's intent.
- **Probe what the harness bypasses.** Playwright's `page.reload()` / `goto()` never fire `beforeunload`. Ask the page the question the browser would ask:

  ```ts
  const wouldPromptOnUnload = (page: Page) =>
    page.evaluate(() =>
      !window.dispatchEvent(new Event("beforeunload", { cancelable: true })),
    );
  ```

  `dispatchEvent` returns `false` if *any* listener cancelled — the screen's, the router's, anyone's — so it measures the prompt, not a handler.
- **Positive control in the same test.** Immediately after the silence assertions, make the guard arm (open a draft) and assert the probe reports `true`. Without it a probe that always returns `false` passes vacuously.

## Prove the test can fail

- **Run the revert check, don't reason it.** Undo the fix (one line), run the test, watch it go red on the *silence* assertion, restore, watch it go green. Paste both results in the report.
- **Name what the test does not cover.** The probe ran on one screen; four sibling screens carry the same option shape but no silence test. Say so — "verified by identical shape, not by test" — rather than "verified".

## In the manual pass

- **Add a negative-space step.** "Open a clean screen; refresh; nothing should happen." One second, and nothing else in the walkthrough will prompt anyone to do it.

