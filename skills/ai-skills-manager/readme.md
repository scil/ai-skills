# ai-skills-manager — where this came from

A procedural skill for the content of one skill: what its description carries, what its body keeps, what moves behind a pointer, and how a drifted fork is folded back. It was split out of `ai-docs-organizing` on 2026-09-16 along the line that already separated `ai-agents-md` from it: one skill owns the *content of one file*, the other owns the *loading model and the budget across files*.
一个流程型 skill，管单个 skill 的内容：description 装什么、正文留什么、什么下沉到指针后面、漂移的 fork 怎么并回。2026-09-16 从 `ai-docs-organizing` 拆出，切线与 `ai-agents-md` 和它之间的切线相同：一个管*单个文件的内容*，另一个管*跨文件的加载模型与预算*。

## Why split / 为什么拆

The skills material in `ai-docs-organizing` had two natures. The roster — which directories each harness scans, the four provenance classes, "the contract lists no skills", the Codex budget warning and the `skills-reserve` parking — is about the loading layer and stayed. The rest — the description is a trigger and nothing else; router body plus verbatim references; the no-op test; a word count is a guideline; folding a fork back — is about one `SKILL.md`, and needed what the roster material does not: a sources file with a refresh gate, because the skill format is vendor-specified (agentskills.io, Anthropic, OpenAI) and changing. Moving ~600 words between files would not have justified a new always-loaded description; the refresh machinery does.
`ai-docs-organizing` 里的 skills 内容有两种性质。花名册——各壳扫哪些目录、四种来源类别、"契约不列 skill"、Codex 的预算警告与 `skills-reserve` 停放——属于加载层，留下。其余——description 只是触发条件；路由器正文加原文 references；空指令测试；词数只是参考；fork 并回——属于单个 `SKILL.md`，并且需要花名册内容不需要的东西：带刷新门的来源文件，因为 skill 格式由厂商规定（agentskills.io、Anthropic、OpenAI）且在变。只是在文件间搬 600 词不值得多付一条常驻 description；刷新机制才值得。

## Old section → new home / 新旧映射

| Was | Now |
|---|---|
| `ai-docs-organizing/SKILL.md` "Skills, hooks, memory", the sentence "A description carries its trigger and nothing else… lives in the contract once" | principle 1 here; a one-clause pointer remains there |
| `ai-docs-organizing/SKILL.md` "Slimming a skill, and folding a fork back" (whole section) | principles 2, 4, 6 and the Slim / Fold-back paths here; the section there is a two-line pointer |
| `ai-docs-organizing/references/process.md` §9 (whole section, including the fold-back paragraph) | `references/slimming.md`, verbatim; §9 there is a stub so §10 and §11 keep their numbers |
| `ai-docs-organizing/SKILL.md` description "…or before adding a skill or an AGENTS.md section" | "before adding a skill" dropped there; the case is this skill's Grow path |
| — (new) | `references/review-checklist.md`, `references/sources.md`, `references/refresh.md`, `references/changelog.md`; principle 3 (no-op test) grounded in a vendor source; principle 5 (one home) lifted from process.md §11 step 3 into a principle |

Nothing was deliberately dropped. The instance the slimming ladder was harvested from (docs-maintainer 3,529 words → 990-word router with three references, 2026-09-13) stays in `ai-docs-organizing/readme.md` item 8.

## The filler pass (2026-09-16) / 废话清理

A review of all fourteen skills in the collection found the same four kinds of non-rule text in thirteen of them: self-description (Scope essays, origin stories, dates), justification beside rules that stood alone (round counts, token figures, incident narratives), the same content twice in one file (closing reference lists, anti-pattern tables, a rule at three steps), and project or machine names in shared skills. Nine skills were slimmed in nine commits (`fix-bugs` 1,249 → ~600 words; `codex-review` 1,900 → ~1,050; the rest 10–30 %); no rule was dropped. The kinds, dispositions and a detector are principle 7 and `references/filler.md`; the checklist rows that had prescribed a **Scope.** paragraph and a closing references list were corrected in the same change.
对集合里全部十四个 skill 的一次评审，在十三个里发现了同样四类非规则文字：自我描述（Scope 长段、起源故事、日期）、给本已成立的规则附加的理由（轮数、token 数、事故叙事）、同一文件里的重复（结尾引用列表、反模式表、一条规则出现在三步里）、以及共享 skill 里的项目或机器名。九个 skill 在九个提交里瘦身，没有丢任何规则。四类、处置方式和检测脚本成为原则 7 和 `references/filler.md`；此前要求写 **Scope.** 段和结尾引用列表的清单行同步改正。

## Boundaries / 边界

| Question | Owner |
|---|---|
| What goes in one skill's description, body, references; slimming; fork fold-back | this skill |
| Which directories load skills, provenance classes, roster budget, parking, "the contract lists no skills" | `ai-docs-organizing` |
| Creating a skill from nothing; evals and triggering benchmarks | `skill-creator` (Anthropic) |
| The instruction file's content | `ai-agents-md` |
| Where any other project fact lives; a doc section that has become a procedure → a skill | `docs-maintainer` |

## How to maintain / 怎么维护

`SKILL.md` stays a router: principles, the gate, four paths (Review-and-apply, Grow, Fold a fork back, Refresh — Slim was merged into Review on 2026-09-16 as its apply step, since both ran the same measurements and tests), each reference linked where it is used. Vendor facts about the format live only in `references/sources.md` (with the tier and the date); loading facts about a harness live in `ai-docs-organizing/references/harness-loading.md` and are pointed at, never copied. When a review or a slim teaches a rule the checklist lacks, add the row with its incident. The refresh runs through the sibling's `check-sources.ps1` with `-Path`; do not fork the script.
`SKILL.md` 只放原则、刷新门、四条路径（Review 并执行、Grow、并回 fork、Refresh —— Slim 于 2026-09-16 并入 Review 作为其执行步骤，因为两者跑的是同一套测量和测试），引用在使用处链接。格式的厂商事实只放 `references/sources.md`（带层级与日期）；壳的加载事实放 `ai-docs-organizing/references/harness-loading.md`，只指向不复制。评审或瘦身教会了清单没有的规则，就连同事故加一行。刷新用兄弟 skill 的 `check-sources.ps1 -Path`，不要 fork 脚本。
