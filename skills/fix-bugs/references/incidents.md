# fix-bugs — the incidents behind the rules

Each rule in `SKILL.md` came out of one of these. Read the one the rule points at when the rule alone does not land; add a new incident here (and only a one-line pointer in `SKILL.md`) when a fix teaches something the rules did not already say. Stack-specific mechanics go in `references/<stack>.md` instead.

## The list row — four dead strips, one missing layer

Reported four times running as "this part of the row looks pressable and does nothing": the status line, then the bottom gutter, then the same gutter moved to a wrapper that still was not the opener, then the space above and below the centred `⋯` on a tall row. Each patch moved padding around and created the next dead strip. The fix that ended it was structural — one transparent pointer layer over the whole row, everything beneath it `pointer-events: none`, only the real controls re-enabled above — and it was available at the first report.

Rule: *fix the class, not the instance* — on the second finding of the same shape, state the invariant in one sentence and make it true everywhere. The tell of an instance fix is the diff: the new `if` sits beside the last `if`.

## A decline closes a card — four costumes, one statement

"An author's decline closes that card to that account" was reported four times in four costumes: the landing page still offered it; a request queued from *before* the decline was still honoured; a pass earned in another browser was merged onto the declined account at sign-in; a claim opened before the decline was consumed after it. Four screens, four procedures. All four ended at the one function that inserts the relationship record. Three patches went next to the site named in the report; the fix that ended it asked the question at that insert.

Its scope was one caller kind: the author's own admission route goes through the same insert and is deliberately exempt, because admitting *is* the author deciding, and the record of a decision must not block the person reversing it. Writing the exemption down is what proved the routes were enumerated rather than flattened.

Rule: *the fix goes at the one statement that decides* — the narrowest point every route must pass through to produce the outcome — and *a class fix must be able to name its own scope*. It is the concurrency rule "the statement that writes must be the statement that decides" applied to **coverage**: the concurrency version loses to a race, the coverage version loses to a route you did not think to guard.

## The overlay that tested itself

A UI fix shipped green and broken: the regression test reached into the DOM for the overlay the fix had just added and clicked *that*, instead of pressing where a person presses. It could not have gone red without the fix, because it asserted the implementation.

Rule: *the revert check* — would this go red if the fix were undone? — and *test at the layer that can observe the defect*: for stacking or `pointer-events` that is a real browser pressing coordinates, since a DOM emulator does no hit-testing.
