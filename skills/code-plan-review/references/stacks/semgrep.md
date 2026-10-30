# Binding: Semgrep (and other code scanners run by a plan)

How the catalog's questions show up when a plan runs Semgrep, or a scanner like it, and acts on its findings. Load this file when a plan or a CI job runs `semgrep scan` or keeps Semgrep rules. Checked against Semgrep 1.183.0 (2026-10).

Each entry: **shows up as** · **look for** · **fix**.

## K. A pipeline judges input

**K2.2 — "no findings" from a scan of no files.**
- *Shows up as:* a scan reports zero results with exit code 0 because it scanned nothing: run on `tests/fixtures/` inside a repository, Semgrep 1.183.0 scanned no file (its default ignores skip paths such as `tests/`). A clean-fixture test passes for the wrong reason, and a real audit of code kept under such a path reports it clean.
- *Look for:* a pass condition on `results` alone; fixtures or scanned code inside a checkout or under `tests/`, `vendor/` or similar paths.
- *Fix:* read `paths.scanned` (and `errors`) from the JSON report and treat zero scanned files as "error"; scan a copy outside any checkout; keep a vulnerable fixture per rule as the positive control, run in the same way as the real scan.
