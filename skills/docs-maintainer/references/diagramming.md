# Diagramming

Use PlantUML for architecture, key runtime flows, and hard-to-follow nodes. Do not diagram trivial or self-evident structures.

- Add a PlantUML diagram to the C4 L1 and L2 docs (`architecture/c4-context`, `architecture/c4-container`) to depict actors, containers and their boundaries, alongside the prose. Keep L1 and L2 stable and hand-maintained. L3 component views exist only as generated artefacts under `generated/components` (C4's own guidance: "only create component diagrams if you feel they add value, and consider automating their creation"); L4 code diagrams are not created ("most IDEs can generate this level of detail on demand").
- Add a PlantUML sequence or activity diagram to each important runtime flow under `architecture/flows/<name>`; one flow per file, one diagram per flow.
- Add a PlantUML diagram to a `code-locator` or `repo-map` entry only when the structure is a genuine trap: nontrivial state machines, retry/rollback paths, concurrency, or multi-service handoffs that are hard to reconstruct from code alone. Do not diagram straightforward call chains.
- Write diagrams as fenced ` ```plantuml ` code blocks directly in the owning node, next to the prose they illustrate. Use a linked `.puml` file only when the project's documentation tooling requires external diagram files.
- Keep each diagram small and focused on one boundary, flow, or component group. Split into multiple diagrams instead of building one dense diagram.
- Validate diagrams the project's checks can render, such as a PlantUML CLI, editor preview, or CI rendering step, before treating a diagramming task as complete.
- Update the diagram in the same change as the code, boundary, or flow it depicts; an outdated diagram is a documentation defect equal to outdated prose.
