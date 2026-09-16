# Rust — candidate non-inferable lines

A menu; check the repo before offering any row.

| Candidate line | Why not inferable | Enforcement |
|---|---|---|
| CI runs `cargo clippy --all-targets -- -D warnings`; a warning is a failure. | `cargo build` passes locally with warnings. | CI job |
| `cargo fmt` is the formatter; do not hand-align. | Obvious once seen, but agents "tidy" imports. | CI `cargo fmt --check` |
| Snapshot tests (`insta`) are reviewed with `cargo insta review`, never by editing `.snap` files. | Snapshot files look like fixtures. | review |
| New code goes in a new crate, not `{{core_crate}}`, unless it is that crate's concern. | A monolith invites additions; the boundary is a decision, not a fact of the tree. | advisory (openai/codex states this rule) |
| Integration tests live in `tests/` per crate; unit tests in a sibling `*_tests.rs`, not inline `mod tests`. | Both layouts exist in the ecosystem. | advisory |
| `Cargo.lock` is committed; do not run `cargo update` in a task. | Updates look like harmless refreshes. | CI `--locked` |
