# Sources

last-refresh: {{YYYY-MM-DD}}
gate-days: {{7 for fast-moving vendor topics · 30 for standards}}

Read by `ai-agents-md/scripts/check-sources.ps1 -Path <this file> [-GateDays N] [-Update]`. Rows ordered by tier; the tier is the first part of `kind`. Columns: `id` (stable key) · `kind` (`T1-vendor` · `T1-standard` · `T2-research` · `T3-exemplar` · `T4-report`) · `url` · `fingerprint` (`gh:<sha12>` GitHub file · `sha:<hex12>` page · `manual:<date>` site that blocks scripts · `-` not yet computed) · `checked` (when we fingerprinted it) · `purpose` (what is taken, **and what is not**) · `source-date` (what the source states: published, revised, version; GitHub rows get `commit <date>` from the script; a page with no date says `undated (living …)`).

| id | kind | url | fingerprint | checked | purpose | source-date |
|---|---|---|---|---|---|---|
| {{owner-docs}} | T1-vendor | {{url}} | - | - | {{Owner}}. {{what this skill takes from it; what it does not}} | undated (living vendor page) |
| {{standard}} | T1-standard | {{url}} | - | - | {{the standard's own statement used}} | {{version, date}} |
| {{paper-slug}} | T2-research | https://arxiv.org/abs/{{id}} | - | - | {{Authors, venue}}. Scope: {{models · languages · task type · input provenance · what measured}}. Finding: {{numbers}}. Limits: {{authors' words}}. Owner of: {{which rule it explains}} — or "one study; shapes no rule". | v1 {{date}}, rev. {{date}} |
| {{ex-repo}} | T3-exemplar | https://github.com/{{owner}}/{{repo}}/blob/{{branch}}/{{path}} | - | - | {{size, what pattern it shows}} | commit (filled by the script) |
| {{report}} | T4-report | {{url}} | - | - | {{who, what it points to; "reported" numbers named as such}} | {{date}} |
