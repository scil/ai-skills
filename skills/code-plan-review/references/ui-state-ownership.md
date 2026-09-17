# Batch: UI state ownership — Rules 7, 8, 16, 17

## Rule 7 — Pick the hook by who owns the value

Anything derivable is derived during render. Request facts come from the data library; UI facts come from state; an effect exists only for a named external system.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A screen shows or edits a value that arrives from outside it — a prop, a session, a query result, a route param.
- The screen can mount before that value has resolved: a session still loading, a query not yet fetched, a param not yet parsed.
- The value can change while the screen is mounted: a refetch, a sign-in elsewhere, a parent re-render with new props.
- The plan has a form or a draft.

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A state ledger for the screen**: one row per value the screen holds; columns: where it comes from (prop, query, session, param, user input); who owns it (the source, or the screen); whether it is derived during render or stored; if stored, what re-seeds it when the source changes, and what the screen shows before the source resolves. A stored row whose source is not the user and whose re-seed cell is empty is visible as such.
- **Each effect named for its external system** — a subscription, a DOM API, a timer — in the pseudocode. An effect with no system named is visible as such.

### Tell

- The plan seeds state from a prop, a session or a query result ("initialise the form from the profile"); a ledger row stored from a non-user source with an empty re-seed cell.
- `useState(someProp)` or its equivalent: the value is read once at mount.
- "When X changes, update Y" is planned as an effect; an effect with no external system named.
- A screen can mount before the value it seeds from has resolved, and the before-resolve cell is empty.

### Write

- **Derive during render**: compute the value from the prop or query on every render; store only what the user has changed.
- **Seed a draft from the resolved value, keyed to it**: when a draft must be local, key the component or reset the draft on the source's identity, so a screen mounted before its session resolves does not freeze on the missing value.
- **An effect names its external system** (a subscription, a DOM API, a timer); "run code when this changes" belongs in the derivation or the event handler.

### Prove

- **Mount before the value resolves, then resolve it**; assert the screen shows the resolved value, not the seed.
- **Change the source after mount**; assert the derived value follows.

### View

- **Does the ledger match the component?** Open the named component; every `useState`, ref and effect is a row or a named system. One with no row is a finding against the ledger, before any finding against the design.
- **Every `useState(<prop or query value>)` is a finding** unless the plan says how it re-seeds.
- **Every effect that copies a value from one place to another is a finding.**
- **Can this screen mount before its data? What does it show then, and after?**

## Rule 8 — One observer per save that can be in flight independently

A mutation observer reports only its most recent call. Two overlapping saves sharing one observer share one answer: "what happened last".

### Where

- One screen has two or more saves: text fields and a photo; a toggle and a form; an autosave and a submit.
- One of them is slow or external — an upload, a third-party call — beside fast ones.
- Nothing in the UI structurally prevents two saves from being in flight at once: no single submit button disabled while pending.

### Asks for

- **A save ledger for the screen**: one row per save; columns: what triggers it; whether it can be in flight while each other save is (yes, or the UI mechanism that prevents it); the observer it uses; the surface that renders its pending and error state. Two rows that can overlap and share an observer, or a row whose surface is "the screen", is visible as such.

### Tell

- One screen has two or more saves and the plan says "the mutation" in the singular; two ledger rows that can overlap and name the same observer.
- A shared "saving…" or error state covers saves that can overlap; a ledger row whose surface is the screen.
- An upload or a slow save sits beside fast ones.

### Write

- **Saves that can overlap get their own observer each**, plus a shared scope id so their writes serialise on the server.
- **Saves the UI structurally prevents from overlapping** (one submit button, disabled while pending) may share one observer.
- **Each surface renders its own observer's state**, not a screen-wide one.

### Prove

- **Overlap them**: fire save A, fire save B before A resolves; resolve A with an error and B with success, then the reverse. Assert each surface shows its own outcome and neither overwrites the other's.

### View

- **Does the save ledger match the component?** Open the named component; every mutation hook or submit handler is a row. One with no row is a finding against the ledger, before any finding against the design.
- **Which saves on this screen can be in flight at the same time, and does each have its own observer?**
- **Does any error or pending state belong to the screen rather than to the save that produced it?**

## Rule 16 — A refill is computed on a baseline

A save response is the server's answer to the value it was sent. If the user keeps typing during the round trip, the response arrives carrying a value 1.2 seconds old, and `setState(response)` swallows what was typed since. Nothing failed: the server was right, the request succeeded, and the clobbering write is the screen's own success response. The other update source is the user's next keystroke, which looks nothing like interleaving and is exactly that.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A save response is written back into a field the user can still edit while the save is in flight.
- Per-field autosave, debounced save, or "save on every change".
- The plan says "reset the form from the response", "sync state with the server", or "refill".
- Two requests for the same field can be in flight and resolve out of order.
- The update-source table lists "the user's next keystroke" against any field, or should.

### Asks for

- **A refill ledger per field the response can touch**: whether the field is refilled from the response at all; whether it is server-only (`id`, `updatedAt`, a normalized form) or user-editable; for an editable field, the baseline check — a token captured *when the request leaves*, or a dirty-since-send flag — and what happens to a response that fails it. An editable field refilled with an empty baseline cell is visible as such.
- **The token's read and increment points as numbered steps**: read at send, increment at send, compared at arrival.

### Tell

- `setState(response)`, `form.reset(response)` or a spread of the response into state, on a field the user edits.
- The token is read when the response arrives (it reads the newest value and guards nothing); the token is incremented in an effect (too late — the request has left); `isPending` is the judgement for whether a refill is safe.
- A ledger row that refills an editable field with no baseline.
- The plan treats a disabled submit button as the defence: that prevents sending twice, not a late response landing on a changed field.

### Write

- **Refill only what the server alone knows**: `id`, `updatedAt`, server-normalized values; never the field the user is editing.
- **Guard the refill by a baseline**: capture a monotonic token at send; on arrival, apply only if the token is still current and the field has not changed since send; otherwise discard the response — it is stale, not wrong.
- **Read and increment the token at send**, in the handler, never in an effect and never at arrival.
- **Keep double-submit and late-refill apart**: the first is the request going out twice (a disabled button, an idempotency key), the second is one response coming back too late (this rule); a form needs both.

### Prove

- **Type during the round trip**: delay the response, type after send, deliver; assert the typed characters survive — the assertion that goes red when the guard is removed.
- **Out of order**: send A, send B, deliver B then A; assert the field shows B's outcome.
- **Server-only refill**: assert `updatedAt` and the normalized form do update from the response while the edited field does not.

### View

- **Does the ledger match the component?** Open it; every write from a response into state is a row. A write with no row is a finding against the ledger, before any finding against the design.
- **For each refill: what was the user allowed to do between send and arrival, and does the refill check it?**
- **When is the token read, and when incremented?** Arrival, or an effect, is a finding.
- **Which refilled fields could the user have been editing?** Each is a finding unless the ledger names its baseline.

## Rule 17 — Judge against the value that will be stored

A schema trims, collapses whitespace and normalizes the draft before storing it. Every check made on the raw draft — is it dirty, is it valid, is it equal to the stored value, may Save be enabled — answers about a value that will not be stored, and a Save button that lights up for a whitespace-only change, or a Back button that discards a draft one character from valid, follows.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A field's stored value differs from its typed value: trim, whitespace, case, locale number or date parsing, a canonical form.
- A Save or Done control's enabled state, a dirty check, an "unsaved changes" guard, or an equality check against the stored value.
- An edit control can open before the stored value has arrived, or while another write to the same field is in flight.
- The plan is a tap-to-edit row, an inline editor, or a form that resets from the server.

### Asks for

- **The four gates as numbered steps, in this order**, on the pseudocode of every editable field: (1) has the stored value arrived; (2) is another write to this field in flight; (3) does the draft parse through the shared schema; (4) does the parsed value differ from the stored one. Each gate names what the control does when it fails — and why Save is disabled is said on the spot. A gate missing or out of order is visible as such.
- **The shared schema named** — the one the server uses — and the statement that the client sends the parsed value, not the raw draft.
- **What an unparseable draft counts as** for the leave-page guard: unsaved text, never "unchanged".

### Tell

- Dirty computed as `draft !== stored` on the raw string; Save enabled by `draft.length > 0`.
- A parse on the client that is narrower than the server's (`trim()` beside a schema that also collapses whitespace), or the raw draft sent and the server left to normalize.
- The editor can open before gate 1: the row shows a fallback and opening it edits a value the user never saw; saving overwrites a sentence they never read.
- Gate 2 missing: a `reset` that runs when "no editor is open" wipes a draft opened during an in-flight write.
- A greyed-out Save with no reason shown; a draft that fails to parse read as "same as stored" so the Back button discards it.
- A leave-page dialog wired to one editor's cancel while another editor holds the draft.

### Write

- **Parse once, through the shared schema, and use the parsed value for every check and every payload**: dirty, valid, equal, enabled, and the request body all read the same parsed value.
- **Gate in order**: stored value fetched → no write in flight → parses → differs. Say on the spot why Save is disabled.
- **An unparseable draft is unsaved text** for every guard that asks.
- **The leave-page guard can clear whichever editor holds the draft**, not a hard-coded one.

### Prove

- **Whitespace-only change**: type the stored value with extra spaces; assert nothing to save and no request — the assertion that goes red when a check reads the raw draft.
- **Open before fetch**: mount with the query pending, open the editor; assert Save cannot fire and the fallback is not editable as if stored.
- **Draft during in-flight write**: start a save, open another editor, let the save resolve; assert the draft survives.
- **Invalid draft, then Back**: assert the leave guard arms.

### View

- **Do the gates match the component?** Open it; the order of the checks in the code is the order in the plan, and each reads the parsed value. A check on the raw draft is a finding against the plan, before any finding against the design.
- **Which value does this check read — the draft or the parse?** Each raw read is a finding.
- **Can this editor open before its stored value arrived, and what does Save do then?**
- **What does the leave guard say for a draft that does not parse?**
