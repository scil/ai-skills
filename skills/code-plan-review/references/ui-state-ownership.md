# Batch: UI state ownership — Rules 7, 8

## Rule 7 — Pick the hook by who owns the value

Anything derivable is derived during render. Request facts come from the data library; UI facts come from state; an effect exists only for a named external system.

### Tell

- The plan seeds state from a prop, a session or a query result ("initialise the form from the profile").
- `useState(someProp)` or its equivalent: the value is read once at mount.
- "When X changes, update Y" is planned as an effect.
- A screen can mount before the value it seeds from has resolved.

### Write

- **Derive during render**: compute the value from the prop or query on every render; store only what the user has changed.
- **Seed a draft from the resolved value, keyed to it**: when a draft must be local, key the component or reset the draft on the source's identity, so a screen mounted before its session resolves does not freeze on the missing value.
- **An effect names its external system** (a subscription, a DOM API, a timer); "run code when this changes" belongs in the derivation or the event handler.

### Prove

- **Mount before the value resolves, then resolve it**; assert the screen shows the resolved value, not the seed.
- **Change the source after mount**; assert the derived value follows.

### View

- **Every `useState(<prop or query value>)` is a finding** unless the plan says how it re-seeds.
- **Every effect that copies a value from one place to another is a finding.**
- **Can this screen mount before its data? What does it show then, and after?**

## Rule 8 — One observer per save that can be in flight independently

A mutation observer reports only its most recent call. Two overlapping saves sharing one observer share one answer: "what happened last".

### Tell

- One screen has two or more saves (text fields and a photo; a toggle and a form) and the plan says "the mutation" in the singular.
- A shared "saving…" or error state covers saves that can overlap.
- An upload or a slow save sits beside fast ones.

### Write

- **Saves that can overlap get their own observer each**, plus a shared scope id so their writes serialise on the server.
- **Saves the UI structurally prevents from overlapping** (one submit button, disabled while pending) may share one observer.
- **Each surface renders its own observer's state**, not a screen-wide one.

### Prove

- **Overlap them**: fire save A, fire save B before A resolves; resolve A with an error and B with success, then the reverse. Assert each surface shows its own outcome and neither overwrites the other's.

### View

- **Which saves on this screen can be in flight at the same time, and does each have its own observer?**
- **Does any error or pending state belong to the screen rather than to the save that produced it?**
