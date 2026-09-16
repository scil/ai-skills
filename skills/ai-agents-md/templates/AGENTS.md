# {{PROJECT_NAME}}

<!--
Maintainer notes (Claude Code strips block HTML comments before injection; Codex sends them — keep them short).
Every line below must pass the admission threshold in ai-agents-md/references/rules.md §1:
non-inferable · costly when wrong · repeated · team agreement · architecture boundary · verification requirement.
Delete any section that has no such line. Target: < 4 KB, < 80 lines at the root.
Growth loop: an agent fails → it repeats or is costly → hook/CI/lint if enforceable → one line here with Instance: and date.
Every PR: does this change retire a rule, change one, earn one?
-->

{{ONE_LINE_WHAT_THIS_REPO_IS_IF_NOT_OBVIOUS_FROM_README}}

## Boundaries

<!-- ≤ 6 lines. Only irreversible or costly actions. The real brake is the sandbox/approval config; these lines are the behavioural layer. -->

- MUST NOT commit secrets, tokens or credentials; `.env*` is gitignored and stays so. Enforced by: {{SECRET_SCAN_HOOK_OR_CI}}.
- MUST NOT edit {{GENERATED_DIRS}} by hand — regenerate with `{{REGENERATE_COMMAND}}`. Enforced by: {{CI_JOB_OR_advisory}}.
- MUST NOT modify a deployed migration under `{{MIGRATIONS_DIR}}`; schema changes add a new one. Enforced by: {{MIGRATION_CHECK_OR_advisory}}.
- MUST NOT {{EXTERNAL_IRREVERSIBLE_ACTION, e.g. create issues / PRs / releases}} unless the task says so. Enforced by: advisory.

## Commands

<!-- Only the non-obvious pick. The scripts block in the manifest is the truth; do not copy it. -->

- Package manager is `{{PM}}` (a second lockfile is a mistake, not a choice). Enforced by: {{preinstall check | advisory}}.
- {{ONE_NON_OBVIOUS_COMMAND_RULE, e.g. "`pnpm test -- <path>` filters by file; `--filter` selects a workspace"}}.

## Verification

<!-- Scoped done-criteria. Unconditional "run everything" raises cost because agents follow it. -->

- A change under `{{PATH_A}}` MUST pass `{{CMD_A}}` before it is reported done. Enforced by: CI job `{{JOB_A}}`.
- A change to {{KIND_B}} MUST include a regression test when the defect can be reproduced automatically. Enforced by: review.

## Architecture rules

<!-- Boundaries not encoded in code. Name the test or lint that enforces each, or tag advisory. -->

- {{LAYER_X}} MUST NOT import from {{LAYER_Y}}; access goes through `{{GATEWAY_PACKAGE}}`. Instance: {{INCIDENT_YYYY_MM_DD}}. Enforced by: {{ARCH_TEST_OR_advisory}}.

## Conventions that differ from defaults

<!-- Only what the formatter/linter cannot see. -->

- {{CONVENTION}}. Enforced by: {{LINT_RULE_OR_advisory}}.

## Known traps

<!-- The gotcha no config confesses. One line each, with the incident. -->

- {{TRAP}}. Instance: {{YYYY_MM_DD}}.

## Pointers

<!-- One line per doc the agent must read for a kind of question. Large doc → say how to read it. -->

- {{KIND_OF_QUESTION}}: `{{DOC_PATH}}` — read the map at the top, then the section, then the spec it names.

## Definition of done

<!-- Optional. Only if the team wants a fixed shape for the final report. -->

- The final message states what changed, which checks ran, and what remains open.
