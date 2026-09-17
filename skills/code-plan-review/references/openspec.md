# Running the plan pass inside OpenSpec

In an OpenSpec repository the plan is the change's `design.md` and the plan pass is a fifth artifact, `review.md`, that the CLI requires before `tasks.md` and therefore before apply. No hook is involved: `openspec instructions apply` reports `state: "blocked"` while a required artifact is missing. Verified on OpenSpec CLI 1.12.0.

## Where things live

```
openspec/schemas/<name>/schema.yaml        # the forked schema: artifacts, requires, apply gate
openspec/schemas/<name>/templates/*.md     # skeletons the CLI serves; never copied into a change
openspec/config.yaml                       # schema: <name>; rules per artifact; apply guidance
openspec/changes/<change-id>/
  .openspec.yaml                           # pins the schema the change was created with
  proposal.md · specs/<capability>/spec.md · design.md · review.md · tasks.md
openspec/archive/<change-id>/              # the whole folder after archive; review.md travels with it
```

The structured intermediates — numbered pseudocode at the deciding statements, the mechanism's diagram as fenced text, named participants, numbered messages, assumptions with how each was verified — are sections of `design.md`, under the Decision they belong to and in an `## Assumptions` section. They are not a separate artifact: the review anchors its rows to their numbers, and a sixth file would put every anchor across two documents.

## Adopt, once per repository

1. **Fork the built-in schema** and add the artifact. The fork copies `spec-driven` into the repository; only the diff below is yours.

   ```bash
   openspec schema fork spec-driven <name>
   ```

   In `openspec/schemas/<name>/schema.yaml`:

   ```yaml
   - id: design
     # keep the forked instruction; append:
     instruction: |
       …
       The review artifact that follows anchors its findings to this document, so
       the design also carries what <skill path>/SKILL.md lists under "What a
       reviewable plan contains" (the stack in one line; numbered pseudocode at
       the deciding statements; the diagram the mechanism needs as fenced Mermaid;
       participants named,
       messages and transitions numbered; an Assumptions section, each with how it
       was verified). Which diagram, if any, is your judgement from what the change
       touches.
     requires: [proposal]

   - id: review
     generates: review.md
     description: Trap review of the design, one batch of incident-harvested rules per fresh context
     template: review.md
     instruction: |
       Do not write this artifact's findings yourself: the context that wrote
       design.md is the wrong one to grade it.
       Follow the Plan pass in <skill path>/SKILL.md: check design.md against
       "What a reviewable plan contains" and return to the design if an item is
       missing; dispatch one fresh-context subagent per batch file — all of them,
       in one step — with the skill's plan prompt verbatim, design.md, the
       batch file and the change's spec deltas; assemble outputs verbatim under
       one "## <batch>" heading each, keeping every APPLIES, SKIPPED and SEARCHED
       line;
       merge: verify each row at its anchor, return a row with no anchor or no
       proof to its batch once and list it under Unresolved if it comes back
       still empty (never drop it), resolve blocking rows in design.md (recorded
       under Decisions), re-run only the batches the resolution touched, dedupe
       OUT-OF-BATCH lines across batches into one list under Accepted with a
       disposition each.
       Complete when every batch has an APPLIES line and a verdict, every
       blocking row is resolved in design.md or listed under Accepted with the
       author's reason, no row is unanchored, and Unresolved is empty. Moving a
       line from Unresolved to Accepted needs the reason, not the move.
     requires: [design]

   - id: tasks
     # append to the forked instruction:
     #   every blocking row that changed the design has a task whose
     #   verification is that row's proof column.
     requires: [specs, design, review]

   apply:
     requires: [tasks]
     tracks: tasks.md
   ```

   `<skill path>` is where the skill is reached in that repository (for a junction-linked shared skill, `.agents/skills/code-plan-review`).

2. **Template slots.** `templates/review.md`: one `## <batch>` heading per batch file in the router's table, in that order, then `## Accepted` and `## Unresolved`, with a leading HTML comment saying to paste each subagent's output verbatim and never to fill a section from the design's context. `templates/design.md`: an HTML comment under Decisions naming the pseudocode and diagram requirement, and an `## Assumptions` section before Risks.

3. **`openspec/config.yaml`.**

   ```yaml
   schema: <name>
   rules:
     design:
       - >-
         Name the project's bindings where a rule in <skill path> applies — the
         database handle types, the visibility gate function, the query-key helpers —
         so the review can check the design uses them, not a hand-rolled equivalent.
       - >-
         A change that touches <the project's trap surfaces: a mutation, a conditional
         write, two procedures over the same tables, a lifecycle status, a session read
         on the client> carries the numbered pseudocode and the diagram the skill's
         "What a reviewable plan contains" asks for; the review returns a design that
         lacks them.
   operations:
     apply:
       guidance:
         - Read review.md with the other context files; implement each blocking row's
           mitigation column, and treat a blocking row that is neither resolved in
           design.md nor listed under Accepted, or any line under Unresolved, as a
           blocker to pause on.
   ```

   Write rules as `>-` folded scalars: a plain scalar containing `: ` parses as a mapping, and the CLI then ignores the artifact's rules with a one-line warning ("Rules for 'design' must be an array of strings") that is easy to miss.

4. **Existing changes are untouched.** Each change's `.openspec.yaml` pins the schema it was created with; only changes created after the config switch use `<name>`.

5. **Prove the gate with a throwaway change**, then delete it:

   ```bash
   openspec schema validate <name>
   openspec new change tmp-probe
   openspec status --change tmp-probe --json          # artifacts: … design, review (requires design), tasks (requires specs, design, review)
   openspec instructions design --change tmp-probe --json   # rules: two strings, no warning
   openspec instructions apply --change tmp-probe --json    # state: "blocked"
   ```

   The CLI's first line on `new change` may still print the built-in schema's name before `Schema: <name>`; the change's `.openspec.yaml` is the fact.

6. Done when the schema validates, the probe shows `review` between `design` and `tasks` with apply blocked, the design instruction served by the CLI names "What a reviewable plan contains", and the project's instruction file names the schema and the review artifact in its process line.

## Per change

`/opsx:propose` (or `/opsx:continue`) walks the artifacts in dependency order, so the review runs after the design and before the tasks without anyone remembering to ask for it. Two cautions the instruction text carries, because the propose loop runs in one context: the review's findings come from subagents, never from the loop; and a blocking row is resolved by editing `design.md` and recording the decision, not by editing `review.md`.
