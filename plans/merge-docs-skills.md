# Plan: merge three docs skills into one

Status, 2026-11-20: steps 1 to 6 are done in the working tree and not committed. Step 7 waits for the owner. Step 8 is open: the junctions in Leafi, ThanksPorch, share-with and point-composer point to directories that no longer exist until step 8 runs. Both registries are past their 30-day gate, so the next run of the skill starts with a refresh.

## Goal

Merge `ai-agents-md`, `ai-docs-organizing` and `docs-maintainer` into one skill. The three skills already form one system. The layer model of `docs-maintainer` (layers 0 to 6) contains the other two: layer 0 is the instruction file (`ai-agents-md`), and the loading budget across layers is `ai-docs-organizing`. Today each skill opens with a hand-off line to the other two. Two skills repeat "one owner per fact", and two skills keep a separate refresh gate. `docs-maintainer` runs a script that `ai-agents-md` owns. After the merge, one skill owns all of it, and no rule is lost.

## Non-goals

- No change to what any rule says. This is a move and a deduplication, not a rewrite. A rule that looks wrong goes into the open-items register below, not into the merged text.
- No change to `ai-skill-audit`. It owns the content of one `SKILL.md` and stays separate.
- Historical records keep the old names: the changelog entries, `GPT-5.6-SKILLS-AUDIT.md`, daily logs, `skills-use-log.csv`, past plan entries and ADRs in other repositories.

## Decisions (owner, 2026-11-20)

| # | Decision | Result |
|---|---|---|
| D1 | Name of the merged skill | `project-docs`. |
| D2 | Old names after the merge | No stub directories. A stub is one more skill in every roster and a second copy of the description. The junctions point to the new name. |
| D3 | Where path steps live | Content that most runs need stays in `SKILL.md`: the principles, the loading model, the refresh gate and the path index. A run takes one path, so each path's steps live in `references/paths/`. |
| D4 | Sources registries | Registries with different subject areas stay separate: `sources-instruction-file.md` and `sources-docs-system.md`, each with its own changelog. A gap in days only is not a reason to keep two rules: both registries use `gate-days: 30`, and the script default becomes 30. The `gate-days:` line in each registry can change it. The tier definitions are one table, in `refresh.md`. |

## Target layout

```
project-docs/
  SKILL.md                     principles, loading model, refresh gate, path index
  readme.md                    the three origin stories, plus the merge, dated
  agents/openai.yaml           one interface entry
  scripts/check-sources.ps1    moved from ai-agents-md, default gate 30 days
  templates/
    AGENTS.md  AGENTS.nested.md  CLAUDE.md      from ai-agents-md
    ownership-map.md                            from docs-maintainer
  references/
    paths/                     instruction-file.md, loading-system.md, docs-system.md
    instruction-file/          rules.md, review-checklist.md, harness/, stacks/   (ai-agents-md)
    loading/                   harness-loading.md, process.md                     (ai-docs-organizing)
    docs-system/               structure.md, cross-cutting.md, diagramming.md,
                               adopting-openspec.md, alongside-mattpocock.md       (docs-maintainer)
    refresh/                   refresh.md (merged, one tier table),
                               sources-instruction-file.md, changelog-instruction-file.md,
                               sources-docs-system.md, changelog-docs-system.md
```

`SKILL.md` sections, in order:

1. Frontmatter. One description that names the triggers of all three old descriptions. `disable-model-invocation: true` stays.
2. One paragraph that defines the instruction file, the harness and the layer model (layers 0 to 6).
3. Principles. Merge the three lists (5 + 5 + 6 items) and delete duplicates: "one owner per fact", "the environment is the source of truth", "every rule names its check or `advisory`". Each merged principle keeps the wording of the strongest original.
4. The loading model comes first, with the probe (from `ai-docs-organizing`).
5. Every run starts with the refresh gate (D4).
6. Paths, grouped by object:
   - Instruction file: Create, Review, Update (grow from an incident).
   - Loading system: Audit and reorganize (the 7-step process), Source and symptom, Skills, hooks and memory, Hot pointer docs.
   - Docs system: Adopt, Create from nothing, Update after a change, Garden. File-First Split Rule and Alongside Matt Pocock's skills go here.
   - Refresh.
7. The three "Hand-offs" lines are deleted. One line remains: the content of one `SKILL.md` goes to `ai-skill-audit`.

## Steps

1. The open work in `docs-maintainer` (`SKILL.md` and the new `references/alongside-mattpocock.md`) moves with the merge. Leave the unrelated `code-plan-review` and `playwright-real-phone/` changes alone. Nothing is committed until the owner says so.
2. Write the rule-by-rule checklist before any move: one row for each principle, path step, "Done when" line and hand-off in the three old `SKILL.md` files, each with its planned new place. This is the register for the whole job (see L1 below).
3. Move files with `git mv` into the target layout, so history follows the files. Merge the two `refresh.md` and the two tier tables. The two registries and the two changelogs stay separate (D4).
4. Write the new `SKILL.md` and `readme.md`. Fill every row of the checklist with its new line.
5. Fix every relative link inside the merged skill (`../ai-docs-organizing/...`, `ai-agents-md/scripts/...`, `§n` pointers into `process.md`). Make sure that `check-sources.ps1` has no path to its old directory.
6. Update the references in this repository, from this explicit list (not from a search-and-replace):
   - `readme.md`: the "four docs skills" table becomes two rows (`project-docs`, `ai-skill-audit`), and the hand-off examples follow.
   - `ai-skill-audit/`: `SKILL.md`, `readme.md`, `references/sources.md`, `refresh.md`, `review-checklist.md`, `slimming.md`, `filler.md`.
   - `harvest-exp/SKILL.md`, `harvest-exp/readme.md`, `ai-harness/SKILL.md`.
   - `tiered-research/`: `SKILL.md`, `templates/sources.md`, `references/ai-agents.md` (the script path), `readme.md` (current-state lines only).
7. When the owner says so, commit this repository's change as one commit.
8. Other repositories, one commit each, only after you approve each one:
   - Junctions and manifests: `Leafi/.claude/skills` (two junctions, `ai-agents-md` and `docs-maintainer`, become one), `ThanksPorch/.claude/skills`, `share-with/.claude/skills`, `point-composer/.agents/skills`. In repositories with `scripts/win/link-shared-skills.ps1`, the `.gitignore` lines are the manifest: change the line, then run the script.
   - Instruction files: `point-composer/AGENTS.md` (line 74) and `wordpress-Guesthouse-demo/AGENTS.md` (the line 3 comment).
   - `symlink-center/docs/ai.md`, lines 17 and 37. These lines also name sections that do not exist any more.
   - Ownership maps: `Leafi/docs/ownership-map.md`, `ThanksPorch/docs/ai/ownership-map.md`, `share-with/docs/ai/ownership-map.md`.
   - Logseq pages that name the skills: `ai-coding.md`, `AI Agent___Context Files___skills.md`, `ThanksPorch.md`, `iking___shop.md`. Check their console buttons too.
   - Not changed: `point-composer/packages/core/test/fixtures/skill-docs-maintainer.md` and its name in `test/helpers.ts`. It is a parser test fixture, a frozen copy of a file, not a link.
9. Prove it (next section).

## Proof

- The checklist from step 2 has no empty row. Every old rule has a new place, or a reason why it was deleted as a duplicate, with the line that it duplicates.
- `SKILL.md` is 150 lines or fewer, and its byte count is reported.
- Every relative link in `project-docs/` resolves to a file that exists.
- `pwsh -NoProfile -File project-docs/scripts/check-sources.ps1 -Path <each registry> -GateOnly` runs for both registries.
- A search for the three old names across `E:\GitHub\scil` and `E:\GitHub\scil-only-me` finds only the historical files that the non-goals list.
- Every junction from step 8 resolves. In one project, Claude Code and Codex both list `project-docs` and neither lists an old name.

## Self-review against code-plan-review

- I1.1, I2.3 (one truth, several copies): the tier table exists twice today. The merge keeps one copy, in `refresh.md`, and both registries link to it.
- L1.1 (what is put off comes back): the step-2 checklist is the register. "Done" is the proof list, not an impression.
- L2.1 (the selection is the set you mean): the rename uses the explicit file list in steps 6 and 8. A search-and-replace on `docs-maintainer` also changes the test fixture name `skill-docs-maintainer`.
- L3.1 (a run that stops half way): after step 7, the old directories are gone and the junctions in step 8 are broken until they are repointed. Do step 8 in the same session, right after step 7. If step 8 stops, the junction list above is the record of what is left.
