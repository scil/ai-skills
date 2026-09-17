# fix-bugs — OpenSpec projects

What `SKILL.md` §1 resolves to in a project that keeps its requirements in OpenSpec (`openspec/specs/` accepted, `openspec/changes/<name>/` in progress).

## §1 Where the requirement that binds may be

- **Two folders, always both.** `grep` the capability name under `openspec/specs/` **and** `openspec/changes/*/specs/`. A change's delta binds from the moment the change is accepted, but it is copied into `openspec/specs/` only when the change is archived — so a search of the main specs alone finds nothing while the requirement still holds, and a fix written against "no rule covers this" contradicts the rule one folder over.
- **Read the delta as a diff.** An `ADDED` requirement is new law; a `MODIFIED` one replaces the accepted text for the same requirement, so read the change's version, not the main spec's.
- **A conflict is a change, not an edit.** If the fix cannot satisfy an accepted requirement, open an OpenSpec change with a `MODIFIED` delta for that requirement before changing the code. A quiet edit that contradicts the spec is a review finding, however correct the code.
