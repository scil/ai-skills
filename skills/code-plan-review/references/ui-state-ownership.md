# Batch: UI state ownership — Rules 7, 8

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
