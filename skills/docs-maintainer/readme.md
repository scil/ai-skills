# docs-maintainer — how it got its current shape

A procedural skill for the documentation system of a repository whose first reader is an agent. Created 2026-05; slimmed to a router with three references 2026-09-13; restructured by loading layer and given tiered sources and a refresh gate on 2026-09-15. This file records the 2026-09-15 decisions and what they rest on.
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

## Old node names / 旧节点名

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

`SKILL.md` stays a router. Layer rules and the mapping table live in `references/structure.md`; the template in `templates/ownership-map.md`; every rule's source in `references/sources.md` with a `purpose` that says what is taken and what is not. A restructure found necessary by a refresh is proposed in `changelog.md` first. There is no Chinese mirror (removed 2026-10-19, below).
`SKILL.md` 只做路由；层规则与映射表在 `structure.md`；模板在 `templates/`；每条规则的来源在 `sources.md`。刷新发现需要重构时先在 `changelog.md` 提议。不再有中文镜像（2026-10-19 删除，见下文）。

## Cleanup, 2026-10-19 / 清理

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

## No-op pass, 2026-10-19 / 空指令清理

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
