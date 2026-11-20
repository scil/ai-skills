# Python — candidate non-inferable lines

A menu; check the repo before offering any row.

| Candidate line | Why not inferable | Enforcement |
|---|---|---|
| Environment tool is `{{uv | poetry | pip-tools}}`; install with `{{cmd}}`, never `pip install` into the system interpreter. | Several lock formats coexist; the agent may pick the wrong one. | advisory, or a `Makefile`/`justfile` target |
| Run tests with `{{pytest -q path}}`; the full suite needs `{{service}}` and runs in CI only. | External dependency of the suite is invisible from the tree. | CI job |
| Type checking: `{{mypy | pyright}} --strict` is a gate. | Not visible unless CI config is read. | CI job |
| Minimum Python is `{{3.x}}`; no `from __future__` imports for features already available. | Version floor lives in `pyproject`, but agents add compatibility shims by habit. | `ruff` rule UP |
| Migrations under `{{dir}}` are generated with `{{alembic | django}}` and never edited once merged. | Generated files look like source. | CI check |
| Notebooks are not committed with outputs. | Convention, not a fact of the tree. | `nbstripout` pre-commit |
