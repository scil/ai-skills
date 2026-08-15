# Designing documents that live in a vault

Syntax is in `obsidian-markdown.md`. This file is about what makes a vault document *worth keeping*:
structure, reader calibration, and the patterns that turn a write-up into a reference someone
returns to.

## Calibrate to the reader before writing a line

The single most common failure is writing at the wrong altitude. A recap written for someone who
already knows the domain is useless to the person who just lived through the work but does not yet
have the vocabulary — and they will tell you it is "too simple" only *after* you have written it.

Before writing, pin down:

- **What does this reader already have vocabulary for?** If the document will use a term they have
  not defined themselves in conversation, that term needs introducing.
- **What will they do with it?** Read once and act (a runbook), or read repeatedly to learn (a
  primer)? Different structures.
- **Will they read it cold, months later?** Then in-document context beats external links.

When the reader is new to the domain, **build the vocabulary first and use it consistently
afterward**. Do not sprinkle definitions in parentheses as you go — front-load them, then let the
rest of the document reuse them. A reader who has the words can follow anything; a reader who does
not will bounce off paragraph three.

If a document gets rejected as too advanced, the fix is not "add more explanation inline". It is a
restructure: concepts first, then architecture, then events.

## Structures that work

### The primer (teaching a domain)

```
0. Cast of characters — the parts and their roles, in one table
1. Concept cards — the vocabulary, one card each
2. Architecture — the naive design, why it failed, the real one
3. The incidents — what broke, explained using the vocabulary from §1
4. Methodology — the transferable lessons
5. Self-test — folded Q&A
6. Glossary / quick reference
7. What to learn next
```

Why this order: each section can only use words the previous ones established. §3 becomes easy to
write and easy to read because every failure is just a recombination of §1's concepts.

**Concept card format** — one analogy, one grounding:

```markdown
### ⑤ NAT: the mail room

**Analogy**: your router keeps a mail room. It only accepts a reply if you sent
the original letter — and "matching" is strict: same street number *and* same
room number. Different room number? Discarded, no notice.

**In our system**: this is why gate 5 was unwinnable inside a container.
```

The analogy carries the intuition; the grounding makes it concrete and locally true. Skip either
half and the card stops working.

### The runbook / control panel

Actions first, explanation folded underneath. The reader is here to *do* something; anything they
must scroll past is friction. Put every reference table in a collapsed callout at the bottom.

### The decision record

Context → options considered → what was chosen → **why the rejected options were rejected**. That
last part is what makes it valuable in six months, when someone (possibly you) proposes the rejected
option again.

## Patterns that earn their place

- **Fold the reference, expose the action.** `> [!question]- ` for self-test answers, `> [!abstract]- `
  for cheat sheets. A 400-line document with folded sections reads like a 150-line one.
- **Self-test questions** turn passive reading into retention. Write them to test *transferable
  judgment* ("a friend says X, how do you diagnose?"), not recall of details.
- **Reading-path guidance at the top.** "First pass: §0–1. Then: §2–3. Then close the doc and try
  §5." Costs three lines, changes how the document gets used.
- **Show the obvious-but-wrong design first.** Architecture is memorable when the reader understands
  what *failed*. A diagram of the naive version followed by the real one teaches more than the real
  one alone.
- **Turn the reader's own questions into sections.** If they had to ask, the document had a gap —
  and others will hit the same one. A question asked mid-project is free user research.
- **State the transferable lesson explicitly.** After each incident, one line: what should someone
  take away when the specifics no longer apply. Do not make the reader infer it.
- **A "what to learn next" section** at the end sets expectations for the phase that follows and
  makes the document feel like a stage rather than a dead end.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Chronological dump ("then I tried… then I tried…") | Order of discovery ≠ order of understanding |
| Terms used before they are defined | Reader bounces early and does not come back |
| Every detail at the same visual weight | Nothing is findable; folded callouts exist for this |
| Explanation with no worked example | Abstract advice does not survive contact with a real problem |
| A document with no stated audience | Ends up pitched at the writer, i.e. at nobody |
| Duplicating content that lives in the repo | Two sources of truth; link to the repo file instead |

## Splitting vs. one long note

Prefer **one substantial note with a table of contents** over many fragments, unless sections have
genuinely different lifecycles (a stable primer vs. a frequently-edited runbook — those should be
separate, and should link to each other).

Obsidian's outline pane, folded callouts and heading anchors make long notes navigable. Fragmenting
early produces a graph of stubs that nobody reads.

When you do split: **link both directions**, and link to the *specific heading*
(`[[Primer#Concept ⑫]]`) rather than the whole note.
