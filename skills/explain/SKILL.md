---
name: explain
disable-model-invocation: true
argument-hint: "<method> [ground] <subject>"
description: Explain a mechanism, flow or design of a system with a chosen method (analogy so far), starting from what the reader observes. Argument `ground` adds a code-reading step with file:line pointers. Use when asked to explain how something works, by analogy or another named method.
---

# Explain

Origin: [`readme.md`](readme.md).

## Arguments

`<method> [ground] <subject>`, from the slash command or the invoking prompt; words other than a method name and `ground` name the subject.

- **method**: a row of the table below; with none named, pick the row whose "When" fits the subject.
- **`ground`**: run Ground before the method's steps; the reader cannot check the explanation against the code themselves (typically a system an AI wrote). Without it, define internal names without pointers.

| Method | When | Steps |
|---|---|---|
| `analogy` | a mechanism with actors, order and a failure path | [methods/analogy.md](methods/analogy.md) |

## Reader

Someone who uses the system but did not write its code: they know what it does from the outside, not its internal names. Every method opens with the reader's real scene, in what they can observe.

## Ground

Before writing, read the code that implements the subject. Where code and docs disagree, follow the code and say so. Mark anything you did not verify in code as "(inferred)". Give each internal name a file:line pointer where it is first defined.
