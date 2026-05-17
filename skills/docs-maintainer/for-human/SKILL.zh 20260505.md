# AI 时代项目文档结构模板（中文人类阅读版）

这个文件是 `docs-maintainer/SKILL.md` 的等价中文版本，只供人类阅读，因此放在 `for-human/` 目录下。真正给 AI Agent 执行的技能说明以英文 `SKILL.md` 为准。

## 目标

这套文档体系的第一读者是 AI 编程 Agent，而不只是人类开发者。它要让项目事实可发现、可链接、可验证、可维护，并尽量减少 Agent 依赖猜测。

## 工作方式

1. 先检查仓库结构、现有文档、API 契约、部署文件、测试和最近变更。
2. 找出事实源：源码、Schema、测试、ADR、部署配置、API 规范、Runbook、产品词汇表。
3. 从下面的模板中创建最小可维护结构，不要盲目生成空目录。
4. 文档要便于 Agent 读取：标题清楚、段落短、链接明确、owner 明确。
5. 易变的实现细节尽量留在代码和 Schema 附近，文档用链接指向事实源。
6. 每次代码或架构变更，只更新受影响的文档；重大技术选择写 ADR。
7. 用 Markdown lint、链接检查、拼写检查、OpenAPI/AsyncAPI 校验、图表渲染或项目 CI 验证文档。

## 带注释的目录结构

下面是默认目标结构。注释用于解释每一项，实际文件名和目录名里不要包含这些注释。

## C4 第 3 层组件视图规则

`architecture/c4/03-components/` 应从项目真实的 C4 第 2 层容器和模块边界推导出来。它是 C4 第 3 层组件视图区，不是固定文件清单。

- 小型或中型项目优先用 `03-components/README.md`，按真实容器或组件组分节。
- 只有当某个真实容器或组件组足够复杂、需要独立维护时，才拆成单独文件。
- 文件名应来自项目真实架构，例如 `web-api.md`、`mobile-app.md`、`admin-console.md`、`orchard-modules.md`、`checkout-service.md`、`background-jobs.md`、`integration-adapters.md`、`ml-pipeline.md`。
- 不要因为示例里出现过 `backend-api.md`、`worker.md`、`frontend-app.md` 就创建这些文件；只有它们确实是当前项目准确、有用的组件视图时才创建。
- 不存在的组件视图应直接省略。例如纯客户端项目不应有空的 `worker.md`，纯后端服务也不应有占位的前端组件文档。

```text
docs/                                      # 长期项目文档根目录
  index.md                                # 文档入口：项目是什么，以及不同读者或 Agent 从哪里开始
  doc-map.md                              # 问题到文档的索引，帮助人和 AI 快速检索
  ownership.md                            # 文档 owner、更新频率、事实源、过期检查规则

  product/                                # 产品和领域知识：系统为什么存在、服务谁
    vision.md                             # 产品目标、边界、非目标、成功标准
    users.md                              # 用户角色、权限、核心任务、重要流程
    requirements/                         # PRD、用户故事、验收标准、范围变更
      README.md                           # 需求索引，链接当前有效需求和历史需求
    glossary.md                           # 领域词汇表，统一人、代码、测试和 AI Agent 的语言

  architecture/                           # 架构知识：系统如何组织、受哪些约束
    overview.md                           # 架构总览：主要模块、依赖、设计原则
    c4/                                   # C4 视图：从系统边界逐层到必要的代码级结构
      01-system-context.md                # C4 第 1 层：用户、外部系统、系统边界、信任边界
      02-container.md                     # C4 第 2 层：应用、服务、数据库、队列、Worker、第三方容器
      03-components/                      # C4 第 3 层：按项目实际容器和模块拆分的组件视图
        README.md                         # 紧凑组件视图索引，按真实容器或组件组分节
        project-specific-component.md     # 可选独立组件视图，文件名来自真实容器或模块，而不是模板标签
      04-code/                            # C4 第 4 层：只记录确实需要解释的复杂代码结构
        core-domain.md                    # 核心领域代码：状态机、算法、插件模型、不变量
      dynamic/                            # 动态视图：时序、状态变化、跨边界流程
        login-flow.md                     # 登录流程：认证、会话、错误路径、安全边界
        order-lifecycle.md                # 业务生命周期：从创建到完成或取消的关键状态
      deployment.md                       # 部署视图：环境、网络、配置、发布拓扑
    adr/                                  # 架构决策记录，解释为什么做出某个重要选择
      0001-record-architecture-decisions.md # ADR 示例或模板：状态、背景、决策、备选、后果
    data-model.md                         # 数据模型：实体、关系、约束、迁移、数据归属
    security.md                           # 安全设计：认证、授权、密钥、数据保护、威胁模型
    quality-attributes.md                 # 质量属性：性能、可靠性、可观测性、合规、可维护性

  engineering/                            # 工程实践：开发者如何安全修改和交付系统
    setup.md                              # 本地启动：依赖、环境变量、初始化、常见错误
    repo-map.md                           # 代码地图：目录职责、模块边界、主要入口文件
    conventions.md                        # 工程约定：命名、分层、错误处理、日志、提交规范
    testing.md                            # 测试策略：单测、集成、端到端、夹具、覆盖边界
    debugging.md                          # 调试指南：日志、追踪、常用命令、排障路径
    release.md                            # 发布流程：版本、构建、审批、部署、验证
    migrations.md                         # 迁移指南：数据库、配置、数据修复、回滚注意事项

  api/                                    # 接口契约，尽量机器可读
    openapi.yaml                          # REST API 契约：路径、请求、响应、错误、示例
    asyncapi.yaml                         # 事件或消息契约：通道、payload、生产者、消费者
    auth.md                               # 认证与授权：Token、Scope、角色、权限
    errors.md                             # 错误模型：错误码、语义、重试行为、用户提示
    examples.md                           # 集成示例：真实请求、响应、边界情况

  operations/                             # 运行维护知识，保障线上可恢复、可解释
    runbooks/                             # 操作手册：告警、事故、人工任务的步骤
      README.md                           # Runbook 索引，按告警、服务或场景组织
    incidents/                            # 事故记录：时间线、影响、根因、修复、预防措施
      README.md                           # 事故索引，按日期、系统、严重程度组织
    monitoring.md                         # 指标、日志、追踪、仪表盘、告警阈值
    rollback.md                           # 回滚指南：应用、数据、配置、回滚后验证

  ai/                                     # AI Agent 上下文，帮助模型可靠理解和修改项目
    AGENTS.md                             # Agent 工作规则：流程、禁止事项、测试要求、Review 期望
    context-map.md                        # Agent 首读地图：重要文件、模块边界、事实源
    facts.md                              # 稳定事实，Agent 可以可靠引用，不必每次重新推导
    gotchas.md                            # 常见坑、隐藏约束、Agent 容易重复犯的错误
    prompts/                              # 可选：给人、CI、自动化 Agent 复用的任务提示词
      doc-audit.md                        # 文档审计提示词：检查过期、缺失、重复、不一致
      adr-writer.md                       # ADR 写作提示词：把技术选择整理成决策记录
      release-notes.md                    # 发布说明提示词：从 diff、issue、PR 生成变更摘要
    evals/                                # 文档评测：测试 Agent 能否正确回答项目问题
      doc-freshness.md                    # 新鲜度评测：检查文档是否匹配代码、配置、API、测试
      api-doc-consistency.md              # API 一致性评测：检查示例、契约、实现是否一致
    llms.txt                              # 可选的 LLM 入口文件，提供精选链接和推荐阅读顺序

  changelog.md                            # 面向用户的变化、迁移提醒、破坏性变更、发布说明
```

## Diataxis 的位置

不要把顶层文档结构强行改成 Diataxis 的四个目录。对 AI 来说，按领域和事实源组织通常更好，因为 Agent 更常问：“API 契约在哪里？”“架构决策在哪里？”“Runbook 在哪里？”

Diataxis 更适合作为文档意图层：

```text
Tutorial     # 教程：新人学习路径或入门流程
How-to       # 操作指南：为了完成某个明确任务的步骤
Reference    # 参考：精确事实、Schema、命令、选项、契约
Explanation  # 解释：背景、取舍、概念、为什么这么做
```

可以在 `docs/doc-map.md` 或重要文档顶部标注：

```text
Intent: Reference
Audience: AI agents, backend engineers
Facts of record: openapi.yaml, src/routes/, integration tests
Staleness trigger: any API route, schema, or auth behavior change
```

Diataxis 适合 AI，因为它告诉 Agent 应该如何读取文档：How-to 应该按步骤执行，Reference 应该当成事实查询，Explanation 应该辅助推理但不能覆盖代码或 Schema。

但 Diataxis 本身不够。AI 时代的文档还需要事实源、owner、检索地图、变更影响规则和评测。

## `docs/ai/prompts/` 的作用

`docs/ai/prompts/` 是可选目录。它不是事实源，不应该放项目真相。

它用于保存可复用的任务提示词，供人、CI、定时任务或文档 Agent 反复运行。例如：

- 大 PR 后审计文档是否需要更新。
- 根据技术决策生成 ADR 草稿。
- 根据合并的 PR 生成发布说明。
- 检查 API 示例是否仍匹配契约。
- 让 Agent 刷新 `docs/ai/context-map.md`。

如果项目已经有更成熟的自动化系统，可以把它改名为 `docs/ai/tasks/`、`docs/ai/workflows/`，或者直接删除。只有这些提示词真的会被复用时，才保留这个目录。

## 维护规则

审查变更时使用下面的影响矩阵：

```text
公共 API 改动        -> 更新 docs/api/openapi.yaml、docs/api/examples.md、docs/changelog.md
事件/消息改动        -> 更新 docs/api/asyncapi.yaml、消费者说明、相关 Runbook
架构边界改动         -> 更新 docs/architecture/c4/02-container.md 或 03-components/，必要时新增 ADR
核心技术选择改动     -> 新增 docs/architecture/adr/NNNN-title.md
数据模型改动         -> 更新 docs/architecture/data-model.md、docs/engineering/migrations.md
部署/配置改动        -> 更新 docs/architecture/deployment.md、docs/engineering/setup.md、回滚文档
测试策略改动         -> 更新 docs/engineering/testing.md
告警/事故改动        -> 更新 docs/operations/runbooks/ 或 docs/operations/incidents/
AI 反复犯错          -> 更新 docs/ai/AGENTS.md、docs/ai/context-map.md 或 docs/ai/gotchas.md
```

## Agent 文档原则

- 把代码、Schema、测试、部署文件、ADR 当作事实源。
- 让 `docs/doc-map.md` 和 `docs/ai/context-map.md` 短、准、链接清楚。
- C4 第 1 层和第 2 层要稳定维护。
- C4 第 3 层用于复杂容器，并应从真实 C4 第 2 层容器和模块边界推导；第 4 层只用于难以就地理解的复杂代码。
- ADR 用来记录重要决策，不记录普通实现细节。
- API 和事件优先使用机器可读契约。
- 不要在很多文档里重复启动命令、环境变量、API 示例。
- 如果项目里存在多个 Agent 指令文件，要明确一个规范来源，并有意地链接或同步。
- `03-components/` 下的文件名应是项目特定的，不要保留与真实系统不匹配的占位组件文件。

## 可复用任务提示词

这些提示词可以放在 `docs/ai/prompts/`，也可以作为自动化任务使用。

```text
Review the current git diff and identify documentation impact.
Output affected docs, reasons, proposed updates, whether an ADR is needed, and whether API contracts, runbooks, changelog, or agent rules must change.
Do not edit files yet; provide the plan first.
```

```text
Generate or refresh docs/ai/context-map.md from the repository.
Include first-read files, module boundaries, facts of record, common traps, areas where agents must not guess, and docs that must be updated after code changes.
```

```text
Draft an ADR for the following technical decision.
Include Status, Context, Decision, Alternatives, Consequences, Migration, and Follow-up.
Explain why the decision was made; do not repeat low-level implementation details.
```

```text
Review docs/ using Diataxis.
Classify existing documents as Tutorial, How-to, Reference, or Explanation.
Report duplicated, missing, stale, or misplaced documents and propose a migration plan.
```

```text
Check whether documentation matches the codebase.
Focus on setup commands, environment variables, API examples, config options, directory descriptions, and test commands.
Output mismatches, evidence locations, and recommended fixes.
```
