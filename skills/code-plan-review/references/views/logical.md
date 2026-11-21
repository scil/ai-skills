# L · Logical view

The domain: who can do what, which entities exist and their states, the constraints over them, decision rules, and branches over values. The 4+1 logical view. Ask each gate first. If the plan has no surface for a gate, skip its subtree.

## CWE-284 · Access control

### L1. Does the plan decide who the caller is, or act on data that a caller names or another user owns?

- **L1.1** The client decides "signed in or guest" or "as user X" and picks the behavior or the endpoint. Or the identity rides in a request body the client sets. Suggest: the server decides from the request's credentials on every endpoint and reports which branch it took. The client renders the outcome.
- **L1.2** A caller-supplied id is used after an existence check as if existence were permission, or one user's request reaches another user's data with no named check. Suggest: one line per crossing, naming its ownership check or the project's one visibility gate. "Not found" and "not yours" are the same answer.
- **L1.3** A value is inferred from a precondition ("exactly one grant, so it is this one", "this runs only after approval") or a state is called impossible, but another route, job or create call reaches the code without it. A helper is reused by a route whose warrant differs. Suggest: list every caller and every writer of the columns involved. Check the condition where the value is inferred, inside the helper.
- **L1.4** Does the spec withhold an outcome from the caller ("declined looks like waiting", "does not reveal whether the account exists")?
  - **L1.4.1** The withheld outcomes differ on some channel: body, status, a reason field, copy, mail, a later read, a retry, a push, or the ability to ask again. Suggest: one response, one sentence and one constraint for both. The reason goes to a server-side column and never leaves.
  - **L1.4.2** The outcomes differ only on a measured channel: time, size, the rate of answers. This is a row only when an outsider can probe at scale (guessable or enumerable input, or an unauthenticated path with no rate limit) and the gap is large (a wait, a queue, a sent message, an external call). Otherwise list it as unlikely with that warrant. Suggest: remove a large gap at its source. Name a residual of a few reads in Non-Goals. Never pad or fake timing.

## CWE-664 · Resource lifetime

### L2. Does the plan add or change an entity, its states, or a rule over it?

- **L2.1** The spec states a rule (a cap, a holder, "at most one", "never again", "only while") that no column, constraint or single write enforces. It lives in prose, a comment, or a check in every caller, and returns with each caller that forgets it. Suggest: add the concept (a column, a counter, a status). Enforce the rule in the one statement that writes, with its exemptions beside it, and delete the caller checks.
- **L2.2** "Is there a row" is asked of an entity with several states, so a blocked or expired row reads as "none" or as "reuse it". Or a holder is derived from relationships while a column holds it. Suggest: for each query, which states count. For each question, the one column that is the truth.
- **L2.3** The fix for a bug a concurrency test found is a lock, but the bug also fails single-threaded. Suggest: fix the model, not the timing.
- **L2.4** An entity's identity comes from content that a process can return differently next time (recognized text, a fingerprint, a scraped title). A re-read gets a new identity and loses its history, or two items collide. Suggest: a stable id assigned once. Content proposes a match and never keys history.
- **L2.5** A public path (a scan, an anonymous submit, a webhook) inserts rows and nothing bounds how many. Suggest: a bound with an owner, self-healing on public paths, ordered by last touched.

### L3. Does the plan add, remove or loosen a constraint, a field, or a schema version?

- **L3.1** A constraint is removed or loosened (a write-once field becomes mutable, a unique index loses a column) with no list of the paths it blocked. Suggest: list those paths and what now stops each.
- **L3.2** A removed field was the input of a guard, a purge or a coverage test. The plan replaces the subject in a sentence, the guard's input set becomes empty, and a check over an empty set passes everything. Suggest: give each guard its new subject as a mechanism in the same change. An empty input set refuses. One test per guard shows it still refuses.
- **L3.3** A new writer meets constraints written for the old writers, or a new constraint meets old writers and old rows (another endpoint, an admin tool, a job, an import, seeds, test fixtures). The first one that does not fit fails at runtime. Suggest: for each table written, list every constraint and whether the new rows satisfy it. For each new constraint, search every insert and update across the tree, tests included, and list each writer with its result.
- **L3.4** A migration step targets "the current schema", which later changes edit, instead of a frozen copy of the version it produces. Or the plan describes a migration runner the code does not have. Suggest: freeze each version's schema for its step. Cite the real runner. Test migration from every supported version against a freshly created file.

## CWE-682 · Calculation

### L4. Does the plan define a decision algorithm: scoring, matching, or when to advance, commit or flag?

- **L4.1** The decision is spread over several prose rules that answer only when read together, and each review round finds an input where two rules disagree or none applies. Suggest: state the algorithm once as pseudocode with exact thresholds, tie-breaks and boundary cases (empty input, first and last item, a repeat, a restart). Hand-run it on named inputs and keep the traces as the first tests.

## CWE-697 · Comparison

### L5. Does the plan branch on a value with more than two states (an enum, an optional, a query result, a number where zero is real)?

- **L5.1** The branch names fewer states than the value has, or a truthiness test hides a third state. Suggest: list the states from the type or the producer and the branch each takes. Branch on the discriminant.
  - **L5.1.1** A `switch` has no default, or a default that returns a normal case, so a new member goes unnoticed. Suggest: an exhaustiveness check that stops compiling when a member is added.
  - **L5.1.2** The branch structure is copied from a sibling and lost one branch. Suggest: diff the two.
- **L5.2** The states no branch names fall into a branch that offers or performs a write, decides access, or reports "ok" ("no failure seen, so healthy", while a monitor is paused or a list is empty). Suggest: unknown and error reach a read-only branch first. "Ok" needs positive evidence for every member, and "unknown", "none" and "stale" are their own outcomes. Tests include a paused, an empty and a failed case.
- **L5.3** A formatter builds a line from a field with no branch, so empty or missing input renders as a blank or a zero. Suggest: every formatter states its output for empty, missing and malformed input. One test feeds it an empty record.
