# docs-maintainer — how it got its current shape

A procedural skill for the documentation system of a repository whose first reader is an agent. Created 2026-05; slimmed to a router with three references 2026-09-13 (see `for-human/ref.md` for the earlier history); restructured by loading layer and given tiered sources and a refresh gate on 2026-09-15. This file records the 2026-09-15 decisions and what they rest on.
面向"第一读者是代理"的仓库文档系统的流程型 skill。2026-05 创建；2026-09-13 瘦身为路由器；2026-09-15 按加载层重构，并加入分层来源与刷新门控。本文记录 2026-09-15 的决定及其依据。

## Why restructure by loading layer / 为什么按加载层重构

The old Annotated Structure was a `docs/` tree by topic (product, architecture, engineering, api, operations, ai). It assumed the reader would browse. The evidence gathered for `ai-agents-md` says agents do not browse: in 557 real sessions, 60.5% of documentation interactions were with instruction files and working notes, 10.6% with classical technical docs, 1.3% with API references (Gao & Chen, 2026-08). Agents also go looking proactively (70.2%) rather than after a failure (7.5%), so what they find is what the always-loaded map points at. Both vendors say the same thing from the other side: Anthropic moves "a section of CLAUDE.md that has grown into a procedure rather than a fact" into a skill and trims layouts and overviews from the file; OpenAI keeps the main file concise and references task-specific markdown files. So the organizing question changed from "what topic is this" to "how does this fact reach the agent, and what does each read cost" — the seven layers.
旧结构是按主题分的 `docs/` 树，假设读者会浏览。为 `ai-agents-md` 收集的证据表明代理不浏览：557 个真实会话里，60.5% 的文档交互发生在指令文件和工作笔记上，经典技术文档 10.6%，API 参考 1.3%；而且代理是主动去找（70.2%）而不是失败后才找（7.5%），所以常驻地图指向什么，它们就找到什么。两家厂商从另一面说了同一件事。于是组织问题从"这是什么主题"变成"这个事实怎么到达代理、每次读花多少"，即七层。

## The bold changes, each with its source / 大改动及其依据

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

## What was kept / 保留了什么

Code-wins; one owner per fact; the File-First Split Rule; the Adopting path (route, do not scaffold) and its "skipped — reason" convention; the locator entry discipline; C4 L1/L2 by hand with PlantUML; the cross-cutting checklist.
保留：代码优先、一个事实一个主人、先文件后拆分、"接管而非搭建"及其"跳过—原因"约定、定位器条目纪律、手绘 C4 一二层、交叉变更清单。

**Removed the same day: `rules/tauri-command-api.md`.** A shared, project-agnostic skill carried a rule for one framework; by this skill's own routing principle its owner is the Tauri project. What it said, for that project to re-home as one ownership-map row: Tauri commands are a provided API whose facts of record are the handlers, the frontend wrapper and the shared types; a generated command index (layer 3) owns the surface; hand-written text covers only admin, permission, preview and destructive-guard behaviour, in the security quality-attribute doc.
**当天删除 `rules/tauri-command-api.md`。** 共享 skill 不该带单一框架的规则；按本 skill 自己的路由原则，它的主人是那个 Tauri 项目。该项目可把它收为归属表一行：命令处理器、前端封装与共享类型是事实来源；生成的命令索引拥有接口面；手写只保留权限、预览与破坏性操作的守护说明，放在安全文档。

## Sources, tiers and the 30-day gate / 来源分层与 30 天门控

Same tiering as `ai-agents-md`: vendor and standard sites decide; research corroborates in pairs; exemplars illustrate; reports point. The checker script is shared (`ai-agents-md/scripts/check-sources.ps1 -Path … -GateDays 30`). Thirty days rather than seven because C4, MADR, OpenAPI and llms.txt move slowly; the vendor pages on skills and plans are read first when the script reports a change.
分层与 `ai-agents-md` 相同。检查脚本共用。门控 30 天而非 7 天：C4、MADR、OpenAPI、llms.txt 变化慢；脚本报告变化时先读厂商关于 skills 和 plans 的页面。

## Boundaries / 边界

`ai-agents-md` owns layer 0's content. `ai-docs-organizing` owns the loading model, byte budgets and the diet of an oversized contract or hot doc. This skill owns layers 1–6: where every other fact lives, in what shape, with what check.
`ai-agents-md` 管第 0 层内容；`ai-docs-organizing` 管加载模型、字节预算与瘦身；本 skill 管 1 到 6 层。

## How to maintain / 怎么维护

`SKILL.md` stays a router. Layer rules and the mapping table live in `references/structure.md`; the template in `templates/ownership-map.md`; every rule's source in `references/sources.md` with a `purpose` that says what is taken and what is not. A restructure found necessary by a refresh is proposed in `changelog.md` first. The Chinese mirror `for-human/SKILL.zh.md` lags this version and says so in its header.
`SKILL.md` 只做路由；层规则与映射表在 `structure.md`；模板在 `templates/`；每条规则的来源在 `sources.md`。刷新发现需要重构时先在 `changelog.md` 提议。中文镜像滞后并在头部注明。
