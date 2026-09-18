# Batch: domain model — Rule 10

This batch is resolved first at merge. A concept the domain lacks cannot be guarded: the check cannot be written into a `WHERE` on a column that does not exist, and a lock on a wrong rule makes it wrong the same way every time. Its test is serialization: remove every overlap and run the flow single-threaded from the start — if the bug survives, the domain is wrong, not the interleaving, whatever tool was at hand when the bug was found.

## Rule 10 — A concept must exist before it can be guarded

An entity with several states answered with "is there a row"; a rule the spec states that no column can express; a write anyone can trigger that nothing bounds; a value derived from other rows when a column already holds it; a constraint removed without counting the paths it was blocking. Each is a missing or wrong concept, and each was first mistaken for a race because it surfaced in a concurrency test.

### Stack

Any store with a schema; the words are relational (column, unique index, enum) and translate to a document store as the field the documents carry and the validation rule or index that expresses it. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The spec states a rule over an entity: a cap, a holder, an owner, "at most one", "never again", "only while", "blocked", "removed", "expired".
- A query or a write filters on a status, or the entity has an enum, a `status` column or a lifecycle diagram.
- A path that needs no authorization — a public resolve, a scan, an anonymous submit, a webhook — inserts or updates rows.
- The plan derives a value from other rows or relationships ("the holder is whoever the live edge points at") rather than reading a column.
- The plan removes or relaxes a constraint: a write-once field becomes mutable, a unique index loses a column, a status condition is dropped.
- Two questions are answered from one piece of data ("who holds this card" and "which relationship this card can take back" both read the edge).

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A state ledger per entity the change touches.** One row per state the entity can be in, read from the enum or the column's values in the named schema file, not from the plan's memory; per query and per write in the plan, a column saying which states *count* for it — "alive", "any", "blocked too" — and the column that *is* the truth for each question the plan asks of the entity. A query with an empty "counts" cell, or two questions sharing a truth column, is visible as such. The ledger is a living intermediate (SKILL.md, "Project intermediates"): the project's `state-ledgers.md` holds each entity's states and the truth column of every question already asked of it, and the plan carries the delta — the states, questions or truth columns it adds or alters, each naming the file's row — or one line saying no row changes, checked against the file; the change's own queries' "counts" cells are delta rows.
- **A cap-owner table.** One row per write reachable without authorization: the path, the table it writes, the bound on how many rows it can create (a column, a unique index, a sweep), the owner of that bound, and whether the bound is instantaneous or self-healing. An empty bound cell is visible as such. The table lives in the project's `state-ledgers.md` beside the ledgers, and the plan carries the delta.
- **The field each rule needs.** Beside each rule the spec states over the entity: the column or index that expresses it, as file and line in the schema, or "missing — added by this change" with the migration named.
- **For a removed or relaxed constraint:** the list of every path that could produce the state the constraint forbade, found by grepping the named files' writers, each with what now stops it.

### Tell

- A rule the spec states with no column or index that can express it — the plan enforces it in prose, in a comment, or in an `if` that reads something else.
- "If a row exists" or "on conflict, use the existing row" on an entity whose state ledger has more than one state; a "counts" cell that says "any" for a query the spec scopes to alive rows, or "alive" for a query the spec says must also refuse removed ones.
- A cap-owner row with an empty bound cell; a public path that inserts and the plan's only caps govern a different action.
- A holder, owner or recipient computed from relationships while a column in the ledger holds it; two questions answered from one column with no sentence saying what each asks.
- A constraint removed with no path list, or a path list that stops at "only constructible by hand".
- The plan's mitigation for a bug found by a concurrency test is a lock, and the bug survives serialization.

### Write

- **Add the concept first, then talk about guards.** Give the row the column the rule needs (a provenance id, a `grant_limit` and `granted_count`, a status); only then does "the check must be in the write" (Rule 2) become writable.
- **Ask "is this row alive", never "is there a row".** After a uniqueness conflict, lock the row, read its state, and decide by the ledger's "counts" column; a request that can never be satisfied is refused, not readable.
- **Every write anyone can trigger has a bound and an owner.** Bound by what it did last (last shown, last touched), not by when the row was created, or an early arrival that just refreshed is the one swept; make the bound self-healing where the path is public (Rule 13 says why).
- **Read the column that is the truth; do not derive it.** When two questions share one piece of data, write down what each asks and give each its own source.
- **Before removing a constraint, enumerate the paths it blocked**, and for each say what now stops it; the most ordinary path (the create call with a plain parameter) is the one that is missed.

### Prove

- **One test per non-counting state**: seed the entity in each state the ledger says does not count for the query, run the query, assert it is ignored — and the reverse for the states that count.
- **The bound test**: at the bound, one more write from the public path; assert the excess is refused or swept, and that an early arrival which was recently shown is not the one swept.
- **The truth-column test**: change the derived relationships without changing the column, assert the answer follows the column.
- **One test per path in the removed-constraint list**, asserting the forbidden state is not produced there.
- **The serialization test is the classification's proof**: the test above runs single-threaded and fails before the fix; if it only fails under overlap, the incident belongs to db-concurrency, not here.

### View

- **Does the ledger match the schema?** Open the enum or the column in the named schema file; a state the schema has and the ledger omits is a finding against the ledger, before any finding against the design.
- **Which column expresses this rule?** If the answer is a comment, a helper's name or "the code checks it", the concept is missing.
- **Which states count for this query, and does the spec agree?** "Is there a row" is a finding on any entity with more than one state.
- **Who bounds this insert?** For each public path in the diff: the column, index or sweep, and its owner.
- **Is this value read or derived?** A holder, owner or recipient computed from edges, joins or counts while a column exists is a finding.
- **What did this constraint block?** For every dropped or relaxed constraint in the diff, the path list, and a test per path.
- **Does the bug survive serialization?** If the plan's mitigation is a lock or a conditional write and the answer is yes, the row is mis-filed: return it as a domain-model finding.
- **Is the missing state already in the type?** A state the type or the query result admits and a branch ignores is not a missing concept; it is Rule 23 (branch-completeness), and the row goes there as OUT-OF-BATCH.
