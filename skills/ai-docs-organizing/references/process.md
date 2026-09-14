# Process artifacts — templates and patterns

## 1. Inventory by loading layer

| Layer | What goes here | Ask of each item |
|---|---|---|
| A. Always-loaded contract | instruction files and their chain, the memory index, config the tooling injects into generation (e.g. an openspec `config.yaml`) | bytes, who loads it, where it stops |
| B. Skills | grouped by provenance: project-owned · shared via junction · vendored (lock file) · tool-generated; plus user-level rosters loaded into every session here | SKILL.md words, package bytes, whether a duplicate exists at another level |
| C. Harness wiring | hooks and the scripts they run, settings, launch configs, lock files, `.gitignore` comments that encode policy | what it actually detects (read the regex) |
| D. Pointer-reached docs | plan, specs, code locator, design docs, prompts, READMEs the contract names | entry sizes, cited paths exist; **how many skills / contract lines route to it** — two or more makes it *hot* (§10) |
| E. Human mirrors | translations, "for-human" folders inside skill directories, the vault | does any agent load it; does it carry a project decision |
| F. Residue | stale worktrees, deleted apps still described, skills for things that no longer exist | verify with `ls` before calling it stale |

Tag every number with provenance and the date. Re-count anything a reviewer disputes.

## 2. Disposition table for a diet

One row per block of the contract:

| Block (lines) | Disposition | Owner afterwards |
|---|---|---|
| destructive-action rules, scattered | gather into a 5-line block at the top | contract |
| a rule with rationale | stay, compressed to invariant + `Instance:` + test/spec | contract |
| an executable recipe | move to the doc that owns hands-on procedures, or delete if superseded (check the route/command it names still exists) | that doc |
| an inventory of scripts/commands | delete — `ls` and `package.json` answer it | environment |
| retired-environment history | one line each | contract + the doc that tells the story |
| per-skill routing paragraphs | delete — each skill's `description` is its trigger, and the contract lists no skills; trace the meta-rule that produced the list (§7) | (none) |
| a product rule with tests but no spec | a spec requirement written from the tests; one sentence + test name stays | spec |

Then a rule-by-rule checklist (old line → new home) kept beside the change, so "every rule survived" is checkable rather than claimed.

## 3. The byte-budget guard (shape)

```ts
export const REPO_CHAIN_BUDGET_BYTES = 28 * 1024;
export const START_DIRECTORY_CHAINS = {
  ".": ["AGENTS.md"],
  src: ["AGENTS.md", "src/AGENTS.md"],
};
it("keeps every start directory's chain within budget", ...);   // sums real file sizes
it("measures the files it claims to measure", ...);            // nested file > 0; root+nested == sum; bridge file is one import line
```

Run it before the rewrite: it must go red on the old contract.

## 4. Specs for rules that lived only in the contract

Write the requirement from the shipped behaviour and the tests that prove it, and name each scenario after its *situation* so it maps to a test name ("Tapping the receded backdrop", not "Backdrop does nothing"). Where the contract's prose disagrees with the tests, the prose is the stale party — correct the prose, keep the code. Sync the delta to the main spec if the behaviour already ships, so pointers to `specs/<capability>` resolve immediately.

## 5. Hook baseline

`SessionStart` writes `git status --porcelain` as `{path: mtimeMs}` to `%TEMP%/<project>-docs-nudge/<session_id>.json`. `Stop` counts a path as changed this session when it is absent from the baseline or its mtime moved; with no baseline it falls back to the whole tree. "Docs touched" means owner paths only (contract files, `openspec/`, `docs/`, `.agents/`, Markdown under `src/`). Exercise the cases by piping JSON payloads through the scripts: new code + no doc → block; new code + owner doc → allow; stale stray `.md` only → still blocks for new code; `stop_hook_active` → allow.

## 6. Memory triage table

```
| Memory | Bin | Owner / reason |
| <name> | a | already in <owner> |          → delete (or keep a one-line pointer if it adds a how-to-apply)
| <name> | b | written into <owner> |       → then delete
| <name> | c | behaviour / harness quirk |  → keep
| <name> | d | stale: <why> |               → delete
```

Write the table first, delete second, regenerate the index from the survivors, and check every survivor is indexed. Expect roughly half of a mature memory store to be bin a: the repo caught up with it.

## 7. Tracing a symptom to its source

Questions to ask of every problem the inventory surfaces, with the command that answers each:

| Question | How to answer |
|---|---|
| Which commit introduced this section or sentence? | `git log --format='%h %ad %an %s' --date=short -S'<heading or distinctive phrase>' -- <file>` — the oldest hit is the origin; read its diff for the rule that arrived with it |
| Where else was the rule copied? | `git grep -n -i '<phrase>' -- <contract> <docs skill> <hooks> .gitignore`, plus the agent's memory directory (outside git: `Select-String` / `rg` there) |
| Is a tool regenerating it? | look for `generatedBy`, a lock file, a CLI (`openspec`, a skills installer, TanStack Intent markers) — then change the generator's input and regenerate, never the output |
| Is a hook nudging toward it? | read the hook script's regexes and the reason text it emits |
| Did an event happen that nobody propagated? | `ls` the thing the sentence describes (the app, the route, the environment); check the commit that removed it for what it forgot |
| What will make it regrow? | whatever answered the first question — a rule still standing, a generator unchanged, a memory still loaded |

Kinds of source seen so far, and the fix for each:

- **A meta-rule in the contract** ("routing stays here; skill files must not reference each other") → delete or invert it in the contract, and delete the ownership row it spawned in the docs skill, in one change; then remove the section it produced.
- **A memory that enshrined a habit** ("a skill is not registered until listed in AGENTS.md") → delete the memory; its owner is now the docs skill.
- **A recipe that outlived the environment** (a smoke script opening a route that no longer exists) → delete the recipe; the event that obsoleted it (the one-command dev environment) is already recorded where it happened.
- **A removal nobody propagated** (an app deleted, its skill and two sentences kept) → delete the leftovers; the guard is the path-exists check in the inventory.
- **A measurement in the wrong unit** (words, when the harness cuts by bytes) → change the unit, add the byte guard, re-count.

The trace goes into the change's design or proposal, one line per source: *commit · rule · copies touched · guard added*.

## 8. Reviewing the plan with the other agent

```bash
codex exec -s read-only -c approval_policy="never" -c model_reasoning_effort="medium" \
  -o tmp/review-round1.md -- "Review <plan.md> as a DESIGN and as a set of CLAIMS, not as prose. \
  1) VERIFY every factual claim against the repository — VERIFIED / WRONG / COULD-NOT-CHECK with evidence. \
  2) REVIEW the recommendations: what will be hard, what will keep going wrong, conflicts with <contract> / <ownership rules>, \
     information a future reader loses, anything wrong about how YOU load instructions and skills. \
  3) LIST what the inventory missed. Severity, target, evidence, concrete fix; one-line verdict."
```

Round 2 asks it to mark each round-1 finding ADDRESSED / PARTLY / NOT and hunt new problems. Verify every finding yourself; a finding that checked the wrong path is rejected with the right path. Two rounds usually converge for a plan; a loop that does not is telling you the design is wrong (`codex-review`).

## 9. Slimming a skill into a router plus references

1. **Land pending edits first.** `git status` the skill's directory; if someone else's uncommitted changes sit in the file, commit them as their own change before rewriting — the slim's diff must contain only the slim.
2. **Classify every section** as *step* (what the agent does, in order), *in-file reference* (rules consulted on demand by every path), or *disclosed reference* (needed by some paths only, or large). Only the first two stay in `SKILL.md`.
3. **Move disclosed blocks verbatim** into `references/<topic>.md`, one level deep, one topic per file (a structure tree; a diagramming rule set; a cross-cutting checklist plus the small rules that only apply on that path). Fold tiny standalone sections (a "framework rule", a "location rule") into the path that uses them as one sentence plus a pointer.
4. **Write the router**: a two-line purpose; principles — only the ones that change behaviour, each one paragraph; the split rule; the paths, each a numbered list of steps ending on a *done when …* line, the most common path first; a references-and-templates list. The description stays the trigger list; the body stops restating triggers.
5. **Apply the no-op test** sentence by sentence: delete what a current model does unprompted ("prefer clear headings"). The test is model-relative — settle a disagreement by running the skill, not by debate.
6. **Check every pointer** in the router and the references resolves (`Test-Path` each relative link); a moved section breaks the links that named it.
7. **Record the old-section → new-home map** in the change's design doc or, when there is none, in the commit message body, one line per section, naming any sentence deliberately dropped and why.
8. **Mark human mirrors** (`for-human/*.zh.md`) as lagging, in their own header, with the shape of the lag; do not retranslate as a side effect.
9. **Report the landed number honestly.** A 500–700-word target is a guideline; a router of 900 words in which every sentence is a rule, a step, or a done-criterion has met the goal, and a 600-word router that dropped a rule has not.

Folding a drifted project-local fork back into the shared skill is the same move at the skill-set level: generic rules and templates go up into the shared skill; the project's owners by name go into a project doc its agents read (an ownership map, pointed at from the contract); the fork is deleted; the shared skill is linked in through the ignore manifest. Every reference to the fork (hooks' reason text, in-flight change tasks) is updated in the same commit; archived history is left alone.

## 10. Dieting a hot pointer doc

**Find the hot docs**: `git grep -n -l '<doc path>' -- <contract> .agents/skills/*/SKILL.md` — a doc named by the contract or by two or more skills as *the* place for a kind of question is read whole by every task of that kind.

**Measure per `## ` section, in bytes** (PowerShell; the same idea in any shell):

```powershell
$lines = Get-Content $f -Encoding utf8
$h = @(); for ($i=0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^## ') { $h += [pscustomobject]@{ line=$i; title=$lines[$i] } } }
for ($j=0; $j -lt $h.Count; $j++) { $end = if ($j+1 -lt $h.Count) { $h[$j+1].line } else { $lines.Count }
  "{0,6} B  {1}" -f [Text.Encoding]::UTF8.GetByteCount(($lines[$h[$j].line..($end-1)] -join "`n")), $h[$j].title }
```

**Disposition, one row per block** (the same table as §2, with the hot-doc dispositions):

| Block | Disposition | Owner afterwards |
|---|---|---|
| shipped behaviour that a spec / test owns | concept + the reasoning that produced it + owner name; the mechanics go | the spec |
| target state that ships nowhere | stays whole | this doc |
| the "why" behind a decision (why either party may complete; why not a seventh mode) | stays — it has no other owner | this doc |
| changelog comments, "revised by" narratives | archive file beside the doc | `archive/` |
| padded tables | rewrite with trimmed cells (often 40–60% of a table's bytes) | — |
| a superseded MVP variant kept beside the target type | delete; one sentence says what shipped instead | — |

**The map at the top** — one row per section:

```
| § | Answers | Shipped contract lives in |
| 6 | What can be shared; placement, the three axes, pinning, editing, removal | `resource-sharing`, `resource-placement`, `offering-*` |
```

plus the reading rule, in the doc *and* in every skill that routes to it: *read the map, then the section that answers your question, then the spec it names; do not read the whole file for one question.*

**Split test, after the diet**: a section still > ~10 KB **and** read for a different purpose than its neighbours → its own file with a two-line stub; otherwise leave it. Then check every `§n` pointer and every path that named the moved section.

**Report**: bytes before → after per section, what was handed to which owner, and the reading rule's new location.
