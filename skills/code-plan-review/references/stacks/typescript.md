# Binding: TypeScript

How the catalog's questions show up in TypeScript code, client or server. Load this file when the tree is TypeScript. The question is the catalog's; this file only says what it looks like here.

Each entry: **shows up as** · **look for** · **fix**.

## A. The client sends a request / C. Who is asking

**A1.3, C3.2, I1.1 — the value checked is not the value stored; input acted on unchecked.**
- *Shows up as:* a type annotation on `req.body`, `JSON.parse(…) as T`, or a form value cast to its type — types vanish at runtime, so nothing was checked.
- *Fix:* one runtime schema (Zod, Valibot, ArkType) shared by client and server; the client sends `schema.parse(draft)` and every dirty/valid/equal check reads the parsed value; the server parses before its first dependent read.

## F. A branch over a value with several states

**F1.1 — fewer states than the value has.**
- *Shows up as:* `x ?? fallback` where `null` and `undefined` mean different things; `x || fallback` where `0` or `''` is a real value; `if (!x)` over a number.
- *Fix:* name the states in the type (a discriminated union with a `status` field) and branch on the tag.

**F1.2 — a boolean that hides a state.**
- *Shows up as:* `const hasData = !!data`, `const isEmpty = !data?.length` — undefined (unknown) and `[]` (known empty) collapse into one value.

**F1.3 — a `switch` that stops being exhaustive.**
- *Fix:* `default: return assertNever(x)` with `function assertNever(x: never): never { throw new Error(…) }`, so adding a member fails to compile; the lint rule `@typescript-eslint/switch-exhaustiveness-check`.

## B. The server handles a write

**B2.2 — which handle a helper needs.**
- *Fix:* the parameter type names it (a transaction type, or `Pick<Db, 'insert'>` for a helper that only inserts), so passing the pool where a transaction is required does not compile; no `as` cast at call sites.

## H. Someone already owns this

**H1.3 — how a library behaves, without a source.**
- *Fix:* cite the `.d.ts` line from `node_modules` (the installed version, not the docs' latest) or the docs page for that version.
