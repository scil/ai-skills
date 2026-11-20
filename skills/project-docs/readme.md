# project-docs — where this came from

This skill owns the documents that an AI coding agent reads in a project: the instruction file (`AGENTS.md`, `CLAUDE.md`), the loading system across harnesses, and every other durable project fact. It was three skills until 2026-11-20. The three origin stories follow, under their old names, so that the next reader can tell a decision from a leftover.

## The merge, 2026-11-20

`ai-agents-md`, `ai-docs-organizing` and `docs-maintainer` became one skill. The layer model of `docs-maintainer` (layers 0 to 6) already contained the other two: layer 0 is the instruction file, and the loading budget across layers was `ai-docs-organizing`. Each skill opened with a hand-off line to the other two, two skills repeated "one owner per fact", and `docs-maintainer` ran a script that `ai-agents-md` owned. Merging did not save always-loaded bytes, because all three were slash-command only. The gain is one owner for each rule, and no rule that an agent misses because it lives in the skill that was not loaded.

Owner decisions:

- Name: `project-docs`, because the skill covers the whole docs system, not one file.
- No stub directories under the old names. A stub is one more skill in every roster. The junctions in the projects point to the new name.
- Content that most runs need stays in `SKILL.md`: the principles, the loading model, the refresh gate and the path index. A run takes one path, so the steps of each path live in `references/paths/`.
- Registries with different subject areas stay separate: `sources-instruction-file.md` and `sources-docs-system.md`, each with its own changelog. A gap in days only is not a reason for two rules: both use `gate-days: 30`, and the script default is 30. The tier table exists once, in `references/refresh/refresh.md`.

The rule-by-rule checklist of the merge is `plans/merge-docs-skills-checklist.md` in this repository. Old changelog entries keep the old names, because they are history.

## ai-agents-md — where this came from

A procedural skill for the *content* of one agent instruction file. It was built on 2026-09-15 from two conversations the user had (one with ChatGPT, one with Claude), a controlled study, and a probe of the harnesses and exemplar files on that day. This file records what was kept, what was rejected, and why, so the next reader can tell a decision from a leftover.
这是一个关于"一份指令文件的内容"的流程型 skill，2026-09-15 由两段对话（ChatGPT、Claude）、一篇对照研究和当天对 harness 与示例文件的实测建成。本文记录保留了什么、否决了什么、为什么，方便后来者分辨决定与残留。

### The two conversations, absorbed critically / 两段对话的批判性吸收

| Claim | Source | Verdict | What the skill does |
|---|---|---|---|
| Nine sections: project context, architecture, repository map, commands, coding rules, architecture rules, testing, safety, definition of done | ChatGPT | **Rejected in part, with the study's own caveats.** Gloaguen et al. found an Overview section in 95–100% of generated files; removing it (Table 7 ablation) changed nothing, and files did not shorten the steps to the first relevant file. Caveats the authors state: Python only, so tooling may already be in the models' parametric knowledge; open-source repos with READMEs; bug-fix and small-feature tasks. When they deleted the repos' documentation, context files *did* help (+2.7%). So an overview is out when the README, manifest and tree already answer it, which is the normal case; in an undocumented or closed-source repo, the one paragraph the README would have carried is admissible under criterion (a). | Section menu keeps Boundaries, Commands (non-obvious pick only), Verification, Architecture rules, Conventions that differ, Traps, Pointers, DoD. A Pointers line to `ARCHITECTURE.md` replaces the overview, as OpenAI's harness post does. |
| Admission threshold: non-inferable, costly, repeated, team agreement, architecture boundary, verification requirement | ChatGPT | **Kept.** Matches the study's "only specific additional instructions beyond the codebase". | `rules.md` §1, the test every line must pass. |
| MUST / SHOULD / MAY wording | ChatGPT | **Kept**, with positive phrasing added (a "Do not" list keeps the forbidden behaviour in view). | `rules.md` §2 |
| Event-driven updates; failure → lesson → rule; three PR questions add/change/delete | ChatGPT | **Kept.** Same as Claude Code's official add-triggers. | Principle 4, Update path |
| Definition of done = run lint, typecheck, test before finishing | ChatGPT | **Reworded.** The study measured that unconditional testing instructions raise cost significantly because agents obey them. | Verification is scoped per kind of change; the rest is CI's. |
| "OpenAI keeps AGENTS.md around 100 lines, as a table of contents to `docs/`" | ChatGPT | **Kept, verified — and first misjudged here.** The source is OpenAI's "Harness engineering" post (Lopopolo, 2026-02-11): a ~1M-line, fully agent-generated internal product with "a short AGENTS.md (roughly 100 lines)… primarily a map", after "one big AGENTS.md" failed for four named reasons. The first draft of this readme called the claim contradicted because `openai/codex/AGENTS.md` is ~550 lines; that is a different repository, and both facts stand. | Principle 1 cites the four failure modes; the Pointers section is the "map" role. `openai/codex` stays registered as what a large team's file grows into. |
| AGENTS.md is the canonical file; CLAUDE.md = `@AGENTS.md` + Claude-only lines; symlink fragile on Windows | Claude | **Kept, verified** against Claude Code docs; `supabase/supabase` runs it live (11-byte bridge). | Principle 2, `templates/CLAUDE.md` |
| `.claude/rules/*.md` with `paths:` loads only on matching files; imports load at launch and save nothing | Claude | **Kept, verified.** | `harness/claude-code.md`; rule placement in `rules.md` §2 |
| Under 200 lines per CLAUDE.md is official | Claude | **Kept, verified.** | `rules.md` §5 |
| Block HTML comments stripped before injection | Claude | **Kept, verified** — for Claude Code only; Codex docs say nothing, so comments are assumed sent. | Template comments are short. |
| `/init`, `CLAUDE_CODE_NEW_INIT=1`, `/import` (v2.1.213+), `/doctor` trims (v2.1.206+), `/context` | Claude | **Kept, verified.** | `harness/claude-code.md`; the Create path still runs the admission pass over anything `/init` produces. |
| Rules are context, not enforcement; use a `PreToolUse` hook to block | Claude | **Kept, verified.** Was also ai-docs-organizing's principle 7 until 2026-10-19, when it moved here. | Principle 3: every rule names its layer or is `advisory`. |
| Avoid "always double-check": over-verification on Opus 5 / Fable 5 | Claude | **Kept, verified — after a first "not found".** The Claude Code memory docs do not say it; the platform prompting docs do. *Prompting Claude Opus 5*: explicit verification instructions "cause over-verification… removing them reduces wasted tokens with no loss in quality"; "avoid instructing re-checks it already performs ('double-check your answer')". *Prompting best practices*: Opus 4.5/4.6 "may now overtrigger… dial back any aggressive language" such as "CRITICAL: You MUST". *Prompting Claude Fable 5*: "skills developed for prior models are often too prescriptive… consider removing older instructions". | `rules.md` §2 "No emphasis words" and §3 Verification scoping; `harness/claude-code.md` model notes, with the three URLs. |
| "A study of 2,500 repos found 150 lines is the knee, cost +20–23%" | Claude | **Conflated, three ways.** The 2,500-file analysis (GitHub blog, 2025-11) is about Copilot custom-agent files and gives no line count; "under 150 lines, under 50 per section" is a rule of thumb from a vendor guide (morphllm) with no study behind it; +20–23% is the ETH paper's cost figure for *generated* files. The same guide also calls the efficiency paper (Lulla et al.) "Princeton researchers"; its author list names no Princeton affiliation, so that label is not repeated here. | Each source registered separately with what it actually says; no line knee is claimed anywhere in this skill. |
| "AGENTS.md makes agents faster and cheaper" (28.6% runtime, 16.6% tokens) | circulating, via morphllm | **Kept as a second, narrower study — and reconciled.** Lulla et al. (arXiv 2601.20404, 2026-01/03): gpt-5.2-codex only, 10 repos, 124 small PRs (≤ 100 LoC, ≤ 5 files), *developer-written* files taken from the repo at the PR's commit, no correctness evaluation (a 50-task sanity check). Median wall-clock −28.6%, median output tokens −16.6%, mean input tokens −9.7%. Gloaguen et al. measured *success* and *total cost* across three agents with generated and developer files. They agree where they overlap: developer-written beats generated, and files help when they carry what the repo does not already say (Gloaguen: with repo docs removed, even generated files gain +2.7%). They differ on cost because Lulla counts a single agent on tiny tasks where exploration dominates and the file shortcuts it; Gloaguen counts input tokens too and finds instructions trigger more testing and reading. | Principle 1 states both: a file of non-inferable rules saves exploration; a file of overviews and unconditional test instructions costs more. |
| `anthropics/claude-code` as the canonical CLAUDE.md shape, "short, opinionated, structured around build/test/lint/commit" | Claude (via ayautomate's "12 best CLAUDE.md examples") | **Wrong.** The full git tree of that repo (1,592 entries, default branch `main`, 2026-09-15) contains no file named `CLAUDE.md` or `AGENTS.md` at any depth; the repo holds issues, plugins and docs, not the CLI's source. The blog's description is invented. | `anthropics/claude-code-action/CLAUDE.md` (3.5 KB, real) registered instead; the blog's other picks that do exist (`sst/opencode`, `supabase/supabase`, `vercel/next.js`) were checked individually. |
| Persona ("you are a test engineer…") makes files work | GitHub blog, cited by both | **Not transferred.** Measured on Copilot custom agents, where the file *is* the agent definition; a repository instruction file is read by an agent whose role the harness already set. | Persona lines are on the "never enters" list. |
| Root file 20–30 lines / "shorter is better" | Claude (via blogs) | **Partly.** The study supports "less", not a number. The field study of the 100 biggest repos is bimodal (37% over 1,500 words, 10% under 150). | Template target < 4 KB / < 80 lines, stated as a guideline; bytes are the unit Codex cuts by. |

### Authority tiers, and why one study was not enough / 权威分层，以及为什么一篇研究不够

The user's second review made two demands: the harness vendors' own documentation is the first authority, and a single ETH study is too thin a base for principle 1. Both held up. `sources.md` now carries a tier in every `kind`; the refresh rule admits a Tier 1 statement alone, a Tier 2 finding only when two studies agree or one explains a vendor rule, and never a rule from an exemplar or a blog.
用户第二轮提出两点：厂商官方文档是第一权威；原则 1 只压在一篇 ETH 论文上太薄。两点都成立。`sources.md` 的 `kind` 现在带层级；刷新规则是：一层可单独入规则，二层要两篇研究一致或能解释一层的规则，三四层不能成为规则来源。

What the vendors say, and where they differ / 厂商怎么说、哪里不同：

- **Anthropic** (Claude Code best practices, memory docs): an Include/Exclude table; "would removing this cause Claude to make mistakes? If not, cut it"; `/doctor` trims directory layouts, dependency lists and architecture overviews; hooks are deterministic, the file is advisory; one emphasized line is allowed, many are not. / Anthropic：有明确的收录/排除表；`/doctor` 会删目录布局、依赖清单、架构概览；hook 是确定性的，文件是建议性的；允许强调一行，不允许强调多行。
- **OpenAI** (Codex best practices): a good file covers "repo layout and important directories", how to run, build/test/lint, conventions and PR expectations, do-not rules, what done means; "short, accurate… add new rules only after you notice repeated mistakes"; split into referenced task files when it grows. / OpenAI：好文件覆盖"仓库布局与重要目录"、运行方式、命令、约定、禁令、完成标准；"短而准确……只在发现重复错误后加规则"；变大就拆成被引用的任务文件。
- **The one divergence** is the repository map: OpenAI lists it, Anthropic trims it. The skill admits it as a Pointers line when the tree does not make it obvious, and rejects a listing `ls` reproduces. / 唯一分歧是仓库地图：OpenAI 列入，Anthropic 删除。skill 的处理：树结构不明显时作为 Pointers 一行收录，`ls` 能复现的清单不收。

What seven studies say / 七篇研究怎么说：

| Study | Scope | Finding | Weight here |
|---|---|---|---|
| Gloaguen et al. 2026-02 (ETH) | 3 agents, Python, generated + developer files, success + cost | generated: no gain, +20–23% cost; developer: +2.4% n.s.; overview ablation: nothing; docs removed: +2.7% | the cost mechanism; generated < developer |
| Lulla et al. 2026-01 | gpt-5.2-codex, 124 small PRs, developer files, efficiency only | −28.6% runtime, −16.6% output tokens | developer files cut exploration |
| Shepard & Albrecht 2026-06 | refined guidance via probes | 25.5% → 33.0% resolution, all from reaching the right file; patch quality flat | a map can help; quality rules do not |
| Arabat & Sayagh, MSR 2026 | 15,549 agentic PRs, 148 projects, before/after | 27.7% of projects up ≥ 20% merge rate, 26.35% down; improvers had longer, more structured files | against "shorter is always better" |
| Chatlatanagulchai et al. 2025-11 | 2,303 files, 1,925 repos | tests 75.9%, implementation 70.8%, architecture 68.1%; security 14.8%; files evolve like config code | what people write; treat as code |
| Galster et al., AIware 2026 | 2,853 repos | context files dominate; often the only mechanism; AGENTS.md as standard | why the file matters |
| Voria et al. 2026-06 | mining study of file maintenance | taxonomy of changes; links to code quality | treat as code |

Where they agree: developer-written beats generated; the file is followed, so what it asks for is what it costs; it should be maintained like code. Where they disagree: whether a map helps (Gloaguen no, Shepard yes) and whether shorter is better (Arabat: the improvers were longer). Principle 1 was rewritten to lead with the vendors and to state the disagreement instead of picking a side.
一致处：手写优于生成；文件会被执行，写了什么就付什么成本；要像代码一样维护。分歧处：地图是否有用、是否越短越好。原则 1 已改为以厂商为先，并陈述分歧而不是选边。

### What the harness probe added / 实测补充

- `vercel/next.js/AGENTS.md` is 30 KB — 2 KB under the Codex cap before any global or nested file. A popular exemplar can itself be over budget; watching exemplars is partly watching for that.
- `microsoft/vscode/AGENTS.md` is 271 bytes: a pointer to `.github/copilot-instructions.md`. The pointer-only pattern is legitimate when another file is already the canonical one.
- `ghostty-org/ghostty/AGENTS.md` (1.4 KB) passes the admission threshold line by line: build/test commands with a filter, one C-enum sentinel invariant, one hard boundary (agents never open issues or PRs). It is the closest thing to a model answer found.

### The refresh gate, and why it is 7 days and a script / 为什么是 7 天和脚本

The user's original point 3 asked for a source and research check on every invocation. Every invocation would mean 20 fetches and two searches before any review could start, on the user's clock and tokens, and general search returns SEO copies of the same posts. The compromise: a `last-refresh` date in `sources.md` (in the repo, because Codex has no memory and both harnesses must see the same date), a 7-day gate the user chose, a script that fingerprints every source so the model reads only what moved, an allowlisted search, and a changelog entry that *proposes* edits. The skill never rewrites its own rules from a fetch.
用户原第 3 点要求每次调用都检查。那意味着每次审核前先抓 20 个 URL、搜两次，且泛搜索多为同几篇文章的 SEO 副本。折中：`sources.md` 里的 `last-refresh` 日期（放仓库，因为 Codex 没有记忆、两个 harness 要看同一日期）、用户选定的 7 天门控、指纹脚本让模型只读变化的来源、白名单搜索、以"提议"形式写入 changelog。skill 不会从一次抓取直接改写自己的规则。

### Boundary with the neighbours / 与相邻 skill 的边界

- **ai-docs-organizing** owns the system: which files load, chain budgets, the diet of an oversized contract, layers, memory triage. This skill links to its harness table and never restates the numbers.
- **docs-maintainer** owns where every other project fact lives (the ownership map). This skill's Pointers section is one line per owner, never the owner's content.
- **writing-for-agents** (mattpocock) is general prose guidance for agent-read documents; this skill is specific to the instruction file and its admission threshold.

### How to maintain / 怎么维护

`SKILL.md` stays a router: principles that change behaviour, the gate, four paths ending on a done-criterion. Facts about a harness go in `references/harness/<name>.md` with the date verified; the admission threshold and wording rules in `rules.md`; sources only through `sources.md` with a `purpose` that says what is *not* taken from them. A new failure mode found while creating or reviewing a file becomes a checklist item with its incident, here in this readme.
`SKILL.md` 只做路由。harness 事实进 `references/harness/`，注明核实日期；准入与措辞规则在 `rules.md`；来源只经 `sources.md` 登记，并写明不从它取什么。新发现的失败模式变成清单项，事故记在本文。

## ai-docs-organizing — where this came from

A procedural skill, not one lesson deep: it holds the norms and the process for organizing the documents agents read, and the incident that produced them. Add to it when an organizing round teaches something the process did not already say; project-specific facts stay in the project.
这是一个流程型 skill，不是"一课深"：它装的是整理 AI 文档的规范与流程，以及产生它们的那次事故。只有当一轮整理教会了流程里没有的东西时才往里加；项目专属事实留在项目里。

### The incident (2026-09-12/13, ThanksPorch) / 事故

**The ask.** Plan how to organize the project's AI documents — `AGENTS.md`, skills, hooks, memory — for two agents (Claude Code on Opus 5, Codex on GPT), considering that different models have different requirements, strengths and weaknesses. Then have Codex review the plan, then execute it.
**任务。** 为两个代理（Claude Code / Opus 5，Codex / GPT）规划 AI 文档的整理，考虑不同模型的差异；再让 Codex 评审计划，然后执行。

**What the review found that the plan had missed.** The plan measured `AGENTS.md` at 9,877 words and proposed a diet in words. Codex's first-round blocker: the file was 66,794 bytes and Codex reads its `AGENTS.md` chain only up to `project_doc_max_bytes` — 32 KiB by default, no override set, no notice. A probe with file reads forbidden confirmed it: Codex's copy ended mid-sentence in line 305, and *Working Discipline, AI Failure Guards, Testing Discipline, Domain Guardrails, Project Skills* had never arrived. Claude Code, meanwhile, auto-loads `CLAUDE.md`, which the repo did not have — so it received none of the contract automatically. Both agents had worked for months on a contract neither fully held.
**评审抓到、计划漏掉的。** 计划按"词数"称重并按词数减肥；Codex 第一轮的 blocker：文件 66,794 字节，而 Codex 只读到 `project_doc_max_bytes`（默认 32 KiB），静默截断。禁止读文件的实测证实：Codex 的副本在第 305 行句中结束，五个关键章节从未到达。Claude Code 则只自动加载 `CLAUDE.md`，仓库没有——所以它一点都没自动拿到。两个代理数月来都在一份谁都没拿全的契约上工作。

**Other findings that changed the plan.** "AGENTS.md is Codex's only brake" was narrowed: the brake is the sandbox/approval config; prose is the behavioural layer. Proposed destinations broke the project's own ownership rules (no parallel docs tree, no directory READMEs). Deleting a vendored skill's compiled duplicate would have broken its documented interface. A `prepare` step that recreates junctions would mutate the checkout. The tap-to-edit prose in the contract contradicted the shipped behaviour and its E2E tests on two points; a spec written from the prose would have enshrined the stale version. One finding was rejected with evidence (it had checked `<worktree>/node_modules`; the tree was at `<worktree>/src/node_modules`).
**其它改变计划的发现。** "唯一刹车"改成"唯一行为层"；原定的搬迁目的地违反项目自己的归属规则；删第三方 skill 的编译副本会破坏其接口；`prepare` 自动建 junction 会改动检出；契约里的 tap-to-edit 描述与已上线行为和 E2E 测试有两处矛盾——按文字写 spec 会把过期版本写进规格。一条发现被有据驳回（它查错了路径）。

**What was done.** Contract 66,794 → 28,078 bytes under a 28 KiB chain budget (4 KiB reserved for the user-level global file), guarded by a unit test that went red on the old file first; a one-line `CLAUDE.md` bridge; every rule kept as invariant + `Instance:` + enforcing test, with a rule-by-rule checklist; two homeless rules became specs written from the tests; a `nextjs` skill for a deleted app removed; `OVERLAY.md` declared the one project-owned file inside a vendored skill; a `SessionStart` baseline for the docs-nudge hook; memory triaged 75 → 30 files; one user-level preference file for both harnesses. Probe afterwards: last heading `## Reference Sources`, all sections present, global file received, no cut. Codex, having read the new global file, answered the probe bilingually — the preference had reached it.
**做了什么。** 契约减到 28 KiB 预算内并有先变红的守卫；一行桥接文件；规则逐条保留并有映射表；两块无主规则按测试写成 spec；删了服务对象已不存在的 skill；定了覆盖文件模型；钩子加会话基线；记忆 75→30；用户级偏好一份两用。事后实测：完整到达、无截断；Codex 读到新的全局偏好后用双语作答——偏好真的到了它那里。

### Why it happened, and the rule each part became / 原因与规则

1. Nobody had asked what each harness actually loads. → *The loading model comes first; probe, don't assume.*
2. Size was measured in words. → *Budget in bytes, for the whole chain, guarded in the gate.*
3. Project facts had accumulated in one agent's memory. → *The repo is the only shared memory; memory is for behaviour.*
4. The contract carried recipes, inventories and history beside its rules. → *Information hierarchy; the environment is truth.*
5. The plan's own numbers were partly wrong. → *Verify claims, tag provenance, review with the other agent before editing.*
6. Prose had drifted from tests. → *Specs from shipped behaviour, never from the prose.*
7. The contract carried a "Project Skills" section — one line to a paragraph per skill, ~3 KB — because its first version (2026-05-28) had ruled "routing stays here; skill files must not route to other skills", and the docs skill had turned that into an ownership row. Traced to the source and deleted the same day: descriptions carry triggers, the ignore manifest carries membership, the contract names no skill. The harness re-read the changed descriptions within the session. A first attempt moved the skills' *order* ("domain model → data layer → implementation") into three descriptions; the user cut it — that order was already a rule about the work in the contract, and restating it per skill only lengthened three always-loaded lines. → *The contract lists no skills; fix the meta-rule, not the list; a description is a trigger, not a workflow.*
   契约里有一节"Project Skills"，每个 skill 一行到一段，约 3 KB——因为第一版契约（2026-05-28）规定"路由只在这里，skill 不得互相引用"，文档 skill 又把它写成了归属规则。当天追到源头并删除：description 承担触发，忽略清单承担成员关系，契约不点任何 skill 的名。壳在会话内就重新读到了改后的 description。第一版尝试把 skill 的*顺序*写进三条 description，用户砍掉了——那个顺序本就是契约里关于工作的规则，逐个 skill 重述只是让三行常驻文字变长。→ *契约不列 skill；改元规则，不改清单；description 是触发条件，不是工作流。*

8. The generic docs skill (`docs-maintainer`) had grown to 3,529 words, with the structure tree, diagramming rules and cross-cutting checklist inline, and a project (`local-docs-maintainer`) had forked it and drifted. Same day: the fork's generic value was merged up (an Adopting path, an Auditing path, an ownership-map template), the project's owners by name moved into a project doc (`docs/ai/ownership-map.md`), the fork was deleted and the shared skill linked in — the harness listed it the moment the junction existed. Then the shared skill was slimmed to a 990-word router (body 905) with three verbatim references, every pointer checked, the old→new map in the commit message, the Chinese mirror marked as lagging. The user's pending edits to the same file were committed first, as their own commit. The router landed at 905 words against a 650 estimate because every remaining sentence was a rule, a step or a done-criterion. → *Fold a drifted fork back; slim by moving verbatim behind pointers; a word count is a guideline, the no-op test is the rule.*
   通用文档 skill 长到 3,529 词，结构树、作图规则、交叉变更清单全都内联，项目里还 fork 了一份并已漂移。同一天：把 fork 的通用价值并回上游（接管路径、审计路径、归属表模板），项目专属的归属名单挪进项目文档，删掉 fork、把共享 skill 通过 junction 接入——junction 一建立，壳就列出了它。然后把共享 skill 瘦身成 990 词的路由器，三个 references 原文搬移，逐个检查指针，新旧映射写进提交信息，中文镜像标注落后。同一文件里用户未提交的改动先单独提交。路由器落在 905 词而不是预估的 650，因为剩下每一句都是规则、步骤或完成条件。→ *fork 漂移就并回；瘦身靠原文下沉到指针后面；词数是参考，空指令测试才是规则。*

9. The domain plan (`docs/2. plan/plan.md`) was 71 KB and four skills named it as *the* place for any domain question — so every domain task paid ≈18k tokens to read it whole, while the skill had filed it under "pointer-reached, costs only its pointer". Two sections (Resource Model, Access Resolver) were 44% of it, mostly describing behaviour that 49 accepted specs already owned; 3 KB was changelog comments; the terminology table was 60% padding. Same day: changelog to `archive/`, tables trimmed, each shipped block collapsed to concept + reasoning + spec name (target-state models kept whole), a question-first map added at the top, the routing skill told to read map → section → spec; 71 → 53 KB, not split. A first instinct to split by section was rejected: sixteen files lose the narrative and break every `§n` pointer, and a split only saves tokens when the pointer names the right file. → *A pointer is cheap until every task of a kind is routed through it; diet a hot doc by handing shipped behaviour to its owner and giving the reader a map; split last, by purpose.*
   领域计划 71 KB，四个 skill 都把它指定为领域问题的唯一入口——每个领域任务整读一次约 18k token，而本 skill 之前把它归为"指针可达，只付指针的钱"。两节占 44%，多是 49 个已接受 spec 已经拥有的行为；3 KB 是改动日志注释；术语表六成是填充空格。当天：日志移到 `archive/`，表格去填充，已发布的块压缩为概念 + 决策理由 + spec 名（目标态模型原样保留），顶部加"按问题找"的地图，路由到它的 skill 加一句"先地图、再一节、再 spec"；71 → 53 KB，未拆分。最初想按节拆分被否决：十六个文件丢掉叙事、打断所有 `§n` 指针，且只有指针能点名正确文件时拆分才省 token。→ *指针只在没被当成必经之路时才便宜；热文档的瘦身是把已发布行为交还所有者、给读者一张地图；最后才按用途拆分。*

### The trace, in the format the skill asks for / 追溯记录

| Symptom | Source (commit · rule) | Copies touched | Guard |
|---|---|---|---|
| `## Project Skills`, ~3 KB, one line to a paragraph per skill, regrowing with every skill added | `7d40898` (2026-05-28, the contract's first commit) · "Keep project skill routing in this section; skill files describe only their own scope and do not route to other skills" | the contract's meta-rule (deleted); `local-docs-maintainer` Ownership Map row "skill routing → AGENTS.md" (replaced by rows for description / ignore manifest / overlay); memory "a skill is not registered until listed" (deleted); the hard-coded name list in the link script (now reads `.gitignore`) | the byte-budget test; the harness re-reading descriptions is the mechanism itself |
| `apps/nextjs` "exists, scheduled for removal" + a skill kept for it | the commit that removed the app propagated nothing | two sentences and the skill + lock entry (deleted) | inventory step: `ls` what a sentence describes |
| a smoke recipe opening `/signup` | predates the one-command dev environment; the route was renamed later | the recipe (deleted) | none needed — the environment is the truth |
| a diet planned in words | the plan measured the wrong unit | re-measured in bytes | the byte-budget test |
| a 71 KB plan read whole by every domain task | this skill's own principle 1 ("pointer-reached costs only its pointer") · four skills routing to it without a reading rule | principle 1 amended; SKILL.md "Hot pointer docs" + process §10; the routing skill's sentence; the plan's own map and archive | the map at the top of the doc; per-section byte count in the inventory (layer D "how many route to it") |

症状 → 源头（提交·规则）→ 触及的副本 → 守卫：这是 skill 要求的追溯格式；上表是本次的实例。

### How to maintain / 怎么维护

Keep `SKILL.md` a router with the principles and the process; put per-harness facts in `references/harness-loading.md` with the date they were verified, and templates in `references/process.md`. When a harness changes its loading rules, update the table and re-run the probe; when a new organizing round finds a new failure mode, add the rule here with its incident.
`SKILL.md` 只放原则与流程；各壳的事实放 `references/harness-loading.md` 并标核实日期；模板放 `references/process.md`。壳的加载规则变了就更新表格并重跑探针；新一轮整理发现新失败模式，就把规则连同事故加进来。

Since 2026-09-15 the *content* of one instruction file — which rules earn a line, wording, enforcement layer, templates, and the vendor and research sources behind them — is owned by the sibling skill `ai-agents-md`, which links to `references/harness-loading.md` here rather than restating it. This skill keeps the system: which files load, chain budgets, layers, the diet, memory triage.
自 2026-09-15 起，单份指令文件的*内容*（哪行有资格、措辞、执行层、模板、背后的厂商与研究来源）归相邻 skill `ai-agents-md`，它引用这里的 `harness-loading.md` 而不重述。本 skill 保留系统层：加载哪些文件、链预算、分层、瘦身、记忆分类。

Since 2026-09-16 the *content* of one skill's `SKILL.md` — the description as trigger, the router body and its references, the slim (formerly process.md §9), folding a fork back — is owned by the sibling skill `ai-skill-audit`, on the same line. The roster stays here: which directories load, provenance classes, the roster budget (§11), "the contract lists no skills". Items 7 and 8 above remain as the incidents that produced both halves.
自 2026-09-16 起，单个 skill 的 `SKILL.md` *内容*——作为触发条件的 description、路由器正文与 references、瘦身（原 process.md §9）、fork 并回——按同一条切线归相邻 skill `ai-skill-audit`。花名册留在这里：加载哪些目录、来源类别、花名册预算（§11）、"契约不列 skill"。上文第 7、8 条作为产生这两半的事故保留。

### Slimmed to a router, 2026-10-19 / 瘦身为路由器

`SKILL.md` had grown to 2,137 words (13 KB), twice the 500–900 word router size this skill sets for project skills, and about 45% of it restated its own `references/process.md` or the sibling `ai-agents-md`. It now holds the principles, the process and one line per topic with a `§n` pointer: 1,046 words, 6.7 KB. No rule was dropped; each moved line has the home below.
`SKILL.md` 长到 2,137 词（13 KB），是本 skill 给项目 skill 定的 500–900 词路由器尺寸的两倍，约 45% 在重述自己的 `process.md` 或相邻的 `ai-agents-md`。现在只留原则、流程、每个主题一行加 `§n` 指针：1,046 词、6.7 KB。没有丢规则，搬走的每行去向见下表。

| Old place in `SKILL.md` | New home |
|---|---|
| Principle 5 "Guards are model-relative… phrase positively" | `ai-agents-md` principle 4 (model-relative guards, write for the agent that failed, prune); positive phrasing was already `ai-agents-md/references/rules.md` |
| Principle 7 "Instructions are a behavioural layer, not the brake" | `ai-agents-md` principle 3, plus the clause "fix the config, not the prose"; the hand-off line here names it |
| Principles 1–4, 6 | principles 1–5, compressed; "a Read tool reads the file, not the section" → "every read is whole-file" in Hot pointer docs |
| Process step 1, the six layer names | `process.md` §1 table (already there) |
| Process step 3 "Disputes" (one long sentence) | the same rule, one short sentence |
| Process step 4, the `codex exec` flags | `process.md` §8 (already there) |
| Source and symptom, five numbered steps | one paragraph with the five verbs; "meeting it again in a month", the guard examples → `process.md` §7 lead; the producer commands were already §7's table |
| "Do not replace it with 'skills are not listed here': a self-referential sentence is another always-loaded line" | the rule stays in Skills; the reason → `process.md` §7, meta-rule bullet |
| "A description carries its trigger and nothing else" | the hand-off line to `ai-skill-audit` |
| Four provenance classes and their policies | `process.md` §1, "Skill provenance classes" |
| The roster budget's cost order | `process.md` §11 (already there) |
| Memory triage bin definitions | `process.md` §6, "Bins" line |
| User-level file "≤ 4 KiB when the cap is 32 KiB" | `references/harness-loading.md` Budgeting (already there) |
| Hot pointer docs, six numbered steps | one sentence in `SKILL.md`; "padded table is half whitespace", "two heaviest sections", "a reader told to read the plan reads the plan", "sixteen one-section files lose the narrative", "prune the pointers that named it" → `process.md` §10 |
| Hot pointer docs Instance (71 → 53 KB) | item 9 above (already there) |

Principles were renumbered 1–5. The two citations by number outside this skill — `ai-agents-md/readme.md` (principle 7) and `ai-agents-md/references/harness/claude-code.md` (principle 5) — were repointed to `ai-agents-md`'s own principles 3 and 4.
原则重新编号为 1–5。本 skill 以外按编号引用的两处——`ai-agents-md/readme.md`（原则 7）和 `ai-agents-md/references/harness/claude-code.md`（原则 5）——已改指 `ai-agents-md` 自己的原则 3 和 4。

## docs-maintainer — how it got its current shape

A procedural skill for the documentation system of a repository whose first reader is an agent. Created 2026-05; slimmed to a router with three references 2026-09-13; restructured by loading layer and given tiered sources and a refresh gate on 2026-09-15. This file records the 2026-09-15 decisions and what they rest on.
面向"第一读者是代理"的仓库文档系统的流程型 skill。2026-05 创建；2026-09-13 瘦身为路由器；2026-09-15 按加载层重构，并加入分层来源与刷新门控。本文记录 2026-09-15 的决定及其依据。

### Why restructure by loading layer / 为什么按加载层重构

The old Annotated Structure was a `docs/` tree by topic (product, architecture, engineering, api, operations, ai). It assumed the reader would browse. The evidence gathered for `ai-agents-md` says agents do not browse: in 557 real sessions, 60.5% of documentation interactions were with instruction files and working notes, 10.6% with classical technical docs, 1.3% with API references (Gao & Chen, 2026-08). Agents also go looking proactively (70.2%) rather than after a failure (7.5%), so what they find is what the always-loaded map points at. Both vendors say the same thing from the other side: Anthropic moves "a section of CLAUDE.md that has grown into a procedure rather than a fact" into a skill and trims layouts and overviews from the file; OpenAI keeps the main file concise and references task-specific markdown files. So the organizing question changed from "what topic is this" to "how does this fact reach the agent, and what does each read cost" — the seven layers.
旧结构是按主题分的 `docs/` 树，假设读者会浏览。为 `ai-agents-md` 收集的证据表明代理不浏览：557 个真实会话里，60.5% 的文档交互发生在指令文件和工作笔记上，经典技术文档 10.6%，API 参考 1.3%；而且代理是主动去找（70.2%）而不是失败后才找（7.5%），所以常驻地图指向什么，它们就找到什么。两家厂商从另一面说了同一件事。于是组织问题从"这是什么主题"变成"这个事实怎么到达代理、每次读花多少"，即七层。

### The bold changes, each with its source / 大改动及其依据

| Change | Source |
|---|---|
| **Plans become layer 1, first-class**, in the ExecPlan shape (purpose · progress · surprises · decision log · retrospective), `active/` → `completed/`, plus a tech-debt tracker | Codex cookbook on ExecPlans; OpenAI Harness engineering (`exec-plans/active`, `completed`, `tech-debt-tracker`); Gao & Chen's "working notes" share |
| **Hand-written API docs are gone by default.** Code is the contract; a machine-readable spec is generated when an external consumer needs it; consumed-API facts live in adapters, fixtures and vendored references | Anthropic: "detailed API documentation — link to docs instead"; Gao & Chen: API references are 1.3% of reads; the project's own facts-of-record principle |
| **Procedures leave `docs/` for skills**: setup, release, migrations, runbooks, audit prompts | Anthropic skills docs; OpenAI Codex skills docs (`.agents/skills`, `scripts/`, `references/`); Galster et al.: skills rarely used unless made explicit |
| **A `generated/` layer** with a regenerate-and-diff rule: schema, API index, dependency graph, C4 L3 | C4 on component and code diagrams; OpenAI `generated/db-schema.md` |
| **A `references/` layer** for vendored third-party docs as `llms.txt` | llmstxt.org; OpenAI `references/*-llms.txt` |
| **Security, reliability, performance get explicit owners** | Chatlatanagulchai et al.: 14.8% and 14.5% coverage in 2,303 files; OpenAI `SECURITY.md`, `RELIABILITY.md` |
| **Repo-map and code-locator stay, as layer-2 docs** | Shepard & Albrecht: the measured gain from guidance is reaching the right file; Gloaguen et al.: but not from the always-loaded file |
| **Governance layer**: ownership map with Layer / Enforced by / Reading rule columns, a quality doc, a gardening cadence | OpenAI: linters and CI validate the knowledge base; a doc-gardening agent; `ai-agents-md`'s "a rule is a wish until it has an enforcement layer" |
| **`templates/docs-ai.md` removed** | one owner per fact: the instruction file's content is `ai-agents-md`'s |
| **Skills keep project bindings in one place** | Gao et al.: 53% of reused skills are never modified; when they are, it is the bindings |

### Old node names / 旧节点名

For a project laid out by the pre-2026-09-15 topic tree. The reasons are the table above. Moved here from `references/structure.md` on 2026-10-19.
给按 2026-09-15 之前主题树布局的项目用；原因见上表。2026-10-19 从 `references/structure.md` 移来。

| Before | After |
|---|---|
| `ai` node, `templates/docs-ai.md` | layer 0, content owned by `ai-agents-md` |
| `product/feature-roadmap`, scattered "future work" | `plans/`, layer 1, ExecPlan shape |
| `api/provided`, `api/consumed`, hand-maintained `openapi.yaml` / `asyncapi.yaml` | `generated/api`, machine-readable only when a consumer needs it; consumed-API facts in adapters, fixtures and `references/` |
| `c4-components`, hand-drawn | `generated/components`, or skipped |
| `engineering/setup`, `release`, `migrations`, `operations/runbook-*`, `ai/prompts` | layer 5 skills; the facts they need stay in layers 2–4 |
| `architecture/security` alone | `quality-attributes/{security, reliability, performance}` |
| `ownership` node | layer 6 `ownership-map` + `quality` + optional `evals` |
| `architecture/dynamic-login-flow` | `architecture/flows/<name>` |

### What was kept / 保留了什么

Code-wins; one owner per fact; the File-First Split Rule; the Adopting path (route, do not scaffold) and its "skipped — reason" convention; the locator entry discipline; C4 L1/L2 by hand with PlantUML; the cross-cutting checklist.
保留：代码优先、一个事实一个主人、先文件后拆分、"接管而非搭建"及其"跳过—原因"约定、定位器条目纪律、手绘 C4 一二层、交叉变更清单。

**Removed the same day: `rules/tauri-command-api.md`.** A shared, project-agnostic skill carried a rule for one framework; by this skill's own routing principle its owner is the Tauri project. What it said, for that project to re-home as one ownership-map row: Tauri commands are a provided API whose facts of record are the handlers, the frontend wrapper and the shared types; a generated command index (layer 3) owns the surface; hand-written text covers only admin, permission, preview and destructive-guard behaviour, in the security quality-attribute doc.
**当天删除 `rules/tauri-command-api.md`。** 共享 skill 不该带单一框架的规则；按本 skill 自己的路由原则，它的主人是那个 Tauri 项目。该项目可把它收为归属表一行：命令处理器、前端封装与共享类型是事实来源；生成的命令索引拥有接口面；手写只保留权限、预览与破坏性操作的守护说明，放在安全文档。

### Sources, tiers and the 30-day gate / 来源分层与 30 天门控

Same tiering as `ai-agents-md`: vendor and standard sites decide; research corroborates in pairs; exemplars illustrate; reports point. The checker script is shared (`ai-agents-md/scripts/check-sources.ps1 -Path … -GateDays 30`). Thirty days rather than seven because C4, MADR, OpenAPI and llms.txt move slowly; the vendor pages on skills and plans are read first when the script reports a change.
分层与 `ai-agents-md` 相同。检查脚本共用。门控 30 天而非 7 天：C4、MADR、OpenAPI、llms.txt 变化慢；脚本报告变化时先读厂商关于 skills 和 plans 的页面。

### Boundaries / 边界

`ai-agents-md` owns layer 0's content. `ai-docs-organizing` owns the loading model, byte budgets and the diet of an oversized contract or hot doc. This skill owns layers 1–6: where every other fact lives, in what shape, with what check.
`ai-agents-md` 管第 0 层内容；`ai-docs-organizing` 管加载模型、字节预算与瘦身；本 skill 管 1 到 6 层。

### How to maintain / 怎么维护

`SKILL.md` stays a router. Layer rules and the mapping table live in `references/structure.md`; the template in `templates/ownership-map.md`; every rule's source in `references/sources.md` with a `purpose` that says what is taken and what is not. A restructure found necessary by a refresh is proposed in `changelog.md` first. There is no Chinese mirror (removed 2026-10-19, below).
`SKILL.md` 只做路由；层规则与映射表在 `structure.md`；模板在 `templates/`；每条规则的来源在 `sources.md`。刷新发现需要重构时先在 `changelog.md` 提议。不再有中文镜像（2026-10-19 删除，见下文）。

### Cleanup, 2026-10-19 / 清理

`SKILL.md` 1,070 → 1,001 words; description 640 → 395 characters; `for-human/` (38 KB) deleted. No rule was dropped.
`SKILL.md` 1,070 → 1,001 词；description 640 → 395 字符；删除 `for-human/`（38 KB）。没有丢规则。

| Old | New home |
|---|---|
| `for-human/SKILL.zh.md` — Chinese mirror, lagging since 2026-09-13 and describing the old topic tree | deleted at the user's request; git history before this commit holds it |
| `for-human/SKILL.zh 20260505.md` — dated copy | deleted; git holds the history |
| `for-human/ref.md` — 2026-05 survey of neighbour skills on skills.sh, plus guidance to keep prompts under `docs/ai/prompts/` | deleted; the prompts guidance contradicted layer 5 (prompts are skills); Diátaxis is in `references/sources.md`; the survey is in git history |
| `SKILL.md` hot-doc sentence (~20 KB threshold) | `structure.md` → Hot documents; `SKILL.md` keeps one pointer clause |
| ~20 KB here vs ~40 KB in `ai-docs-organizing`, unexplained | `structure.md` names both: the map from ~20 KB is this skill's, the diet from ~40 KB is `ai-docs-organizing`'s |
| `structure.md` "What moved, and why (2026-09-15)" | Old node names, above; the reasons were already the bold-changes table |
| Refresh path's tier sentence | `references/refresh.md` admission by tier (already there) |
| Description triggers: owner list, C4, "whether an API needs a document", the 30-day gate | body: principle 3 (layers, API), Creating step 4 (C4), the refresh gate section; the skill is slash-command only, so description triggers do not route it |

### No-op pass, 2026-10-19 / 空指令清理

Each reference sentence was asked whether a current model (Opus 5.5, GPT-5.x) would do it unprompted; those were cut, and each rule repeated across files kept one full copy. `cross-cutting.md` 4,044 → 2,026 B, `diagramming.md` 1,790 → 1,025 B, `structure.md` 12,612 → 12,024 B, `adopting-openspec.md` 6,145 → 6,005 B; 3.5 KB in all. PlantUML kept.
逐句问：当前模型（Opus 5.5、GPT-5.x）不提示也会这么做吗？会的删掉；跨文件重复的规则只留一份完整版本。共减 3.5 KB，保留 PlantUML。

| Old | New home |
|---|---|
| `diagramming.md` "do not diagram trivial structures", "keep each diagram small, split", "update the diagram in the same change" | deleted as no-ops; the same-change rule is also `SKILL.md` Updating step 3 |
| `cross-cutting.md` bullets for config, architecture boundary, setup workflow, schema, new terms, decisions, repeated AI mistakes | the ownership-map template rows for config, architecture, data model, generated schema and repeated mistakes; `SKILL.md` Updating steps 2–4 (terms, decision log, ADR, diagram, regenerate layer 3, promote and complete); `structure.md` layers 0 and 5 (setup lives in the manifest and a skill) |
| `cross-cutting.md` API, safety, dependency-version, framework-bridge bullets | kept, as the four cases the map does not make obvious |
| `cross-cutting.md` → Links "relative links, `#anchors`, validate after moving" | one line: relative, not root-relative; validating links is `SKILL.md` Creating step 5 and gardening |
| `structure.md` statistics (60.5%, 14.8% / 14.5% of 2,303, 1.3%) and "since 2026-09-15" | this readme, Why restructure and the bold-changes table (already there) |
| `structure.md` C4 L3/L4 quotes | `diagramming.md` only |
| `structure.md` tree comment on the code locator (entry discipline, read by search, the user's words) | `structure.md` → Repo map and code locator only; the template keeps its reading-rule cell |
| `structure.md` decision-state list in the `product` comment | `cross-cutting.md` → Future Work; the template keeps its cell |
| `adopting-openspec.md` rule 3 hot-spec text | pointer to `structure.md` → Hot documents, with the OpenSpec reading rule (map → requirement → test) |
