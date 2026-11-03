---
name: code-plan-review
disable-model-invocation: true
description: Review a plan (a design doc, pseudocode, a diagram, a described change) before code exists by walking a catalog of scenarios and asking each one's questions: a client sending a request, a server write, who is asking, screen state, a journey across routes, a branch over several states, the domain model, reuse of libraries, modules and ready-made content, one truth in several copies, a state that changes as time passes, a pipeline that judges input. Use when asked to review a plan or design, before implementing a change that touches any of those, or when harvesting a lesson from an incident into a question here.
---

# Plan review by scenario

A plan is reviewed by reading it with the right questions in hand. The catalog below is those questions, grouped by the scenario that raises them; they are stack-neutral, and how each one shows up in a particular technology — and the concrete fix there — lives in a binding file per technology ([Bindings](#bindings)). A question does not need a confirmed defect to be worth reporting: where the plan leaves room for it, report the possibility and a suggestion. One reviewer walks the whole catalog in one context, without fanning out to subagents of its own; where you can, that reviewer is a session that did not write the plan — a fresh session, or an agent the authoring session delegates the review to. Where the questions came from: [`readme.md`](readme.md).

## How to review

1. **Read the plan**, and the spec it implements if there is one, then **restate the model** in about five lines — who acts, which states exist, who decides what, and what an outsider already holds (are ids guessable, is the path signed-in, is it rate-limited) — so a misreading is corrected before any question is built on it. Questions about outsiders (B3, C3, C4) are judged against that line, not against an attacker with unlimited reach. **Detect the stack** from the manifests, schema and deployment config (package manifests, ORM schema, migrations, the start script or platform config) and load the matching files from `references/stacks/`; a technology with no file is reviewed from the questions alone. Files the plan names that exist in the checkout may be opened, and the tree grepped for callers, sites and exits, to settle a question; that is reading, not asking. A plan reviewed without them is still reviewed.
2. **Walk the catalog**, scenario by scenario. Decide whether the plan touches each top-level scenario; for each it touches, walk its sub-scenarios and ask every question. Judge from what the plan does, not from what it says about itself. Examples in a question illustrate it and never narrow it: ask each question of every layer the plan touches (UI, server, data, infrastructure, domain algorithm, prompt, operations script), and mark a question *unlikely* only for a guard the plan has, never because the plan's layer is not among the examples. A plan that already guards against a question gets that question marked *unlikely* with the guard cited, not skipped. Where a loaded binding has an entry for the question, search with its *look for* and take the suggestion from its *fix*.
3. **Ask once for what only the author can supply.** Some questions cannot be judged from prose or from the files: which paths write a table, the order two paths lock, the arrival rate on a public path, which exits a journey may end at on purpose, which spec rule governs. Collect everything you would need into one message, each item with the question it serves, and ask. The user may decline any or all of it. Do not build the material yourself from the plan's sentences, and do not stop: continue with the rest, and mark the questions that depended on it *cannot tell*, with the possibility as your best guess and the suggestion still given. **Delegated**, with nobody to ask, write the same items under *Decisions for the owner* in the report — each with the row it serves and your recommendation — and carry on exactly as if they had been declined.
4. **Report** in the shape below. Nothing is dropped silently: a question judged unlikely is still listed by number, and a scenario the plan does not touch gets one line saying so.
5. **Done when** every top-level scenario has a table or a not-touched line, every row carries a possibility with its reason and a suggestion, and every material you needed is recorded as supplied, declined, or read from the files.

### A second pass

When the resolutions changed the plan substantially, review again — fixes open new surface. The second pass is narrower:

1. **Re-walk only the scenarios the changed decisions touch**, with the code open as before, and append the result; the first pass's rows stay as they were.
2. **Check that each resolution reached every place the old decision was stated.** A resolution appended as a new section ("this one wins") while the old text still states the old decision is a plan holding two copies of one truth (I1): the implementer reads whichever comes first. Report each such passage as a row; the fix is to correct it where it stands.
3. **Re-ask G4.2 and G4.3** for every constraint, column or state the resolutions added: a new CHECK is the most common fix and the most common new break.

## What to report

First, in this order: **The model, restated** (step 1); **Decisions for the owner** when the review was delegated (step 3), or nothing; **Most severe**, at most five rows from the tables below by number, ranked by what the failure costs — data corrupted, lost or disclosed first; then a screen or action that breaks; then a stale or misleading view; then the rest — so the reader knows where to start without reading every table.

Then one table per scenario the plan touches, holding the questions judged *likely*, *unspecified*, *possible* or *cannot tell*:

| question | where in the plan | possibility | suggestion |
|---|---|---|---|
| A3.1 | step 4, "reset the form from the response" | likely: the intro field stays editable while the save is in flight | refill only server-owned fields; guard the rest by a token captured at send |

- **question**: the catalog number, followed by the binding when the row's shape or suggestion came from one (`B1.2 · postgres`, `A3.11 · tanstack-query`).
- **where in the plan**: the step, sentence or diagram message that raises it; "nowhere" when the plan is silent on something it must say.
- **possibility**, each with a half-sentence why: *likely* (the plan describes the shape — implemented as written, it fails); *unspecified* (the plan is silent where it must speak — an implementer will have to decide, and nothing says how); *possible* (nothing in the plan rules it out); *cannot tell* (depends on material that was declined or absent). A process that requires every *likely* row resolved before code requires the same of *unspecified*; the split only tells the reader which rows are defects and which are gaps.
- **suggestion**: the change to the plan, in one or two sentences. Two rows with one cause get one suggestion that names both; a suggestion that patches one spot while another row names the same cause is the wrong suggestion. A suggestion is proportional. It weighs who can reach the failure and what it costs them against what the fix costs everyone: load, latency, a second copy of a rule, code that must be kept in step. When every available fix costs more than the harm, the suggestion is "accept, and name it in the plan's Non-Goals", and the question goes under `Unlikely:` with that reason, not into the table.

Under each table, one line: `Unlikely: A1.2 (idempotency key, step 6), A1.5 (one save on this screen), …` — the number and the guard, so the record that the question was asked exists without a row.

After the tables: **Not touched**, one line per scenario with the reason; **Materials**, each item asked for and whether it was supplied, declined or read from the files, and the bindings loaded (with any technology in the stack that has none); **Outside the catalog**, a problem you saw that no question names, one line each, so it can become a question later.

Do not rewrite the plan. Do not comment on style, naming or scope. In an OpenSpec repository the plan is the change's `design.md` and the report is `review.md` beside it: [`references/openspec.md`](references/openspec.md).

## Harvest a lesson

1. State the incident: what was planned, what went wrong, and which question, asked of the plan, would have raised it.
2. **Decide the layer.** A new *shape* of problem — one no question describes, in any technology — is a new question. A known shape showing up in a technology in a way its binding does not yet say (a default, an API, a syntax, a limit) is a new or extended binding entry, and the question stays as it is. Something true only of this project (its function names, its tests) belongs in the project's own instructions, citing the question number. Most incidents are bindings.
3. For a question: find the sub-scenario where that moment belongs and append one numbered line: the shape the problem takes in a plan, in stack-neutral words, then *Suggest:* the change, stated as the property the spec needs rather than only the fix the incident used. A moment no sub-scenario covers gets a new sub-scenario; a mechanism no scenario covers gets a new lettered scenario. Numbers are never reused or shifted. Never a new skill. For a binding: add or extend the entry under the question's number in `references/stacks/<technology>.md`, creating the file if the technology has none.
4. Tell the story once in [`readme.md`](readme.md), dated. Done when the question or binding entry exists and the readme holds the incident.

## Bindings

A binding file, `references/stacks/<technology>.md`, says how the catalog's questions show up in one technology layer — a database, a data client, a UI framework, a router, the platform, the language, the hosting shape — and the concrete fix there. Stacks are combinations, so files are per layer, not per stack. Present: [`postgres`](references/stacks/postgres.md), [`tanstack-query`](references/stacks/tanstack-query.md), [`react`](references/stacks/react.md), [`tanstack-router`](references/stacks/tanstack-router.md), [`web-platform`](references/stacks/web-platform.md), [`typescript`](references/stacks/typescript.md), [`node-hosting`](references/stacks/node-hosting.md), [`python-async-http`](references/stacks/python-async-http.md), [`wordpress`](references/stacks/wordpress.md), [`semgrep`](references/stacks/semgrep.md), [`ansible`](references/stacks/ansible.md).

- A file opens with when to load it (what in a manifest or schema shows the technology) and the versions its defaults were checked against.
- Entries are keyed by catalog number, each with *shows up as*, *look for*, *fix*. Only questions whose shape or fix differs in that technology get an entry; no file covers the whole catalog.
- A binding never introduces a question. If an entry describes a shape no question names, the question comes first (Harvest, step 2).
- The catalog never names a product, API or syntax; where a question needs an example, it describes the thing generically and the binding names it.
- A new file is written when a project on that technology is reviewed, not in advance.

## Catalog

Each question is the shape a problem takes in a plan, then the suggestion, in words that hold for any stack. A question applies whether or not the plan already guards against it; the guard makes it unlikely, not absent.

### A. The client sends a request

A form submit, a save, an action button, an autosave, an upload.

#### A1. Before it leaves

1. The control stays enabled while the request is in flight, so a double click or a second Enter sends the same request again. Suggest: disable on send and re-enable on settle; where a duplicate would write twice, an idempotency key the server checks.
2. The same request can also leave from a retry, another tab or a reconnect, which a disabled button does not stop. Suggest: name every sender; the server-side guard (B1) is what covers them all.
3. The payload is the raw draft while the server trims, collapses or normalizes it, so the client's dirty, valid and equal checks answer about a value that will not be stored. Suggest: parse once through the shared schema, send the parsed value, and run every check on it.
4. The control can be used before the data it acts on has arrived: an editor opened while the row still shows a fallback; Save enabled while another write to the same field is in flight. Suggest: gate in order (stored value arrived, no write in flight, parses, differs) and say on the spot why Save is disabled.
5. Two saves on one screen (text fields and a photo; a toggle and a form; autosave and submit) can be in flight at once and share one pending or error state, so the screen reports whichever finished last. Suggest: one observer per save that can overlap; each surface renders its own save's state.

#### A2. While it is in flight

1. The user keeps editing the field whose save is out, so the response will carry a value seconds old (A3.1). Suggest: capture a token when the request leaves; the response is judged against it.
2. The screen can unmount or navigate before the response lands, and the handler writes into a component that is gone or into another route's state. Suggest: ignore or cancel on unmount; tie the handler to the request it belongs to.
3. The reader can change under the screen (sign-out in another tab, a session resolving late), so the response is applied for the wrong person. Suggest: the reader is part of the cache key; identity is decided server-side (C1).
4. A slow step (an upload, a third-party call) sits inside the request beside fast ones and the screen has no state between "saving" and "saved". Suggest: four states per shown value: no data, refetching with data, fresh, error.

#### A3. After the response returns

1. The response is written back into a field the user can still edit, and what was typed during the round trip is gone; nothing fails. Suggest: refill only what the server alone knows (ids, timestamps, normalized forms); guard any other refill by the token from A2.1 and a dirty-since-send check; a stale response is discarded, not applied.
2. Two responses for one field arrive out of order and the older lands last. Suggest: the same token; apply only the newest.
3. The screen has changed since the request left (another item selected, a dialog closed, a route changed) and the update written on return no longer fits where the user is. Suggest: the handler checks the screen still shows the thing the request was about; otherwise it updates the cache and not the view.
4. The control is usable again as soon as the response arrives, before the cache write, navigation or refetch that follows it, so a second click acts on stale state or sends again. Suggest: re-enable after the whole settle; or navigate first and let the destination own the control.
5. "Write, then refetch": until the refetch returns the screen shows the old value, and if the refetch fails it shows it forever. Suggest: write the cache from the response first; mark it stale afterwards.
6. The server derives other entries from the changed row (a count, a list it belongs to, a badge, a "mine" view) and they stay stale. Suggest: list them from the server code and refresh each through the data layer's own handle for it, never a hand-written cache key or path.
7. An optimistic update has no rollback. Suggest: keep the previous value, restore on error, invalidate on settle.
8. The call succeeded but a step inside it did not (text saved, photo not applied) and "saved" is shown. Suggest: per step that may fail alone, the response says whether it applied; the client renders that flag, not the call's status.
9. A failed response is painted as success or as "nothing here": an HTTP client that resolves error statuses as if they succeeded; a "not loading and no data" test rendering the empty state with no error branch. Suggest: an error branch with a way to look again; a non-success status is an error; the empty state is for a successful read that found nothing.
10. The client navigates or refetches on "success" before the server's transaction commits, and the destination reads the old snapshot ("you are not in"; a refresh fixes it). Suggest: the response carries what the next screen needs; navigate after the commit; write the cache from the response.
11. A refusal (403, 404, an access error) goes through the data client's default retries, so the screen that says "not for you" appears seconds late, after backoff, while a spinner suggests the answer is still coming. Suggest: an access refusal is an answer and is not retried; a load fault keeps its retries; the plan names which errors are which.

### B. The server handles a write

#### B1. Check, then write

1. One statement reads (a count under the limit, a status open, a row absent) and a later statement writes; another request fits in the gap, even inside one transaction. Suggest: the condition goes into the write itself (a conditional update, a compare-and-set); the outcome is read from how many rows it changed.
2. An insert is guarded by "not exists" or a count with no unique constraint on the fields the guard tests; two transactions both see absence and both insert. Suggest: a unique constraint decides, with an insert that does nothing on conflict and its row count as the outcome.
3. A uniqueness conflict is read as "the row exists, use it" though the row may be expired, consumed or another caller's. Suggest: lock it, re-read it, decide by its state.
4. The rows-affected count is never read, so the conditional write decided nothing. Suggest: branch on it and report zero rows to the caller.
5. A rule the spec states (never two, single use, first wins, a decline closes it) is enforced by no write's condition. Suggest: name the one statement that enforces it and the column it reads; if no column can express it, see G1.
6. A guard is hung on the first write of a step ("put the condition on the first update; zero rows means refused, abandon the step"), and that write can legitimately change zero rows in healthy cases (it updates rows that are usually already in the target state, or that may not exist), so "zero rows" no longer tells "refused" from "nothing to do" and the guarded work is skipped where it should run. Suggest: a zero-rows outcome must have exactly one meaning; where it can have two, the guard is its own first statement (a read of the condition inside the transaction that already holds the write lock), and both the refused case and the healthy nothing-to-do case are tested.

#### B2. Two paths over the same tables

1. Two paths (two endpoints; an endpoint and a job; a job and its own retry) write the same two tables with no stated lock order, or different orders, and deadlock under load. Suggest: one order, written once beside the tables; a path that needs the other order restructures.
2. A helper takes a fresh connection or the global client while its caller holds a transaction, so it silently escapes the transaction. Suggest: the helper's signature says which handle it needs; no call site casts one into another.
3. The same call can arrive twice at once (a double click, a redelivered webhook, an overlapping cron) and nothing makes the second a no-op. Suggest: idempotency on a key the caller controls, or the conditional write.
4. The concurrency test fires two calls from one process on one connection and never overlaps. Suggest: a second connection holding a transaction open across the other's write; test at N−1 and at N.

#### B3. Locks and arrival rate

1. A write lock (a row lock, an application-level lock, the strictest isolation level) sits on a row a public path reaches (a scan, a landing page, a webhook, an anonymous submit); once arrivals exceed what the lock serves the queue only grows, and every waiter holds a pool connection, so unrelated requests fail. Suggest: public paths read without write locks and write through a conditional statement; state the cost as arrival against service, not as milliseconds.
2. No ceiling on waiting, so a waiter holds its connection until the pool is empty (a lock wait often has no limit by default). Suggest: a lock or statement timeout on the path, and what the caller sees when it is hit.
3. A retry has no backoff or no maximum ("retry until it succeeds"); two writers retry on each other's zero-rows signal forever. Suggest: jittered backoff, a ceiling, a message after the last attempt; zero rows is usually an answer to report, not a reason to retry.
4. A cap on a hot row is exact where the spec would tolerate eventual, or eventual where the spec demands exact. Suggest: say which the spec needs; eventual sweeps the excess later by last touched; exact says what bounds the queue.
5. A sweep takes the same write lock as the interactive path it cleans up after. Suggest: small conditional batches.
6. Exclusion between processes rests on something that is not a lock: a lease or lock file that each process reads and then writes ("absent or expired → take it"), so two processes can both see it free and both proceed, and an expiry lets a slow holder be overtaken mid-operation; or a real lock that only some of the writers of the protected resource take (a second program sharing the folder, work that keeps running after its caller was cancelled, such as an executor thread). Suggest: an operating-system exclusive lock or an atomic create, held for the whole protected operation; list every writer of the resource and confirm each takes it, including work that outlives cancellation. Better still, remove the need for exclusion: partition the resource by owner (one folder, key range or queue per owner) so the operation that needs it touches nothing anyone else writes, and sweep leftovers by owner at a point where nothing runs.

#### B4. One call, several effects

1. One call does two things (write the row and send the mail; save the text and apply the photo) and the second is "best effort", so the caller cannot tell it did not happen. Suggest: the result carries, per degradable step, whether it applied and why; the response contract names those steps.
2. The record is written before the effect that may still be refused (mark redeemed, then grant), so a refusal leaves a record saying it happened. Suggest: grant first, then record, in one transaction.
3. A response leaves early (a stream) before the step that sets a cookie or header has run. Suggest: scope the early return to callers that do not need it.

#### B5. Reads that must agree

1. A read-only procedure issues several statements whose results must agree, over rows another path writes; under default isolation they read two moments and assemble a state that never existed. Suggest: one query where it fits; otherwise a read-only transaction that reads one snapshot; never a lock for a read.
2. A screen assembles one fact from two queries (the list says nobody holds it, the detail says Sam does). Suggest: derive one view from the other.

### C. Who is asking

#### C1. Who the caller is

1. The client decides "signed in or guest" or "as user X" and chooses the behaviour or the endpoint; its session store is unresolved on first paint, cached for the last asker, and changeable from another tab. Suggest: the server decides from the request's credentials on whichever endpoint is hit and reports which branch it took; the client renders the outcome.
2. A control depends on identity and has no state for "not yet known", so unresolved reads as guest. Suggest: inert until a succeeded answer arrives.
3. The identity decision rides in a request body the client could set. Suggest: never; the cookie or token decides.

#### C2. A value inferred from "only X reaches here"

1. A value is derived from a precondition ("exactly one grant, so it is this one"; "this only runs after approval") instead of read, the code is reachable from a route, job or event that does not hold the precondition, and the value is write-once or names another user. Suggest: grep for every caller; check the constraint in code at the point of inference; read a write-once or authorizing value from the source that guarantees it.
2. "Cannot happen" or "only constructible by hand" with no list of the paths that could produce the state; the plainest create call with an ordinary parameter usually can. Suggest: enumerate the writers of the columns involved and what stops each.
3. A helper written for one route is reused by a second whose warrant differs. Suggest: the check moves into the helper.

#### C3. Ids and input crossing a boundary

1. A client-supplied id is used after an existence check as if existence were permission. Suggest: an ownership check against the caller, or the project's one visibility gate by name; "not found" and "not yours" are the same answer.
2. External input (a webhook, an OAuth callback, an upload, a queue message, a query string) is acted on with no shape check before the first dependent read. Suggest: shape, then authorization, then consistency.
3. One user's request reads or writes data another user owns and the plan names no check for it. Suggest: one line per crossing, naming its check.

#### C4. Outcomes the caller must not tell apart

1. The spec withholds an outcome ("declined looks like waiting"; "does not reveal whether the account exists") and the two outcomes differ on some channel: response shape, a `reason` field, status code, copy, mail, or the ability to ask again (a unique index with a status condition lets one outcome retry and not the other). Suggest: one response, one sentence, one constraint for both; the reason goes to a server-side column for support and never leaves.
2. A later read, a retry or a push behaves differently by outcome. Suggest: they obey the same rule.
3. Two withheld outcomes differ only on a *measured* channel: response time, response size, the rate of answers. It is a row only when an outsider can probe it at scale **and** the gap is large. Probing at scale means the input is guessable or enumerable, or the path is unauthenticated with no rate limit. A large gap is one that comes from a wait, a queue, a sent message or an external call, not from a few extra reads. Otherwise it goes under `Unlikely:` with that warrant, for example "ids unguessable; gap is a few reads, below network noise". Suggest: remove the large gap at its source, so the refusal does not wait on a lock, a queue or a call; a residual of a few reads is named in the plan's Non-Goals, never padded or faked.

### D. A screen holds state

#### D1. Where a value comes from

1. Local state is seeded once from an input, a session or a query result, the screen can mount before the source resolves or the source changes while mounted, and the draft keeps the stale seed. Suggest: derive during render; where a draft must be local, key it to the resolved value.
2. "When X changes, update Y" is a reactive side effect (an effect hook, a watcher) that copies a value from one place to another. Suggest: a derivation or the event handler; a side effect exists only to synchronise with a named external system.
3. A previous reader's copy paints for the next reader, stopped by comparing a server timestamp with a client clock. Suggest: the reader, or a generation that advances when the reader changes, goes into the cache key.

#### D2. A draft and the stored value

1. Dirty, valid, equal and "Save enabled" are computed on the raw draft while the schema trims and normalizes; a whitespace-only edit lights Save, and a draft one character from valid is discarded by Back as "unchanged". Suggest: every check reads the parsed value; an unparseable draft counts as unsaved text for every guard.
2. A reset from the server runs while an editor holds a draft opened during an in-flight write. Suggest: no reset while a write is in flight or an editor is open.
3. Save is greyed out with no reason shown. Suggest: the reason on the spot.
4. The leave-page guard is wired to one editor while another holds the draft. Suggest: the guard clears whichever editor holds it.

#### D3. Waiting on a push

1. The screen leaves "waiting" only in the push handler; an event that fires between first render and the subscription going live is never seen, and the screen waits forever. Suggest: subscribe, then read once; the push is a hint to read again.
2. A poll starts on a timer with no immediate first tick. Suggest: tick now, then on the interval.
3. The handler is not idempotent, so a read and a late push double the effect. Suggest: make it idempotent.
4. The screen asks again automatically when an answer disagrees with what it expects (a response for another account, a stale version, a missing row), and nothing says what happens when the second answer disagrees too: the re-ask fires once and the screen waits forever, or it fires on every render and storms. Suggest: a bounded number of automatic attempts keyed on the disagreement, not on anything recreated each render, then a visible state the person can act on (retry, sign in again).

#### D4. A read that failed

1. A parent's error branch returns early above a child block that has its own data, so the whole block disappears. Suggest: the child renders; the parent says it failed.
2. A result is branched on "there is none" while "not known yet" (pending or failed) is also possible and shares the branch, which on this route offers a creation form. Suggest: branch on the discriminant (an error flag, a status); error and unknown land before any branch that offers a write (F2).

### E. A journey across routes

#### E1. Context carried from hop to hop

1. A token or id rides in the URL and every hop must forward it; one exit (a signed-out fallback link, an already-done redirect, a Cancel, Back, a shortcut) is built without it, and the person arrives with nothing and no way back to a URL they never held. Suggest: list every navigation out of every route on the journey (every link, programmatic navigation, redirect and auth callback URL) with the context it forwards or the reason the journey may end there; forward from the same file that reads the value.
2. The journey crosses a sign-in or OAuth round trip and the context must survive the callback URL. Suggest: the callback carries it; or one holder (the session, a cookie, a pending row keyed on the account) replaces N forwards, where an anonymous visitor or an unstorable token does not rule it out.
3. The context is forwarded on the happy path and the other exits are called edge cases. Suggest: the list in E1.1.

#### E2. Redirects

1. A conditional redirect adds a history entry, so Back lands on the page that bounces again. Suggest: the redirect replaces the current entry.
2. Two routes redirect to each other on conditions (home sends the unset-up person to setup; setup sends the set-up person home) and a third state, the read pending or failed, satisfies both or neither. Suggest: the two conditions side by side with the failed-read row; a failed read redirects nowhere and says so.

### F. A branch over a value with several states

#### F1. Which states the branch names

1. A conditional (an `if`, a ternary, a `switch`, a fallback operator, a conditional render) names fewer states than the value has: two kinds of "empty" with different meanings, a status enum, a number where zero is real, a query result with pending, error, empty and data. Suggest: list the states from the type or the producer, the branch each takes, and where the rest land.
2. A boolean ("has x" from truthiness, "is empty" from a missing length) hides a third state before the branch. Suggest: branch on the discriminant.
3. A `switch` has no default, or a default that returns a normal case; a union gains a member and not every `switch` is revisited. Suggest: an exhaustiveness check that stops compiling when a member is added; the matching lint.
4. The branch structure is copied from a sibling and one of the sibling's branches did not come along. Suggest: diff the two.

#### F2. Where the rest lands

1. The states no branch names fall into a branch that offers a write (a form, an enabled button), performs one (a mutation, a redirect) or decides access. Suggest: order the guards so error and unknown reach a read-only branch; the test asserts the form is absent, not that the safe surface is present.
2. A health or status verdict is computed as "no failure seen, so healthy": the states no branch names (a monitor paused or never checked, an empty list of monitors, a probe that returned nothing, a file present but empty) land in "ok", because only the failure states were named. The verdict is shown to people who trust it, and it stays green while nothing is checked. Suggest: "ok" needs positive evidence for every member (each check ran and passed, now); "unknown", "none" and "stale" are their own outcomes, and the tests include a paused, an empty and a failed-probe case that must not read "ok".

### G. The domain says what exists

#### G1. A rule with no column

1. The spec states a rule over an entity (a cap, a holder, "at most one", "never again", "only while") that no column or index can express, and the plan enforces it in prose, a comment, or an `if` that reads something else. Suggest: add the concept first (a column, a counter, a status, a provenance id); then the check can live in the write (B1).

#### G2. An entity with states

1. "Is there a row" is asked of an entity with several states, so a blocked or expired row reads as "none" or as "reuse it". Suggest: per query, which states count; per question, which column is the truth.
2. A holder, owner or recipient is derived from relationships while a column holds it; two questions are answered from one piece of data. Suggest: read the column that is the truth; one source per question.
3. The plan's fix for a bug found by a concurrency test is a lock, and the bug would also fail single-threaded. Suggest: it is a model problem, not a race; fix the concept.

#### G3. A write anyone can trigger

1. A public path (a resolve, a scan, an anonymous submit, a webhook) inserts rows and nothing bounds how many. Suggest: a bound with an owner, self-healing where the path is public, ordered by last touched rather than created.

#### G4. A constraint removed

1. A write-once field becomes mutable, a unique index loses a column, a status condition is dropped, with no list of the paths the constraint was blocking. Suggest: enumerate those paths and what now stops each.
2. A new path writes rows into a table, or into a row shape, that existing foreign keys and check constraints were written for under the old writer (a composite foreign key that assumes the provider owns the referenced row; a check that assumes one kind of row), and the plan names none of them. The first insert or update on the new path fails at runtime, or the design quietly depends on a constraint it would have to drop. Suggest: list every constraint on each table the new path writes, and state for each one whether the new rows satisfy it; a constraint they cannot satisfy is a design decision, settled before code.
3. The reverse of G4.2: the plan adds a constraint (a check, a required column, a foreign key, a unique index, a required field in a shared schema) to existing data and checks it only against the writers the plan itself adds. Every existing writer must now satisfy it too — the obvious endpoint, but also a second endpoint that moves the same row to the same status, an admin tool, a background job, a data import, a seed script, the test fixtures that insert rows directly — and the first one that does not fails at runtime on an action nobody touched. Suggest: search every insert and update of the table or document (and of the constrained field) across the tree, tests included; list each writer with whether its writes satisfy the new constraint; where several writers must each remember to set something, one helper they all call.
4. A field the plan removes (a column, an attribute, a list of ids on each row) is the input of a guard or a purge: a fence that refuses a write when any id listed in the row belongs to someone being deleted, a deletion that finds copies by the ids they list, a coverage test whose set of guarded tables is derived from which tables have the field. The plan replaces the subject in a sentence ("the fence now checks the owner"), not in a mechanism. Once the field is gone the guard's input is empty, and a check over an empty set passes everything, so the guard silently disappears and the coverage test shrinks with it. Suggest: list every check, purge and test that reads the removed field; give each its new subject as a mechanism in the same change (the statement it runs, the explicit set of tables it covers); a guard whose input set is empty refuses rather than passes; one test per guard shows it still refuses after the change.

#### G6. The schema moves

1. A migration step targets "the current schema" (a constant every later change edits) instead of a frozen copy of the version it produces, so the next schema change silently changes what the old step builds: a file several versions behind is migrated straight to the newest shape but stamped with the old version, and the next step then fails on a column that is already gone, stranding the file. The plan for the new step also describes the runner it expects rather than the one the code has (who runs migrations, under which lock, whether a file already at the latest version still gets the cleanup). Suggest: before editing the current schema, freeze it as the previous version's constant and point that step at it; each step advances the version it reports; the new step uses the existing runner, and the plan cites the runner's real entry points; tests migrate from every supported old version to the latest and compare the result with a freshly created file.

#### G5. What names an entity

1. An entity's identity is derived from its content (a hash of the first words read, an image fingerprint, a normalized title), and that content is produced by a process that can return something different next time (recognition, extraction, a scrape, a user's correction). The same thing re-read gets a new identity and loses what hangs on the old one — corrections, history, progress — and two things that share an opening collide, so one inherits the other's. Suggest: a stable internal id assigned once; content-derived values are observations that propose a match, with confirmation when the match is ambiguous, never the key that history is attached to.

### H. Someone already owns this

#### H1. A library already in the plan

1. A hook, component or client takes an options object and the plan reads two options of it; an unset option's default does something (a navigation guard that, by default, also guards the browser's unload and prompts on every clean refresh). Suggest: every option, its value or "unset", its default and what the default does; set explicitly what touches the feature.
2. A hand-written listener, loop or check sits beside a library feature for the same concern: an unload listener beside a navigation guard, a window-resize listener beside a layout hook, a key listener beside a menu primitive, a retry loop beside a client that retries, a CORS or rate-limit step beside the framework's plugin, an existence check beside an ORM conflict option. Suggest: one of the two owns it; feed the library the same predicate in function form and delete the hand-written half.
3. The plan states how a library or the platform behaves with no source. Suggest: the doc page, the type definition or the issue.
4. The pairing is copied from a sibling "with the same guard" and never audited. Suggest: audit once at the source; fix every copy in one change.
5. Every test stubs the hook, so none sees what the library does, and the tests ask only "does it prompt when dirty", never "is it silent when clean". Suggest: one test with the real library; a silence assertion beside the positive one.

#### H2. An interaction about to be hand-written

1. The plan adds an effect, a custom hook or a component for an interaction concern (click-outside, focus trap, hotkeys, drag, a virtualised or sortable list, debounce, scroll lock, navigation blocking, a toast queue, clipboard, file drop) and names no library and no search. Suggest: search the stack and the manifest first (the headless kit, router, form, query and animation packages already imported own many of these; so does the platform — native dialogs, popovers, scroll snapping), then the ecosystem by the concern's name; adopt whole, or reject with a number or a missing feature, or hand-write against a checklist of what the library would have covered (touch, IME, keyboard and screen reader, RTL, nested instances, unmount mid-event, SSR, reduced motion).
2. A new helper is named like a well-known library export (click-outside, debounce, focus-trap, virtualizer) in a tree whose manifest already holds a package exporting it. Suggest: the search.
3. A library is rejected as "too heavy" or "we only need a part" with no number and no scenario. Suggest: the figure, or the scenario it fails.

#### H3. The codebase's own modules

1. A new function, hook, component, schema or helper decides, transforms or renders something an existing module already does under another name, and no search is recorded. Suggest: grep by the entity's name, the fields it touches and the verb of the decision; reuse, extend (naming the seam), or reject with the difference stated.
2. Once the plan lands, a decision has more than one site (old, new or both: a validation written as comparisons against a module's exported numbers in several files) and none is marked the owner. Suggest: one owner the rest import, repointed in the same change; a parity test across the sites.
3. A new module's interface makes the caller assemble, order or already know what the module could own: several raw fields it could derive from one value; two exports that must be called in order; a name that promises an answer but needs the answer as input; a test that must reproduce internal steps to reach it. Suggest: one call that performs the sequence; an object naming what varies; nothing the caller must know beyond the parameter list.
4. A new export forwards its arguments with no decision of its own, and deleting it would make nothing reappear elsewhere. Suggest: call what it wraps.

#### H4. Content about to be hand-made

Hand-made content is not the defect; hand-made content nobody chose is. An item the maintained set has no honest equivalent for (a brand mark, a domain concept, a glyph whose library twin carries the wrong meaning) is hand-made on purpose, and the reason is the record of that choice.

1. The plan draws, types or copies by hand a commodity set that maintained sources publish — icons, illustrations, flags; country, currency, language or time-zone lists; locale names, emoji data, a font — and names no source and no search. Suggest: the source a design or brand document already names, else a search of the ecosystem by the content's name; adopt it behind one module the project owns, and hand-make the items it has no honest equivalent for, each with its reason.
2. A prototype or design handoff is ported verbatim, its hand-made assets with it, though a document the project owns names a source for them. Suggest: map each asset to the named source before porting — the prototype decides the look, the document decides the source; an asset kept hand-made says why.
3. The plan adds one item to a hand-made set. Suggest: ask H4.1 once of the whole set, not only of the new item; the set's size is the figure H2.3 asks for.

#### H5. An operation the owner will repeat

1. The plan adds or changes something the owner will run or open more than once (a script, a command, a web page or tab, a health or configuration check) in a project that keeps a console of such operations, and no step updates it; the plan's own definition of done (tests, review) passes without it, so the operation ships reachable only from a reply that scrolls away. Suggest: a step "update the console": a button for each new recurring operation, the help line or card of each changed one, and the console's own check run; a one-off command stays in the reply and is not a button.

#### H6. A dependency that will move

A third-party library or SDK is owned by someone else, who releases on their own schedule: a new major, a changed transport, a dropped parameter. These questions ask whether the plan can absorb that change in one place and judge it before taking it.

1. A third-party library or SDK (a model provider's client, an HTTP client, an ORM, a workflow engine) is imported from more than one module, or its types (its client, its request and response objects, its exceptions) cross into domain code, so replacing or upgrading it touches many files and every one of them must be re-reviewed. Suggest: one adapter module owns the import behind an interface the project owns, and library types do not cross that interface (the adapter translates them into the project's own); an architecture test fails the build when the import appears anywhere else.
2. The plan puts an implementation behind an interface so it can be swapped (a second provider, a newer major of the same library, a local fallback), but its tests exercise only the current implementation, so a candidate is judged by reading its code and the swap is a leap. Suggest: one contract test suite, written against the interface, that runs against every adapter, current and candidate alike; a candidate is adoptable when it passes the same suite, and a behaviour the suite does not pin is named as untested.
3. A dependency is pinned (an exact version, or held below a major) with no reason naming what breaks without the pin, no condition that lifts it and no date to look again, so it silently ages: the ecosystem moves on, other libraries start requiring what the pin excludes, and the plan's next step must design around two versions of one thing. Suggest: every pin records its reason (what breaks), its lifting condition (the release, fix or decision that ends it) and a review date; at review, check the package's latest release and its default branch, since the fix may be merged and unreleased, and check whether other dependencies now require what the pin holds back.

#### H7. Any mechanism the plan introduces

H2 and H4 are instances of this sub-scenario for interaction concerns and commodity content. It applies at every size and in every layer: a UI behaviour, a server path, a data shape, a migration runner, a retry or deadline policy, a state machine, a domain algorithm (scoring, tracking, scheduling), a policy, a prompt, an operations script.

1. The plan introduces a mechanism and records no search for how others already solve it — a library, an open-source project, a paper, a product, a standard, or the codebase itself — so it is designed from zero and meets, one review round at a time, the edge cases its predecessors already handled. Suggest: one provenance line per mechanism: *adopted* (from where, at which version), *adapted* (what changed and why), or *original* (what was searched, and why nothing fit: a constraint, a number, a missing feature); a mechanism without a line is a row.
2. The plan cites research or references, and a mechanism ignores or contradicts what they found without saying why: the research recorded a pattern, a pitfall or a tool, and the design re-derives the mechanism instead. Suggest: trace each finding to the decision that uses or rejects it; a finding no decision mentions is either adopted now or rejected with its reason.

### I. One truth, several copies

#### I1. Two implementations

1. The same thing is rendered or parsed in two places (an editor's preview and the landing page; client-side trimming beside server normalization; a list row and a detail card) and drifts the day one side changes. Suggest: one component or one schema both sides import; a contract test across the sites; "keep both in sync" is the problem restated.
2. A prop or field named for a part (`recipientName`, `amount`) receives a composed value (a sentence, a formatted string). Suggest: the name states the contract; one line per boundary saying who composes what.
3. One place on disk (or one address, one queue) is named twice in configuration because two parties see it from two viewpoints — the path where a process writes a file and the path another process is told to read it from (a host path and a container path, a cache directory and a subdirectory of it) — and nothing checks that the two names denote the same thing; a template inherits one of them from another component and the first real use fails with the reader's generic error. Suggest: derive one name from the other wherever both parties share a host; where they cannot, a start-up check that the two agree (same basename, a probe file written by one and read by the other) and a message naming both paths when they do not.
4. The work is split across parallel workers (agents, teams, sessions) that meet at an interface (a constant, an environment variable, a path, a file name, a JSON shape), and the plan states the interface only in prose ("the backup service writes its status where the site reads it"), so each side names it on its own and both halves pass their own checks while the joined system reads nothing. Suggest: before the split, the plan fixes each interface by its exact names, paths and formats in one place both workers read; after the merge, a check that each name one side writes is the name the other side reads.

#### I2. A rule at several sites

1. A business rule ("someone who already left a note is not asked again"; "a removed member cannot post") is enforced by every caller rather than by the one statement that writes, and comes back in a new costume per caller that forgot it. Suggest: the rule moves onto the writing statement with its exemptions and their reasons beside it; caller-side checks are deleted.
2. Two rows of this review name the same cause and the suggestion for each is "add a check here". Suggest: one class fix that removes the possibility, listing the rows it covers.
3. A boundary (what may leave the system, what may be stored, who may see what) is stated in several documents — the agent instructions, the product principles, a security page, a decision record, an interface sketch — each with its own list of what is allowed, and the lists differ: one forbids images while another keeps an exception for one; one admits free text with redaction while another admits only an intent and a target. An implementer follows whichever document they read first, and a resolution written into one leaves the others stating the old list. Suggest: one document owns the list as a table (each permitted flow, its payload, its default, who may change it); every other document states the rule in one line and links there; a test enforces the table at the seam where data leaves, not at the import or the field name.
4. A check that guards a pipeline step (a detector, a validator, a classifier) runs inside the normal path, and the plan also allows a shortcut for the cases the normal path refuses (a manual run, a forced mode, an input built by hand for a stuck item), so items taken through the shortcut skip the check and its misses show up only downstream. Suggest: the shortcut is a mode of the same tool (a force flag) that still runs every check and only relaxes the condition it exists for; a hand-built input is not a step of the plan.

#### I3. A promise before an irreversible action

1. A confirmation sentence ("remove Sam"; "charge 3 seats") reads one copy of the value and the write uses another: a snapshot in one, fresh query data at click in the other; or the expected value is sent and the server never checks it. Suggest: one snapshot taken when the confirmation opens feeds both the sentence and the request; the expected value goes into the write's own condition, and zero rows changed is shown as "this changed under you".
2. On a phone the sentence sits at the end of a list and scrolls away while the button stays. Suggest: the sentence beside the button.

#### I4. A deletion that must reach every copy

1. A deletion ("forget this person", "purge this item") lists the stores it clears by their owners — the database, the cache folder, the uploads directory — while a consumer of one of those stores keeps a working copy of its own: an output device that converts or pads each cached file into its own folder and never deletes it, a thumbnail or transcoded rendition, a search index, a sync client, a backup. The deletion reports success and the copy outlives it, often indefinitely because nothing ages it out. Suggest: list every component that reads each store and whether it writes derived copies anywhere; give each copy a bounded lifetime (deleted after use, cleared at start-up or session start, swept by owner) or reach it from the deletion; the deletion's report states what it cannot reach, so the person is not told everything is gone.

#### I5. A change and the check that judges it

1. The project both changes a system (an enforce step, a response action, a migration) and checks it (an audit, a monitor, a scanner), and the change puts something into the set the check reads — a file it installs into a directory checked against an allowlist, a quarantine or backup folder inside the scanned roots, a snapshot written where secrets are searched — while the check's list of what is expected is a separate copy. Every correct change then reports as a finding, or the allowlist is widened by hand until it would also admit an attacker's look-alike. Suggest: list, per change, every artifact it leaves and every check whose scope contains it; the check recognises the change's own artifacts by an identity derived from the change's source (the file's hash in the repository, the path the change writes to), not by a second hand-kept list; an artifact that must stay visible, such as quarantined files, is reported as its own outcome, not as the original finding.
2. The change and the check address different properties of one thing: the change switches a capability off (a filter that disables a kind of credential, a disabled login, a port closed in front of a listener) while the check counts what exists (stored credentials, accounts, the listener), so the check keeps failing after a correct change; or the change removes what exists and the passing check says nothing about whether a new one can be made. Suggest: per check, state which property is the truth (can it be used, does it exist, can a new one be made) and point the change and the check at the same one; where two properties matter, two checks, and the plan says which change satisfies each.
3. The change is tested only on a fixture built by planting the defects it fixes, so every precondition the planting created (a directory, a file, a user, a configuration key) holds in every test instance, and the first clean instance — the common case in production — fails on a missing precondition. Suggest: for each kind of target the change touches, the test matrix holds one instance with nothing planted; the change creates or checks each precondition it relies on instead of assuming it.

### J. Time passes

An expiry, a trial or subscription ending, a hold or reservation lapsing, an invite or token timing out, an auto-close, a grace period, a reminder, "after N days": a state that changes because the clock moved, not because anybody acted.

#### J1. Who makes the change

1. A state changes when a deadline passes and the plan derives it at read time ("shown as expired once the date has passed"). Every decision that reads the *stored* state never sees the deadline: a unique index with a status predicate ("one active per user"), an "is it still held" check before granting it to someone else, a quota or seat count, a refusal to delete while something is active, a permission still granted by a role that has lapsed. The record reads as ended on screen and is still active to every write. Suggest: name who writes the transition — a scheduled sweep (and the runner that executes it), the next touch at every decision point (and the list of those points), or nobody, in which case it is a reminder and not a state; then list every decision that reads the state and which value it reads. An index or constraint predicate usually cannot read the current time.
2. Something must happen *at* the deadline — an email or push sent, a charge taken, a hold released to the next in line, a webhook fired — in a deployment with no scheduler, or with a scheduler the plan never names (a serverless host that scales to zero, a single process that restarts). Nothing happens until somebody makes a request, so "the user is notified when it expires" means "whoever next loads a page sees it". Suggest: name the runner and what it does when it is down or late; or compute it at read time and say so in the spec, with who sees it first.
3. Two clocks decide one deadline: the client computes "overdue", "expires today" or "N days later" from its own clock and time zone (or a day boundary in a third zone, the account's or the venue's) while the server decides from its own, so the screen offers an action the server refuses, or hides one it would allow. Suggest: one side computes it — the server, carried on the response as a flag or an instant — and the other renders it.

### K. A pipeline judges input

Input passes through stages — a sensor, a recognizer, a matcher, a scorer, a model call — and the system acts on what comes out: grades an answer, flags a word as misread, classifies a message, tells a person something about themselves.

#### K1. How the decision is stated

1. The decision is stated as several prose rules in different paragraphs or documents (when to advance, when to commit, when to flag, what a tie or a repeat means) that give an answer only when read together, and each review round finds a new input where two rules disagree or none applies. Suggest: state the algorithm once — pseudocode with its exact costs, thresholds, tie-breaks and boundary conditions (empty input, the first and last item, a repeat, a restart) — in one document every other links to; hand-execute it on a handful of named inputs, ordinary and edge, and keep those traces as the first tests.

#### K2. What an observation may conclude

1. An observation (what a stage reported: a different word heard, a face not seen, a value read) is recorded as a judgement about the person or the world (the reader misread it, the child was absent, the label is wrong) with no evidence independent of the stage that observed it, so the stage's own error becomes a verdict the person is told or that persists in their record. Suggest: keep observations and judgements as separate records; an observation becomes at most a candidate that keeps its uncertainty; a judgement needs evidence the observing stage did not produce (a second modality, the person's confirmation, a measured error rate under an agreed threshold); "unsure" and "unavailable" are outcomes distinct from "wrong", and neither is recorded against the person.
2. An absence of output ("the microphone track is silent", "the sensor sees nothing", "no event arrived") is read as a verdict on the device or the person (muted, broken, absent) from one measurement with no positive control: nobody made the sound, moved, or sent the event the measurement was waiting for, and the transport's own counters (packets, bytes, frames) kept flowing because the encoder never stops. Suggest: a negative measurement needs a positive control taken with the same probe (a known sound, a known motion, a test event), and the plan says which signal proves content as opposed to transport; until then the outcome is "nothing observed", not "device muted".
3. A difference between an installed copy and a reference copy (a checksum, a file list) is concluded as tampering or corruption, and the reference was picked by a matching label — the same name and version number — without showing it came from the same channel as the installed copy (a component bundled inside another package, a vendor's own build, a mirror), so every install from the other channel is reported as tampered. Suggest: per reference, the plan names the channel the installed copy came from and shows the reference is that channel's artifact; where the channels differ, it compares only what both share by construction or reports "not comparable" instead of "changed"; a first run on a known-clean install is the positive control.
4. A liveness check reaches its subject through a layer that can answer on the subject's behalf (an edge cache serving a stored page, a proxy's stale copy, a load balancer's maintenance page, a CDN that serves while the origin is off), so the check stays green while the subject is down. Suggest: the plan names, per check, what answers it; a check of the subject probes a path the layer never serves from storage (no-store, a cache bypass), and a check through the layer is kept as a separate signal of what visitors see.
5. A check that produces evidence (a restore test, a measurement, a scanner) accepts a missing or substituted subject as a normal result: a missing archive counted as zero files, a page that redirected to a login or challenge page measured as the requested page, an empty input scored as clean. The recorded evidence then describes something other than what it names. Suggest: before measuring, the check asserts that its subject exists and is the one requested (the file is present and readable, the final URL and status match the request); a missing or substituted subject is a failure with its own message, never a zero.
6. One observation (an empty page, a timeout, a 404, an empty result) is mapped to one cause (rate limited, server down) and drives an automatic reaction (back off, retry, stop), while other causes produce the same observation and need another reaction (the item is gone for good: deleted, its account suspended, never existed). A run of the benign cause, such as many posts from one suspended account, then triggers back-offs until the job stops, and the gone items are retried forever. Suggest: before the plan picks a reaction, it lists every cause that produces the observation and the signal that tells them apart (a page text, a status code, a header); each cause gets its own outcome, and only the cause the reaction is for counts toward it; a sample of real responses per cause is the test.

#### K3. How long it may take

1. One latency target ("feedback within 1.5 s") covers a path whose stages are met by different mechanisms (a local recognizer, a cached clip, a remote model call, an output device's own start-up delay, a per-utterance handshake that opens a channel or spawns a process before the first byte can play), the stages' allowances already sum past it, or a slow fallback with a long timeout sits on the same path. Suggest: one budget per thing the person perceives (acknowledged, a useful answer, a full explanation), each listing the stages on its path with their measured p50/p95 on the real output device; a stage that cannot meet a budget moves off that path (a handshake paid once per session or per turn, not per line); each path states the deadline at which it gives up and what the person sees then.
2. The plan measures an output's latency or completeness through a probe that shares the device or the channel with the thing it measures (a camera's microphone timing the camera's speaker on a half-duplex device; a process timing its own output through a buffer it also writes), or through a probe whose own start-up and buffering delay is unknown (a wireless microphone that starts a second late), so the number is void or shifted by an amount nobody measured. Suggest: an independent probe whose delay was calibrated first against a known event, placed where the person is; a device that cannot observe itself is named as such in the plan, and its budget is measured by the probe, never by its own counters.

#### K4. The sensor and where it stands

1. A threshold or calibration constant that decides an event (a frame difference that means "the page turned", an energy level that means "speech", a confidence below which a reading is discarded) is set on synthetic or rendered inputs, or on one clean recording, with no measured noise floor of the real sensor in its real place (its compression, its automatic gain, its lighting, the people moving in front of it). The detector either never settles or never fires once it meets the device. Suggest: the plan names, per threshold, the two measurements that bracket it on the real device (what quiet looks like, what the event looks like) and the margin between them; the synthetic value survives only as an explicit test setting with the reason it differs.
2. A recognizer stage assumes the framing of what it is given — an upright page, a face filling the frame, a label larger than N pixels, the object in the centre — and the capture is by a device placed by a person, so the page lies sideways, fills a fifth of the frame, or sits under a hand; accuracy targets were set on inputs that had the assumed framing. Suggest: state the capture geometry as a requirement with a measurable check at run time (fraction of the frame, line height in pixels, orientation score), a fallback when it fails (try the other orientations, ask the person, crop and retry), and a calibration run on real captures before any accuracy figure is promised.
3. The input device is "the default" chosen at open time (the operating system's default microphone or camera, the first device found), and the default can change under the running process — a wireless device drops, a virtual device takes its place — to one that keeps delivering frames that carry nothing (all-zero samples, black frames), so the pipeline reports that it is listening or watching and never hears or sees again. Suggest: name the device in configuration and log the one actually opened; treat a bounded stretch of nothing-valid as the device being lost, distinct from silence; say what the person is told and how capture is retried.
