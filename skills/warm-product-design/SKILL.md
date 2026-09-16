---
name: warm-product-design
disable-model-invocation: true
description: Found the design language of a product whose value is human warmth and relationships (community, neighbours, family, care, mutual help, gifting, gratitude, faith, newcomer support) — especially one named after a place or object (porch, table, hearth, lantern, letter). Use when a product has no style guide, vocabulary table or design tokens yet and the user asks for a UI style, brand-to-design translation, relational copy, a metaphor-derived design language, switchable tokens, or prompts for v0/Figma AI/Claude. Once a project owns a brand spec and a voice skill, those win — this skill founds, it does not govern.
---

# Warm product design

A methodology for designing products where the core value is **emotional connection between real people**, not transactional efficiency. Built from founding ThanksPorch's design language (a gratitude product centred on a written thank-you card); ThanksPorch appears below only as the worked example. Once a project has its own brand spec, token file and voice rules, those are the facts of record and this skill's job is done.

## Why this skill exists

The default design patterns of modern apps (white backgrounds, Inter font, blue primary buttons, "Submit"/"Cancel" copy, push notifications counting unread items) come from SaaS and e-commerce. They optimize for clarity and conversion. For warm/relational products they actively destroy value — they make the product feel like a platform instead of a place, a transaction instead of a relationship.

Designing well for these products requires a different methodology, not just a different color palette. This skill encodes that methodology.

## When this skill applies

Apply this skill when the product has at least one of these markers:

- **Emotional core**: trust, care, gratitude, belonging, mutual help, family, faith, neighborhood
- **Real relationships**: users are connected offline already, or the product helps deepen offline connections
- **Spatial/sensory name**: the product name suggests a physical place or object (Porch, Table, Hearth, Lantern, Garden, Doorstep, Letter, Kitchen, etc.)
- **Anti-marketplace positioning**: explicitly NOT a marketplace, NOT public, NOT transactional
- **Low frequency, high meaning**: users don't open the app daily, but when they do, it matters

If the product is a productivity tool, dashboard, e-commerce platform, or general utility, this skill is the wrong fit — use a generic frontend design approach instead.

## The methodology — five stages

Do these in order. Each stage builds on the previous one. Skipping ahead (e.g., picking colors before defining the emotional anti-patterns) produces incoherent results.

### Stage 1: Diagnose the emotional core

Before any visual decisions, answer four questions in writing:

1. **What should this product FEEL like?** Give 4–6 sensory or situational keywords (e.g., "a Sunday afternoon", "a handwritten letter", "the porch light on a summer evening"). Aim for physical situations, not abstract adjectives like "modern" or "trustworthy".
2. **What should this product NOT feel like?** Equally specific (e.g., "Amazon", "a hospital intake form", "a Slack notification at 11pm"). Anti-patterns are as important as patterns.
3. **Who is the user in the emotional moment?** Not their demographic — their state of mind. ("Someone who just received help and wants to say thank you but doesn't know how" is a real answer; "millennials in tier-1 cities" is not.)
4. **What is the single emotional climax of the product?** The one moment that, if it lands, makes the product worth existing. (For ThanksPorch: somebody who was helped writes a Thanks Card and hands it over.)

Capture answers in a 1-page "emotional brief" document. Every later decision references this document.

### Stage 2: Extract the metaphor

If the product name contains a spatial or sensory metaphor, **mine it systematically**. The metaphor is a free design language — don't waste it.

See `references/metaphor-extraction.md` for the full process. Quick version:

1. List the physical properties of the metaphor (a porch has: a door, a threshold, a porch light, a railing, screen mesh, seasonal weather, a street view, neighbors passing by).
2. For each physical property, find a product concept it maps to (porch light → user availability status; threshold → semi-public visibility; passing neighbors → pass-through chain).
3. Use these mappings to name features, write copy, and pick visual motifs.

The metaphor map becomes the unifying logic of the entire product. Users will sense the coherence without being able to articulate it.

### Stage 3: Build the vocabulary system

The single highest-leverage design intervention is **substituting transactional language with relational language**. This costs nothing, requires no code changes, and transforms how users experience every screen.

See `references/vocabulary-system.md` for the substitution patterns. Quick version:

- "Submit request" → "Ask softly" or metaphor-specific ("Leave a note on the porch")
- "Accept" / "Decline" → "Yes, it's yours" / "Not this time, maybe next"
- "You have 3 pending requests" → "3 neighbors stopped by"
- "User profile" → "Their porch" / "Their corner"
- Empty states: never say "You haven't added anything yet!" — invite, don't pressure

Rules: use relational language for **emotional moments** (buttons, notifications, empty states, thank-yous). Keep boring functional language for forms and settings. The contrast makes the warm moments feel warm.

### Stage 4: Define the design system

Now and only now, pick concrete visual decisions. Build a complete style guide covering:

- **Colors**: warm-biased palette with reasoning (never just hex values — every choice has an emotional justification)
- **Typography**: typically 3 tiers — a serif for warmth in headings, a humanist sans for body, a handwritten font for emotional peaks (use sparingly)
- **Radius**: organic, not toy-round (typically 14–20px for cards)
- **Shadows**: warm-tinted (use the product's text color base for shadow color, not pure black/gray)
- **Spacing**: generous; default to more whitespace than feels necessary
- **Icons**: outline only, not filled — outline feels hand-drawn, fill feels corporate
- **Photo guidance**: natural light, warm tones, hands holding objects, textured backgrounds (never white-background product shots)
- **Three explicit anti-patterns** specific to this product

See `references/style-guide-template.md` for the full template and reasoning.

### Stage 5: Implement as switchable design tokens

Don't write any page until the design system exists as CSS variables in one file. Then write every page using only `var(--token-name)` — never hardcode colors or fonts.

This makes the entire product theme-switchable later (a single file change rebrands the product), and prevents drift when working with AI tools — every generated component stays consistent because the tokens constrain it.

See `references/design-tokens.md` for the implementation pattern.

## Working with AI tools

This methodology is designed to be executed with AI help (Claude for thinking, v0/Figma AI for generation). The workflow:

1. Use Claude to write the emotional brief, metaphor map, and vocabulary table
2. Use Claude to draft the design token CSS file
3. For every page generation request to v0/Figma AI:
   - **Always paste the full token file** as a prefix to the prompt
   - **Write an "emotion script"** (what the user feels on this page) before any feature spec
   - Forbid the AI from hardcoding any colors, fonts, or radius values

See `references/ai-prompting-workflow.md` for prompt templates.

## Prioritizing pages — emotion weight

Not all pages carry equal emotional weight. When time is constrained, prioritize pages where the emotional design has the highest impact on whether the product succeeds:

| Page | Why it matters most |
|---|---|
| Invite landing page | First impression for new users — they came because of a real person, not a brand |
| Empty states | Where new users decide whether to invest in the product |
| Request initiation dialog | The highest psychological barrier in the product — opening up to ask |
| Thank-you / gratitude moment | The emotional climax — what makes users come back |
| Notifications | Tiny but constantly seen — single biggest source of tone drift |

Design these five before designing anything else. A perfect dashboard with a transactional thank-you screen fails. A rough dashboard with a beautiful thank-you screen succeeds.

## Common failure modes

Watch for these and reject them when they appear in AI output or in your own drafts:

- **Pure white backgrounds** (#FFFFFF or #F5F5F5) — instantly destroys warmth. Use a cream/off-white with a hint of yellow.
- **Cold gray shadows** (`rgba(0,0,0,...)`) — make cards feel like they're floating in a void. Use warm-tinted shadows.
- **Title case button labels** ("Submit Request") — feels like a corporate form. Use sentence case or, for warm products, lowercase metaphor copy.
- **Counting notifications** ("3 new") — feels like a task queue. Replace with "X people are waiting" or similar.
- **Filled icons** — feel corporate and stamped. Switch to outline icons everywhere.
- **Generic "Sign up to continue"** flows — first action should be motivated by the person who invited the user, not by the product.
- **Catchall AI fonts** (Inter, Roboto, Space Grotesk) — overused and emotionally flat. Pick characterful pairings (e.g., Lora + DM Sans + Caveat).

## Reference files

- `references/metaphor-extraction.md` — how to mine a product name for a design language
- `references/vocabulary-system.md` — transactional → relational copy substitution patterns
- `references/style-guide-template.md` — complete style guide structure with reasoning
- `references/design-tokens.md` — CSS variable system for theme-switchable designs
- `references/ai-prompting-workflow.md` — prompts and workflow for v0, Figma AI, Claude
- `for-human/` — Chinese reading copies of the above; agents read the English files only

When applying this skill, **read `metaphor-extraction.md` and `vocabulary-system.md` first** — they're the highest-leverage parts of the methodology. Read the others on demand as the relevant stage comes up.

