# S · Scenarios view

Screens, forms, client requests, routes and journeys: what a person does and sees. The 4+1 scenarios view. Ask each gate (`S1`, …) first. If the plan has no surface for a gate, skip its subtree.

## CWE-435 · Interaction between correct parties

### S7. Does the change alter what a machine visitor or a person using assistive technology, another language or another device receives?

- **S7.1** A route change, sign-in wall, redirect or client-only render changes what a machine visitor (crawler, link preview, AI agent) receives. The plan does not say. Suggest: for each changed route, list the machine visitors and the status, content and indexing signals each one gets.
- **S7.2** A new screen, control or message reaches only some people: it has no keyboard path or accessible name, untranslated text, or a layout fixed to one device. Suggest: for each new control or text, state its keyboard path, label, translation source and the smallest screen it supports.

## CWE-664 · Resource lifetime

### S1. Can a response, a push or a poll result land after the screen moved on?

- **S1.1** The person keeps editing while a save is out, and the response refills the field with the old value. Or two responses for one field arrive out of order. Nothing fails. Suggest: capture a token at send. Refill only what the server alone knows (ids, timestamps, normalized forms). Discard a response that is not the newest, or whose field changed since send.
- **S1.2** When the response lands, the screen unmounted, moved to another route or item, or now has another reader (sign-out in another tab, a session that resolved late). Suggest: tie the handler to its request, check that the screen still shows the thing the request was about, and otherwise update only the cache. The reader, or a generation that changes with the reader, is part of the cache key.
- **S1.3** Local state is seeded once from a source that resolves later or changes while mounted, or a side effect copies one value into another. The draft keeps the stale seed. Suggest: derive during render, key a local draft to the resolved value, and keep side effects for a named external system only.
- **S1.4** Does the screen wait for a push, a poll or an automatic re-ask?
  - **S1.4.1** The screen leaves "waiting" only in the push handler, so an event before the subscription is live is lost. Or a poll waits one interval before its first tick. Suggest: subscribe, then read once, and treat a push as a hint to read again. Tick now, then on the interval.
  - **S1.4.2** The handler is not idempotent, so a read and a late push apply the effect twice. Suggest: make the handler idempotent.
  - **S1.4.3** An automatic re-ask on an unexpected answer has no bound: it fires once and waits forever, or fires on every render. Suggest: a bounded number of attempts keyed on the disagreement, then a visible state the person can act on.
- **S1.5** A push, a poll or a sync result redraws a whole region from a template (a panel, a list). The region holds a draft that the person is typing. The draft, the caret and the focus are lost. Suggest: keep each draft in state outside the region and restore it on redraw, or update only the parts that changed.

### S2. Does a write change values that this screen or another one shows?

- **S2.1** The client writes, then refetches, so the old value shows until the refetch returns, and forever if it fails. Or it navigates before the server commits, and the next screen reads the old snapshot. Suggest: the response carries what the next screen needs, the cache is written from it first and marked stale after, and navigation waits for the commit.
- **S2.2** The server derives other entries from the changed row (a count, a list, a badge, a "mine" view) and they stay stale. Suggest: list them from the server code and refresh each through the data layer's own handle, never a hand-written key or path.
- **S2.3** An optimistic update has no rollback. Suggest: keep the previous value, restore it on error, and invalidate on settle.

## CWE-691 · Control flow

### S3. Can a person use a control that sends a write?

- **S3.1** The control works while its request is in flight, before the data it acts on arrived, before identity is known, or again before the settle (cache write, navigation) finished. A double click or a second Enter sends twice. Suggest: gate in order: data and identity resolved, no write in flight, input parses, value differs. Show why a control is disabled. Re-enable after the whole settle. Retries, other tabs and reconnects also send, so a duplicate that writes twice also needs the server guard (P1.2).
- **S3.2** Two saves on one screen (text and a photo, autosave and submit) can be in flight at once and share one pending or error state. Suggest: one observer per save that can overlap, each surface showing its own state.

### S4. Does the change span several routes, a redirect, or a sign-in round trip?

- **S4.1** Context (a token, an id) rides in the URL and every hop must forward it, but one exit drops it: a signed-out fallback link, a Cancel, Back, an already-done redirect, an auth callback. Suggest: list every exit of every route on the journey with what it forwards or why the journey can end there. Or one holder (the session, a cookie, a pending row) replaces the forwards.
- **S4.2** A conditional redirect adds a history entry that Back bounces into. Or two routes redirect to each other, and a pending or failed read satisfies both or neither. Suggest: a redirect replaces the current entry, and a failed read redirects nowhere and says so.

## CWE-697 · Comparison

### S5. Does the screen compare a draft with a stored value, or show a value that a write then uses?

- **S5.1** Dirty, valid, equal and "Save enabled" read the raw draft while the server trims or normalizes it. A whitespace edit lights Save, and a near-valid draft is dropped as "unchanged". Suggest: parse once through the shared schema, send and compare the parsed value, and count an unparseable draft as unsaved text.
- **S5.2** The leave-page guard watches one editor while another holds the draft. Suggest: the guard reads whichever editor holds a draft.
- **S5.3** A confirmation ("remove Sam", "charge 3 seats") reads one copy of the value and the write uses another, or the server never checks the expected value. On a phone the sentence scrolls away from the button. Suggest: one snapshot feeds the sentence and the request. The expected value goes into the write's condition, and zero rows shows "this changed under you". The sentence sits beside the button.

## CWE-703 · Exceptional conditions

### S6. Can a read or a write fail, be refused, or succeed only in part?

- **S6.1** A failed or pending read is painted as success or as "nothing here": an error status resolved as success, or a "none" branch that pending and failed also reach, which offers a creation form. Suggest: a non-success status is an error with a way to look again. Branch on the discriminant, and error and unknown land on a read-only branch before any branch that writes.
- **S6.2** A parent's error branch returns early above a child that has its own data. Suggest: the child renders, and the parent says it failed.
- **S6.3** The call succeeded but a step inside it did not (text saved, photo not applied), and "saved" is shown. Suggest: render the per-step flag the response carries (P5.1), not the call's status.
- **S6.4** A refusal (403, 404, an access error) goes through the client's retries, so "not for you" appears late behind a spinner. Suggest: an access refusal is an answer and is not retried. The plan names which errors are refusals and which are faults.
- **S6.5** A slow step (an upload, a third-party call) has no state between "saving" and "saved". Suggest: each shown value has four states: no data, refreshing with data, fresh, error.
