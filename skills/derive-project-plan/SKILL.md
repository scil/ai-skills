---
name: derive-project-plan
disable-model-invocation: true
description: Use when Codex needs to turn a software reference collection, research corpus, architecture notes, or third-party resource reports into a project-specific development plan, implementation rules, architecture decisions, and acceptance criteria. Trigger after reference gathering, when the user asks to make a plan from references, derive project rules, choose between researched options, or adapt external patterns to a specific codebase without coding yet.
---

# Derive Project Plan

Use this skill to convert a gathered reference collection into project-specific choices. The goal is not to apply every good idea; it is to interrogate the reference material and the user until the plan and rules fit the actual project.

## Workflow

1. Load the reference collection:
   - Prefer a Markdown collection produced by `$gather-code-references`.
   - Identify resource dossiers, theme indexes, decision pools, candidate rules, and research gaps.
   - Do not redo external research unless the collection has a critical gap that blocks planning.

2. Inspect the local project:
   - Reconfirm repository facts that affect the plan: stack, versions, scripts, architecture, tests, deployment shape, and constraints.
   - Separate repository facts, reference-derived recommendations, user preferences, and assumptions.

3. Ask targeted questions before locking decisions:
   - Ask only questions that materially change the plan, confirm a meaningful tradeoff, or resolve a blocker.
   - Prefer concrete options grounded in the reference collection.
   - Continue until goal, success criteria, audience, scope, constraints, tradeoffs, acceptance criteria, and rollout expectations are clear.
   - Use `references/planning-dialogue.md` for the decision sequence.

4. Derive project choices:
   - Convert adoptable reference points into explicit project decisions.
   - Mark each important decision as adopted, deferred, rejected, or needs confirmation.
   - Preserve source mapping so the user can trace why a rule exists.
   - Trim overbuilt patterns even when they come from excellent resources.

5. Produce a decision-complete plan:
   - Include architecture and implementation approach.
   - Include public interfaces, schemas, files, commands, or workflows when they are affected.
   - Include data flow, failure modes, edge cases, migration or compatibility notes, and rollout concerns when relevant.
   - Include tests, validation commands, and acceptance scenarios.
   - Include project rules in imperative form when the output is meant to guide future coding.

## Output

Produce a concise but decision-complete Markdown plan or rules document. The implementer should not need to decide between unresolved options.

Every important rule or architectural choice should show its basis:

- `User preference`: explicitly stated by the user.
- `Project constraint`: discovered from the repo or environment.
- `Reference`: derived from one or more resource dossiers.
- `Assumption`: chosen because the user did not decide and a default was safe.

## Guardrails

- Do not mechanically copy external architectures into the project.
- Do not treat a reference collection as a mandate; it is evidence for choices.
- Do not leave high-impact tradeoffs unresolved.
- Do not code or edit project files unless the user asks for implementation after the plan.
- Do not hide weak evidence. Mark low-confidence recommendations clearly.

