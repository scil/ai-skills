# D · Development view

How the work and the code are organized: parallel workers, tests and checks, new mechanisms, copies of one truth, and dependencies. The 4+1 development view. Ask each gate first. If the plan has no surface for a gate, skip its subtree.

## CWE-435 · Interaction between entities

### D1. Is the work split across parallel workers (agents, sessions, people), or delegated?

- **D1.1** The workers meet at an interface (a constant, an environment variable, a path, a JSON shape) that the plan states only in prose. Each side names it on its own, and both pass their own checks while the joined system reads nothing. Suggest: fix each interface by exact names and formats in one place both read, before the split. After the merge, check that each name one side writes is the name the other reads.
- **D1.2** The workers share one working copy, and the plan names no owner per file. A worker writes from a copy it read earlier and overwrites another's change. Suggest: one writer per shared file, or one copy per worker with a named merge. A worker re-reads the file before it writes and stops if it changed.

## CWE-693 · Protection mechanism failure

### D2. Does the plan add or rely on a test, a validator, an audit or a guard?

- **D2.1** The change and the check that judges it are out of step. The change leaves artifacts in the set the check scans (an installed file, a quarantine folder), or the change and the check address different properties (switched off, against exists). Suggest: list, per change, every artifact it leaves and every check that sees it. The check recognizes the change's own artifacts by an identity derived from the change's source. Point the change and the check at the same property.
- **D2.2** The tests cannot fail for the right reason. They run only on a fixture built by planting the defects, they stub the library under test, they assert only the positive case, or they fix a preference in a file the owner edits by choice. Suggest: one clean instance with nothing planted, one test with the real library, a silence assertion beside each positive one. A test of an owner file checks only rules every valid file obeys.
- **D2.3** The worker that must pass a rule can also edit it, and relaxes it to pass the acceptance command. Suggest: name the rules no step can weaken and lock each with a test. A blocked worker stops and reports. The reviewer reads the diff of guards and tests first.
- **D2.4** A shortcut (a manual run, a forced mode, a hand-built input) takes items past the check that the normal path runs. Suggest: the shortcut is a mode of the same tool that still runs every check and relaxes only its own condition.

## CWE-710 · Coding standards

### D3. Does the plan introduce a mechanism: a module, a helper, an interaction, a content set, an algorithm, a policy?

- **D3.1** No search is recorded for how others already solve it: a library, the platform, an open-source project, a paper, a standard, or the codebase under another name. Suggest: one provenance line per mechanism: adopted (from where, which version), adapted (what changed, why), or original (what was searched, why nothing fit).
  - **D3.1.1** The mechanism is an interaction concern (click-outside, focus trap, hotkeys, drag, a virtual list, debounce, navigation blocking) written by hand, or named like an export of a package already in the manifest. Suggest: search the imported packages and the platform first. Adopt whole, or hand-write against the checklist the library covers (touch, keyboard, screen reader, IME, RTL, unmount mid-event, SSR, reduced motion).
  - **D3.1.2** The mechanism is a commodity content set (icons, flags, country or currency lists, a font) made or copied by hand, ported from a prototype, or grown by one more item. Suggest: the source a project document names, adopted behind one module. Hand-make only items with no honest equivalent, each with its reason. Ask this of the whole set.
  - **D3.1.3** A library is rejected as "too heavy" or "we need only a part" with no number and no failing scenario. Suggest: the figure or the scenario.
- **D3.2** The plan cites research, and a mechanism contradicts or ignores a finding without saying why. Suggest: trace each finding to the decision that uses or rejects it.
- **D3.3** A new module's interface makes the caller assemble, order or already know what the module can own, or an export only forwards its arguments. Suggest: one call that performs the sequence and an object naming what varies. Call what a pass-through wraps.

### D4. After the change, is one decision, rule, value or name stated in more than one place?

- **D4.1** The same thing is rendered, parsed or decided at two sites (a preview and the page, client trimming and server normalizing, a pairing copied from a sibling), and no site is the owner. Suggest: one owner the rest import, repointed in the same change, with a parity or contract test across the sites.
- **D4.2** A boundary or a rule list (what can leave, be stored, be seen) is stated in several documents, and the lists differ. Or a resolution is appended while the old text still states the old decision. Suggest: one document owns the list as a table. The others state the rule in one line and link there. Correct a decision where it stands.
- **D4.3** One place (a path, an address, a queue) is named twice because two parties see it from two viewpoints (a host path and a container path), and nothing checks they agree. Suggest: derive one name from the other, or a start-up check that names both when they differ.
- **D4.4** A field named for a part (`recipientName`, `amount`) receives a composed value (a sentence, a formatted string). Suggest: the name states the contract, with one line per boundary saying who composes what.
- **D4.5** A shared tool changes a default for one caller, and other callers relied on the old one without passing it. Suggest: list every caller and the value it relies on. A caller that relied on the old default passes it in the same change.

### D5. Does the plan use or depend on a library, an SDK or platform behavior?

- **D5.1** The plan reads two options of an options object, and an unset option's default does something. Suggest: list every option, its value or "unset", and what its default does. Set explicitly each option that touches the feature.
- **D5.2** A hand-written listener, loop or check sits beside a library feature for the same concern (an unload listener beside a navigation guard, a retry loop beside a retrying client). Suggest: one of the two owns it. Feed the library the predicate and delete the hand-written half.
- **D5.3** The plan states how a library or the platform behaves with no source. Suggest: the documentation page, the type definition or the issue.
- **D5.4** A third-party library is imported from many modules, or its types cross into domain code, so an upgrade touches many files. Or an interface for swapping exists but tests run only one implementation. Suggest: one adapter owns the import behind a project-owned interface, enforced by an architecture test. One contract test suite runs against every adapter.
- **D5.5** A dependency is pinned with no reason, no lifting condition and no review date. Suggest: record all three. At review, check the latest release and the default branch.
