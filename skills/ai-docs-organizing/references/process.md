# Process artifacts — templates and patterns

## 1. Inventory by loading layer

| Layer | What goes here | Ask of each item |
|---|---|---|
| A. Always-loaded contract | instruction files and their chain, the memory index, config the tooling injects into generation (e.g. an openspec `config.yaml`) | bytes, who loads it, where it stops |
| B. Skills | grouped by provenance: project-owned · shared via junction · vendored (lock file) · tool-generated; plus user-level rosters loaded into every session here | SKILL.md words, package bytes, whether a duplicate exists at another level |
| C. Harness wiring | hooks and the scripts they run, settings, launch configs, lock files, `.gitignore` comments that encode policy | what it actually detects (read the regex) |
| D. Pointer-reached docs | plan, specs, code locator, design docs, prompts, READMEs the contract names | entry sizes, cited paths exist |
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
| per-skill routing paragraphs | one line each; triggers belong in each skill's `description` | contract |
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

## 7. Reviewing the plan with the other agent

```bash
codex exec -s read-only -c approval_policy="never" -c model_reasoning_effort="medium" \
  -o tmp/review-round1.md -- "Review <plan.md> as a DESIGN and as a set of CLAIMS, not as prose. \
  1) VERIFY every factual claim against the repository — VERIFIED / WRONG / COULD-NOT-CHECK with evidence. \
  2) REVIEW the recommendations: what will be hard, what will keep going wrong, conflicts with <contract> / <ownership rules>, \
     information a future reader loses, anything wrong about how YOU load instructions and skills. \
  3) LIST what the inventory missed. Severity, target, evidence, concrete fix; one-line verdict."
```

Round 2 asks it to mark each round-1 finding ADDRESSED / PARTLY / NOT and hunt new problems. Verify every finding yourself; a finding that checked the wrong path is rejected with the right path. Two rounds usually converge for a plan; a loop that does not is telling you the design is wrong (`codex-review`).
