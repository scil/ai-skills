# Locate

Find where a behaviour lives in code the reader did not write, and hand back one entry point for a trace. Always grounded: run [Ground](../SKILL.md#ground) first, with or without the argument.

1. **Behaviour.** Restate the subject as one behaviour the reader can observe: what starts it, and what they see or hear after. When the subject covers several, name them and ask which.
2. **Triggers.** Every outside trigger that starts it: commands, timers or loops, incoming events (input, messages, requests), the tests that exercise it, and the commit that added it. Read the repository's own maps first (architecture docs, code indexes, plan progress) where they exist. Each trigger with file:line and one line on what starts it.
3. **Spine.** The 3–7 functions that do the real work, in the order one run reaches them. Each with file:line, one sentence in the reader's observable terms, and its other callers (search for them): a function shared with another path changes what an edit to it touches.
4. **Modules.** Each module the spine crosses, one line on its job.
5. **Entry.** Recommend one entry point and one scenario through it, with the reason, as the input to [trace](trace.md) or [diagram](diagram.md) step 4. Stop here: the call tree belongs to that method.

Done when every trigger found either leads to a spine function or is named as unrelated.
