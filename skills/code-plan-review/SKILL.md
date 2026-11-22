---
name: code-plan-review
disable-model-invocation: true
description: Review a plan (a design doc, pseudocode, a diagram, a described change) before code exists. Walk a tree of stack-neutral questions, picked by the system views the plan touches and the kind of change it makes. Use it to review a plan or design, or to harvest a lesson into a question.
---

# Plan review by question tree

A plan is reviewed by asking it the right questions. The questions live in five files, one per architecture view. Inside a file they are grouped by defect class and nested as a tree. If the plan has no surface for a node, its children are not asked. Each question is stack-neutral. How a question shows up in one technology, and the fix there, lives in a binding file (`references/stacks/`). The classification standards are recorded in [`references/taxonomy.md`](references/taxonomy.md). How to add a question or a binding is in [`references/maintain.md`](references/maintain.md).

One reviewer walks the tree in one context, without subagents of its own. Where you can, the reviewer is a session that did not write the plan.

## Index

Pick the views by what the plan does and which files it changes. Then add the gates that each change kind always loads. When you are unsure about a view, load it.

| view | file | load when the plan touches | gates |
|---|---|---|---|
| S · Scenarios | [`views/scenarios.md`](references/views/scenarios.md) | a screen, a form, a client request, a route, a redirect, a sign-in round trip, what crawlers or link previews receive | S7 reach · S1 late responses · S2 after a write · S3 controls · S4 journeys · S5 compared values · S6 failures |
| L · Logical | [`views/logical.md`](references/views/logical.md) | who can do what, an entity or its states, a branch over a value, a constraint or schema, a decision rule | L1 access · L2 entities · L3 constraints · L4 decision rules · L5 branches |
| P · Process | [`views/process.md`](references/views/process.md) | a server write, concurrent callers, a lock or retry, one call with several effects, a deadline, a check or sensor that concludes something, a latency target | P1 concurrent writers · P2 load · P3 time · P4 latency · P5 several effects · P6 observations |
| D · Development | [`views/development.md`](references/views/development.md) | a new mechanism or module, a library or SDK, a rule or name stated in several places, a test or check, parallel workers | D1 parallel workers · D2 checks · D3 new mechanisms · D4 copies · D5 dependencies |
| O · Operations | [`views/operations.md`](references/views/operations.md) | work over many items, a step only the owner can unblock, a recurring operation, a deletion or retirement, content or input from another party | O1 deletion · O2 many items · O3 owner steps · O4 outside content |

| change kind | gates it always loads |
|---|---|
| add a mechanism, module or dependency | D3, D5 |
| remove, retire or loosen | L3, O1 |
| migrate a schema or data | L3, O2 |
| run over many items | O2, O3 |
| take in outside content or input | O4 |
| split work across parallel workers | D1 |

## How to review

1. Read the plan and any spec it implements. Restate the model in about five lines: who acts, which states exist, who decides what, and what an outsider already holds (are ids guessable, is the path signed-in, is it rate-limited). Questions about outsiders are judged against that line. Detect the stack from the manifests, schema and deployment configuration, and load the matching binding files. You can open files the plan names and grep the tree for callers, writers and exits. That is reading, not asking.
2. Pick the views and gates from the index.
3. Walk each loaded view. Ask every top gate (`S1`, `L2`, …). If the plan has no surface for a gate, write it under Not reached with the reason and skip its whole subtree. Otherwise ask each node below it, at every depth. A node whose surface is absent takes its subtree with it. A node the plan guards is marked *unlikely* with the guard cited, and its children are still asked. Judge from what the plan does, not from what it says about itself. Judge a node by its shape sentence only. Its `Suggest:` is the fix when the shape holds, not a requirement the plan must meet. Examples in a node illustrate it and never narrow it. Where a loaded binding has an entry for a node, search with its *look for* and take the suggestion from its *fix*.
4. Ask once for what only the author can supply. Examples: which paths write a table, the lock order of two paths, the arrival rate on a public path, which spec rule governs. Put every item in one message, each with the node it serves. Do not build the material yourself from the plan's sentences, and do not stop. Mark the nodes that depended on a declined item *cannot tell*, and still give the suggestion. If nobody can answer (a delegated review), write the items under Decisions for the owner, each with your recommendation. Then continue as if they were declined.
5. Report in the shape below. The review is done when three things hold. Every loaded gate has a row, an Unlikely entry or a Not reached line. Every row has a possibility, its reason and a suggestion. Every material item is recorded as supplied, declined, or read from the files.

### A second pass

When the resolutions change the plan substantially, review again, because fixes open new surface.

1. Re-walk only the gates the changed decisions touch, and append the result. The first pass's rows stay as they were.
2. Check that each resolution reached every place that stated the old decision. A resolution appended as "this wins" while the old text still stands is one truth in two copies (D4.2). Report each such passage as a row.
3. Ask L3.3 again for every constraint, column or state the resolutions added.

## What to report

First: The model, restated. For a delegated review, Decisions for the owner comes next. Then Most severe: at most five rows by node number, ranked by the ISO/IEC 25010 characteristic the failure harms. Safety and security come first: data corrupted, lost or disclosed. Reliability and functional suitability come next: a screen or action that breaks. The rest come last, for example a stale or misleading view.

Then one table per loaded view, with the nodes judged *likely*, *unspecified*, *possible* or *cannot tell*:

| node | where in the plan | possibility | suggestion |
|---|---|---|---|
| S1.1 | step 4, "reset the form from the response" | likely: the field stays editable while the save is in flight | refill only server-owned fields, and guard the rest by a token captured at send |

- node: the node number, and the binding when one supplied the shape or fix (`P1.1 · postgres`).
- where in the plan: the step, sentence or diagram message, or "nowhere" when the plan is silent where it must speak.
- possibility, each with a half-sentence reason. *likely*: the plan describes the defect (incorrect). *unspecified*: the plan is silent where it must decide (missing). *possible*: the plan opens a path to the failure, and the reason names it, but the plan does not show the failure happening. That nothing in the plan rules a failure out is not a reason. *cannot tell*: it depends on material that was declined or absent. Before code, a *likely* or *unspecified* row must be resolved.
- suggestion: the change to the plan, in one or two sentences. Rows with one cause get one class fix that names them all, never "add a check here" per row. A suggestion is proportional: weigh who can reach the failure and what it costs against what the fix costs everyone. If every fix costs more than the harm, the suggestion is "accept, and name it in the plan's Non-Goals". The node then goes under Unlikely with that reason.

Under each table, one line: `Unlikely: S3.1 (Save disabled on send, step 2), …`. Then one line: `Not reached: S4 (no route changes), …`.

After the tables: Not loaded, one line per view with the reason. Materials: each item asked for and its state, plus the bindings loaded and any technology in the stack that has none. Outside the tree: a problem no node names, one line each, so it can become a node later.

Do not rewrite the plan. Do not comment on style, naming or scope. In an OpenSpec repository the plan is the change's `design.md` and the report is `review.md` beside it: [`references/openspec.md`](references/openspec.md).

## Bindings

Present in `references/stacks/`: `postgres`, `tanstack-query`, `react`, `tanstack-router`, `web-platform`, `typescript`, `node-hosting`, `python-async-http`, `wordpress`, `semgrep`, `ansible`, `shell`. Each file says when to load it. Entries are keyed by node number, each with *shows up as*, *look for* and *fix*.
