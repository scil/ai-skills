# Slimming a skill into a router plus references

Moved verbatim from `ai-docs-organizing/references/process.md` §9 on 2026-09-16; the instance it was harvested from is in that skill's `readme.md` (item 8) and summarized in [`../readme.md`](../readme.md).

1. **Land pending edits first.** `git status` the skill's directory; if someone else's uncommitted changes sit in the file, commit them as their own change before rewriting — the slim's diff must contain only the slim.
2. **Classify every section** as *step* (what the agent does, in order), *in-file reference* (rules consulted on demand by every path), or *disclosed reference* (needed by some paths only, or large). Only the first two stay in `SKILL.md`.
3. **Move disclosed blocks verbatim** into `references/<topic>.md`, one level deep, one topic per file (a structure tree; a diagramming rule set; a cross-cutting checklist plus the small rules that only apply on that path). Fold tiny standalone sections (a "framework rule", a "location rule") into the path that uses them as one sentence plus a pointer.
4. **Write the router**: a two-line purpose; principles — only the ones that change behaviour, each one paragraph; the split rule; the paths, each a numbered list of steps ending on a *done when …* line, the most common path first; a references-and-templates list. The description stays the trigger list; the body stops restating triggers.
5. **Apply the no-op test** sentence by sentence: delete what a current model does unprompted ("prefer clear headings"). The test is model-relative — settle a disagreement by running the skill, not by debate.
6. **Check every pointer** in the router and the references resolves (`Test-Path` each relative link); a moved section breaks the links that named it.
7. **Record the old-section → new-home map** in the change's design doc or, when there is none, in the commit message body, one line per section, naming any sentence deliberately dropped and why.
8. **Mark human mirrors** (`for-human/*.zh.md`) as lagging, in their own header, with the shape of the lag; do not retranslate as a side effect.
9. **Report the landed number honestly.** A 500–700-word target is a guideline; a router of 900 words in which every sentence is a rule, a step, or a done-criterion has met the goal, and a 600-word router that dropped a rule has not.

## Folding a fork back — the same move at the skill-set level

Folding a drifted project-local fork back into the shared skill is the same move at the skill-set level: generic rules and templates go up into the shared skill; the project's owners by name go into a project doc its agents read (an ownership map, pointed at from the contract); the fork is deleted; the shared skill is linked in through the ignore manifest. Every reference to the fork (hooks' reason text, in-flight change tasks) is updated in the same commit; archived history is left alone.

## Measuring, in the unit that matters

```powershell
$dir = 'skills/<name>'
$raw = Get-Content "$dir/SKILL.md" -Raw -Encoding utf8
"description chars: " + ([regex]::Match($raw, '(?m)^description:\s*(.*)$')).Groups[1].Value.Trim().Length
"body words:        " + (($raw -replace '(?s)^---.*?---', '') -split '\s+' | Where-Object { $_ }).Count
Get-ChildItem "$dir/references" -File | ForEach-Object { "{0,7} B  {1}" -f $_.Length, $_.Name }
Select-String -Path "$dir/SKILL.md", "$dir/references/*.md" -Pattern '\]\(([^)#]+)' -AllMatches |
  ForEach-Object { $f = $_.Path; $_.Matches | ForEach-Object { $p = Join-Path (Split-Path $f) $_.Groups[1].Value
    if (-not (Test-Path $p)) { "BROKEN  $f -> $($_.Groups[1].Value)" } } }
```

The description is measured in characters because that is what the harness shortens; the body in words because its budget is attention; the references in bytes because a Read tool reads the file, not the section.
