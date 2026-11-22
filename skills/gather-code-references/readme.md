# gather-code-references — decision record

## 2026-11-20: index findings by the code-plan-review standards / 用 code-plan-review 的标准索引发现

### Decision / 决定

Step 5 of `SKILL.md` and the theme indexes of `references/reference-collection-template.md` now follow the standards that `code-plan-review` records in its `references/taxonomy.md`.
`SKILL.md` 第 5 步和 `references/reference-collection-template.md` 的主题索引，改为采用 `code-plan-review` 在 `references/taxonomy.md` 中记录的标准。

- The five architecture views of Kruchten's 4+1 model (scenarios, logical, process, development, operations) are the main index. The skill asks each resource one question per view.
  Kruchten 4+1 模型的五个架构视图（scenarios、logical、process、development、operations）作为主索引。对每个资源按视图各问一个问题。
- Each finding carries a tag: the ISO/IEC 25010 quality characteristic it serves.
  每条发现打上标签：它服务的 ISO/IEC 25010 质量特性。
- A known failure mode is filed under the `code-plan-review` node it matches, with its technology. It is a candidate binding entry for `code-plan-review/references/stacks/`. A failure mode no node names goes under "Outside the tree".
  已知失败模式按匹配的 `code-plan-review` 节点归档，并注明技术。它是 `code-plan-review/references/stacks/` 的候选绑定条目。没有节点能命名的失败模式放进 "Outside the tree"。
- The CWE-1000 pillars are not used directly. The node a failure mode matches already carries its pillar.
  不直接使用 CWE-1000 支柱。失败模式所匹配的节点已带有其支柱。

### Why / 原因

The old list of nine themes was made for this skill alone and had no outside basis. Most of its themes map cleanly onto one view. Its last theme (security, performance, accessibility, compatibility) is a list of quality characteristics, which ISO/IEC 25010 already names. Keying failure modes by node gives the two skills one numbering, so a pitfall found in research reaches a binding with no translation.
旧的九个主题只为本 skill 而设，没有外部依据。大多数主题能干净地对应到一个视图。最后一个主题（安全、性能、可访问性、兼容性）本就是质量特性清单，ISO/IEC 25010 已经命名。按节点归档失败模式让两个 skill 共用一套编号，调研中发现的坑无需转换就能进入绑定。

### Limits / 限制

- The standards index findings across resources. A resource dossier keeps its own shape, as the guardrail "Do not flatten rich resources into a closed table" requires.
  标准只用于跨资源索引。资源档案保持自己的结构，这是护栏 "Do not flatten rich resources into a closed table" 的要求。
- The views overlap, and security and performance cut across all of them. That is why quality is a tag and not a sixth index.
  视图之间有重叠，安全和性能横跨所有视图。所以质量是标签，而不是第六个索引。
- The standards are cited from `code-plan-review/references/taxonomy.md`, not copied. A change to the standards is made there.
  标准引用自 `code-plan-review/references/taxonomy.md`，不复制。修改标准在那里进行。

### Alternatives considered / 考虑过的方案

- Keep the nine themes. Rejected: no outside basis, and no link to the plan review.
  保留九个主题。否决：没有外部依据，也与计划评审无关联。
- Index by CWE pillar. Rejected: the pillars classify defects, and most of what a resource teaches is a pattern, not a defect.
  按 CWE 支柱索引。否决：支柱分类的是缺陷，而资源教给我们的多数是模式，不是缺陷。

## 2026-11-20, later: plan coverage first, check it last, harvest every run / 先规划覆盖、最后检查、每次收割

### Decision / 决定

- Step 2 writes a coverage plan: for each view, the questions this project needs answered, or "not needed" with a reason. Each view that is needed gets at least one planned source.
  第 2 步写覆盖计划：每个视图要回答的问题，或写明"不需要"及原因。每个需要的视图至少计划一个来源。
- Step 3 searches for failure modes on purpose, in issues, advisories, migration guides and changelogs, guided by the matching `code-plan-review` gates.
  第 3 步有意检索失败模式：按匹配的 `code-plan-review` 门，查 issue、安全公告、迁移指南和变更日志。
- Step 6 checks coverage: every view ends with findings, a stated gap, or "not needed".
  第 6 步检查覆盖：每个视图都以发现、已声明的缺口或"不需要"收尾。
- A new step 7 harvests every run into the skill, each lesson to one home, after the user says yes. Changes are logged below under "Harvest log".
  新增第 7 步：每次运行后把经验收割进本 skill，每条经验进唯一归宿，经用户同意后修改。改动记在下方 "Harvest log"。

### Why / 原因

Steps 1 to 4 chose and recorded sources by project facts, research mode and trust, but nothing decided what the research had to cover. The views arrived only in step 5, where they sort what was found and cannot reveal what was missed. A view with no planned source stayed empty, and an empty index looked the same as nothing to learn. Pitfalls live mostly in secondary sources, so they were under-gathered.
第 1 到 4 步按项目事实、调研模式和可信度选择并记录来源，但没有任何一步决定调研必须覆盖什么。视图到第 5 步才出现，只能整理已找到的，无法暴露遗漏的。没有计划来源的视图会是空的，而空索引看起来和"没什么可学"一样。坑多数藏在次级来源里，所以收集不足。

The harvest step exists because the checklists and view questions only improve if each run feeds back what it learned. It follows the same rule as `code-plan-review`: widen before adding, and never a new step or file for one incident.
收割步骤存在，是因为清单和视图问题只有在每次运行反馈经验时才会变好。它沿用 `code-plan-review` 的规则：先放宽再新增，不为单次事故新增步骤或文件。

## 2026-11-20, later: reach joins the scenarios question / 可达性并入 scenarios 问题

### Decision / 决定

The scenarios question in step 5 now asks about reach: machine visitors (search crawlers, link previews, AI-agent interfaces) and people using assistive technology, another language or another device. A reach pitfall goes to `code-plan-review` gate S7, added the same day.
第 5 步的 scenarios 问题现在包含可达性：机器访客（搜索爬虫、链接预览、AI 代理接口）以及使用辅助技术、其他语言或其他设备的人。可达性的坑归入同日新增的 `code-plan-review` S7 门。

### Why / 原因

A comparison with the owner's quality dimensions (Logseq page `d/quality-dimensions`) showed that Reach had no home in either skill. Without a question, the coverage plan never asks for a source on it. Cost showed the same gap and was left out by the owner's decision.
与作者的质量维度（Logseq 页面 `d/quality-dimensions`）对照后发现，两个技能都没有 Reach 的位置。没有对应问题，覆盖计划就不会为它找来源。Cost 有同样的缺口，按作者决定不纳入。

## Harvest log / 收割日志

Each entry: date, the run that taught it, the lesson, and the file changed.
每条：日期、来源运行、经验、修改的文件。
