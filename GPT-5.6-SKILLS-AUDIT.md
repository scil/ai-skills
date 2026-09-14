# GPT-5.6 / Sol 用户级 Skills 审计  
# User-level Skills Audit for GPT-5.6 / Sol

**范围 / Scope:** `C:\Users\i\.agents\skills`  
**审计日期 / Audit date:** 2026-07-11  
**覆盖 / Coverage:** 20 个 Skill 包，包括 `SKILL.md`、references、scripts、templates、examples、rules、metadata 与嵌套 `AGENTS.md`。  
20 Skill packages, including `SKILL.md`, references, scripts, templates, examples, rules, metadata, and nested `AGENTS.md` files.

## 执行结论 / Executive verdict

这套 Skills 可分为三类：  
The portfolio contains three distinct categories:

1. **持久能力扩展 / Durable capability extensions**：本机工具流程、项目约定、经过筛选的框架规则。GPT-5.6 无法自行推断本地 Anki 字段、项目文档所有权或特定规则语料。  
   Machine-specific tools, project conventions, and curated framework rules. GPT-5.6 cannot infer local Anki fields, project documentation ownership, or a vetted rule corpus.
2. **有用的领域视角 / Useful domain lenses**：竞争、市场流动性、PMF、定位、客户研究与创业验证。价值来自紧凑框架和证据模型，而不是通用推理提示。  
   Competition, marketplace liquidity, PMF, positioning, customer research, and startup validation. Their value comes from compact frameworks and evidence models, not generic reasoning prompts.
3. **遗留提示脚手架 / Legacy prompt scaffolding**：角色扮演、强制提问、任意评分、固定周期和重复复查。现代 agent 已原生具备规划、上下文检查和验证能力，这些指令会增加延迟并削弱自主性。  
   Persona theater, compulsory questioning, arbitrary scoring, fixed timelines, and repeated review loops. Modern agents already plan, inspect context, and validate; these instructions add latency and reduce autonomy.

### 总体建议 / Portfolio recommendation

- ✅ 保持不变 / Keep unchanged: **4**
- ✂ 精简 / Simplify: **9**
- 🔀 合并 / Merge: **4**
- 📦 归档 / Archive: **1**
- 🗑 删除 / Delete: **1**
- 理想规模 / Ideal active set: **14–16 Skills**

## 评级标准 / Rating criteria

- **完全替代 / Fully replaced**：几乎全是通用模型行为或格式要求。 / Almost entirely generic model behavior or formatting.
- **大部分替代 / Mostly replaced**：主体能力原生具备，只剩少量清单或模板有价值。 / Most capability is native; only a small checklist or template remains useful.
- **部分替代 / Partially replaced**：通用流程原生具备，但专门框架或证据规则仍有价值。 / Generic workflow is native, but specialized frameworks or evidence rules remain valuable.
- **仍有价值 / Still valuable**：提供显著的非原生流程、知识或约定。 / Supplies material non-native procedure, knowledge, or conventions.
- **必不可少 / Essential**：删除会破坏专门集成或项目契约。 / Removal would reliably break a specialized integration or project contract.

Token 成本按触发后的上下文与检索负担评估，而不只是文件大小。  
Token cost reflects triggered context and retrieval burden, not file size alone.

## 总表 / Portfolio table

| Skill | 用途 / Purpose | GPT-5.6 重叠 / Overlap | 成本 / Cost | 建议 / Recommendation | 核心理由 / Core reason |
|---|---|---|---|---|---|
| `anki-cards` | 本地工具、学习流程、写入安全 / Local tooling, learning workflow, write safety | **必不可少 / Essential** | 轻 / Light | ✅ 保持 / Keep | 包含本机中文 Note Type、字段、Deck、AnkiConnect helper、UTF-8/HTML 陷阱和 TSV fallback；模型无法推断。 / Encodes machine-specific schemas, helpers, encoding/HTML gotchas, and fallback behavior. |
| `competitive-analysis` | 竞争策略领域推理 / Competitive strategy reasoning | **部分替代 / Partial** | 中 / Moderate | ✂ 精简 / Simplify | status quo、替代方案与非对称优势有用；原则重复，855 行引语库昂贵且易过时。 / Useful status-quo, alternatives, and asymmetry lens; repetitive principles and an aging 855-line quote bank. |
| `customer-research` | 研究、证据纪律、综合 / Research, evidence discipline, synthesis | **仍有价值 / Still valuable** | 重 / Heavy | 🔀 合并 / Merge | 偏差、置信度、引用溯源和代理证据很强；与 `user-research`、`research-synthesis` 高度重叠。 / Strong bias, confidence, provenance, and proxy-evidence rules; heavily overlaps two other Skills. |
| `derive-project-plan` | 把外部参考转成项目计划 / Convert references into project plans | **仍有价值 / Still valuable** | 轻 / Light | ✅ 保持 / Keep | 明确区分外部证据与项目决策，并要求可追溯性和验收标准。 / Separates external evidence from project decisions and requires traceability and acceptance criteria. |
| `docs-maintainer` | 项目文档架构与所有权 / Documentation architecture and ownership | **必不可少 / Essential** | 重 / Heavy | ✂ 精简 / Simplify | facts-of-record、repo-map/code-locator 等约定不可原生推断；完整树过度展开。 / Project-specific ownership rules are non-native; the exhaustive tree is over-expanded. |
| `find-skills` | Skill 搜索和安装 / Skill discovery and installation | **部分替代 / Partial** | 中 / Moderate | ✂ 精简 / Simplify | CLI 有用；触发过宽、排行榜优先、固定热度阈值和 `-g -y` 存在风险。 / Useful CLI, but broad triggers, popularity heuristics, and unattended global install are risky. |
| `gather-code-references` | 代码参考研究和证据收集 / Code-reference research and evidence gathering | **仍有价值 / Still valuable** | 轻 / Light | ✅ 保持 / Keep | 提供来源层级、版本验证、原始材料保留及稳定输出契约。 / Provides source hierarchy, version checks, raw-artifact preservation, and a stable output contract. |
| `git-commit` | Conventional Commit 与暂存流程 / Conventional Commits and staging | **仍有价值 / Still valuable** | 轻 / Light | ✂ 精简 / Simplify | 提交约定有价值；Bash-only、heredoc 与当前 PowerShell 环境不兼容。 / Commit convention is useful; Bash-only heredoc syntax conflicts with this PowerShell environment. |
| `marketplace-liquidity` | 双边市场流动性诊断 / Marketplace liquidity diagnosis | **仍有价值 / Still valuable** | 轻 / Light | ✂ 精简 / Simplify | match rate、time-to-match 与供需约束是专门知识；原则可压缩为诊断 schema。 / Specialized match-rate and supply/demand knowledge; principles can become a compact diagnostic schema. |
| `measuring-product-market-fit` | PMF 评估 / PMF assessment | **部分替代 / Partial** | 重 / Heavy | ✂ 精简 / Simplify | 留存、分群、pull 和 Sean Ellis 组合有用；855 行引语与二元化判断过重。 / Useful combined retention, segmentation, pull, and Sean Ellis model; quote corpus and binary framing are excessive. |
| `positioning-messaging` | 定位与信息架构 / Positioning and messaging | **部分替代 / Partial** | 重 / Heavy | ✂ 精简 / Simplify | 定位输入契约有价值；1,403 行引语库和格言式原则不够操作化。 / Useful positioning input contract; a 1,403-line quote bank and aphorisms are not operationally efficient. |
| `product-requirements` | 交互式 PRD 流程 / Interactive PRD workflow | **大部分替代 / Mostly replaced** | 重 / Heavy | 🗑 删除 / Delete | “Sarah”角色、100 分评分、90 分门槛、强制提问与中文覆盖会伤害现代 agent。 / Persona theater, arbitrary scoring, hard gate, compulsory questions, and language override harm modern agents. |
| `research-synthesis` | 研究综合格式 / Research synthesis format | **大部分替代 / Mostly replaced** | 轻 / Light | 🔀 合并 / Merge | 模板有用，但内容已被 `customer-research` 覆盖。 / Useful template, but already covered by `customer-research`. |
| `roadmap-planning` | 路线图工作坊 / Roadmap workshop | **大部分替代 / Mostly replaced** | 重 / Heavy | 📦 归档 / Archive | 517 行、固定 1–2 周、缺失依赖和重复流程使其脆弱。 / 517 lines, fixed 1–2 week process, missing dependencies, and repetition make it brittle. |
| `startup-pressure-test` | 创业想法压力测试 / Startup pressure testing | **仍有价值 / Still valuable** | 中 / Moderate | ✂ 精简 / Simplify | 直接 verdict、证据阶梯、首批客户和两周测试有价值；评分与默认输出应可选。 / Verdict, evidence ladder, first customers, and two-week test are useful; scoring and full output should be optional. |
| `user-research` | 研究方法与访谈设计 / Research methods and interview design | **大部分替代 / Mostly replaced** | 轻 / Light | 🔀 合并 / Merge | 内容正确但仅 265 词，与客户研究没有独立触发价值。 / Sound but only 265 words and not distinct enough to justify a separate trigger. |
| `vercel-react-best-practices` | React/Next 性能规则 / React/Next performance rules | **仍有价值 / Still valuable** | 重 / Heavy | ✂ 精简 / Simplify | 规则有价值，但 SKILL、README、rule files、108 KB `AGENTS.md` 重复。 / Valuable rules duplicated across router, README, granular files, and a 108 KB compiled manual. |
| `vercel-react-native-skills` | RN/Expo 性能和平台规则 / RN/Expo performance and platform rules | **仍有价值 / Still valuable** | 重 / Heavy | ✂ 精简 / Simplify | 版本相关知识有价值；重复语料和无条件库选择会覆盖项目上下文。 / Version-sensitive knowledge is useful; duplicated corpus and unconditional library choices can override project context. |
| `web-design-guidelines` | 拉取最新 UI 规则并审查 / Fetch current UI rules and review code | **仍有价值 / Still valuable** | 轻 / Light | ✅ 保持 / Keep | 以极小本地 prompt 换取最新外部规则，是良好的 progressive disclosure。 / Excellent progressive disclosure: tiny local prompt, current external rules. |
| `write-spec` | PRD、范围和验收标准 / PRDs, scope, acceptance criteria | **部分替代 / Partial** | 重 / Heavy | 🔀 合并为 `product-spec` / Merge | 骨架有价值；250 行教程、重复优先级方法与强制提问过多。 / Useful artifact contract; 250 lines of tutorials, duplicate prioritization, and compulsory questioning are excessive. |

## 逐项审计 / Per-Skill audit

### 1. `anki-cards` — Tier S

**中文：** 原始目的不是一般“生成卡片”，而是安全地写入本机 Anki。它同时属于工具使用、本机约定、学习设计和外部写入安全。`ai-teach-me` Deck、中文字段 `正面/背面`、Cloze 字段、PowerShell helper、UTF-8 bytes、HTML escaping 和 TSV fallback 都是不可推断的事实。“写入前确认”是合理的真实副作用边界，不是重复安全提示。  
**English:** Its purpose is not generic card generation but safe mutation of this machine’s Anki setup. The local deck, Chinese fields, Cloze model, PowerShell helpers, UTF-8 handling, HTML escaping, and TSV fallback are non-inferable. Confirmation before writing is a justified side-effect boundary, not redundant safety theater.

**建议 / Recommendation:** ✅ 保持不变。若以后精简，只删 usage sketch，不删 schema、fallback 和写入边界。  
Keep unchanged. If shortened later, remove only the usage sketch—not schemas, fallback, or write boundaries.

### 2. `competitive-analysis` — Tier A

**中文：** Skill 旨在避免只做功能表格，把竞争集合扩展到“不行动”、手工流程、自建和间接替代，并寻找分发、商业模式和非对称优势。GPT-5.6 已懂 SWOT、Porter 和 moat，因此通用推理重叠较高；真正有价值的是“产品不存在时客户会怎么办”的检查框架。正文把 status quo、alternatives、workarounds 分成多个重复原则，42 KB/855 行 guest 引语会造成权威锚定和时效问题，诸如“40%”之类数字也缺乏当前一手来源。  
**English:** The Skill usefully expands competition beyond feature tables to no-decision, manual work, internal builds, indirect alternatives, distribution, economics, and asymmetry. GPT-5.6 already knows common strategy frameworks; the durable value is the “what would customers do without us?” operating lens. The body repeats status quo/alternatives/workarounds, while the 42 KB quote bank creates authority anchoring and freshness problems.

**建议 / Recommendation:** ✂ 保留 250–400 词流程；当前竞争者和市场数据必须浏览并引用一手来源；删除或大幅压缩引语库。  
Keep a 250–400 word workflow; verify current competitors and market claims from primary sources; delete or radically reduce the quote bank.

### 3. `customer-research` — Tier A

**中文：** 这是研究组合中最强的主 Skill。价值来自频率×强度、分群、引用/日期/来源记录、渠道偏差、置信度、矛盾证据和“不发明 Persona”。2.0.1 新增无第一方评论时的代理证据阶梯，并把 Persona 标为 provisional，这是实质改进。但 270+ 行正文、402 行 source guide 和 evals 仍偏重；固定“3 个来源=高置信”“每分群 5 个数据点”等应标为默认启发式，而非方法学真理。它仍重复 `user-research` 和 `research-synthesis`，且“先选 deliverable”可能阻塞上下文已明确的任务。  
**English:** This is the strongest core Skill in the research cluster. Its value is frequency × intensity, segmentation, quote/date/source capture, channel-bias checks, confidence, contradictory evidence, and refusal to invent personas. Version 2.0.1 adds a useful proxy-evidence ladder for products without first-party reviews and labels resulting personas provisional. It remains heavy and overlaps two Skills; numeric evidence thresholds should be defaults, not universal truths.

**建议 / Recommendation:** 🔀 合并三个研究 Skill，形成 plan / gather / synthesize 三条条件路径。保留新代理证据阶梯，但把“差异化决定 ICP”明确写成待验证假设。  
Merge the three research Skills into conditional plan/gather/synthesize paths. Preserve the proxy-evidence ladder, but treat differentiator-derived ICP as a testable hypothesis.

### 4. `derive-project-plan` — Tier S

**中文：** 负责把参考语料转化为项目特定的架构决策、实施规则、顺序和验收标准，并区分“来源事实”与“项目选择”。57 行/491 词，约束清晰，没有无意义的规划循环。与 `gather-code-references` 相邻但不重复：前者做决策，后者收证据。  
**English:** Converts reference corpora into project-specific architecture decisions, implementation rules, sequencing, and acceptance criteria while separating source facts from project choices. At 57 lines/491 words, it is concise and constraint-oriented. It is adjacent to—but intentionally distinct from—evidence gathering.

**建议 / Recommendation:** ✅ 保持不变。 / Keep unchanged.

### 5. `docs-maintainer` — Tier S

**中文：** facts-of-record、所有权、future candidates 与 current facts 的分离、repo-map/code-locator 分工均是项目约定，无法依赖模型常识替代。问题是 2,240 词正文和约 55 KB 包把完整文档树及每个节点的职责全部内联，容易让小项目也生成庞大文档体系。  
**English:** Facts-of-record ownership, future-vs-current separation, and the repo-map/code-locator split are project conventions that native intelligence cannot replace. The problem is size: the 2,240-word body and ~55 KB package inline an exhaustive tree, encouraging maximal documentation even for small projects.

**建议 / Recommendation:** ✂ 主 `SKILL.md` 压到 500–700 词；完整树移入按需加载的 `references/structure.md`；保留模板和框架条件规则。  
Reduce the router to 500–700 words; move the full tree to an on-demand structure reference; retain templates and conditional framework rules.

### 6. `find-skills` — Tier B

**中文：** 外部 Skill 搜索确实需要工具知识，更新后的 `--owner` 过滤值得保留。但 description 对“how do I do X / can you do X”触发过宽，可能在原生能力足够时仍搜索 Skill。排行榜、1K installs、100 stars 和固定知名作者并不等于安全或质量；`-g -y` 会无确认地全局安装可执行提示/工具内容。  
**English:** External Skill discovery needs real tool knowledge, and the new `--owner` filter is worth keeping. However, broad triggers can cause unnecessary searches. Leaderboard rank, 1K installs, 100 stars, and famous publishers are not security reviews; `-g -y` performs unattended global installation.

**建议 / Recommendation:** ✂ 仅在用户明确要求发现/安装时触发；检查 manifest、来源、维护状态和权限；全局安装前明确确认。  
Trigger only on explicit discovery/install intent; inspect manifest, source, maintenance, and permissions; confirm before global installation.

### 7. `gather-code-references` — Tier S

**中文：** 它规范一手来源优先、版本与兼容性检查、原始材料保留、事实/示例/推断分离，并生成可供 `derive-project-plan` 消费的稳定 artifact。浏览本身是原生能力，但这套证据契约不是。  
**English:** It defines primary-source preference, version and compatibility checks, raw-artifact preservation, fact/example/inference separation, and a stable artifact consumed downstream. Browsing is native; this evidence contract is not.

**建议 / Recommendation:** ✅ 保持不变。 / Keep unchanged.

### 8. `git-commit` — Tier A

**中文：** Conventional Commit 类型与 breaking-change 格式有价值，但 diff 检查、保护用户修改和避免 destructive git 已由现代 agent/system 处理。当前 frontmatter 写 `allowed-tools: Bash`，正文用 `$(cat <<'EOF')`，与 Windows/PowerShell 环境不兼容。“hook 失败后创建 NEW commit”也表达不准确，因为失败时并未产生 commit。最近更新时间变化没有带来语义修复。  
**English:** Conventional Commit types and breaking-change syntax remain useful, while diff inspection and generic git safety are already native/system behavior. `allowed-tools: Bash` and `$(cat <<'EOF')` conflict with Windows/PowerShell. “Create a NEW commit after hooks fail” is confused because a failed commit creates no commit. The recent timestamp change did not fix the semantics.

**建议 / Recommendation:** ✂ 改成 shell-neutral：检查 status/diff、保护无关修改、只暂存逻辑单元、检查 staged secrets、正常运行 hooks、报告 hash。  
Make it shell-neutral: inspect status/diffs, preserve unrelated work, stage the logical unit, scan staged content for secrets, run hooks normally, and report the hash.

### 9. `marketplace-liquidity` — Tier A

**中文：** 双边市场不是一般增长问题；需要定义原子市场（地区×品类×时间）、match/fill rate、time-to-match、重复率、取消率和失败原因。当前四条原则表达重复，引语对执行帮助有限。  
**English:** Two-sided marketplaces require a specialized lens: define the atomic market, then measure match/fill rate, time-to-match, repeat rate, cancellation, and failure causes. The four current principles repeat one another, and quotations add little execution value.

**建议 / Recommendation:** ✂ 改成诊断 schema：识别受约束一侧与失败模式，再选择聚焦、补贴、质量、价格、信任或运营干预，并定义实验。  
Replace principles with a diagnostic schema: identify the constrained side and failure mode, then choose focus, subsidy, quality, pricing, trust, or operational interventions with an experiment.

### 10. `measuring-product-market-fit` — Tier A

**中文：** 留存曲线、Sean Ellis survey、分群、客户 pull、reference customer 和分发组合仍有价值。但正文十条原则互相重叠，43.5 KB/855 行引语库是主要成本；40% 阈值和“宕机时没人愤怒=无 PMF”不能作为普适判定。  
**English:** Retention curves, Sean Ellis surveys, segmentation, customer pull, references, and distribution form a useful combined model. Ten principles overlap, and the 43.5 KB quote bank dominates cost. The 40% threshold and outage-outrage test are not universal verdict rules.

**建议 / Recommendation:** ✂ 用分群证据矩阵输出 insufficient / emerging / strong / eroding；记录样本 N、选择偏差、置信度和下一个证伪测试，避免合成总分。  
Use a segment-level evidence matrix with insufficient/emerging/strong/eroding states; record sample size, selection bias, confidence, and the next falsifying test instead of a synthetic score.

### 11. `positioning-messaging` — Tier A

**中文：** 有价值的核心是 target segment、struggling moment/JTBD、current alternative、unique capability、value、proof 和 objection 的输入契约。正文七条格言不够操作化，74.5 KB/1,403 行引语库会锚定名人观点而非客户证据，并与竞争和客户研究重复。  
**English:** The durable core is an input contract covering target segment, struggling moment/JTBD, current alternative, unique capability, value, proof, and objections. Seven aphoristic principles are not operational, while the 74.5 KB quote bank anchors to famous opinions rather than customer evidence and overlaps adjacent Skills.

**建议 / Recommendation:** ✂ 输出 positioning statement、message hierarchy 和 claims/evidence table；缺证据时转交客户研究；删掉或极度压缩引语库。  
Produce a positioning statement, message hierarchy, and claims/evidence table; route missing evidence to customer research; delete or radically reduce the quote bank.

### 12. `product-requirements` — Tier D

**中文：** 这是最应删除的 Skill。具体问题包括：扮演 “Sarah”、固定问候、100 分加权评分、必须达到 90 分、每轮展示分数和表扬、强制 2–3 个问题、不允许合理假设、自动写入 `docs/{feature}-prd.md`、引用可能不存在的 `AskUserQuestion`，以及无视对话语言强制中文。它声称“concise”，却提供巨大模板；其有效内容也被 `write-spec` 覆盖。  
**English:** This is the clearest deletion candidate. Harmful instructions include acting as “Sarah,” a scripted greeting, arbitrary 100-point scoring, a hard 90-point gate, repeated score/praise loops, compulsory questions, prohibition on reasonable assumptions, automatic file writes, a possibly nonexistent tool name, and a forced Chinese response. Its useful content is duplicated by `write-spec`.

**建议 / Recommendation:** 🗑 删除。只把风险/依赖检查表并入新的 `product-spec`。  
Delete. Preserve only the risk/dependency checklist inside a new `product-spec`.

### 13. `research-synthesis` — Tier B

**中文：** themes、quotes、segments、opportunities 与 further questions 的输出模板正确，但几乎完全包含在 `customer-research` 中；`~~user interviews` 等 connector placeholder 是环境残留。独立 Skill 的边际价值只剩 evidence traceability。  
**English:** The themes, quotes, segments, opportunities, and further-questions template is sound but almost entirely covered by `customer-research`. Connector placeholders are environment residue. Its only distinct residual value is evidence traceability.

**建议 / Recommendation:** 🔀 合并到研究 Skill 的 synthesize 分支，保留 source IDs、矛盾证据、样本限制和 insight→recommendation 链接。  
Merge into the synthesis path, preserving source IDs, contradictory evidence, sample limits, and finding-to-recommendation traceability.

### 14. `roadmap-planning` — Tier C

**中文：** 更新后新增 `argument-hint` 和 Input 段，明确“已提供的信息不要重问”，这是对自主性的真实改善。但主要缺陷未变：517 行、固定五阶段和 1–2 周、参与者/耗时/epic 数量硬编码、完整流程重复一次，并引用不存在的 `workshop-facilitation`、`epic-hypothesis`、`prioritization-advisor` 等 Skill。它把一次路线图请求扩大成组织级工作坊。  
**English:** The update adds an argument hint and a good input rule: consume supplied context and do not re-ask answered questions. The dominant defects remain: 517 lines, a fixed five-phase 1–2 week process, hard-coded participants/durations/epic counts, repeated summaries, and references to missing component Skills. It expands a roadmap request into an organizational workshop.

**建议 / Recommendation:** 📦 归档。新建不超过 300 词的 `product-planning`，只负责 outcome、evidence/confidence、priority、capacity/dependency、Now/Next/Later 与沟通叙事。  
Archive. Replace with a sub-300-word `product-planning` Skill owning only outcomes, evidence/confidence, prioritization, capacity/dependencies, Now/Next/Later, and narrative.

### 15. `startup-pressure-test` — Tier A

**中文：** 直接 strong/weak/pivot verdict、现实替代方案、付费意愿、可触达首批客户、founder fit、MVP 与两周可证伪实验，是有用的反奉承协议。问题是固定总分制造虚假精度，完整默认输出可能超出窄问题范围；当前竞争者和市场事实必须联网验证。  
**English:** A direct strong/weak/pivot verdict, current alternatives, willingness to pay, reachable first customers, founder fit, MVP, and a falsifiable two-week test form a useful anti-flattery protocol. Fixed scores create false precision, and the full default output may exceed a narrow request. Current market claims require browsing.

**建议 / Recommendation:** ✂ verdict 与证据缺口必选；评分、founder fit、首十客户、MVP 和 launch plan 按深度条件启用。明确区分观察、推断和假设。  
Require verdict and evidence gaps; make scoring, founder fit, first-ten plan, MVP, and launch plan conditional. Separate observations, inference, and hypothesis.

### 16. `user-research` — Tier B

**中文：** 方法菜单、非引导式访谈和分析结构正确，而且很轻。但 41 行/265 词不足以支撑独立触发，与 `customer-research` 的方法和访谈内容重复。  
**English:** Its method menu, non-leading interview guidance, and analysis structure are sound and lightweight. At 41 lines/265 words, however, it does not justify a separate trigger and overlaps the main research Skill.

**建议 / Recommendation:** 🔀 合并为 plan-research 分支，保留按决策风险选方法、招募/分群、过去行为问题、同意/隐私和预设分析方案。  
Merge into a plan-research path, preserving method selection by decision risk, recruitment/segmentation, past-behavior questions, consent/privacy, and preplanned analysis.

### 17. `vercel-react-best-practices` — Tier A

**中文：** React/Next 的 waterfall、bundle、server/client boundary 和版本敏感 API 规则有真实价值。但包约 225 KB/76 文件：`SKILL.md` 列规则、README 再列、rule files 展开、108 KB `AGENTS.md` 又完整编译。低影响 JS 微优化和绝对 “always/never” 容易导致无 profiling 的过度重构。  
**English:** React/Next waterfall, bundle, server/client boundary, and version-sensitive API rules are genuinely useful. But the ~225 KB/76-file package repeats its corpus in `SKILL.md`, README, granular rules, and a 108 KB compiled `AGENTS.md`. Low-impact micro-optimizations and absolute language can cause unprofiled over-refactoring.

**建议 / Recommendation:** ✂ 只保留 lean router + granular rules；移除发布包中的 README/compiled `AGENTS.md`；先检查版本、项目约定和 profiling 证据。  
Keep only a lean router plus granular rules; remove README/compiled manual duplication; inspect versions, project conventions, and profiling evidence first.

### 18. `vercel-react-native-skills` — Tier A

**中文：** RN/Expo/Reanimated、列表、原生导航和平台陷阱是专门且版本敏感的知识。问题与 React 包相同：约 155 KB，SKILL/README/rules/73.8 KB `AGENTS.md` 重复。FlashList、expo-image、Galeria、Zeego、native form sheet、精确依赖版本等被写成普适偏好，可能与平台目标、license、New Architecture、React Compiler 或现有栈冲突。  
**English:** RN/Expo/Reanimated, list, navigation, and platform pitfalls are specialized and version-sensitive. The ~155 KB package duplicates content across router, README, rules, and a 73.8 KB compiled manual. Universal preferences for specific libraries or architectures may conflict with targets, licenses, compiler state, or the existing stack.

**建议 / Recommendation:** ✂ 删除编译重复；规则标成 correctness / measured performance / preference；引入新依赖前检查版本和项目授权。  
Remove compiled duplication; classify rules as correctness, measured performance, or preference; inspect versions and obtain project authorization before adding dependencies.

### 19. `web-design-guidelines` — Tier A

**中文：** 这是优秀的 progressive disclosure：本地只有 39 行，每次从权威 URL 拉取最新规则，再按文件和行输出问题。它避免把易过时规则嵌入 prompt。唯一小问题是工具名 `WebFetch` 未必是所有 host 的实际名称，且缺少网络失败路径。  
**English:** This is excellent progressive disclosure: only 39 local lines, with fresh rules fetched from an authoritative URL and findings reported by file/line. It avoids embedding stale guidance. Minor issues are a host-specific `WebFetch` name and no network-failure path.

**建议 / Recommendation:** ✅ 保持不变。未来可补充 fetch 失败时披露 freshness，并询问是否使用缓存/原生规则。  
Keep unchanged. Optionally disclose freshness failure and ask before using cached/native guidance.

### 20. `write-spec` — Tier A（重构后 / after refactor）

**中文：** problem、goals/non-goals、优先级需求、验收标准、metrics、dependencies、risks 和 open questions 是有用的 artifact contract。但 250 行/1,985 词重复解释 user story、MoSCoW 与 P0/P1/P2、指标示例和 scope creep；强制多轮提问和 review offer 与现代 agent 自主检查上下文冲突；`CONNECTORS.md` 和 `~~project tracker` 等引用不可靠。  
**English:** Problem, goals/non-goals, prioritized requirements, acceptance criteria, metrics, dependencies, risks, and open questions form a useful artifact contract. But 250 lines repeat user-story tutorials, two prioritization systems, metric examples, and scope-creep advice. Mandatory questioning/review conflicts with autonomous context inspection, and connector placeholders are unreliable.

**建议 / Recommendation:** 🔀 与有效的 PRD 内容合并为 400–600 词 `product-spec`。先检查已有上下文，只问会改变范围或外部影响的问题；不编造指标目标；只有用户要求或 repo 约定时才写文件。  
Merge the useful PRD content into a 400–600 word `product-spec`. Inspect available context first, ask only questions that materially alter scope or external impact, never invent metric targets, and write files only when requested or conventional.

## 跨 Skill 分析 / Cross-skill analysis

### 重复与合并 / Duplication and merge map

| 组合 / Cluster | 重叠 / Overlap | 现代方案 / Modern disposition |
|---|---|---|
| 研究 / Research | `customer-research`、`user-research`、`research-synthesis` 都覆盖方法、访谈、主题、分群、引用和交付物。 / All cover methods, interviews/assets, themes, segments, quotes, and deliverables. | 一个 `customer-research`，包含 plan / gather / synthesize 条件路径。 / One Skill with conditional plan/gather/synthesize paths. |
| PRD / Specification | `product-requirements` 与 `write-spec` 都收集上下文、提问、生成 PRD、定义 stories/criteria/metrics。 | 删除前者，将后者改为简洁 `product-spec`。 / Delete the former; turn the latter into concise `product-spec`. |
| 路线图 / Roadmap | `roadmap-planning` 与 spec、PMF、research 都涉及 metrics、risks、priority 和 sequencing。 | 归档现有包；可选新增只负责优先级和顺序的微型 `product-planning`。 / Archive current package; optionally add a tiny sequencing-only Skill. |
| GTM 推理 / GTM reasoning | competition、positioning、pressure-test、research 共享 ICP、alternatives、differentiation 和 evidence。 | 保持不同触发，但明确 handoff：research 管证据，competition 管格局，positioning 管表达，pressure-test 管创业 verdict。 / Keep distinct triggers with clear ownership. |
| React 规则 / React corpora | 两个 Vercel 包均重复 router、README、rules 和 compiled manual。 | 各自保留 router + granular rules；Web React 与 RN 不合并。 / Keep router + granular rules; do not merge web and native domains. |
| 参考管线 / Reference pipeline | `gather-code-references` 与 `derive-project-plan` 前后相连。 | 不合并：一个管证据，一个管项目选择。 / Keep separate: evidence collection vs project decisions. |

### 主要矛盾 / Major contradictions and hazards

1. **自主性 vs 强制提问 / Autonomy vs compulsory questioning**：`product-requirements` 的 90 分门槛与禁止假设最严重；现代规则应是先检查上下文，只问实质性阻塞问题。 / Inspect context first and ask only materially blocking questions.
2. **自动写文件 vs 用户意图 / Automatic writes vs user intent**：artifact 位置必须跟随请求和 repo 约定。 / Artifact location must follow the request and repository conventions.
3. **语言覆盖 / Language override**：Skill 不应无条件强制中文或规定隐藏思维语言。 / Skills should not override response language or prescribe hidden reasoning language.
4. **不存在的工具与依赖 / Missing tools and dependencies**：`AskUserQuestion`、抽象 connector token 和 roadmap 的相对 Skill 引用不可靠。 / Tool and dependency references must map to real, stable interfaces.
5. **固定流程 / Fixed process**：固定天数、参与者和 epic 数量不能适应不同团队。 / Fixed days, participants, and epic counts do not generalize.
6. **热度不等于安全 / Popularity is not safety**：stars、installs 和作者名只能作为弱信号。 / Stars, installs, and publisher names are weak signals only.
7. **重复安全 / Duplicated safety**：通用 git 安全交给 system；Skill 只保留提交特定约定。 / Let system policy own generic git safety.
8. **绝对框架建议 / Absolute framework advice**：性能和库偏好必须先看版本、profiling 和项目约定。 / Performance and library preferences require version, profiling, and project context.
9. **陈旧引语 / Aging quote corpora**：当前市场事实必须查当前一手来源，不能依靠旧访谈名言。 / Current market facts require current primary sources, not old interview aphorisms.

## Tier 排名 / Tier ranking

### Tier S — 必不可少 / Essential

- `anki-cards`
- `docs-maintainer`（精简后 / after slimming）
- `gather-code-references`
- `derive-project-plan`

这些 Skill 包含本地工具、项目事实或稳定证据管线，模型无法可靠重建。  
These encode local tooling, project facts, or a stable evidence pipeline that the model cannot reliably reconstruct.

### Tier A — 有价值 / Valuable

- `customer-research`（合并后 / merged）
- `competitive-analysis`
- `marketplace-liquidity`
- `measuring-product-market-fit`
- `positioning-messaging`
- `startup-pressure-test`
- `git-commit`
- `vercel-react-best-practices`
- `vercel-react-native-skills`
- `web-design-guidelines`
- `write-spec` → `product-spec`

### Tier B — 可选 / Optional

- `find-skills`
- `user-research`（合并前 / until merged）
- `research-synthesis`（合并前 / until merged）

### Tier C — 遗留 / Legacy

- `roadmap-planning`

### Tier D — 删除 / Remove

- `product-requirements`

## 理想现代 Skill 集 / Ideal modern Skill set

建议从 20 个缩减为以下 14–16 个：  
Reduce the 20 packages to the following 14–16 active Skills:

1. `anki-cards` — 本地集成 / local integration
2. `gather-code-references` — 证据收集 / evidence collection
3. `derive-project-plan` — 参考到项目决策 / references to project decisions
4. `docs-maintainer` — 精简 router + 按需 references / lean router + on-demand references
5. `customer-research` — 合并 plan/gather/synthesize / merged research paths
6. `competitive-analysis` — 紧凑竞争框架 / compact competition framework
7. `marketplace-liquidity` — 市场诊断 / marketplace diagnosis
8. `measuring-product-market-fit` — 分群证据矩阵 / segment evidence matrix
9. `positioning-messaging` — 证据支持的定位 / evidence-backed positioning
10. `startup-pressure-test` — 自适应深度压力测试 / adaptive pressure test
11. `product-spec` — 替代两个 PRD Skill / replacement for both PRD Skills
12. `product-planning` — 可选微型路线图 Skill / optional tiny roadmap Skill
13. `git-commit` — shell-neutral 提交约定 / shell-neutral commit convention
14. `vercel-react-best-practices` — router + granular rules
15. `vercel-react-native-skills` — router + conditional granular rules
16. `web-design-guidelines` — 实时规则 adapter / live-rule adapter

若追求最小集合，可省略 `find-skills` 与 `product-planning`，保持 **14 个 active Skills**。  
For maximum minimalism, omit `find-skills` and `product-planning`, leaving **14 active Skills**.

## GPT-5.6 Skill 编写原则 / Modern authoring rules

1. 触发条件只放 frontmatter，不在正文重复。 / Put trigger conditions only in frontmatter.
2. `SKILL.md` 主要做 router 和强约束，通常控制在 500–700 词内。 / Keep the body as a router and constraint set, usually under 500–700 words.
3. 详细框架和示例移入一层 references，按需加载。 / Move detailed frameworks and examples to one-level-deep, on-demand references.
4. 不要同时发布 granular files 和完整 compiled duplicate。 / Never ship granular sources alongside a full compiled duplicate.
5. 只保留模型无法安全推断的内容：本地 schema、API、项目约定、证据标准、版本陷阱、脆弱流程。 / Preserve only non-inferable schemas, APIs, conventions, evidence standards, version pitfalls, and fragile procedures.
6. 用自适应规则替代强制规划/提问/复查循环。 / Replace mandatory planning/question/review loops with adaptive behavior.
7. 删除 persona theater、`think step by step`、任意评分、表扬脚本和固定质量门槛。 / Remove persona theater, step-by-step prompting, arbitrary scores, praise scripts, and fixed gates.
8. 研究与策略输出区分观察、推断、假设和建议。 / Separate observation, inference, assumption, and recommendation.
9. 对竞争者、版本、API、法规和指标等不稳定事实使用当前一手来源。 / Verify unstable claims from current primary sources.
10. 外部写入和全局安装需要明确确认；其他通用安全不必在每个 Skill 重复。 / Confirm external writes and global installs; avoid duplicating generic safety elsewhere.

## 推荐迁移顺序 / Recommended migration order

1. 删除 `product-requirements`，把少量有效风险/依赖内容并入 `product-spec`。  
   Delete `product-requirements`; move its small useful risk/dependency subset into `product-spec`.
2. 合并三个研究 Skill。  
   Merge the three research Skills.
3. 归档 `roadmap-planning`；只有真实使用频率足够时才建简短替代。  
   Archive `roadmap-planning`; create a short replacement only if usage justifies it.
4. 删除两个 Vercel Skill 的 compiled `AGENTS.md`/README 重复。  
   Remove compiled manual/README duplication from both Vercel Skills.
5. 精简三个引语密集的产品 Skill。  
   Slim the three quote-heavy product Skills.
6. 通过 progressive disclosure 精简 `docs-maintainer`。  
   Slim `docs-maintainer` through progressive disclosure.
7. 让 `git-commit` shell-neutral，并缩窄 `find-skills` 的触发。  
   Make `git-commit` shell-neutral and narrow `find-skills` triggers.

此顺序先消除行为冲突，再减少 token 和存储成本，同时保留真正差异化的能力。  
This order removes behavioral conflicts first, then reduces token and storage cost while preserving genuinely differentiated capability.
