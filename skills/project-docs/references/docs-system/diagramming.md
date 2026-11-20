# Diagramming

PlantUML, written as fenced ` ```plantuml ` blocks inside the owning node next to the prose they illustrate; a linked `.puml` file only when the project's tooling requires external diagram files. A diagramming task is complete when the project's renderer (PlantUML CLI, editor preview or CI step) renders it.

- **C4 L1 and L2** (`architecture/c4-context`, `architecture/c4-container`): one diagram each, hand-maintained. **L3** component views exist only as generated artefacts under `generated/components` — C4: "only create component diagrams if you feel they add value, and consider automating their creation". **L4** is never drawn — "most IDEs can generate this level of detail on demand".
- **Runtime flows**: one sequence or activity diagram per `architecture/flows/<name>`, one flow per file.
- **Locator and repo-map entries** get a diagram only for a genuine trap: a nontrivial state machine, a retry or rollback path, concurrency, a multi-service handoff that is hard to reconstruct from code.
