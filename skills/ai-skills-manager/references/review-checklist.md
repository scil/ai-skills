# Review checklist — one skill's SKILL.md

Walk it in order: description, body, references, mirror. Each line is a question with the disposition that a *no* produces. Verify against the tree, not the prose — `Test-Path` every link, read the referenced file's size, run the description-length line from [`slimming.md`](slimming.md).

## Description (always loaded, every harness, every turn)

| Question | If no |
|---|---|
| Is every clause a trigger — a situation, a phrase the user would say, a symptom? | Move ownership prose ("owns X; Y is Z's") to a **Scope.** paragraph under the H1; move an order of work to the instruction file (ai-agents-md). |
| Would the skill still fire on its own cases if the harness cut the description in half? | Put the two or three most distinctive triggers first; drop synonyms that only lengthen it. |
| Does it say what the skill is *not* for, when a sibling skill shares the territory? | Add one "Not for …" clause naming the sibling's case; longer than that is the sibling's description, not this one's. |
| Is it shorter than, or the same length as, before this review? | A description grows only when a trigger was missing — record the incident. |

## Body (loaded on trigger; budget is attention)

| Question | If no |
|---|---|
| Does the body open with a Scope paragraph and a two-line purpose, then principles, then paths? | Reorder; the reader arriving mid-task needs the path, not the essay. |
| Does each principle change what the agent does? | Apply the no-op test: delete what the current model does unprompted; keep what it gets wrong. |
| Does each path end on a *done when …* line the agent can check? | Write the criterion from the failure the path prevents. |
| Is every block that only some paths need, or that exceeds a screen, behind a pointer? | Move it verbatim to `references/<topic>.md`, one level deep. |
| Does the body restate anything an owner already holds — the instruction file's rules, a spec, conventions readable from the code? | Delete the copy; keep the owner's name and the facts with no other owner. |
| Does the body restate the description's triggers? | Delete; the description already fired. |
| Is a word count stated as a goal anywhere? | Replace with the landed number and the rule that stopped the cut. |

## References (loaded when a path names them)

| Question | If no |
|---|---|
| Does every relative link in the router and the references resolve? | Fix or drop the pointer; a stale pointer misleads and never saved a token. |
| Is each reference one topic, one level deep, named for its topic? | Split or merge; a reference named `misc.md` is the body's overflow, not a reference. |
| Is any reference read whole by every path — a hot reference? | Put a question-first map at its top and the reading rule in the path that routes to it (ai-docs-organizing → Hot pointer docs). |
| Was a block moved verbatim, or rewritten in transit? | Diff against the previous body; rewrite in a separate change so the move stays reviewable. |

## Mirror and history

| Question | If no |
|---|---|
| Does a human-language mirror (`for-human/*.zh.md`) exist, and does its header say how it lags? | Add the lag note; do not retranslate as a side effect of a review. |
| Does the commit or design doc carry the old-section → new-home map for the last restructure? | Write it now from the diff; the next reader must tell a decision from a leftover. |
