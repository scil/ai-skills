# Rules for what goes into an instruction file, and how it is written

## 1. Admission threshold

A line enters `AGENTS.md` only if at least one holds, and the line says which:

| # | Criterion | Test |
|---|---|---|
| a | **Non-inferable** — the agent cannot learn it from the tree in one read | Can `ls`, the manifest, the lockfile, CI or lint config answer it? Then it is inferable: out. |
| b | **Costly when wrong** — data loss, a deployed migration edited, a secret committed, an irreversible external action | Would a wrong guess cost more than a turn? |
| c | **Repeated** — the agent has done it wrong at least twice, or a human typed the same correction twice | Name the incidents (`Instance:`). A first occurrence is a prompt, not a rule. |
| d | **Team agreement** — a convention that differs from the tool's default and is not encoded anywhere the agent reads | Is it already in a linter or formatter config? Then the config owns it: out. |
| e | **Architecture boundary** — who may call whom, where a kind of code may live | Is there a test or lint that enforces it? Name it; otherwise tag `advisory` and consider adding one. |
| f | **Verification requirement** — what must be run before a change counts as done, scoped to the kind of change | Unconditional "run everything before every change" raises cost (agents follow it); scope it: "a change under `packages/db/` runs `pnpm db:test`". |

Everything else — stack description, directory map, dependency list, architecture overview, code style the formatter enforces, pasted code, the current task — stays out. The controlled study (Gloaguen et al.) found an Overview section in 95–100% of generated files; removing it changed nothing, and files did not get agents to the right file sooner. Two qualifications from the same study and a second one (Lulla et al.): when a repository has no README or docs, a context file *does* help, so criterion (a) then admits the one paragraph the README would have carried; and developer-written files of non-inferable rules measurably cut exploration time on small tasks. The line to hold is "what the tree cannot say", not "as short as possible".

## 2. Shape of a rule

```
- <Positive invariant, MUST / MUST NOT / SHOULD / MAY>. Instance: <what went wrong, yyyy-mm-dd>. Enforced by: <hook | CI job | lint rule | test name | advisory>.
```

- **Positive phrasing.** "Database access goes through `packages/db`" activates the right behaviour; a list of "Do not…" keeps the forbidden one in view. Use MUST NOT only for the destructive-action block.
- **Modal words carry meaning.** MUST / MUST NOT: hard rule. SHOULD: default, an exception needs a stated reason. MAY: allowed. Replace "prefer", "try to", "usually", "be careful to".
- **Falsifiable.** "Use 2-space indentation" can be checked; "format code properly" cannot. A rule with no possible violation is not a rule.
- **No emphasis words.** "ALWAYS", "CRITICAL", "double-check", "be thorough" produce over-compliance in current models: extra verification passes, repeated test runs, more reasoning tokens. Anthropic's own prompting docs say to remove verification instructions and "dial back any aggressive language" for the Opus 4.5+ line (`harness/claude-code.md`); the controlled study measured the same mechanism on GPT-5.2. State the condition once, plainly.
- **Enforcement layer named.** A rule that only exists in prose is `advisory`; say so, and prefer moving it to a `PreToolUse` hook (Claude Code), a Codex hook, a CI job, a lint rule or a test. The instruction file is context, not configuration.
- **One home.** A rule lives in the root file, or a nested file for its subtree, or a path-scoped `.claude/rules/*.md` (Claude Code only, loaded when matching files are touched). Never two of these.

## 3. Section menu

Each section exists only if it has at least one admitted line. The order puts the highest-cost mistakes first.

| Section | Admits | Typical enforcement |
|---|---|---|
| **Boundaries** (top, ≤ 6 lines) | never-do actions: secrets, deployed migrations, generated dirs, production data, force-push, creating issues/PRs without being asked | sandbox/approval config, `PreToolUse` hook, `.gitignore`, branch protection |
| **Commands** | only commands whose *choice* is non-obvious: the package manager when several lockfiles could exist, the test filter syntax, the one script that must run before another | the scripts block in the manifest is the truth; here only the non-obvious pick |
| **Verification** | scoped done-criteria per kind of change | CI job names |
| **Architecture rules** | boundaries not encoded in code | a dependency-cruiser / eslint-boundaries / arch test, else `advisory` |
| **Conventions that differ from defaults** | naming, file placement, error handling patterns the formatter cannot see | lint rule where possible |
| **Known traps** | the gotcha no config confesses: a flaky suite, an OS-specific path, a tool that rewrites line endings | the incident it came from |
| **Pointers** | one line per doc the agent must read for a kind of question ("domain rules: `docs/plan.md`, read the map first") | the doc exists (`Test-Path`) |
| **Definition of done** | what the final message must report, if the team wants a fixed shape | advisory |

Persona lines ("You are a senior…") are out: the harness sets the role, and the study of 2,500 files that recommended them measured Copilot custom agents, not repository instruction files.

## 4. What never enters

- Secrets, tokens, account names, internal hostnames.
- The current task, sprint, or who is working on what — that is the issue tracker.
- A list of skills — each harness discovers them by scanning; the list is a second copy paid every turn.
- Content copied from the README — measured to hurt.
- History and rationale essays — one `Instance:` clause, then a pointer if the story matters.
- Rules for other agents' quirks that this repo does not run.

## 5. Sizes

- **Codex** concatenates the chain (global + root + nested on the cwd path) and stops adding at 32 KiB without notice. Budget the chain, in bytes, for every directory an agent is started in; a root file under 4 KB leaves room for nesting.
- **Claude Code** targets under 200 lines per file; `@imports` load at launch and count in full; nested `CLAUDE.md` files load on demand; `.claude/rules/*.md` with a `paths:` frontmatter load only when matching files are read.
- Report bytes and lines before and after every edit. Words are the wrong unit.

## 6. Growth and pruning loop

```
agent fails → human corrects → does it repeat, or is it costly? 
   no  → it was a prompt; nothing written
   yes → hook / CI / lint if enforceable; one line here with Instance: and date
every PR → does this change retire a rule? change one? earn one?
every refresh (7 days) → has a harness or a source changed what this file should say?
```

The three PR questions replace calendar reviews. Two rules that contradict each other are resolved at once: the agent otherwise picks one at random, and a trusted file spreads the error further than an untrusted one would.
