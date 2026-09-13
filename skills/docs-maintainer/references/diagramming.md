# Diagramming

Use PlantUML for architecture, key runtime flows, and hard-to-follow nodes. Do not diagram trivial or self-evident structures.

- Add a PlantUML diagram to C4 architecture docs (`c4-system-context`, `c4-container`, `c4-components`) to depict actors, containers, components, and their boundaries, alongside the required prose. Keep C4 L1 and L2 stable and hand-maintained; use L3 for complex containers, and L4 only for code structures that cannot be understood locally.
- Add a PlantUML sequence or activity diagram to important runtime flows such as `dynamic-login-flow` and other cross-boundary flows named in the Annotated Structure.
- Add a PlantUML diagram to a `code-locator` or `repo-map` entry only when the structure is a genuine trap: nontrivial state machines, retry/rollback paths, concurrency, or multi-service handoffs that are hard to reconstruct from code alone. Do not diagram straightforward call chains.
- Write diagrams as fenced ` ```plantuml ` code blocks directly in the owning node, next to the prose they illustrate. Use a linked `.puml` file only when the project's documentation tooling requires external diagram files.
- Keep each diagram small and focused on one boundary, flow, or component group. Split into multiple diagrams instead of building one dense diagram.
- Validate diagrams the project's checks can render, such as a PlantUML CLI, editor preview, or CI rendering step, before treating a diagramming task as complete.
- Update the diagram in the same change as the code, boundary, or flow it depicts; an outdated diagram is a documentation defect equal to outdated prose.
