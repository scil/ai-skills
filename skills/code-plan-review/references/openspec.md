# Running the review inside OpenSpec

In an OpenSpec repository the plan is the change's `design.md` and the review is a fifth artifact, `review.md`, that the CLI requires before `tasks.md` and therefore before apply. No hook is involved: `openspec instructions apply` reports `state: "blocked"` while a required artifact is missing. Verified on OpenSpec CLI 1.12.0.

## Where things live

```
openspec/schemas/<name>/schema.yaml        # the forked schema: artifacts, requires, apply gate
openspec/schemas/<name>/templates/*.md     # skeletons the CLI serves; never copied into a change
openspec/config.yaml                       # schema: <name>; apply guidance
openspec/changes/<change-id>/
  .openspec.yaml                           # pins the schema the change was created with
  proposal.md · specs/<capability>/spec.md · design.md · review.md · tasks.md
openspec/archive/<change-id>/              # the whole folder after archive; review.md travels with it
```

A repository that adopted the skill's earlier shape may still hold `openspec/intermediates/`. The skill no longer reads or asks for it; keep the folder as documentation or delete it.

## Adopt, once per repository

1. **Fork the built-in schema** and add the artifact. The fork copies `spec-driven` into the repository; only the diff below is yours.

   ```bash
   openspec schema fork spec-driven <name>
   ```

   In `openspec/schemas/<name>/schema.yaml`:

   ```yaml
   - id: review
     generates: review.md
     description: Scenario review of the design, by the code-plan-review skill
     template: review.md
     instruction: |
       Run <skill path>/SKILL.md over design.md in this context, in a session that
       did not write design.md where possible: walk the catalog, ask once for any
       material only the author can supply, and write the report here in the
       skill's shape — one table per scenario the design touches with its Unlikely
       line, then Not touched, Materials, Outside the catalog. Resolve every row
       marked likely by editing design.md (recorded under Decisions), never by
       editing this file; a row carried as it stands goes under Accepted with the
       reason.
     requires: [design]

   - id: tasks
     # append to the forked instruction:
     #   every row resolved in design.md has a task.
     requires: [specs, design, review]

   apply:
     requires: [tasks]
     tracks: tasks.md
   ```

   `<skill path>` is where the skill is reached in that repository (for a junction-linked shared skill, `.agents/skills/code-plan-review`).

2. **Template.** `templates/review.md`: a leading HTML comment pointing at the skill's "What to report", then headings for the per-scenario tables, `## Not touched`, `## Materials`, `## Outside the catalog`, `## Accepted`.

3. **`openspec/config.yaml`.**

   ```yaml
   schema: <name>
   operations:
     apply:
       guidance:
         - >-
           Read review.md with the other context files; a row marked likely that is
           neither resolved in design.md nor listed under Accepted is a blocker to
           pause on.
   ```

   Write multi-line strings as `>-` folded scalars: a plain scalar containing `: ` parses as a mapping, and the CLI then ignores the entry with a one-line warning that is easy to miss.

4. **Existing changes are untouched.** Each change's `.openspec.yaml` pins the schema it was created with; only changes created after the config switch use `<name>`.

5. **Prove the gate with a throwaway change**, then delete it:

   ```bash
   openspec schema validate <name>
   openspec new change tmp-probe
   openspec status --change tmp-probe --json          # artifacts: … design, review (requires design), tasks (requires specs, design, review)
   openspec instructions apply --change tmp-probe --json    # state: "blocked"
   ```

   The CLI's first line on `new change` may still print the built-in schema's name before `Schema: <name>`; the change's `.openspec.yaml` is the fact.

6. Done when the schema validates, the probe shows `review` between `design` and `tasks` with apply blocked, and the project's instruction file names the schema and the review artifact in its process line.

## Per change

`/opsx:propose` (or `/opsx:continue`) walks the artifacts in dependency order, so the review runs after the design and before the tasks without anyone remembering to ask for it. A likely row is resolved by editing `design.md` and recording the decision, not by editing `review.md`; `review.md` is appended to, never rewritten, so the rows that were raised stay visible beside what was decided.
