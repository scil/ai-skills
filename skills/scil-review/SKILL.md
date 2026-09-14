---
name: scil-review
description: Review a diff for under-used library APIs and one-sided guards. Use when reviewing a change that uses a library hook, adds a listener or effect beside one, guards a navigation or an unload, copies a pattern across files, or when asked why a library was not used fully. Owns what the reviewer looks for and how to act on it; scil-coding owns the fix and scil-testing owns the proof.
---

# Reviewing for the API that was not used

The lesson of 2026-09-11: five screens used a router's `useBlocker` and, beside it, a hand-rolled `beforeunload` listener. Every review had passed it. The hook's unread option (`enableBeforeUnload`, default `true`) armed a browser prompt on every clean refresh; the comment beside it explained a wrong model; the pattern had been copied four times with "the same guard X carries". Each check below is one question that would have surfaced it.

## What to look for

**Beside every library hook in the diff**

- **List the unset options.** Open the hook's options type and name every field the code does not set, with its default. A default that *does something* is a finding unless the code says why it is acceptable.
- **A hand-rolled listener for an event the library handles.** `addEventListener` for an event family the hook already covers is the tell. Ask: does the library own this? Grep its `dist` for the event name; if it does, the listener is a duplicate and one of the two is wrong.
- **A comment describing library or browser behaviour.** "The browser owns this prompt; all we can do is opt in" is an assumption, not evidence. Verify it against the library source, and ask the author to cite what they read.
- **"The same guard X carries".** Has X been audited? A pattern present N times has had N chances to be wrong and zero to be checked. Review the pattern once, at its source, and the finding applies to all N.

**Every guard**

- **Where is the silence test?** A guard tested only as "prompts when dirty" is half-tested. Ask for the assertion that it stays quiet when clean, and after anything that saves itself.
- **Does the test run the real library?** If the suite stubs the hook, the guard's library half is untested there; ask where the browser-level probe is.

**Scope**

- **One symptom, how many sites?** A report names one screen; grep the pairing (`useBlocker` + `beforeunload`) across the tree and expect the fix at every site with the same option shape.
- **Does an existing requirement already forbid the symptom?** "Leaving with nothing written SHALL simply leave, without a prompt" already existed; the fix brought code into compliance, so no MODIFIED delta — say that explicitly rather than leaving the spec question open.

## How to act on it

- **Compare the two designs in code, side by side.** Own handler + `enableBeforeUnload: false` versus `enableBeforeUnload: () => predicate` — both are correct; the second has one predicate instead of two and no listener to explain. Choose by which one cannot drift, and show the diff, not just the argument.
- **Ask why, after the fix.** "Why did the code use the library without using its capability?" produced these checks. The fix closes one bug; the why closes the class.
- **Report coverage honestly.** Fixed on five screens, probed on one: say "verified by test on settings; by identical shape elsewhere".
