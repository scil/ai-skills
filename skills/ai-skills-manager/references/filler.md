# Filler in a SKILL.md — four kinds, one disposition each

A sentence in a skill body is paid for on every trigger. It earns that if it changes what the agent does: a rule, a step, a done-criterion, a hand-off, a definition on first use. Everything else is filler, and it survives reviews because each kind looks reasonable on its own. The instance this file was harvested from: fourteen skills reviewed on 2026-09-16, thirteen carried at least one kind ([`../readme.md`](../readme.md)).

## The four kinds

| Kind | What it looks like | Disposition |
|---|---|---|
| **Self-description** — text about the file, not for the reader | "**Scope.** This skill owns X, covers Y, Z…"; "this skill encodes…"; "the lesson this skill was born from…"; "since 2026-09-15"; "owned by the sibling skill since…"; "Origin, and what was kept or rejected from…" | Ownership → one **Hand-offs:** line under the H1, naming only where work this skill does not own is sent. Story → `readme.md`, with the date. Dates in prose → deleted (git and `sources.md` `last-refresh` are the freshness signals). Coverage lists → deleted; the headings are the table of contents. |
| **Justification beside a rule that stands alone** | "A recent change took nine rounds…"; "Measured, and the reason this section exists: 22 rounds, ~45 findings…"; "63k / 73k / 238k tokens"; "Test runs are expensive; most fixes need…" under a heading that already says it; "A perfect dashboard with a transactional thank-you screen fails" after a rule that said which pages come first | One line per incident in `readme.md`. The rule keeps at most a parenthetical (`(Incident: the list row)`) or one number that sets a threshold ("roughly 3× per step up"). |
| **The same content twice in one file** | A closing "References" / "Reference files" list when every file is already linked at its step; an "Anti-patterns" table whose rows restate the rules above it; "When this skill applies" restating the description; "Why this skill exists" whose one useful sentence is already in the intro; a rule stated at three steps (an audio flag at "Defaults", "Two ways", and step 7); a "Usage sketch" restating the tooling table; a per-section pointer to a reference the intro already lists | Keep the copy at the step that uses it; delete the others. A reference that would lose its only link gets an inline pointer where it is used. |
| **A project, machine or product name in a shared skill** | A repo's gate command (`pnpm -F @org/pkg …`) and doc names; "this machine's `~/.codex/config.toml`"; a user's shorthand ("sol" = model X); a product's vocabulary inside an incident ("owner shelf row", a named function) | Stack- or tool-generic mechanics → `references/<stack-or-tool>.md`, keyed by the body section they serve (`react-web.md`, `openspec.md`). Project bindings (paths, commands, spec locations) → that project's own instruction file, never the shared skill. User shorthand → the user's own instruction file or memory. Incidents → re-told in neutral terms ("the one function that inserts the record"). |

## What is not filler

- `Instance:` lines and `(Incident: …)` pointers — they tell the reader where to look when the one-sentence rule does not land.
- A definition on first use of a term the reader may not have.
- "Work the phases in order", "done when …" — instructions.
- One number that sets a threshold or a budget.
- A `readme.md`: it is where the stories go, and a human reading the repo finds it in one click.

## Detector

Hits are candidates for the review table, not findings — a date inside a command block or a name inside a neutral example is fine. Pass the names that must not appear in a shared skill with `-Names`.

```powershell
param([string]$Skill = 'skills/<name>', [string[]]$Names = @())
$body = Get-Content "$Skill/SKILL.md"
$kinds = [ordered]@{
  'self-description' = '(?i)\bthis skill\b|^\*\*Scope\.\*\*|\bOrigin\b|\bborn\b|\bsince 20\d\d|\b20\d\d-\d\d-\d\d\b|\bowned by\b|reason this (section|file) exists|\bencodes\b'
  'justification'    = '(?i)\bMeasured\b|\b(\d+|two|three|four|five|six|seven|eight|nine|ten) rounds\b|\b\d+k\b|\btook (\d+|two|three|four|five|six|seven|eight|nine|ten)\b|\bis expensive\b|\bthe reason\b'
  'duplicate-section'= '^## (References|Reference files|Anti-patterns|When this skill applies|Why this skill exists|Usage sketch)\b'
  'machine-or-user'  = '[A-Za-z]:\\|~/\.|\bthis machine\b|\$env:|pnpm -F @'
}
if ($Names.Count) { $kinds['project-name'] = ($Names | ForEach-Object { [regex]::Escape($_) }) -join '|' }
for ($i = 0; $i -lt $body.Count; $i++) {
  foreach ($k in $kinds.Keys) { if ($body[$i] -match $kinds[$k]) { '{0,-18} L{1,-4} {2}' -f $k, ($i + 1), $body[$i].Trim() } }
}
# Links that appear more than once — usually a closing list duplicating inline pointers
[regex]::Matches(($body -join "`n"), '\]\(([^)#]+)\)') | ForEach-Object { $_.Groups[1].Value } |
  Group-Object | Where-Object Count -gt 1 | ForEach-Object { 'duplicate-link      x{0,-3} {1}' -f $_.Count, $_.Name }
```

Then, for every hit that is a finding, one row in the review report with its disposition from the table above; the reduction is reported as the landed word count, never as a target hit.
