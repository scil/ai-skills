# Path: the loading system across harnesses

Read this to audit or reorganize everything the agents load in a project: instruction files, skills, hooks, per-agent memory. Use it when a second harness joins a repo (Claude Code beside Codex or the reverse), when an instruction file passes ~25 KB or a hot pointer-reached doc (a plan, a domain model, a locator) passes ~40 KB, when an agent keeps missing a rule that is "written down", or before adding an `AGENTS.md` section. `§n` points into [`../loading/process.md`](../loading/process.md).

## Process

1. **Inventory by loading layer**, not by folder (§1).
2. **Measure** the bytes of every instruction chain an agent can start in (root, nested files on the path, the user-level global file); probe each harness; count skills and check for a roster-budget warning.
3. **Verify every claim against the tree** and tag its provenance: `[repo]`, `[user-config]`, `[external-local]`, `[runtime]` (with the probe), `[session]` (dated). Name each dispute between documentation, probes and sources, with the evidence on each side and the finding its weight supports.
4. **Review the plan with the other agent before editing** — read-only, as a design and as claims (§8, `codex-review`); it knows its own loading model. Verify each finding; reject with evidence.
5. **Decide a disposition per block** (§2): stay compressed · move to an existing owner · delete because the environment is the truth · delete as stale. Amend the ownership map deliberately; never invent an owner to legalize a move. Trace every problem to its source first ([`SKILL.md`](../../SKILL.md) → Source and symptom).
6. **Execute in order**: the byte-budget guard, red on the old contract (§3; raising the harness's limit restores text, not attention); specs for contract-only rules, written from shipped behaviour and tests, never the prose (§4); the contract; skills; hooks; memory; the user-level file.
7. **Prove**: guard green; probe again (the file's last heading arrives, no mid-sentence cut); the full gate; a rule-by-rule checklist giving every original rule its new home.

## Skills, hooks, memory

- **The contract lists no skills.** A skill is registered by existing; a "Project Skills" section is a second copy of every description. Delete it with the meta-rule that forced it, and write no "skills are not listed here" line — that rule belongs in this skill. Shared-skill membership lives in the ignore manifest the link script reads.
- **Four provenance classes, four policies** (§1); **the roster is a budget** — Codex shortens *every* description once it overflows (§11).
- **A Stop-hook nudge needs a SessionStart baseline**, or a stray edit silences it forever; count only owner paths (§5).
- **Memory triage, four bins** (§6); regenerate the index from what survives.
- **User-level preferences live in one file**, where the harness without imports reads natively, imported by the other and sized within the shared budget.

## Hot pointer docs

A doc that the contract or two or more skills name as *the* place for a kind of question costs bytes × reads, and every read is whole-file. Diet before splitting (§10): measure sections in bytes; hand shipped behaviour to its spec, keeping concept, reasoning and owner (unshipped target state stays whole); history to an archive; a question-first map on top, and the reading rule — map, section, owner — in the skill that routes there; split last, by purpose; prune the pointers that named it. Instance: [`../../readme.md`](../../readme.md), the ai-docs-organizing part, item 9.
