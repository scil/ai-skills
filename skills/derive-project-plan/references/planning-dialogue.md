# Planning Dialogue Guide

Use this guide to turn reference material into decisions.

## Question Order

1. Goal and success criteria:
   - What outcome should the project or change achieve?
   - How will the user know it worked?

2. Audience and operating context:
   - Who uses or maintains it?
   - Is the priority speed, maintainability, safety, cost, UX, scale, or learning?

3. Scope:
   - What must be included now?
   - What is explicitly out of scope?

4. Constraints:
   - Existing stack, versions, hosting, CI, data, compliance, timeline, budget, and team skill.

5. Tradeoffs from the reference collection:
   - Present concrete options from the resources.
   - Recommend one option and explain the source basis.

6. Rules and defaults:
   - Convert accepted choices into imperative project rules.
   - Mark assumptions when the user does not choose and the default is safe.

7. Acceptance:
   - Define tests, checks, manual scenarios, migration success, and rollback expectations.

## Decision Record Shape

Use this shape for important choices:

- Decision:
- Status: adopted | deferred | rejected | needs confirmation
- Basis: user preference | project constraint | reference | assumption
- Source mapping:
- Why:
- Consequences:
- Validation:

## Final Plan Shape

Keep the plan decision-complete:

- Summary.
- Goals and non-goals.
- Key architecture and project rules.
- Public interfaces, schemas, commands, or workflows affected.
- Implementation sequence.
- Edge cases and failure modes.
- Test and validation plan.
- Rollout, migration, compatibility, or monitoring notes when relevant.
- Assumptions and unresolved follow-ups.
