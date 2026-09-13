# ai-docs-organizing — where this came from

A procedural skill, not one lesson deep: it holds the norms and the process for organizing the documents agents read, and the incident that produced them. Add to it when an organizing round teaches something the process did not already say; project-specific facts stay in the project.
这是一个流程型 skill，不是"一课深"：它装的是整理 AI 文档的规范与流程，以及产生它们的那次事故。只有当一轮整理教会了流程里没有的东西时才往里加；项目专属事实留在项目里。

## The incident (2026-09-12/13, ThanksPorch) / 事故

**The ask.** Plan how to organize the project's AI documents — `AGENTS.md`, skills, hooks, memory — for two agents (Claude Code on Opus 5, Codex on GPT), considering that different models have different requirements, strengths and weaknesses. Then have Codex review the plan, then execute it.
**任务。** 为两个代理（Claude Code / Opus 5，Codex / GPT）规划 AI 文档的整理，考虑不同模型的差异；再让 Codex 评审计划，然后执行。

**What the review found that the plan had missed.** The plan measured `AGENTS.md` at 9,877 words and proposed a diet in words. Codex's first-round blocker: the file was 66,794 bytes and Codex reads its `AGENTS.md` chain only up to `project_doc_max_bytes` — 32 KiB by default, no override set, no notice. A probe with file reads forbidden confirmed it: Codex's copy ended mid-sentence in line 305, and *Working Discipline, AI Failure Guards, Testing Discipline, Domain Guardrails, Project Skills* had never arrived. Claude Code, meanwhile, auto-loads `CLAUDE.md`, which the repo did not have — so it received none of the contract automatically. Both agents had worked for months on a contract neither fully held.
**评审抓到、计划漏掉的。** 计划按"词数"称重并按词数减肥；Codex 第一轮的 blocker：文件 66,794 字节，而 Codex 只读到 `project_doc_max_bytes`（默认 32 KiB），静默截断。禁止读文件的实测证实：Codex 的副本在第 305 行句中结束，五个关键章节从未到达。Claude Code 则只自动加载 `CLAUDE.md`，仓库没有——所以它一点都没自动拿到。两个代理数月来都在一份谁都没拿全的契约上工作。

**Other findings that changed the plan.** "AGENTS.md is Codex's only brake" was narrowed: the brake is the sandbox/approval config; prose is the behavioural layer. Proposed destinations broke the project's own ownership rules (no parallel docs tree, no directory READMEs). Deleting a vendored skill's compiled duplicate would have broken its documented interface. A `prepare` step that recreates junctions would mutate the checkout. The tap-to-edit prose in the contract contradicted the shipped behaviour and its E2E tests on two points; a spec written from the prose would have enshrined the stale version. One finding was rejected with evidence (it had checked `<worktree>/node_modules`; the tree was at `<worktree>/src/node_modules`).
**其它改变计划的发现。** "唯一刹车"改成"唯一行为层"；原定的搬迁目的地违反项目自己的归属规则；删第三方 skill 的编译副本会破坏其接口；`prepare` 自动建 junction 会改动检出；契约里的 tap-to-edit 描述与已上线行为和 E2E 测试有两处矛盾——按文字写 spec 会把过期版本写进规格。一条发现被有据驳回（它查错了路径）。

**What was done.** Contract 66,794 → 28,078 bytes under a 28 KiB chain budget (4 KiB reserved for the user-level global file), guarded by a unit test that went red on the old file first; a one-line `CLAUDE.md` bridge; every rule kept as invariant + `Instance:` + enforcing test, with a rule-by-rule checklist; two homeless rules became specs written from the tests; a `nextjs` skill for a deleted app removed; `OVERLAY.md` declared the one project-owned file inside a vendored skill; a `SessionStart` baseline for the docs-nudge hook; memory triaged 75 → 30 files; one user-level preference file for both harnesses. Probe afterwards: last heading `## Reference Sources`, all sections present, global file received, no cut. Codex, having read the new global file, answered the probe bilingually — the preference had reached it.
**做了什么。** 契约减到 28 KiB 预算内并有先变红的守卫；一行桥接文件；规则逐条保留并有映射表；两块无主规则按测试写成 spec；删了服务对象已不存在的 skill；定了覆盖文件模型；钩子加会话基线；记忆 75→30；用户级偏好一份两用。事后实测：完整到达、无截断；Codex 读到新的全局偏好后用双语作答——偏好真的到了它那里。

## Why it happened, and the rule each part became / 原因与规则

1. Nobody had asked what each harness actually loads. → *The loading model comes first; probe, don't assume.*
2. Size was measured in words. → *Budget in bytes, for the whole chain, guarded in the gate.*
3. Project facts had accumulated in one agent's memory. → *The repo is the only shared memory; memory is for behaviour.*
4. The contract carried recipes, inventories and history beside its rules. → *Information hierarchy; the environment is truth.*
5. The plan's own numbers were partly wrong. → *Verify claims, tag provenance, review with the other agent before editing.*
6. Prose had drifted from tests. → *Specs from shipped behaviour, never from the prose.*
7. The contract carried a "Project Skills" section — one line to a paragraph per skill, ~3 KB — because its first version (2026-05-28) had ruled "routing stays here; skill files must not route to other skills", and the docs skill had turned that into an ownership row. Traced to the source and deleted the same day: descriptions carry triggers, the ignore manifest carries membership, the contract names no skill. The harness re-read the changed descriptions within the session. A first attempt moved the skills' *order* ("domain model → data layer → implementation") into three descriptions; the user cut it — that order was already a rule about the work in the contract, and restating it per skill only lengthened three always-loaded lines. → *The contract lists no skills; fix the meta-rule, not the list; a description is a trigger, not a workflow.*
   契约里有一节"Project Skills"，每个 skill 一行到一段，约 3 KB——因为第一版契约（2026-05-28）规定"路由只在这里，skill 不得互相引用"，文档 skill 又把它写成了归属规则。当天追到源头并删除：description 承担触发，忽略清单承担成员关系，契约不点任何 skill 的名。壳在会话内就重新读到了改后的 description。第一版尝试把 skill 的*顺序*写进三条 description，用户砍掉了——那个顺序本就是契约里关于工作的规则，逐个 skill 重述只是让三行常驻文字变长。→ *契约不列 skill；改元规则，不改清单；description 是触发条件，不是工作流。*

## The trace, in the format the skill asks for / 追溯记录

| Symptom | Source (commit · rule) | Copies touched | Guard |
|---|---|---|---|
| `## Project Skills`, ~3 KB, one line to a paragraph per skill, regrowing with every skill added | `7d40898` (2026-05-28, the contract's first commit) · "Keep project skill routing in this section; skill files describe only their own scope and do not route to other skills" | the contract's meta-rule (deleted); `local-docs-maintainer` Ownership Map row "skill routing → AGENTS.md" (replaced by rows for description / ignore manifest / overlay); memory "a skill is not registered until listed" (deleted); the hard-coded name list in the link script (now reads `.gitignore`) | the byte-budget test; the harness re-reading descriptions is the mechanism itself |
| `apps/nextjs` "exists, scheduled for removal" + a skill kept for it | the commit that removed the app propagated nothing | two sentences and the skill + lock entry (deleted) | inventory step: `ls` what a sentence describes |
| a smoke recipe opening `/signup` | predates the one-command dev environment; the route was renamed later | the recipe (deleted) | none needed — the environment is the truth |
| a diet planned in words | the plan measured the wrong unit | re-measured in bytes | the byte-budget test |

症状 → 源头（提交·规则）→ 触及的副本 → 守卫：这是 skill 要求的追溯格式；上表是本次的实例。

## How to maintain / 怎么维护

Keep `SKILL.md` a router with the principles and the process; put per-harness facts in `references/harness-loading.md` with the date they were verified, and templates in `references/process.md`. When a harness changes its loading rules, update the table and re-run the probe; when a new organizing round finds a new failure mode, add the rule here with its incident.
`SKILL.md` 只放原则与流程；各壳的事实放 `references/harness-loading.md` 并标核实日期；模板放 `references/process.md`。壳的加载规则变了就更新表格并重跑探针；新一轮整理发现新失败模式，就把规则连同事故加进来。
