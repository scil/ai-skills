# codex-review — the incidents behind the rules

The rules in `SKILL.md` were measured on these; they are here so the body can state the rule without the story.

- **Nine rounds on a list-row change (2026-08).** Rounds 6–9 were all real defects round 1 never mentioned — the reason one pass is called a sample. Four consecutive rounds each reported a different dead click region, each patch creating the next: the "instance vs class" trap.
- **Twenty-two rounds, ~45 findings, on a confirmation flow (2026-09).** About 30 findings were one class (state describing the current user going stale) and two were defects no self-review would have found. The class traced to a decision made before any code — moving a "is this reader signed in" branch from server to client. Nine rounds of patching instances did not touch it. Hence the five-round budget and "review the design first".
- **Two `medium` rounds missed a tie.** "Newest write wins" compared timestamps with `>`; a same-millisecond tie kept the older write and resurrected a stale receipt. An `xhigh` round found it. Hence the starting-tier rule for risky surfaces.
- **Token cost across four rounds of one change:** 63k / 73k / 238k / 203k output tokens — roughly 3× per effort step.
- **A full-access sandbox committed the working tree unprompted**, emptying `--uncommitted` for the next round. Hence `sandbox_mode=read-only` and the post-run `git log` check.
- **An untracked, globally-ignored editor file was flagged in three separate rounds.** Hence "findings that are not yours".
- **A lint error and a typecheck error both reached codex** because the gate was piped through `| Select-Object -Last 5`. Hence "unfiltered".
