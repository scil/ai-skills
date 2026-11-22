# Classification standards

The question tree uses three published standards and one list made for this skill. This file records each one, its source, what it decides, and why it was chosen. Adopted on 2026-11-20.

## Axis 1: architecture view (picks the files)

Source: Philippe Kruchten, "The 4+1 View Model of Architecture", IEEE Software 12(6), 1995. It is the most cited split of a software architecture into views.

| prefix | 4+1 view | file | covers here |
|---|---|---|---|
| S | scenarios | `views/scenarios.md` | screens, client requests, routes, journeys |
| L | logical | `views/logical.md` | access rules, entities and states, constraints, decision rules, branches |
| P | process | `views/process.md` | concurrent writers, load, time, latency, calls with several effects, observations |
| D | development | `views/development.md` | parallel workers, tests and checks, new mechanisms, copies, dependencies |
| O | physical | `views/operations.md` | deletion, runs over many items, owner steps, outside content |

The physical view is named "operations" here, because its questions are about what runs and operates the system, not about hardware topology.

## Axis 2: defect class (groups the gates inside a file)

Source: MITRE CWE, view CWE-1000 "Research Concepts", its ten pillars. A pillar is the most abstract kind of weakness in CWE. The pillars cover correctness, security and maintainability, not security only. Checked against cwe.mitre.org on 2026-11-20.

| pillar | name | gates here |
|---|---|---|
| CWE-284 | Improper Access Control | L1 |
| CWE-435 | Improper Interaction Between Multiple Correctly-Behaving Entities | S7, D1 |
| CWE-664 | Improper Control of a Resource Through its Lifetime | S1, S2, L2, L3, P1, P2, P3, P4, O1 |
| CWE-682 | Incorrect Calculation | L4 |
| CWE-691 | Insufficient Control Flow Management | S3, S4, O2, O3 |
| CWE-693 | Protection Mechanism Failure | D2 |
| CWE-697 | Incorrect Comparison | S5, L5 |
| CWE-703 | Improper Check or Handling of Exceptional Conditions | S6, P5, P6 |
| CWE-707 | Improper Neutralization | O4 |
| CWE-710 | Improper Adherence to Coding Standards | D3, D4, D5 |

A gate carries one pillar, the one its children mostly share. In a file, gates are ordered by pillar number.

Alternative considered: IBM Orthogonal Defect Classification (ODC), defect types (Chillarege et al., IEEE TSE 18(11), 1992). ODC was built for design and code review and is smaller, but it has no class for access control or for duplicated code. One ODC idea is kept: its split between "missing" and "incorrect" maps onto the report's *unspecified* and *likely*.

## Axis 3: severity (orders "Most severe")

Source: ISO/IEC 25010:2023, the product quality model. Its nine characteristics are functional suitability, performance efficiency, compatibility, interaction capability, reliability, security, maintainability, flexibility and safety. The report ranks a failure by the characteristic it harms: safety and security first, then reliability and functional suitability, then the rest. The full text is paid. The names were confirmed only in part from public pages.

## Change kinds (adds gates whatever the view)

Change kind is a term coined for this skill: the kind of change a plan makes, which predicts gates that apply whatever the view. No accepted standard predicts this. The nearest is ISO/IEC/IEEE 14764, whose maintenance types (corrective, adaptive, perfective, preventive) say why a change is made, not which questions apply. The list and its gates are in the index of `SKILL.md`.

## The tree

Questions nest to any depth: gate, node, child, grandchild. A node's id is its parent's id plus a dotted number (`S1`, `S1.4`, `S1.4.1`). A child is placed under a node only if the child can occur only where the parent's surface exists. Then a reviewer who finds no surface for a node can skip its whole subtree. A guarded node does not skip its children.
