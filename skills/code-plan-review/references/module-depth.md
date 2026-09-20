# Batch: module depth — Rules 25, 26, 27

Depth is the goal; search and consolidation are just the two ways a plan fails to reach it before code exists. The three rules are one theme in three costumes: the past already solved this and nobody looked (25), the present solves it twice because nobody was told (26), and the one true solution still leaks its insides regardless of any of that (27). The stack/hook-specific member of this family — a hand-written listener or interaction beside a library feature that already owns the concern — lives in library-hooks-listeners, Rules 1 and 24; this batch is that same question aimed at the codebase's own modules, at any granularity from a pure function to a package, instead of at the ecosystem.

## Rule 25 — A new module is preceded by a search of the ones that exist

A module's interface is a promise: callers get its behaviour by learning a little and delegating the rest. Every time a plan introduces new behaviour without first asking whether a seam already carries it, that promise gets reissued somewhere else — a second, shallower copy of a module that was already deep, or two half-modules where one deep one would have served both. The cost does not show up at the site that skipped the search; it shows up at the second site that needed the same thing and wrote it a third way, and at the module whose one caller now can't tell what it's for.

### Stack

Any. Never skipped — this rule is about the codebase's own modules, at every granularity from a pure function to a package, not about a particular framework or store.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The plan introduces a new function, hook, component, schema, validator, DB helper, or package-level export that decides, transforms, renders, computes, or validates something an entity already has behaviour for elsewhere in the codebase — under any name, not necessarily the same one.
- The plan's Decisions section names an existing capability ("like X", "similar to the Y flow") without a stated reason the new code does not call or extend it.
- Two modules in the plan — one new, one already in the tree — would return the same answer, perform the same effect, or paint the same output for the same input, whether or not the plan's author noticed.
- A new module's interface asks its caller to supply, in pieces, something the module could have assembled itself from what it's already given — a sign the module is shallow (its interface is nearly as complex as what it does) rather than deep.

### Asks for

- **A module search ledger.** One row per new function/hook/component/schema/package export the plan introduces: the behaviour in the entity's own words (not the name chosen for the new code); the grep(s) run for that behaviour across the tree — by the entity's name, by the fields or parameters it touches, by the verb that names the decision ("valid", "complete", "format", "resolve") — the same discipline Rule 24 already uses for the ecosystem, aimed inward at this repository instead; every existing candidate the grep(s) surfaced; and a disposition per candidate — *reuse as-is*, *extend* (name the seam: the new parameter, the new named outcome), or *reject* (the candidate answers a different question, or sits at the wrong layer — stated, not implied). A row with an empty grep cell, or a *new module* disposition with no rejected-candidates list, is visible as such.
- **The new module's own interface, stated in one line**: what it takes, what it returns, and what it does NOT ask the caller to know or supply separately — so the reviewer can judge depth without reading the implementation.

### Tell

- A new function/component/hook whose name, parameters, or body closely resemble an existing one, found by grepping the entity's name or the decision's verb, with no ledger row explaining why the existing one was not reused or extended.
- A Decision that says "similar to X" or "like the existing Y" with no disposition on why it is not X or Y.
- A new module whose interface requires the caller to pass in several raw fields the module could have derived from one value already in its possession — the caller is doing part of the module's job before calling it.
- A validation, formatting, or classification rule expressed as a comparison against another module's exported constant, at a site that is not that module's own file (the narrowest, most common shape this rule catches — the one this rule was written for).
- The search turns up more than one existing candidate for the same question — this ledger does not pick a favourite to copy from; it hands the full candidate list to Rule 26, which decides the owner and proves the collapse.

### Write

- **The property**: a behaviour any entity has is decided, transformed, or rendered in exactly one place; every other site asks that place for the answer rather than reconstructing it, at whatever granularity the behaviour lives — a function, a hook, a component, a schema, a package.
- **One implementation of it**: the search ledger is filled — grep run, candidates listed, disposition stated — before the new module is written, the same discipline Rule 24 already requires for the ecosystem, aimed at this repository's own tree first. A *new module* disposition survives only when the rejected-candidates list names a real difference in question or layer, not merely that a candidate exists.
- **A new module earns its own file/export when, and only when, a second caller needs the same behaviour** — the deletion test: if this module were deleted, would the logic reappear at more than one call site? If yes, it was earning its keep and stays a module; if the plan cannot name a second call site today, say so and keep the logic inline until one arrives, rather than pre-building a seam nothing yet varies across.

### Prove

- **The ledger-completeness check**, at review time, not a red test: the reviewer's own grep for the entity's name and the decision's verb must not turn up a candidate the ledger omits. An omitted candidate is a blocking finding against the ledger, before any finding against the design — the same mechanism Rule 24 already proves by.
- **Once two modules ARE found answering the same question** (caught here, or later in a diff pass): a boundary-value or input parity test across the sites, asserting they agree — the assertion that goes red the moment the surviving site's logic changes without the collapsed one changing with it. This is the same proof Rules 19 and 26 already use; this rule's own contribution is catching the second copy BEFORE it is written, not just proving the fix once it's found.

### View

- Does the search ledger's grep hits match what my own grep for the behaviour finds? An omission is a finding against the ledger first.
- For each *reject* disposition: does it name a real difference (a different question answered, a different layer), or does it just restate that the candidate exists?
- For the new module's stated interface: does it ask the caller for raw parts it could derive itself from what it's already given? Would a caller need to read the implementation to use it correctly, or does the one-line interface answer that?
- Run the deletion test on the new module: if it vanished, would its logic reappear at more than one site today, or only one?
- Did the search find more than one candidate? If so, does the ledger say so plainly rather than quietly reusing one of them — and has Rule 26 been given the list?

## Rule 26 — Wherever a decision has more than one site, one of them is the owner

Rule 25 asks whether a search happened before new code was written. This rule does not care when each site was written — only how many exist right now, once this plan lands, and whether one of them is designated as the owner the rest call. A decision duplicated by two old sites that predate this plan is not a smaller problem than one the plan just introduced twice — the plan is simply the moment someone finally looked.

### Stack

Any. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- The plan's own pseudocode, across two or more of its own new sites, computes, validates, formats, or decides the same thing from the same shape of input.
- Rule 25's search ledger, for any row, surfaces more than one existing candidate for the same question — the search that rule requires before writing new code incidentally reveals that the codebase already answers this question in two or more places, with no candidate marked as the one the others call.
- A grep for the entity's name or the decision's verb (run for Rule 25, or run on its own where no new module is even being proposed yet) turns up two or more existing sites deciding the same thing, whether or not this plan touches any of them.
- The plan's Decisions section names an existing site as "the" place this is handled, while a search shows a second site doing the same thing under a different name.

### Asks for

- **A site tally, not just a same-plan list**: for each decision this rule catches, every site that decides it — pre-existing sites Rule 25's ledger found, and any new sites this plan adds — in one list, not two separate ones; the single site marked as owner; and, for every other site, whether it already imports the owner or still carries its own copy. A tally of two or more with no owner marked is visible as such regardless of how old each site is.

### Tell

- A Rule 25 ledger row with two or more candidates and no note on which one (if any) is the owner the others should call.
- Two pseudocode blocks — old, new, or one of each — performing the same comparison, computation, or classification with different local names.
- "Keep both in sync", "match the other place", or "same rule as the other screen" as a stated mitigation, wherever the sites first appeared.

### Write

- **The property**: when a decision has more than one site — however old each one is — exactly one of them is the owner every other site calls; a plan that adds a third caller to an already-duplicated decision picks the owner (or names a new one) and repoints the others in the same change, rather than adding a third copy beside the first two.
- **One implementation of it**: factor the shared logic into its own function/hook/schema if no site is already fit to be the owner, or designate the best-placed existing site as the owner and have every other site — old and new — import it, in the same plan that noticed the duplication.

### Prove

- **A parity test across every site the tally names** — old and new — one input, every site or call path, assert identical output: the assertion that goes red the moment any one site's copy is edited alone, whether that site predates this plan or not.

### View

- Does any decision have more than one site once this plan's search and pseudocode are both accounted for — old sites Rule 25 found, and new ones the plan adds?
- Is one of them named as owner? If not, is naming one part of this plan, or deferred?
- If the mitigation is "make the new site match the old one", is a class fix (one shared module, old sites repointed) proposed, or an instance fix (a third copy added beside two that already existed)?

## Rule 27 — An interface answers the question, not lists the parts

A module can be the only implementation of something and still be shallow: its interface asks the caller to assemble what the module could have assembled itself, or to call its exports in an order nothing enforces, or to already know the answer to a related question before calling it. No duplicate has to exist for this to cost something — the cost is paid by every future caller who has to read the implementation to use the interface correctly, and by every test that has to reproduce the module's internal steps just to reach it.

### Stack

Any. Never skipped.

### Where

Any one of these makes the rule apply, whether or not the plan already guards against it. Judge from the spec deltas and the named files, not from the plan's own claims.

- A new function/component/hook/schema's parameter list grows with each caller's special case, rather than absorbing the variation inside it.
- Correct behaviour requires calling two or more of the module's exports in a specific order, with nothing in the interface enforcing that order.
- The module's name promises an answer ("isXValid", "resolveY", "formatZ") but its signature requires the caller to already hold a value only the module itself should need to compute.
- A new export forwards its arguments to another call with no branch, no decision, and no transformation of its own — a pass-through introduced where the thing it wraps could be called directly.
- Writing a unit test for the new module requires reproducing more than one internal step or setting up more than one unrelated precondition before its behaviour can be exercised.

### Asks for

- **An interface statement, one line per new module**: what it takes, what it returns or does, and — the deletion test — what happens if it is deleted: does complexity reappear at a second site (it earned the seam), or does it simply vanish (it was a pass-through)?
- **A caller-knowledge list**: everything a caller must already know or hold to call this module correctly, beyond its stated parameters (an order of calls, a field that must be set first, an invariant between two arguments). An empty list is the deep case; anything on it is a candidate the module could absorb instead.

### Tell

- A caller-knowledge list that is not empty for a genuinely new module.
- A parameter added to an existing new-in-this-plan function specifically to carry one caller's special case, where the module could instead have derived that case from a value it already receives.
- A pass-through whose deletion test says "nothing reappears".
- A test for the new module that sets up more than the module's own stated parameters before it can be exercised.

### Write

- **The property**: a caller learns the module's interface once and never needs to open its implementation to use it correctly; everything the module needs, it derives or asks for itself rather than requiring the caller to assemble it.
- **One implementation of it**: collapse a growing parameter list into fewer parameters that carry meaning (an object naming what varies, not each variant as its own flag); where an order of calls is required, expose one function that performs the sequence instead of several the caller must chain correctly; delete a pass-through and let callers use what it wrapped.

### Prove

- **The test-surface check**: the module's own test file exercises it through its stated interface alone — no internal step reproduced, no second precondition object built by hand — the same claim `codebase-design`'s "the interface is the test surface" principle makes; a test that has to reach past the interface is evidence the interface is not the real seam.

### View

- Could you write the module's doc comment from its parameter names and return type alone, without describing a branch inside it?
- Run the deletion test: does its complexity reappear at a second site, or does it just vanish?
- Does calling this module correctly require knowing anything not on its parameter list?
