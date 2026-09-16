# Node / pnpm workspaces — candidate non-inferable lines

A menu. Offer each only after checking the repo: if the fact is already in a config the agent reads, or the repo does not have the problem, the line does not enter. Each row says why code alone does not reveal it.

| Candidate line | Why not inferable | Enforcement |
|---|---|---|
| Package manager is `pnpm`; a second lockfile is a mistake. | An agent that sees `package.json` may reach for `npm`; `packageManager` field is often absent. | `preinstall` script `npx only-allow pnpm`, or advisory |
| `pnpm test -- <path>` filters by file; `pnpm --filter <pkg> test` selects a workspace. | Filter syntax differs per runner (vitest / jest) and per workspace tool; wrong guess runs the whole suite. | advisory |
| Generated clients under `{{dir}}` are regenerated with `{{cmd}}`, never edited. | Generated code looks like source. | CI diff check after regenerate |
| A change under `packages/db/` runs `pnpm db:test`; the full suite runs in CI. | Scoped verification; the agent would otherwise run everything. | CI job name |
| Node version is pinned in `.nvmrc` / `engines`; do not upgrade it in a task. | Version bumps look like harmless fixes. | `engine-strict=true` in `.npmrc` |
| Windows: pnpm's deep `node_modules` cannot be removed with `Remove-Item` without `\\?\` prefix. | OS-specific trap. | advisory |
