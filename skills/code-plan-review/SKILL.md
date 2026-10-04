---
name: code-plan-review
disable-model-invocation: true
description: Review a plan (a design doc, pseudocode, a diagram, a described change) before code exists by walking a catalog of scenarios and asking each one's questions: a client sending a request, a server write, who is asking, screen state, a journey across routes, a branch over several states, the domain model, reuse of libraries and modules, one truth in several copies, a state that changes as time passes. Use when asked to review a plan or design, before implementing a change that touches any of those, or when harvesting a lesson from an incident into a question here.
---

# Plan review by scenario

A plan is reviewed by reading it with the right questions in hand. The catalog below is those questions, grouped by the scenario that raises them; they are stack-neutral, and how each one shows up in a particular technology — and the concrete fix there — lives in a binding file per technology ([Bindings](#bindings)). A question does not need a confirmed defect to be worth reporting: where the plan leaves room for it, report the possibility and a suggestion. One reviewer walks the whole catalog in one context, without fanning out to subagents of its own; where you can, that reviewer is a session that did not write the plan — a fresh session, or an agent the authoring session delegates the review to. Where the questions came from: [`readme.md`](readme.md).

## How to review

1. **Read the plan**, and the spec it implements if there is one, then **restate the model** in about five lines — who acts, which states exist, who decides what — so a misreading is corrected before any question is built on it. **Detect the stack** from the manifests, schema and deployment config (package manifests, ORM schema, migrations, the start script or platform config) and load the matching files from `references/stacks/`; a technology with no file is reviewed from the questions alone. Files the plan names that exist in the checkout may be opened, and the tree grepped for callers, sites and exits, to settle a question; that is reading, not asking. A plan reviewed without them is still reviewed.
2. **Walk the catalog**, scenario by scenario. Decide whether the plan touches each top-level scenario; for each it touches, walk its sub-scenarios and ask every question. Judge from what the plan does, not from what it says about itself. A plan that already guards against a question gets that question marked *unlikely* with the guard cited, not skipped. Where a loaded binding has an entry for the question, search with its *look for* and take the suggestion from its *fix*.
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
- **suggestion**: the change to the plan, in one or two sentences. Two rows with one cause get one suggestion that names both; a suggestion that patches one spot while another row names the same cause is the wrong suggestion.

Under each table, one line: `Unlikely: A1.2 (idempotency key, step 6), A1.5 (one save on this screen), …` — the number and the guard, so the record that the question was asked exists without a row.

After the tables: **Not touched**, one line per scenario with the reason; **Materials**, each item asked for and whether it was supplied, declined or read from the files, and the bindings loaded (with any technology in the stack that has none); **Outside the catalog**, a problem you saw that no question names, one line each, so it can become a question later.

Do not rewrite the plan. Do not comment on style, naming or scope. In an OpenSpec repository the plan is the change's `design.md` and the report is `review.md` beside it: [`references/openspec.md`](references/openspec.md).

## Harvest a lesson

1. State the incident: what was planned, what went wrong, and which question, asked of the plan, would have raised it.
2. **Decide the layer.** A new *shape* of problem — one no question describes, in any technology — is a new question. A known shape showing up in a technology in a way its binding does not yet say (a default, an API, a syntax, a limit) is a new or extended binding entry, and the question stays as it is. Something true only of this project (its function names, its tests) belongs in the project's own instructions, citing the question number. Most incidents are bindings.
3. For a question: find the sub-scenario where that moment belongs and append one numbered line: the shape the problem takes in a plan, in stack-neutral words, then *Suggest:* the change, stated as the property the spec needs rather than only the fix the incident used. A moment no sub-scenario covers gets a new sub-scenario; a mechanism no scenario covers gets a new lettered scenario. Numbers are never reused or shifted. Never a new skill. For a binding: add or extend the entry under the question's number in `references/stacks/<technology>.md`, creating the file if the technology has none.
4. Tell the story once in [`readme.md`](readme.md), dated. Done when the question or binding entry exists and the readme holds the incident.

## Bindings

A binding file, `references/stacks/<technology>.md`, says how the catalog's questions show up in one technology layer — a database, a data client, a UI framework, a router, the platform, the language, the hosting shape — and the concrete fix there. Stacks are combinations, so files are per layer, not per stack. Present: [`postgres`](references/stacks/postgres.md), [`tanstack-query`](references/stacks/tanstack-query.md), [`react`](references/stacks/react.md), [`tanstack-router`](references/stacks/tanstack-router.md), [`web-platform`](references/stacks/web-platform.md), [`typescript`](references/stacks/typescript.md), [`node-hosting`](references/stacks/node-hosting.md).

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

1. The spec withholds an outcome ("declined looks like waiting"; "does not reveal whether the account exists") and the two outcomes differ on some channel: response shape, a `reason` field, status code, timing, copy, mail, or the ability to ask again (a unique index with a status condition lets one outcome retry and not the other). Suggest: one response, one sentence, one constraint for both; the reason goes to a server-side column for support and never leaves.
2. A later read, a retry or a push behaves differently by outcome. Suggest: they obey the same rule.

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

### I. One truth, several copies

#### I1. Two implementations

1. The same thing is rendered or parsed in two places (an editor's preview and the landing page; client-side trimming beside server normalization; a list row and a detail card) and drifts the day one side changes. Suggest: one component or one schema both sides import; a contract test across the sites; "keep both in sync" is the problem restated.
2. A prop or field named for a part (`recipientName`, `amount`) receives a composed value (a sentence, a formatted string). Suggest: the name states the contract; one line per boundary saying who composes what.

#### I2. A rule at several sites

1. A business rule ("someone who already left a note is not asked again"; "a removed member cannot post") is enforced by every caller rather than by the one statement that writes, and comes back in a new costume per caller that forgot it. Suggest: the rule moves onto the writing statement with its exemptions and their reasons beside it; caller-side checks are deleted.
2. Two rows of this review name the same cause and the suggestion for each is "add a check here". Suggest: one class fix that removes the possibility, listing the rows it covers.

#### I3. A promise before an irreversible action

1. A confirmation sentence ("remove Sam"; "charge 3 seats") reads one copy of the value and the write uses another: a snapshot in one, fresh query data at click in the other; or the expected value is sent and the server never checks it. Suggest: one snapshot taken when the confirmation opens feeds both the sentence and the request; the expected value goes into the write's own condition, and zero rows changed is shown as "this changed under you".
2. On a phone the sentence sits at the end of a list and scrolls away while the button stays. Suggest: the sentence beside the button.

### J. Time passes

An expiry, a trial or subscription ending, a hold or reservation lapsing, an invite or token timing out, an auto-close, a grace period, a reminder, "after N days": a state that changes because the clock moved, not because anybody acted.

#### J1. Who makes the change

1. A state changes when a deadline passes and the plan derives it at read time ("shown as expired once the date has passed"). Every decision that reads the *stored* state never sees the deadline: a unique index with a status predicate ("one active per user"), an "is it still held" check before granting it to someone else, a quota or seat count, a refusal to delete while something is active, a permission still granted by a role that has lapsed. The record reads as ended on screen and is still active to every write. Suggest: name who writes the transition — a scheduled sweep (and the runner that executes it), the next touch at every decision point (and the list of those points), or nobody, in which case it is a reminder and not a state; then list every decision that reads the state and which value it reads. An index or constraint predicate usually cannot read the current time.
2. Something must happen *at* the deadline — an email or push sent, a charge taken, a hold released to the next in line, a webhook fired — in a deployment with no scheduler, or with a scheduler the plan never names (a serverless host that scales to zero, a single process that restarts). Nothing happens until somebody makes a request, so "the user is notified when it expires" means "whoever next loads a page sees it". Suggest: name the runner and what it does when it is down or late; or compute it at read time and say so in the spec, with who sees it first.
3. Two clocks decide one deadline: the client computes "overdue", "expires today" or "N days later" from its own clock and time zone (or a day boundary in a third zone, the account's or the venue's) while the server decides from its own, so the screen offers an action the server refuses, or hides one it would allow. Suggest: one side computes it — the server, carried on the response as a flag or an instant — and the other renders it.
