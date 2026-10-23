# tiered-research — where this came from

A method skill for research whose output is verdicts and a source table. It was harvested on 2026-09-16 from a memory written the day before, at the user's request that the lesson live in a skill rather than in one agent's memory.
一个方法型 skill：产出是判断和来源表。2026-09-16 由前一天写的记忆迁入，用户要求经验放在 skill 而不是某个代理的记忆里。

## The incident (2026-09-15) / 事故

While building `ai-agents-md`, six critical verdicts were given on two chat transcripts about AGENTS.md / CLAUDE.md. A second, deeper pass at the user's request found two of the six wrong, both for the same reason: the wrong corpus.
建 `ai-agents-md` 时对两段对话下了六条批判性判断。用户要求深挖后发现两条错了，原因相同：查错了语料。

- "Avoid 'always double-check'" was called *not found* after searching the Claude Code documentation; it is stated in Anthropic's platform prompting docs for Opus 5 and Fable 5. / 查的是 Claude Code 文档，其实在平台 prompting 文档里。
- "OpenAI keeps AGENTS.md around 100 lines" was called *contradicted* by the ~550-line `openai/codex/AGENTS.md`; the claim came from OpenAI's Harness-engineering post about a different, internal repository. Both facts are true; the comparison object was wrong. / 拿 `openai/codex` 仓库去比，而原话说的是另一个内部仓库。

Two further findings shaped the method. The user said one ETH study was "not enough weight" and that the agent vendors' own documentation must be the first authority; when the sources were then tiered, the seven studies disagreed exactly along their scope lines and the two vendors agreed on everything but one item, so stating the disagreement was the honest result. And a "canonical" example file that several blogs recommended did not exist anywhere in the repository's 1,592-entry tree; one API call settled it.
另两点定型了方法：用户说单篇 ETH 研究分量不够、厂商官方文档必须是第一权威；分层之后，七篇研究恰在各自范围上分歧，两家厂商只有一处不同，陈述分歧才是诚实结果。多篇博客推荐的"典范"文件在仓库全树里根本不存在，一次 API 调用就查清。

## The rules each part became / 规则

1. Wrong corpus → *name the corpus before the verdict; widen only after it is exhausted.*
2. Wrong comparison object → *the verdict vocabulary has WRONG OBJECT and CONFLATED, not just "wrong".*
3. One study → *tiers: the owner's docs decide, research corroborates in pairs, exemplars illustrate, reports point.*
4. Studies "contradicting" → *record scope fields before findings; the scope difference is the finding.*
5. Blog-described exemplar → *verify the object directly.*
6. Circulating numbers → *pull splices apart; register each piece.*

## The IT-security harvest (2026-10-23) / IT 安全经验

A defence plan for a WordPress VPS was researched with this method by four parallel subagents. Its lessons went into `references/it-security.md`, at the user's request that they live in this skill as a separate, security-only file. The lessons were: severity differs between project, CNA and distro; a breach detail found only in the attacker's claims stayed "reported"; a "free" tool recommended from memory had ended its free licences 9 days earlier; `DISALLOW_FILE_MODS` silently disables auto-updates; Docker bypasses ufw; a security scanner was itself compromised; a practitioner's four principles had been used as the report's frame until the user asked for a recognised framework; and one subagent brief about offensive tools was stopped by a safety classifier, while a defender-only brief succeeded.
用本方法、四个并行子代理为一台 WordPress VPS 做了防御方案调研。按用户要求，经验单独放进 `references/it-security.md`，只管 IT 安全。经验包括：项目、CNA、发行版的严重性评级不同；只出现在攻击者说法里的入侵细节仍记为"报道"；凭记忆推荐的"免费"工具 9 天前已停发免费许可；`DISALLOW_FILE_MODS` 会悄悄关闭自动更新；Docker 会绕过 ufw；安全扫描器自身被投毒；报告一度以某位从业者的四条原则为框架，直到用户要求改用公认框架；一个询问攻击工具的子代理任务被安全分类器拦停，而只问防守信息的任务说明顺利完成。

## Boundaries / 边界

`gather-code-references` collects third-party coding resources for an implementation; `derive-project-plan` turns references into project decisions; `ai-agents-md` and `docs-maintainer` carry sources registries built with this method and share the checker script. This skill owns the judging and registering method only.
`gather-code-references` 为实现收集编码资源；`derive-project-plan` 把参考变成项目决策；`ai-agents-md` 与 `docs-maintainer` 的来源表用本方法建、共用检查脚本。本 skill 只管判断与登记方法。

## How to maintain / 怎么维护

Add a row to the corpus table in `references/verdict-protocol.md` §1 when a new wrong-corpus incident happens; add a scope field to `source-tiers.md` §2 when two studies disagree on a dimension not listed. Keep `SKILL.md` a router.
新的"查错语料"事故加进 `verdict-protocol.md` §1 的表；两篇研究在未列维度上分歧时，把该维度加进 `source-tiers.md` §2。`SKILL.md` 只做路由。
