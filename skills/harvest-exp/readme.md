# harvest-exp — where the rules came from

a finding is one kind of evidence, and the destination table decides where it goes.

- **Findings go to code-plan-review, not memory.** The user's global rule: lessons from incidents become questions or bindings there, never a new skill.
- **No cross-project lesson in project memory.** Claude's memory loads per project directory; a general lesson stored there is never seen by another repository. The first version said memory "enters every session's context" — only the `MEMORY.md` index loads, and only in that project.
- **Procedures become skills.** docs-maintainer's rule: a procedure is a skill, never a doc section.
- **Repository facts are placed by docs-maintainer.** Its layers and ownership map choose the owner better than a hand-written "AGENTS.md / README / runbook" list, and the prompt stopped naming one project's section headings so it works in any repository.
- **The global instruction file is edited only by replacement.** It shares Codex's 32 KiB instruction budget, is capped at 4 KiB, and was about 3.9 KiB when this skill was written.
- **Evidence over recollection** was added because long sessions get compacted and lose verbatim error text.
- **Only the candidate table is shown.** The original asked for a five-section retrospective in chat; the sections survive as the scan list in step 2.
