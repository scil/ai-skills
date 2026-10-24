# Trace

Follow one concrete scenario through the code like a debugger. Always grounded: run [Ground](../SKILL.md#ground) first, with or without the argument.

1. **Scenario.** The one the user gave; otherwise the most common path through the subject, named before tracing. One scenario only.
2. **Trace.** Numbered steps, one per hand-off that matters; merge trivial calls. Each step gives:
   - (a) the function running, with file:line;
   - (b) the values that matter, taken from a test, fixture, log or an actual run where one exists, otherwise marked "(inferred)";
   - (c) side effects: storage writes, messages sent, output shown or spoken;
   - (d) where control goes next, and why.
3. **Next reads.** The 3 files or functions to read next, each with the reason.
4. **Risky step.** The one step where a bug most likely hides, with the reason: a branch, shared state, a timing assumption, an untested path.
