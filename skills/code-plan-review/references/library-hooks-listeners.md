# Batch: library hooks and listeners — Rules 1, 24

## Rule 1 — Use the API you are already holding

A library hook, component or option object that you use partially will keep doing what its unset options say. The 2026-09-11 lesson: five screens paired a router's `useBlocker` with a hand-rolled `beforeunload` listener; the hook already owned that event through an unread option (`enableBeforeUnload`, default `true`), so the browser asked "changes may not be saved" on every clean refresh, on five screens, for months, with a comment explaining the wrong model.

### Stack

Any library with an options object, on either side; the examples are TanStack Router, the DOM and Playwright, and translate to any router, layout hook, HTTP or queue client, ORM or framework plugin. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The plan uses a library hook, component, client or plugin that takes an options object: a router's blocker, a layout or virtualiser hook, an HTTP or queue client, an ORM insert, a framework plugin.
- Beside it, the plan adds a listener, effect, loop or check for a concern in the same family: navigation or unload, resize, keys, scroll, retries, CORS, limits, conflicts, acknowledgements.
- The plan copies a pairing from a sibling screen or module.
- The plan states how a library or the browser behaves.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **An options ledger per library API used**: every field of its options type, read from the `.d.ts`; the value set, or "unset"; the default; what the default does to this feature. A row "unset" whose default touches the concern is visible as such.
- **Each hand-written listener, loop or check paired with the library feature it sits beside**, and one sentence saying which of the two owns the concern, with the source that says so — the guide, or a grep of the library's `dist` for the event name.
- **For a copied pairing**: the sibling audited against the ledger, and the list of every copy in the tree.

### Tell

- The plan pairs a library hook, component or option object with a hand-written listener or effect for the same event family (`beforeunload` beside a navigation blocker; `resize` beside a layout hook; `keydown` beside a menu primitive; `scroll` beside a virtualiser).
- The same shape on the server: a hand-rolled retry loop beside an HTTP or queue client that already retries; a hand-written CORS, body-limit or rate-limit step beside the framework's plugin for it; a manual existence check before an insert beside an ORM whose conflict option already decides it; an explicit acknowledge in a consumer whose client acknowledges on its own.
- A ledger row "unset" whose default touches a concern a hand-written listener also handles; a ledger with fewer rows than the type has fields.
- The plan says "the same guard screen X carries" or "copy the pairing from the sibling" with no audit and no copy list.
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

- **Does the ledger match the `.d.ts`?** Open the options type; a field the type has and the ledger omits is a finding against the ledger, before any finding against the design.
- **List the unset options** of every library hook in the diff, with defaults. A default that does something is a finding unless the code says why it is acceptable.
- **A hand-rolled listener for an event the library handles** is the tell; grep the library's `dist`. If the library owns it, one of the two is wrong.
- **A comment describing library or browser behaviour is a claim**; ask the author to cite what they read.
- **"The same guard X carries" — has X been audited?** Review the pattern once at its source; the finding applies to all N copies.
- **Where is the silence test, and does any test run the real library?** A guard proven only as "prompts when dirty" through a stubbed hook is untested on its library half.
- **One symptom, how many sites?** Grep the pairing across the tree and expect the fix at every site with the same option shape.
- **Does an existing requirement already forbid the symptom?** If the spec already says "leaving with nothing written SHALL simply leave", the fix is compliance, not a spec change — say so.
- **Compare the two designs in code, side by side** (own handler + `enableBeforeUnload: false` versus `enableBeforeUnload: () => predicate`); choose the one that cannot drift, and show the diff.
- **Ask why, after the fix.** The fix closes one bug; the why closes the class — and becomes the next rule here.

## Rule 24 — Search before you write an interaction

Rule 1 is about the API already in your hands. This rule is one step earlier: before a plan hand-writes any interaction or event concern on a UI surface, it searches — first the stack and the dependency tree, then the ecosystem — and carries the search as a ledger. A hand-written listener is the *last* option, taken only after both searches came back empty or a found library was rejected for a named reason. The requirement was stated on 2026-09-18, not harvested from an incident; the Rule 1 incident is its nearest relative — five screens hand-rolled an event the router already owned.

### Stack

Bound to a UI surface: a plan whose named files render in a browser or a native client (React and the DOM are the examples; Vue, Svelte, Solid, React Native, Flutter with the names translated). Skipped, on a `SKIPPED` line, for a plan that touches no UI file — a server-only change has no interaction to search for.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The spec deltas describe an interaction: pointer, keyboard, focus, scroll, resize, drag and drop, paste, hotkey, long-press, swipe, click-outside, focus trap, scroll lock, virtualised list, sortable list, resizable panel, debounced or throttled input, undo, toast or notification queue, navigation blocking, enter or exit animation, clipboard, file drop, IME-aware input.
- The plan adds an effect with `addEventListener`, a custom hook, or a component that implements one of those.
- The plan names no library for the concern, or names one it has not yet installed.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A concern list**: one row per interaction or event concern the plan implements, named as the concern ("focus trap inside the dialog", "reorder by drag on touch and pointer"), not as the code ("a keydown handler").
- **A search ledger per concern, two tiers in order, each with what was searched and what it returned**:
  1. *The stack and the dependency tree*: the UI framework and its first-party ecosystem; every package in the manifest, including the headless kit, router, form, query and animation libraries the named files already import; transitive packages in the lockfile that could be promoted. Checked in the package's docs or `.d.ts`, or a grep of its `dist` for the event name. Result: the API found, or "none", per package looked at.
  2. *The ecosystem*: a web search by the concern's name; the candidates seen, each with a maintenance signal (last release, weekly downloads, open issues), its size, and whether it covers the concern's edge cases. Result: candidates, or "none" with the query used.
  Each row ends in a **disposition**: *adopt* (which package, which API); *reject* (a reason that names a number or a missing feature); or *hand-write* (both tiers returned none, or every candidate was rejected). A row whose disposition is hand-write and whose tier 2 cell is empty is visible as such.
- **For a hand-written concern, an edge-case checklist**: the cases a library would have handled — touch as well as pointer, IME composition, keyboard and screen-reader access, RTL, nested instances, unmount during the event, server rendering, reduced motion — each marked *handled at step N* or *out of spec, because …*. An unmarked case is visible as such.

### Tell

- The plan writes "add a listener / effect / handler for X" with no library named and no search ledger beside it.
- A custom hook whose name is a well-known library export — `useClickOutside`, `useHotkeys`, `useDebounce`, `useResizeObserver`, `useIntersectionObserver`, `useFocusTrap`, `useVirtualizer`, `useDrag`, `useBlocker` — in a plan whose manifest already holds a package that exports it, or a headless kit whose primitive owns it (a dialog primitive owns focus trap, Escape, click-outside and scroll lock; a router owns blocking; a form library owns dirty tracking).
- A ledger whose tier 1 says "none" and whose disposition is hand-write, with tier 2 blank — the ecosystem was never searched.
- A rejection with no number and no missing feature: "too heavy", "simpler to write ourselves", "we only need a small part of it".
- A tier 1 row that names the framework but not the packages the named files import — the search stopped at the framework's own API.
- The plan says a library "does not support X" with no source (Rule 1's claim Tell, one step earlier).
- A hand-written concern with no edge-case checklist, or a checklist where "touch" or "keyboard" is unmarked.

### Write

- **The property**: every interaction concern has one owner, and the owner is the most-exercised implementation reachable — the framework, then a package already installed, then a mature library, then hand-written code — each step taken only after the one before returned nothing or was rejected for a named reason. The fix below is the search that establishes the owner; the property is that the order was followed and the record shows it.
- **Search the stack first, in the files.** Open the manifest; for each package the named files import, open its docs or `.d.ts` for the concern; grep its `dist` for the event name. The framework's own API (React's `useSyncExternalStore`, the DOM's `dialog` and `popover`, CSS `scroll-snap`, `overscroll-behavior`, `:focus-visible`) counts as tier 1 — a concern the platform owns needs no package.
- **Then the ecosystem, by the concern's name.** One web search per concern; take candidates that have a maintenance signal; compare them on the edge cases the concern needs, not on the happy path.
- **Adopt whole.** Once a library owns the concern, use its form for the whole concern and feed it the plan's predicate (Rule 1's "one predicate, fed to the library"); delete the hand-written half rather than keeping both.
- **Reject with a number or a scenario.** "Adds 34 kB gzipped to a route budgeted at 20"; "does not support nested dialogs, which scenario 3 needs"; "last release 2021, 140 open issues". A reason that names neither is not a reason.
- **Hand-write against the checklist.** When both tiers come back empty, the edge-case checklist becomes the plan's pseudocode: each case is a numbered step or a line saying it is out of spec and why. The checklist is what the library would have given for free; writing it down is the price of not taking it.
- **Record the search in the code.** A comment on the hand-written hook names what was searched and why each candidate was rejected, so the next reader does not redo the search — or redoes it with the sources in hand.

### Prove

- **An adopted library mounts for real in one test** (Rule 1's "a stubbed hook is an absent library"), asserting the outcome, not the handler's intent.
- **A hand-written concern has one test per checklist row** — the touch path, the keyboard path, the unmount-mid-event path. A checklist row marked *handled* with no test is the row a library would have covered.
- **A rejection that names a missing feature names the scenario the library fails**; that scenario has a test on the hand-written code, so the reason for writing it is the assertion that proves it needed writing.
- **Silent when not applicable** (Rule 1): a click-outside that closes nothing when the click is inside; a hotkey that does nothing while an input has focus; a drag that does not start on a scroll gesture.

### View

- **Does the ledger match the manifest?** Open `package.json` and the lockfile. A package present that owns the concern and is absent from tier 1 of the ledger is a finding against the ledger, before any finding against the design.
- **Was tier 2 run?** A hand-write disposition with tier 2 blank is a finding; do not run the search for the author. A hand-write disposition with tier 2 filled: run one web search yourself by the concern's name, record it on a `SEARCHED` line, and treat an obvious maintained candidate the ledger omits as a finding against the ledger.
- **Is each rejection a number or a scenario?** "Too heavy" with no size, "does not fit" with no feature named: ask for the figure or the scenario.
- **Grep the tree for the concern hand-written elsewhere** — the hook name and the event name. A second hand-written copy of the same concern means the adoption, or the checklist, applies at both; name every site.
- **Does the headless kit already in the tree own this?** A dialog, menu, combobox or tooltip primitive in the manifest owns focus, Escape, click-outside and scroll lock; a hand-written version beside it is Rule 1's Tell, and one of the two is wrong.
- **Is the checklist complete for this concern?** Name the standard cases yourself — touch, IME, keyboard and screen reader, RTL, nested, unmount mid-event, SSR, reduced motion — and each one the checklist lacks is a row.
- **A "does not support X" claim — where was it read?** Ask for the issue, the doc page or the `.d.ts` line.
