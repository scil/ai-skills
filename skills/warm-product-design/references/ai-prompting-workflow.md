# AI prompting workflow

How to use AI tools (Claude, v0, Figma AI) to actually generate warm-product UI without falling into generic SaaS patterns. This is a workflow document — read it whenever using AI to produce pages or components.

## The core problem

AI tools are trained on the entire internet, which means their default outputs reflect **average SaaS aesthetics** — white backgrounds, Inter font, blue primary buttons, "Submit" copy. Without constraints, they will regress every warm product into a generic SaaS dashboard.

The solution is to **front-load every prompt with constraints** — the design tokens, the vocabulary substitution table, and the emotional brief. With these constraints, AI tools become useful collaborators. Without them, they pull the design toward the mean.

## The three-prompt workflow

For any page or component, use three prompts in sequence — each from a different tool, each doing what it does best.

### Prompt 1: Claude — write the "emotion script"

Before any visual generation, ask Claude to write the **emotional state script** for the page. This is *not* a feature spec.

Example prompt:

```
For the ThanksPorch project (warm relational product where users share
resources with neighbors), write the emotional script for the "Thank-you
moment" page.

The emotional script should describe:
- The user's emotional state arriving at this page
- The one feeling we want them to leave with
- What they need to see in what order
- What they should NOT see
- The single most important UI element on the page and why

Do NOT describe colors, fonts, layout grids, or specific components.
Just describe the emotional logic.
```

Claude returns something like:

> The user is the sharer. Someone they helped has just confirmed receipt of a resource. The user's state arriving is neutral-curious — they got a notification, they opened it. The state we want them to leave with is "warmth received" — a small, genuine sense of having made a difference.
>
> What they need to see first: the recipient's note. Not their name, not the resource, the note. The note is the gift. Everything else is context.
>
> What they need to see second: who wrote it (small avatar, name). This grounds the message.
>
> What they should NOT see: any "share this!" call to action, any stats ("you have given 3 gifts this month"), any prompt to do more. The moment is sacred — leave them in it.
>
> The single most important UI element is the recipient's note, rendered in handwriting font, large, centered, with negative space around it. Everything else is supporting cast.

This script is now the **brief** for the next two prompts.

### Prompt 2: Claude — generate the spec with constraints

Now ask Claude to translate the emotion script into a specific component spec, using the design tokens and vocabulary table.

Example prompt:

```
Using the ThanksPorch design tokens [paste tokens] and vocabulary table
[paste table], translate this emotion script [paste script from prompt 1]
into a concrete component spec for v0.

The output should include:
- Layout structure
- Specific tokens for each element (background, text color, font, radius, shadow, spacing)
- Exact copy for any text (using the vocabulary table)
- Any required interactions
- A note on what NOT to include

Do not include any hex codes, font names, or pixel values — only token references.
```

Claude returns a structured spec with token names. This is what gets sent to v0.

### Prompt 3: v0 — generate the implementation

Now hand the spec to v0 with the tokens as the first constraint:

```
Build a React component using the following design tokens. You MUST use
var(--token-name) for every color, font, radius, shadow, and spacing
value. Do NOT hardcode any visual values.

Design tokens:
[paste full tokens.css]

Component spec:
[paste spec from prompt 2]

Constraints:
- Use only Tailwind utility classes mapped to the tokens, or inline style
  with var() references
- Use Lora for any serif heading (--font-heading)
- Use DM Sans for body (--font-body)
- Use Caveat ONLY where the spec says handwriting (--font-handwrite)
- Background must be var(--color-background), not white
- Buttons must be var(--color-primary) with white text, radius var(--radius-md)
- No filled icons — only outline (use lucide-react)
```

v0 generates the component. Because the tokens constrain it, the output is on-brand instead of generic.

## Why three prompts and not one

The temptation is to send everything to v0 at once ("here are tokens, here are vocab, build me a page"). This fails because:

1. v0 (and Figma AI) are good at translating specs into code, but bad at the upstream creative thinking
2. Claude is good at emotional logic and copy, but generates lower-fidelity visuals
3. Splitting the work plays to each tool's strengths

Three prompts also create a **review checkpoint** between each stage. You can correct the emotion script before committing to a spec, and correct the spec before generating code. Without the checkpoints, errors compound.

## The token prompt prefix

For any v0 or Figma AI generation, prepare a **standard prefix** that you paste at the start of every prompt. This prefix never changes, so it can be copy-pasted reliably.

Template prefix:

```
You are designing components for [PRODUCT NAME], a [one-sentence positioning].

Required design tokens (use var(--name) — never hardcode):

[paste full tokens.css here]

Required vocabulary (use these phrasings exactly when generating copy):

[paste relevant vocabulary substitution rows]

Required constraints:
- Background is var(--color-background) — never white
- Body line-height is 1.7
- Buttons: primary action uses var(--color-primary), radius var(--radius-md)
- Icons: outline only (lucide-react, Tabler outline, or Phosphor regular)
- Typography: heading uses var(--font-heading), body var(--font-body)
- No filled icons, no Inter/Roboto fonts, no rgba(0,0,0,...) shadows
- Sentence case for all UI text, never Title Case

Anti-patterns to avoid:
[list the 3 product-specific anti-patterns]

Now build the following:
[component description]
```

Paste this prefix before every new component request. The first prompt of a session sets the constraints; every subsequent prompt benefits from a fresh paste because chat memory drifts.

## Iterating after generation

When v0 returns output that's almost right but drifted, **don't ask for general changes**. Ask for token-specific changes.

- ❌ "Make it feel warmer"
- ✅ "Replace the bg-white class with style={{background: 'var(--color-background)'}}, and change font-sans to font-serif on the heading"

Specific, token-referenced corrections work. Vague tonal feedback doesn't, because the AI doesn't know which knob to turn.

## Common AI failure modes and corrections

| Failure | Why it happens | Correction prompt |
|---|---|---|
| Used `bg-white` instead of token | Tailwind default | "Replace bg-white with bg-[var(--color-background)] or inline style" |
| Used Inter font | Most common training default | "Change font-family to var(--font-heading) for headings and var(--font-body) for body" |
| Used filled icons | Default Lucide icons are mixed | "Replace all filled icon variants with outline versions (e.g., HeartIcon → Heart from lucide-react outline)" |
| Used "Submit" copy | Form convention | "Replace 'Submit' with [vocabulary-table entry]. Replace 'Cancel' with [entry]." |
| Used title case | Common style preset | "Use sentence case throughout — only the first word of each label is capitalized" |
| Used rgba(0,0,0,...) shadow | Tailwind defaults | "Replace shadow color with var(--shadow-card) reference" |
| Used hard-coded hex values | Direct hex feels easier to the AI | "Replace every hex value with a var(--color-*) reference from the tokens" |
| Counted notifications ("3 new") | Generic SaaS pattern | "Rewrite the notification as 'X people are waiting' or similar — see vocabulary table" |

## When NOT to use AI generation

Use AI for:
- Generating component structures from specs
- Drafting copy variations
- Translating emotion scripts to layouts
- Generating boilerplate (forms, lists, etc.)
- Producing illustrative SVGs

Don't use AI for:
- **The original emotion script** — this is the human's call, AI can help articulate but shouldn't originate
- **The metaphor extraction** — needs human taste and product knowledge
- **The vocabulary table** — needs the human to read each row aloud and accept/reject
- **Choosing the brand colors** — AI suggestions tend toward training-mean palettes; human curation matters here
- **Reviewing the final result** — automated checks miss the emotional drift that's the whole point

## Working with Claude specifically

Claude (this assistant) is well-suited for:
- Writing the emotional brief
- Extracting the metaphor
- Generating vocabulary substitutions
- Producing the design token file from style decisions
- Reviewing v0 output for drift from constraints

When asking Claude for these things, give it:
- The product positioning paragraph
- Any prior decisions already made (tokens, copy)
- The specific output format you want

Claude is less suited for:
- Producing pixel-perfect visual mockups (use Visualizer for sketches, v0 for code)
- Generating Figma files (use Figma AI directly)
- Producing photography or illustration (use image generation tools, but with explicit warm-product anti-patterns in the prompt)

## Saving the artifacts

Across a project's life, accumulate these artifacts in a `design-system/` folder:

```
design-system/
  emotional-brief.md           ← Stage 1 output
  metaphor-map.md              ← Stage 2 output
  vocabulary.md                ← Stage 3 output
  style-guide.md               ← Stage 4 output (filled template)
  tokens.css                   ← Stage 5 output (the actual code)
  emotion-scripts/             ← one per page
    landing.md
    empty-state.md
    thank-you.md
    request-dialog.md
    notification.md
  prompts/
    v0-prefix.txt              ← the standard token+vocab prefix
```

This makes the design system reproducible and lets new contributors (human or AI) get up to speed quickly.
