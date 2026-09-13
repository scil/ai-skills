# AI Agent 项目文档系统

## 目的

使用这个技能来创建和维护以 AI 编程 Agent 为第一读者的项目文档。人类可读性仍然重要，但这套文档系统首先要让项目事实可发现、稳定、可链接，并且让 Agent 可以安全使用。

英文 `SKILL.md` 是 Agent 执行时读取的正式版本。这个中文文件只供人类阅读。

## 工作模式

根据任务选择对应路径。

### 新建文档

1. 检查仓库结构、源码、现有文档、API 契约、部署文件、测试和示例。
2. 如果这是本仓库第一次创建这套文档系统（还没有 `docs/` 目录），询问用户文档应该放在 in-repo `docs/` 目录，还是本机 Obsidian vault——只选一处存放，不要两边都建。如果用户选 vault，加载 `obsidian-vault-ops` 技能，把带注释的结构建在 vault 里而不是 `docs/`，并在仓库里留一条简短指针（例如写进仓库 `README.md` 或 `docs/ai.md`），记录 vault 名称和文件夹，方便之后的 Agent 找到它。如果用户选 `docs/`，或者 `docs/` 已存在，直接用 in-repo `docs/`，本次 session 内不再重复询问。
3. 识别事实源：源码、schema、测试、ADR、部署配置、API 规范、runbook 和产品词汇表。
4. 先用带注释的结构选择 owning node，再应用 File-First Split Rule。
5. 创建最小有用的文档结构。不要生成项目维护不起的空目录或大量薄文件。
6. 文档应稳定、便于 Agent 读取：标题清楚、段落短、链接明确、owner 明确。
7. 按下面的 Diagramming 规则，为架构、重点流程和难懂节点补充 PlantUML 图。
8. 用可用检查验证文档，例如 Markdown lint、链接检查、拼写检查、OpenAPI/AsyncAPI 校验、图表渲染或项目 CI。

### 更新文档

1. 检查代码或架构变更、受影响源码、现有文档、测试和最近 diff。
2. 从带注释结构里的 owning node 出发，只更新受影响文档。
3. 易变实现细节应靠近代码和 schema；文档用链接指向它们，不要在 prose docs 里复制。
4. 如果变更跨边界，同一次变更中更新所有受影响 owner。
5. 对重要架构、技术或策略决策写 ADR。
6. 如果架构边界、重点流程，或某个已画图的难懂节点发生变化，在同一次变更里更新对应 PlantUML 图；图过期和文字过期一样都算文档缺陷。
7. 用项目可用检查验证变更过的文档。

## File-First Split Rule

先用带注释结构选择 owning node，再决定该节点应该是 section、独立文件，还是目录。

默认每个文档主题使用一个 Markdown 文件。只有当主题很大、高风险、独立 owner、链接很多、机器可读、频繁 review，或容易造成真实编辑冲突时，才拆分。

拆分时，不要默认创建目录 `README.md`。目录结构和文件名本身就是有用索引。只有当导航确实有价值时，才把导航放在父主题文件、仓库 `README.md` 或 `docs/ai.md` 里。

## Agent 文档原则

- 把代码、schema、测试、部署文件和 ADR 当作事实源。
- 仓库 `README.md` 和 `docs/ai.md` 应短、准确、链接清楚；除非项目明确要求，不要创建单独的 index 或 context-map 文件。
- 保留一个规范 AI first-read list。默认把 AI first-read 链接、问题路由、Agent 运行规则和 gotchas 放在 `docs/ai.md`。
- `docs/ai/prompts/` 和 `docs/ai/evals/` 只放可复用任务资产。不要把项目事实、Agent 规则、first-read 路由或 gotchas 放进去。
- C4 L1 和 L2 应稳定、手动维护；C4 L3 用于复杂 container；C4 L4 只用于无法就地理解的代码结构。
- Future work 在 accepted 或 implemented 前，不要进入 current-fact docs。可选库、候选 provider、rollout 建议和 backlog notes 应放在 product requirements 或带明确 decision status 的 ADR 里。
- ADR 记录重要架构、技术或策略决策，不记录普通实现细节。
- API 和事件优先使用机器可读契约。
- 不要在多处 prose 文件里重复 setup 命令、环境变量和 API 示例。
- 项目文档之间使用普通相对 Markdown 链接；同文件标题使用 `#anchors`。
- 避免 root-relative 链接，例如 `/docs/architecture/config.md`，除非仓库已有约定。移动或重命名文档后要验证链接。
- 如果项目有多个 Agent 指令文件，保留一个规范来源，并有意链接或同步。
- 把带注释结构当作要保留的信息类别，而不是必须盲目创建的文件。偏好更少、更密、更有索引价值的文件，而不是很多薄 stub。
- 拆分后的 C4 component 文件名应是项目特定的。不要保留与真实系统不匹配的占位 component 文件。
- code locator 是人工维护的地图，不是生成式 inventory。它应帮助 Agent 选择从哪里开始，然后指回代码这个事实源。

## Diagramming（图表规则）

用 PlantUML 表达架构、重点流程和难懂节点。不要给简单直白的结构画图。

- 给 C4 架构文档（`c4-system-context`、`c4-container`、`c4-components`）配一张 PlantUML 图，展示 actor、container、component 及其边界，作为文字说明的补充，而不是替代。
- 给重要运行时流程（例如 `dynamic-login-flow` 及带注释结构里其它跨边界流程）配一张 PlantUML 时序图或活动图。
- 只有当结构确实是坑——复杂状态机、retry/rollback 路径、并发、跨多个服务的交接——才给 `code-locator` 或 `repo-map` 条目配图；不要给直白的调用链画图。
- 直接在 owning node 里用 ` ```plantuml ` 代码块写图，紧挨着它说明的文字；只有项目文档工具链要求外部图片文件时，才用链接的 `.puml` 文件。
- 每张图只聚焦一个边界、流程或 component group，保持小而集中；宁可拆成多张图，也不要画一张过密的图。
- 在把画图任务标记完成前，用项目可用的方式（PlantUML CLI、编辑器预览、CI 渲染步骤）验证图能正常渲染。
- 图要和它描绘的代码、边界或流程在同一次变更里一起更新。

## 带注释的结构

这是信息架构，不是必建文件树。把稳定项目事实路由到下面的 owning node；不要在 AI helper docs 中复制 product、architecture、API、testing、operations、repo-map 或 code-locator 事实。节点名故意省略 `.md`：每个节点可以是 section、独立文件，或按 File-First Split Rule 拆出的目录。注释说明 ownership 和更新触发条件；不要把注释写进实际名称。

```text
docs/                                      # 长期项目文档根
  product                                 # Owns 产品目标、用户、词汇、需求、边界和非目标；当产品行为、命名、UX 契约、已接受需求或未来范围变化时更新。
    requirements                          # Owns accepted、implemented、candidate、rejected 或 historical requirements，并带 Candidate、Proposed、Accepted、Rejected、Implemented 等 decision state labels；当范围、验收标准、UX 契约或 decision state 变化时更新。
    feature-roadmap                       # Owns 可选 candidate backlog/roadmap，并带 decision state labels、sources、trigger conditions、constraints 和 rollout order；当候选范围、decision state 或 rollout order 变化时更新。

  architecture                            # Owns 架构总览、C4 L1/L2、数据模型、配置摘要、安全摘要、部署摘要和质量属性；当边界、职责、状态模型、拓扑、主要流程或质量约束变化时更新。
    overview                              # Owns 主要模块、依赖、边界、职责拆分和设计原则；当架构边界或职责变化时更新。
    c4-system-context                     # Owns C4 L1 用户、外部系统、系统边界和信任边界，配一张 PlantUML 图；当 actor、外部系统或信任边界变化时更新。
    c4-container                          # Owns C4 L2 应用、服务、数据库、队列、worker 和第三方 container，配一张 PlantUML 图；当 container 或运行时拓扑变化时更新。
    c4-components                         # Owns 真实 container 或 component group 的 C4 L3 component view，配一张 PlantUML 图；当 component 边界、ownership 或重要交互变化时更新。
    data-model                            # Owns 实体、关系、约束、迁移、状态定义、enum 语义和数据 ownership；当 schema、状态、生命周期语义或数据字典条目变化时更新。
    config                                # Owns config roots、profiles、schema、path rules、examples、environment expansion、removed names 和 migrations；当 config 字段、profile 行为、路径、默认值或迁移变化时更新。
    security                              # Owns 认证、授权、密钥、数据保护、破坏性操作安全、权限和 threat model；当 safety、preview/confirmation、权限或 trust behavior 变化时更新。
    dynamic-login-flow                    # Owns 一个重要运行时序列、状态转换或跨边界流程，配一张 PlantUML 时序图或活动图；当该流程变化时更新。
    deployment                            # Owns 托管环境、网络、运行时拓扑、部署信任边界和生产布局；当部署拓扑或运行时架构变化时更新。
    adr                                   # Owns Architecture Decision Records；当出现重要架构、技术或策略决策时新增 ADR。
      0001-record-architecture-decisions

  engineering                             # Owns setup、repo map、约定、testing、debugging、release、migrations 和 code locator；当命令、workflow、build/package 布局、migration guidance、tests、repo structure 或 problem entry paths 变化时更新。
    setup                                 # Owns 本地 setup、依赖、环境变量、初始化、常见失败和本地运行时布局；当 install、run、debug、env 或本地路径行为变化时更新。
    testing                               # Owns 测试策略、检查命令、fixtures、覆盖边界和必需回归主题；当测试命令、覆盖预期或 fixture profile 变化时更新。
    release                               # Owns 版本、build/package 步骤、release 默认值、审批、部署交接和验证；当 packaging、release config 或 release verification 变化时更新。
    migrations                            # Owns 数据库、config、数据修复和 rollback migration guidance；当 schema、config 或数据迁移行为变化时更新。
    repo-map                              # Owns 系统地图：目录/模块职责、主要功能分布、入口点和 ownership；当 repo structure、module boundaries、feature locations 或 entry points 移动时更新。
    code-locator                          # Owns problem-to-file 入口索引和 change recipes，对真正难懂的节点配一张 PlantUML 图；解决 recurring 或 subtle problems 后，用涉及文件、invariants/traps 和 focused verification 更新。

  api                                     # Owns API contracts 和 direction rules；把方向相关的 auth、errors、examples、quotas 和 adapters 放在对应方向下；当 signatures、payloads、return types、errors、examples、events、webhooks 或 upstream contracts 变化时更新。
    command-api                           # Owns 可选本地 app command bridge；适用时加载 framework-specific rules，并当 command signatures、payloads、side effects 或 safety behavior 变化时更新。
    provided                              # Owns 本项目暴露给调用方的接口：HTTP routes、RPC methods、SDK methods、events、webhooks、plugin hooks、schemas 和 error contracts；事实源是 server routes/controllers、handlers、schemas、OpenAPI/AsyncAPI files、contract tests 和 implementation tests；当暴露的 routes、methods、SDKs、events、webhooks、schemas、errors、examples 或 compatibility behavior 变化时更新。
    consumed                              # Owns 本项目调用或依赖的上游接口：backend services、third-party APIs、SDKs、payment/auth/map/email providers、vendor webhooks 和 sibling services；事实源是 clients/adapters、上游官方文档、observed responses、fixtures、mocks 和 integration tests；当 upstream contracts、adapters、auth、quotas、mocks、fixtures 或 risks 变化时更新。
    openapi.yaml                          # Owns REST API 机器可读契约；当 REST paths、requests、responses、errors 和 examples 变化时更新。
    asyncapi.yaml                         # Owns event/message 机器可读契约；当 channels、payloads、producers、consumers 和 compatibility notes 变化时更新。

  operations                              # Owns monitoring、runbooks、incidents、rollback 和 recovery procedures；当 logging、alerting、rollback、manual repair、partial-failure 或 incident response 变化时更新。
    rollback                              # Owns application、data、config 和 post-rollback verification；当 recovery、undo、backup/restore 或 partial-failure repair behavior 变化时更新。
    monitoring                            # Owns metrics、logs、traces、dashboards、alerts 和 thresholds；当 observability、logging 或 alert behavior 变化时更新。
    runbook-alert-name                    # Owns 某个 alert 或 scenario 的 step-by-step operational procedure；当 manual action、escalation 或 verification 变化时更新。
    incident-YYYY-MM-DD-title             # Owns incident record：timeline、impact、root cause、fix 和 prevention；重要事故后新增。

  ai                                      # Owns Agent 规则、first-read map、question routing 和 gotchas；当 repeated AI mistakes、retrieval paths、guardrails 或 docs routing 变化时更新。
    prompts                               # 可选 reusable AI prompts；只在确实复用时保留。不是 facts-of-record 区域。
      doc-audit                           # Owns 可复用的人类/CI/Agent 文档审计 prompt；不得包含项目事实；当 audit 输出预期或 docs impact categories 变化时更新。
      adr-writer                          # Owns 可复用 ADR drafting prompt；不得包含项目事实；当 ADR 格式或决策 workflow 变化时更新。
    evals                                 # 可选 reusable documentation evals；只在确实复用时保留。不是 facts-of-record 区域。
      doc-freshness                       # Owns 用于检查 Agent 是否能从当前 docs 和 code 回答项目问题的 eval；当 questions、expected source docs 或 facts of record 变化时更新。

  ownership                               # Owns owners、update cadence、facts of record 和 stale-document review rules；当 ownership、review cadence 或 canonical fact sources 变化时更新。
  changelog                               # Owns 面向用户的 changes、migrations、breaking changes 和 release notes；发布、破坏性变更、迁移和用户可见行为变化时更新。
```

## Cross-Cutting Change Rule

从带注释结构中的 owning node 出发。如果变更跨边界，同一次变更中更新每个受影响 owner，而不是把同一事实复制到多处。

- API 行为变化可能影响 API docs、机器可读契约、示例、测试和 changelog entries。
- Config schema、profile、path 或 default 变化可能影响 architecture config docs、engineering setup/migration docs、examples 和 tests。
- 破坏性操作、permission、preview、confirmation 或 rollback 行为变化可能影响 architecture security docs、operations rollback docs、API safety notes 和 tests。
- Architecture boundary、runtime topology 或 responsibility 变化可能影响 architecture overview、C4 views、deployment 或 operations docs；如果决策重要，还要写 ADR。
- Local setup、build、packaging、release 或 test workflow 变化可能影响 engineering docs 和仓库 README。
- Framework-specific command 或 API bridge 变化必须先加载相关 rule file，例如 `rules/tauri-command-api.md`，再更新 API docs 和 wrappers。
- Future-work suggestions 在 accepted 或 implemented 前属于 product requirements 或 roadmap docs，并带 decision status；只把稳定结果事实提升到 current-fact docs。
- Repeated AI mistakes 或 retrieval failures 属于 `docs/ai.md`；重复的跨主题事实应移动到 owning docs，并从 helper prose 中删除。

## Repo Map And Code Locator Rule

当结构导航和 problem-first navigation 都有用时，保持二者分离。

`repo-map` 是系统地图。它帮助 Agent 在修改前理解代码库形状。

`code-locator` 是问题入口索引。它回答：遇到这个 issue 或 workflow，应先看哪里，什么 invariant 不能破，应该运行什么 focused check？

## Future Work Promotion Rule

Future work、backlog、optional providers、rollout advice 和 candidate ideas 在 accepted 或 implemented 前，不得进入 current-fact docs。

当 candidate 变成 accepted 或 implemented，只把稳定结果事实提升到 owning current-fact nodes。历史 candidate context 留在 `product/requirements`、`product/feature-roadmap` 或 ADR。

## Framework-Specific Rules

对于 Tauri desktop apps，在创建或更新 Tauri command API documentation 前，加载 `rules/tauri-command-api.md`。

## Obsidian Location Rule（存放位置规则）

只在第一次创建这套文档系统时问一次存放位置；之后的更新不要再问。

带注释的结构只存在一个地方：in-repo `docs/` 目录，或者通过 `obsidian-vault-ops` 技能选定的本机 Obsidian vault。不要两边都建，也不要在两边之间互相镜像——单一位置就是唯一事实源。选了 vault 时，把本技能的所有规则（带注释的结构、File-First Split Rule、Cross-Cutting Change Rule、Diagramming）都应用在 vault 文件夹里，取代 `docs/`；如果 vault 名称或文件夹之后移动了，记得同步更新仓库里的那条指针笔记。
