# Batch: library hooks and listeners — Rule 1

## Rule 1 — Use the API you are already holding

A library hook, component or option object that you use partially will keep doing what its unset options say. The 2026-09-11 lesson: five screens paired a router's `useBlocker` with a hand-rolled `beforeunload` listener; the hook already owned that event through an unread option (`enableBeforeUnload`, default `true`), so the browser asked "changes may not be saved" on every clean refresh, on five screens, for months, with a comment explaining the wrong model.

### Tell

- The plan pairs a library hook, component or option object with a hand-written listener or effect for the same event family (`beforeunload` beside a navigation blocker; `resize` beside a layout hook; `keydown` beside a menu primitive; `scroll` beside a virtualiser).
- The plan names two options of a hook whose type has more, and says nothing about the rest.
- The plan says "the same guard screen X carries" or "copy the pairing from the sibling".
- The plan explains a library's or the browser's behaviour in a sentence with no source named.

### Write

- **Read the whole options type.** Open the `.d.ts` and read every field, not the two you came for.
- **Unset ≠ off.** For every option left unset, say its default and what the default *does*. If it touches your behaviour, set it explicitly even when the value equals the default — the line documents that you looked.
- **The guide, not only the reference.** The type says what exists; the guide says what the author intended it for.
- **Same event, stop sign.** A DOM listener for an event family the library already handles (`beforeunload` beside `useBlocker`; `resize` beside a layout hook; `keydown` beside a menu primitive) means the library probably owns it. Grep the library's `dist` for the event name before writing the listener.
- **One predicate, fed to the library.** When the library exposes the second case as an option, feed it the *same* condition the first case uses, in function form so it is evaluated at the event:

  ```ts
  useBlocker({
    shouldBlockFn: () => hasUnsavedText,        // in-app navigation
    enableBeforeUnload: () => hasUnsavedText,   // browser unload — same predicate
    withResolver: true,
  });
  ```

- **Replace, don't add.** Once the library form works, delete the hand-rolled listener. Both together is correct whenever dirty and wrong whenever clean — and nobody checks clean.
- **A comment is a claim.** Write what you *verified* ("the router's own listener is disabled here because …") and name the source that would prove you wrong.
- **The second copy is the audit.** Copying "the same guard X carries" inherits X's unaudited debt; verify the pattern once against the library at the second copy, and fix all copies in one change.

### Prove

- **Arms when dirty AND silent when clean.** The silence assertion is the one people skip, and the one that catches over-blocking. Also assert silence *after* anything that saves itself (a photo picked → stored) and *after* resolution (arm, Cancel/Save, stood down). Three states, three assertions.
- **A stubbed hook is an absent library.** `vi.mock(router, () => ({ useBlocker: () => ({ status: "idle" }) }))` is fine for the screen's own logic, but that suite can no longer see what the hook does. Keep **one** test where the real hook mounts (browser e2e), asserting the outcome, not a handler's intent.
- **Probe what the harness bypasses.** Playwright's `reload()` / `goto()` never fire `beforeunload`. Ask the page the question the browser would ask:

  ```ts
  const wouldPromptOnUnload = (page: Page) =>
    page.evaluate(() =>
      !window.dispatchEvent(new Event("beforeunload", { cancelable: true })),
    );
  ```

  `dispatchEvent` returns `false` if *any* listener cancelled — so it measures the prompt, not a handler.
- **Positive control in the same test.** After the silence assertions, arm the guard and assert the probe reports `true`; without it a probe that always returns `false` passes vacuously.
- **Run the revert check, don't reason it.** Undo the fix, watch the *silence* assertion go red, restore, watch it go green; paste both.
- **Name what the test does not cover.** "Verified by test on settings; by identical shape on four siblings" — never plain "verified".
- **Manual pass gets a negative-space step.** "Open a clean screen; refresh; nothing should happen."

### View

- **List the unset options** of every library hook in the diff, with defaults. A default that does something is a finding unless the code says why it is acceptable.
- **A hand-rolled listener for an event the library handles** is the tell; grep the library's `dist`. If the library owns it, one of the two is wrong.
- **A comment describing library or browser behaviour is a claim**; ask the author to cite what they read.
- **"The same guard X carries" — has X been audited?** Review the pattern once at its source; the finding applies to all N copies.
- **Where is the silence test, and does any test run the real library?** A guard proven only as "prompts when dirty" through a stubbed hook is untested on its library half.
- **One symptom, how many sites?** Grep the pairing across the tree and expect the fix at every site with the same option shape.
- **Does an existing requirement already forbid the symptom?** If the spec already says "leaving with nothing written SHALL simply leave", the fix is compliance, not a spec change — say so.
- **Compare the two designs in code, side by side** (own handler + `enableBeforeUnload: false` versus `enableBeforeUnload: () => predicate`); choose the one that cannot drift, and show the diff.
- **Ask why, after the fix.** The fix closes one bug; the why closes the class — and becomes the next rule here.
