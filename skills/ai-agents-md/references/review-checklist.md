# Review checklist for an existing AGENTS.md / CLAUDE.md

Run top to bottom. Each item names what to check and what a hit becomes in the findings table (line · defect · disposition).

## A. Loading and size (measure, do not estimate)

1. **Chain bytes per start directory**: root + each nested file on the path + the user-level global file. Codex cap is 32 KiB combined. Over → *ai-docs-organizing* diet, not a rewrite here.
2. **Lines per file** against the 200-line Claude Code target. Over → split by scope (nested file, `.claude/rules/` with `paths:`), not by section.
3. **Bridge integrity**: `CLAUDE.md` is `@AGENTS.md` plus Claude-only lines; no shared rule lives only in the bridge. `Test-Path` the imported file.
4. **Nested files only point upward** and only carry rules that differ from the root.

## B. Every line: admission

5. **Inferable** — the manifest, lockfile, `ls`, CI or lint config answers it (stack, directory map, dependency list, formatter-enforced style, an overview). → delete as inferable.
6. **Stale** — a path that does not exist, a script not in the manifest, a tool not in the lockfile, an app or environment that was retired. Verify each with `Test-Path`, `Select-String -SimpleMatch` in the manifest, `git log -S` for when it left. → delete as stale, and find what removed the thing without propagating.
7. **One-off** — a rule with no `Instance:` and no plausible repeat. → delete or downgrade to a pointer.
8. **Task-list contamination** — "currently working on", "next sprint", names of people. → delete; the tracker owns it.
9. **README duplication** — same sentence exists in the README or a doc. → delete here, pointer if needed.
10. **Skill list** — a section enumerating skills. → delete; trace the meta-rule that produced it.
11. **Secrets or internal identifiers.** → remove, rotate if committed.

## C. Every line: wording

12. **Vague modal** ("prefer", "try to", "usually", "be careful"). → reword MUST / SHOULD / MAY.
13. **Unfalsifiable** ("write clean code", "test thoroughly"). → reword to a checkable condition or delete.
14. **Emphasis words** (ALWAYS, CRITICAL, double-check, be thorough, IMPORTANT). → remove the emphasis; keep the condition.
15. **Negative-only phrasing** outside the Boundaries block. → invert to the positive invariant.
16. **Unconditional verification** ("run the full suite before every change"). → scope to the kind of change; name the CI job that runs the rest.
17. **Contradiction** with another line, a nested file, a `.claude/rules/` file, or the user-level file. → resolve now, one survives.

## D. Every rule: enforcement

18. **No enforcement layer named.** → add `Enforced by:` or tag `advisory`; propose the hook / CI / lint / test that could own it.
19. **Enforceable but only in prose** (a forbidden path, a forbidden command). → move to a `PreToolUse` hook or Codex hook; keep one line.
20. **Destructive-action policy scattered** → gather into the top Boundaries block, ≤ 6 lines.

## E. Structure

21. **Sections with no admitted line** → delete the heading.
22. **Order**: Boundaries first, then Commands, Verification, Architecture rules, Conventions, Traps, Pointers, Definition of done.
23. **Maintainer notes** in prose → move to HTML comments (stripped by Claude Code before injection; Codex sends them — keep them short).
24. **Pointers resolve**: every path named exists; every doc pointed at has a reading rule if it is large.

## Report shape

```
| Line | Text (first words) | Defect (checklist #) | Disposition | Evidence |
```

Then: bytes and lines before → after if all dispositions were applied; which rules moved to which enforcement layer; which findings the user rejected and why.
