# Diagram

One picture of the whole; on request, the same picture failing, the call order inside it, and a page stepping through it.

By default run only steps 1–2. Steps 3–5 run when the request asks for them, with the overview or alone. An interactive page alone still needs step 4's analysis, shown only on the page.

1. **Draw** the subject as one diagram of at most 5 boxes (Mermaid unless the host renders another format better). Name boxes in the reader's observable terms where one exists, and mark the entry: where the reader's action or the outside event comes in. When the subject needs more boxes, group it into 5 or fewer and name the box worth zooming into; a zoom is a new diagram of that box under the same rules, never a sixth box. Under the diagram, list what was left out to stay at 5. More arrows than boxes plus 2 means the grouping is wrong: regroup.
2. **Arrows.** Number the arrows in the order of one typical run (①②③…). One sentence per arrow, in that order: what travels along it, and what sends it.
3. **Failure** (when the request asks what goes wrong, or for the full set). Draw the same diagram with one thing going wrong, the most likely or most costly failure; say which boxes and arrows change and what the reader would observe.
4. **Call order** (when the request asks for the flow, the call order, who calls whom, or the full set). Grounded, as in [trace](trace.md): a second diagram (a sequence diagram unless branching dominates), of the functions behind the boxes, showing who calls whom, where control passes, and where it branches or forks. Every name in it gets a plain gloss beside the diagram; each key step gets its code excerpt (a few lines, with file:line).
5. **Interactive** (when the request asks for it or for the full set, and the host can publish a page). Build it as a page that steps through the flow one arrow at a time, highlighting the active box and showing that step's gloss and excerpt; motion only for that stepping.
