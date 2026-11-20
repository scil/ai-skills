# Obsidian Vault Ops(中文说明)

给 AI 用的技能:在 Obsidian 仓库里写笔记、整理笔记。
本文是给人读的摘要;AI 实际读的是同级目录的 `SKILL.md` 和 `references/`。

## 控制台不在这里了

2026-11-20 起,Obsidian 控制台(点按钮跑项目命令的笔记)退役,所有项目的控制台都在 Logseq 里。
怎么设计按钮、写 runner、写卡片,见 `logseq-ops` 技能(`references/console-design.md`、`references/runner-scripts.md`)。
runner 文件名 `scripts\win\run_for_obsidian_console.ps1` 保持不变。

## 三条铁律

1. **每次重新定位仓库路径。** 用户会重组目录(项目文件夹、改名),记忆里的路径会写错地方。
   定位办法是**问 Obsidian 自己**,而不是满硬盘搜:`%APPDATA%\obsidian\obsidian.json`
   (mac 在 `~/Library/Application Support/obsidian/`,Linux 在 `~/.config/obsidian/`)
   里记着所有开过的 vault 路径,还标了哪个是**当前打开的那个**。
2. **写插件配置(`.obsidian/**/data.json`)前必须让用户完全退出 Obsidian。** 否则被内存里的设置覆盖。
3. **插件的配置格式从 `main.js` 里提取,不要猜。** 猜错会把插件配置写坏。

## 高价值的 Obsidian 写法

- **先定读者和用途**:读一次就去做事(runbook),还是反复读来学(入门笔记)?写错层次是最常见的失败。
- **可折叠 callout**(`> [!question]- 标题`)是长笔记里最有用的排版工具:自测题(问题露出、答案折叠)、速查表。
- **带锚点的双链**(`[[笔记#标题]]`)能精确指向解释,而不是甩一整篇文档过去。
- **加配套笔记时,两边都要加链接**,单向链接会烂掉。
- `file:///` 链接里的中文和空格**必须百分号编码**,否则点了没反应。
