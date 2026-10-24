---
name: explain
disable-model-invocation: true
argument-hint: "<method> [ground] <subject>"
description: Explain a mechanism, flow or design of a system, or test the user's grasp of it, with a chosen method — analogy, layers, locate, trace, diagram, socratic, teach-back. Argument `ground` adds a code-reading step with file:line pointers. Use when asked to explain how something works, to find where a behaviour lives in unfamiliar code, to walk through a scenario, or to quiz or check the user's understanding.
---

# Explain

Origin: [`readme.md`](readme.md).

## Arguments

`<method> [ground] <subject>`, from the slash command or the invoking prompt; `ground` may stand anywhere, and the words other than a method name and `ground` are the subject.

- **method**: a row of the table below; with none named, pick the row whose "When" fits the request and say which.
- **`ground`**: run Ground before the method's steps; the reader cannot check the explanation against the code themselves (typically a system an AI wrote). Without it, define internal names without pointers. `locate`, `trace` and a diagram's call order always ground.

| Method | When | Reader | Steps |
|---|---|---|---|
| `analogy` | a mechanism with actors, order and a failure path | default | [methods/analogy.md](methods/analogy.md) |
| `layers` | first contact with a system or concept | beginner | [methods/layers.md](methods/layers.md) |
| `locate` | code the reader did not write: they can name a behaviour, not an entry point | default | [methods/locate.md](methods/locate.md) |
| `trace` | the code reads fine, but how it runs is unclear | default | [methods/trace.md](methods/trace.md) |
| `diagram` | the whole picture at a glance; on request its failure, call order, interactive page | default | [methods/diagram.md](methods/diagram.md) |
| `socratic` | the user wants to master it, not just follow | beginner | [methods/socratic.md](methods/socratic.md) |
| `teachback` | the user explains it and wants the gaps found | default | [methods/teachback.md](methods/teachback.md) |

## Reader

**Default**: someone who uses the system but did not write its code: they know what it does from the outside, not its internal names. **Beginner**: also new to the domain, so domain terms need the same care as internal names. Methods that explain open with the reader's real scene, in what they can observe. Plain, concrete words; one idea per paragraph.

## Ground

Before writing, read the code that implements the subject. Where code and docs disagree, follow the code and say so. Mark anything you did not verify in code as "(inferred)". Give each internal name a file:line pointer where it is first defined.
