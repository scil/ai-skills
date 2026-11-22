# O · Operations view

Where the system runs and what operates it: deletions and retirements, runs over many items, steps the owner must unblock or will repeat, and content from other parties. The 4+1 physical view, named "operations" here. Ask each gate first. If the plan has no surface for a gate, skip its subtree.

## CWE-664 · Resource lifetime

### O1. Does the plan delete, purge or retire something?

- **O1.1** A deletion lists the stores it clears by their owners (the database, a cache folder, uploads), while a consumer keeps a copy of its own: a converted file, a thumbnail, a search index, a sync client, a backup. The deletion reports success and the copy outlives it. Suggest: list every reader of each store and the copies it writes. Give each copy a bounded lifetime or reach it from the deletion. The report states what the deletion cannot reach.
- **O1.2** The plan retires a component and searches for references only in the repositories it works in. References also live in user-level instructions, other repositories and notes, and the component did jobs others relied on. Suggest: list where references can live and search each place. Name a new owner for each job, or state that it is dropped. Afterwards, the old name appears only in history.
- **O1.3** A cleanup frees everything it reaches, including resources that other owners still use (a cached material, a pooled connection, a shared buffer). The next user reads a freed resource, or the cache rebuilds it on every use. Suggest: each resource has one owner. A cleanup frees only what its caller created, and a shared cache frees on its own schedule.

## CWE-691 · Control flow

### O2. Does the work cover many items: a batch, a migration over records, a cleanup or deploy over files, a rename, a test run, a backlog?

- **O2.1** The set is chosen by a property that other things also have, now or later (a glob, a prefix, a query, a page selector, a folder), or by one too narrow. Extras are acted on, or members are dropped. Suggest: define the set by what makes a thing a member, such as a list its producer wrote. Print the count and a sample before acting. A destructive action gets a dry run first.
- **O2.2** Part of the work is put off (skipped, "later", a TODO, a disabled test), and the only record is a log line or a reply. Or a skipped step also fed a later step its input. The run reports complete. Suggest: every put-off item goes into one register, and "done" is a check that pairs every input with an outcome. For each skippable step, the later steps get their input from a source that does not depend on it.
- **O2.3** A run decides what to do by comparing the target with a record of the last run, and an early step moves that record. After a failure, a re-run sees nothing changed and skips what never ran. Suggest: only the last step writes the record, after every step succeeded. The plan states what a second run does after a failure at each step, and one test fails a middle step and runs again.
- **O2.4** A run handles at most N items in a fixed order, so the same first N fill every run. Suggest: take first the items handled longest ago. The report gives the number left.
- **O2.5** A script edits many files by text replacement and changes more bytes than intended (line endings, a byte-order mark, escape sequences that shell quoting turned into control characters). A diff that hides whitespace shows only the intended lines. Suggest: binary-safe replacement that keeps each file's encoding, replacement text as raw strings in a script file, and a check of what a normal diff hides.

### O3. Does a step need something only the owner supplies, or create an operation the owner will repeat?

- **O3.1** A step needs a login, a key, a terminal, a device or an approval, and the work before it runs on recorded data, so nobody learns the step cannot run until the end. Suggest: list what the owner supplies per step. Test each item with one cheap real call at the start and before its step. A step that did not run stays an open entry (O2.2).
- **O3.2** The acceptance command needs a state that only the owner sets (a feature switched on, a record a live run writes), so it runs clean and shows nothing. Suggest: name the state each acceptance command needs and who sets it. If only the owner sets it, prove the command on a copy with that state written by hand. The worker does not change the owner's state.
- **O3.3** The plan adds or changes an operation the owner will run more than once, in a project that keeps a console of such operations, and no step updates the console. Suggest: a step "update the console": a button per new recurring operation and the help line of each changed one.

## CWE-707 · Neutralization

### O4. Does the system keep, show, pass on or act on content or input another party wrote?

- **O4.1** External input (a webhook, an OAuth callback, an upload, a queue message, a query string) is acted on before any shape check. Suggest: shape, then authorization, then consistency, before the first dependent read.
- **O4.2** Content from outside (a clone, an archive, a package) is stored where a project tool finds files by discovery (a test runner, a type checker, a linter, a watcher). Suggest: store it outside every root a project tool scans, and refuse a store path inside the project. One test shows that a file planted in the store is not collected.
- **O4.3** Text from outside (a description, a README, a commit message) reaches an output that an agent or a model reads, and can hold a sentence written as an order. Suggest: mark the text as third-party data in every such output and cut it to one plain line. A model that reads it gets no tools and returns only schema-shaped data.
