# Maintaining the tree

Read this before you add or change a node or a binding. The classification is in [`taxonomy.md`](taxonomy.md). The incidents behind the nodes are in [`../readme.md`](../readme.md).

## Rules for a node

1. A node names one defect shape in general words: what the plan does, and how it fails. It has one shape sentence of 40 words or fewer and one `Suggest:` sentence of 25 words or fewer. Examples in parentheses illustrate and never narrow.
2. A node belongs to exactly one view and sits under one gate, whose pillar it shares. If it fits no gate, it is too narrow or belongs to one project.
3. Before adding a node, read its gate. If a node already covers the shape, widen its wording or add an example. Add a new node only when no wording can cover it.
4. A node goes under a parent only if it can occur only where the parent's surface exists. Otherwise it is a sibling.
5. A gate holds at most about six children. More children means a missing middle level: group them under a new parent.
6. No product, API or syntax appears in a node. Those go in a binding. No incident story appears in a node. That goes in the readme.
7. Numbers can be reassigned in a rebuild, which records the old-to-new mapping in the readme.

## Harvest a lesson

1. State the incident: what was planned, what went wrong, and which node, asked of the plan, raises it.
2. Decide the layer. A known shape in a technology whose binding does not yet say so (a default, an API, a limit) is a binding entry. A shape no node describes, in any technology, is a node. A fact true only of one project goes in that project's instructions, citing the node. Most incidents are bindings.
3. For a node, apply the rules above. For a binding, add or extend the entry under the node's number in `stacks/<technology>.md`, and create the file if the technology has none.
4. Tell the story once in the readme, dated. Never a new skill.

## Rules for a binding

- A binding file says how nodes show up in one technology layer (a database, a data client, a UI framework, a router, the platform, a language, a hosting shape) and the concrete fix there. Files are per layer, not per stack.
- A file opens with when to load it (what in a manifest or schema shows the technology) and the versions its defaults were checked against.
- Entries are keyed by node number, each with *shows up as*, *look for* and *fix*. Only nodes whose shape or fix differs in that technology get an entry.
- A binding never introduces a shape. If an entry describes a shape no node names, add the node first.
- A new file is written when a project on that technology is reviewed, not in advance.

## Validation

`evals/cases.md` holds fixed plans and what a review of each must and must not report. After a rebuild or a change to a gate, run every case in a session that did not write the change.
