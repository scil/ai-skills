# Batch: single source of truth — Rules 19, 20, 21

One truth, more than one copy. Every rule here fails single-threaded and single-user — its cause is how many copies exist, not who went first — so the serialization test that sends an incident to db-concurrency does not send it here. The three rules are one theme in three costumes: the same thing implemented twice (19), one rule enforced in several places (20), the value shown to the user and the value the write uses (21). The defence is the same each time: delete the second copy and make everyone read the only one; a condition, a sync step or an `if` added to keep two copies agreeing is maintenance on the second copy. The batch reads across layers by design — a promise is made in a component and kept in a `WHERE` — so its intermediates name files on both sides. The cache-shaped member of this family, server copy against client cache, lives in server-state-cache, Rule 3.

## Rule 19 — One policy, one place

Two implementations of one thing start drifting the day one of them is changed first, and the drift is found only when somebody happens to hold both outputs at once. No assertion fires on its own.

### Stack

Any. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The same value is rendered on two surfaces (an editor's preview and a landing page; a list row and a detail card; web and mobile).
- The same input is parsed, trimmed, normalized or validated on two sides (client and server; two endpoints; a form and an import).
- A UI package and an app both touch the same text, sentence or format.
- A prop, field or parameter is named for a *part* (`recipientName`, `amount`) and receives a *composed* value (a localized sentence, a formatted string).
- The plan says "mirror", "keep in sync", "the same logic as", or "also apply on the other side".

### Asks for

What the plan must carry for the Tells below to be checked by inspection rather than inferred from prose. A plan where a Where holds and one of these is missing is returned for it, not reviewed.

- **A site list per shared thing.** For each value rendered or parsed in more than one place: every site, found by grepping the named files' tree for the field, the schema or the render; the one owner (the component, the schema, the helper) as file and export; and each site's relation to the owner — *imports it* or *re-implements it*. A "re-implements" cell is visible as such. The list is a living intermediate (SKILL.md, "Project intermediates"): the project's `sites.md` holds every shared thing's sites, and the plan carries the delta — the sites it adds, removes or re-points, each naming the file's row — or one line saying no site changes, checked against the file; a new site of a thing the change did not otherwise touch is still a delta row.
- **The contract stated by the name.** For each prop, field or parameter that crosses a package boundary: what it holds in one phrase (a raw name; a whole localized sentence, bidi-isolated), and that the name says so.
- **Who does not touch what**, one line per package boundary the change crosses (for example: the UI package composes nothing localized; the app composes the sentence and passes it whole).

### Tell

- A site-list row that re-implements the owner; two renderers of one entity in two files; two `parse`/`trim`/`normalize` steps for one field on two sides.
- The client sends the raw value and the server normalizes it, so the client's own equality and dirty checks disagree with what was stored.
- A prop named for a part fed with a composed value, or a composed value assembled inside the package the boundary line says composes nothing.
- "Keep both in sync" as a mitigation anywhere in the plan.
- The plan compares outputs from two surfaces by eye rather than by one shared component or a contract test.

### Write

- **Share the one component**: two faces of one thing are painted by one component, with the differences as props.
- **Share the one schema**: the client runs the same parse the server runs — the shared validator's `safeParse` — and sends the *normalized* value, so every check on both sides reads the same value.
- **Let the name state the contract**: a prop that carries a whole sentence is named for a sentence; with the right name, putting the wrong thing in becomes conspicuous.
- **Write down who does not touch what**: one line per boundary, in the plan and at the boundary in code.
- **"Change both sides" is not a defence**; it postpones the next drift to the next change.

### Prove

- **A contract test across the sites**: one input, both surfaces or both parsers, assert identical output; this is the assertion that goes red when one side changes alone.
- **The normalized-value test**: submit a value that differs from the stored one only by what normalization removes; assert the client reports nothing to save and the server writes nothing.
- **Where no unit test can hold both** (visual output), a visual-diff assertion: render both surfaces from one input under the test runner and assert the two screenshots match — the assertion that goes red when one surface changes alone. A side-by-side pair pasted into the review by hand is evidence for the reviewer, not a proof (Principle 6): nothing turns red the next time one side moves.

### View

- **Does the site list match the tree?** Grep for the field, schema or renderer; a site grep finds that the list omits is a finding against the list, before any finding against the design.
- **Which single file owns this rendering / this parse, and does every site import it?**
- **What does this prop's name promise, and what is passed?**
- **Is any "sync" step in the diff a second copy being maintained?** If so, which copy is deleted instead?

## Rule 20 — A rule lives on the single writing statement

A business rule written in several places is reported in several costumes — one per site that forgot it — and each report gets its own `if`. The fourth report is when someone notices they are one rule. A class fix moves the rule to the one statement that writes; an instance fix adds another `if` where the finding pointed.

### Stack

Any. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A rule of the spec ("a declined person is not admitted again", "a removed member cannot post", "a consumed token grants nothing") is enforced by more than one path, or the plan adds an enforcement site.
- More than one path creates the same kind of row (an edge, a membership, a grant) or performs the same effect.
- A finding in a previous review, or an earlier row in this one, was resolved by adding a check at the anchor named.
- The plan carries an exemption to a rule ("except when the author decides").

### Asks for

- **A rule × site table.** One row per rule the change enforces or touches: the rule in the spec's words; every site that enforces it today, by file and line, found by grepping the effect (every caller that creates the row); the single writing statement that performs the effect; and whether the rule is checked *at* that statement or *before* it at each site. A rule with more than one enforcing site and no row saying which one is the writer is visible as such. The table lives in the project's `sites.md` beside the site list, and the plan carries the delta.
- **Exemptions at the writer**, each with its reason in one sentence, in the same table row.

### Tell

- A rule × site row with two or more enforcing sites; a rule enforced by every caller rather than by the statement they call.
- A mitigation in this review that reads "add a check at anchor N" while another row names the same rule (Principle 7).
- An exemption stated at a call site, or in prose, rather than at the writer with its reason.
- The plan's history for this rule already shows a second appearance: the same shape reported before under a different feature.

### Write

- **Move the rule onto the single statement that writes** — the function that creates the edge, the `INSERT` that mints the grant — so no caller can forget it; then delete the caller-side checks.
- **Define the exemption at the same place, with its reason**, or the exemption grows into the next scattered rule.
- **On the second appearance of a shape, stop and change the rule**; a second instance patch is the start of the four-round road.

### Prove

- **One test per former site's path, through the writer**: each path that used to enforce the rule itself now reaches the writer and is refused there; the assertion that goes red is the refusal at the writer when the caller-side check is gone.
- **The exemption test**: the exempted path passes, and a path that resembles it but lacks the reason does not.

### View

- **Does the rule × site table match the callers?** Grep for the effect; every caller that creates the row is a site. A caller the table omits is a finding against the table, before any finding against the design.
- **Which single statement enforces this rule, and does any caller enforce it instead?**
- **Is this the second appearance of this shape?** If yes, the mitigation must remove the possibility, not add a check.
- **Where is the exemption, and is its reason next to it?**

## Rule 21 — A promise travels into the writing statement

A confirmation sentence before an irreversible action names a value: who will be removed, what will be sent, how many will be charged. If the sentence reads one copy of that value and the write uses another — a snapshot in one, fresh data in the other — the sentence is a lie on the one action that cannot be undone. This rule is the intersection of two families: the value has two copies (this batch) *and* it is one state with several update sources (Rule 2), so its defence has half from each.

### Stack

Any client with a confirmation and any store with a conditional write (Rule 2's Stack gate says which); where Rule 2 is skipped for the store, the `WHERE` half of this rule is skipped with it and the snapshot and layout halves stay. Never skipped whole.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- An action cannot be undone — an eviction, a deletion, a send, a charge, a hand-over — and the UI confirms it with a sentence.
- The sentence names a value that another actor can change between render and click: a holder, a recipient, a count, a price.
- The plan adds an expected-value field to the write (Rule 2's conditional `WHERE`) and the client computes it.
- The confirmation and its button are laid out on a phone-sized screen.

### Asks for

- **A promise table.** One row per irreversible action: the sentence as rendered, with its value placeholders; the snapshot the sentence reads (the object, and the moment it is taken — at click, at open, at render); the request field the write receives; the `WHERE` in the writing statement that checks it, by file and line; and the sentence's position relative to the button (same row, or the distance in rows). A sentence and a request that read different objects, an empty `WHERE` cell, or a sentence not beside its button, is visible as such.

### Tell

- The sentence reads a snapshot and the request reads live data, or the reverse; the plan recomputes `expected…` from fresh query data at click; a promise-table row whose snapshot moment is the confirming click rather than the confirmation's opening.
- A promise-table row with an empty `WHERE` cell: the expected value is sent and the server evicts whoever is there.
- The sentence renders at the end of a list and the button stays fixed, so on a phone the sentence scrolls away while the button does not.
- The plan calls the expected value "a hint" or "for display".

### Write

- **One snapshot object feeds both.** When the confirmation opens, capture `{ who, their name, current holder, holder's name }` once; the sentence renders from that object, and the confirming click submits that same object — never a value re-read at the click. The moment is the opening of the confirmation, not the click that confirms it: a snapshot taken at confirm reads what the sentence never showed, and is the drift this rule exists for.
- **The expected value goes into the writing statement's own `WHERE`** (Rule 2), and zero rows affected is reported to the user as "this changed under you", not as success.
- **The sentence sits beside the button** — in the selected row, next to the control — so what is read is what is clicked.
- **Replace the value anywhere along the way with "the newest" and the sentence becomes a lie**; the guard was dismantled once by the client and once by the layout in the same feature.

### Prove

- **Change the holder between render and click**: render the confirmation for holder A, change the holder to B on another connection, click; assert the write affects zero rows and the UI reports the change — the assertion that goes red if the `WHERE` or the snapshot is removed.
- **The snapshot test**: mutate the query cache after the sentence renders, click; assert the request carries the sentence's value, not the cache's.
- **The layout test at the phone viewport**: with the list long enough to scroll, assert the sentence and the button are in the same viewport when the button is reachable.

### View

- **Does the promise table match the component and the handler?** Open both: the sentence's data source in the component, the request field in the mutation, the `WHERE` in the handler. A layer the table skips is a finding against the table, before any finding against the design.
- **Trace the value from the sentence to the `WHERE`. Does its source change anywhere between?**
- **What does the user see when the write affects zero rows?**
- **On a phone, is the sentence visible when the button is?**
