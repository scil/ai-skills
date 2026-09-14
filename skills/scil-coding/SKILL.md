---
name: scil-coding
description: Use a library's API fully before writing code beside it. Use when adopting or already using a library hook, component, or config object — especially when about to add a DOM listener, an effect, or a guard next to it, or when copying such a pairing from a sibling file. Owns how the code is written; scil-testing proves it and scil-review reads it.
---

# Use the API you are already holding

The lesson of 2026-09-11: five screens paired a router's `useBlocker` with a hand-rolled `beforeunload` listener. The hook already owned that event through an option nobody read (`enableBeforeUnload`, default `true`), so the browser asked "changes may not be saved" on every refresh, with nothing dirty — on all five screens, consistently, with a comment explaining the wrong model. Each rule below is one thing that would have prevented it.

## Before using a hook or option object

- **Read the whole options type.** Open the `.d.ts` and read every field, not the two you came for. Four lines would have shown `enableBeforeUnload?: boolean | (() => boolean)`.
- **Unset ≠ off.** For every option you leave unset, say its default and what the default *does*. A default that does something is a decision the author made for you; if it touches your behaviour, set it explicitly even when the value equals the default — the line documents that you looked.
- **The library's guide, not only the reference.** The type says what exists; the guide says what the author intended it for. `useBlocker`'s guide covers the unload case in its second paragraph.

## While writing beside a library

- **Same event, stop sign.** A DOM listener you are about to write for an event family the library already handles (`addEventListener("beforeunload")` next to `useBlocker`; a `resize` observer next to a layout hook; a `keydown` handler next to a menu primitive) means the library probably owns it. Grep the library's `dist` for the event name — ten seconds — before writing the listener.
- **One predicate, fed to the library.** When the library exposes the second case as an option, feed it the *same* condition the first case uses, in function form so it is evaluated at the event:

  ```ts
  useBlocker({
    shouldBlockFn: () => hasUnsavedText,        // in-app navigation
    enableBeforeUnload: () => hasUnsavedText,   // browser unload — same predicate
    withResolver: true,
  });
  ```

  Two predicates that must agree is a drift waiting to happen; one predicate cannot drift.
- **Replace, don't add.** Once the library form works, delete the hand-rolled listener. Both together is the state that hid this bug: correct whenever dirty, wrong whenever clean, and nobody checks clean.
- **A comment is a claim.** "The browser owns this prompt; all we can do is opt in" was a model, written down until it looked like knowledge. Write what you *verified* ("the router's own listener is disabled here because …"), and name the source that would prove you wrong.

## When copying the pairing from a sibling

- **The second copy is the audit.** "The same guard the full editor carries" inherits the first copy's unaudited debt. At the second copy, verify the pattern once against the library — five copies without an audit are five bugs with one cause.
- **Fix all copies in one change.** A symptom reported on one screen and a pattern present on five is a five-file diff, with the same option shape at every site.
