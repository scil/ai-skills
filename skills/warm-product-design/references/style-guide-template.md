# Style guide template

A complete structure for defining a warm-product visual system. Use this template to produce the design decisions that go into the design token file. Every category below should be answered with **specific values plus emotional reasoning** — the reasoning matters because it lets future contributors (human or AI) make consistent extensions.

## How to use this template

Don't just fill in color values. For each section, write:

1. The concrete decision (hex codes, font names, pixel values)
2. The reasoning (why this choice serves the emotional brief)
3. The anti-choice (what was rejected and why)

The anti-choices are as important as the choices. They prevent future drift.

## 1. Color palette

A warm product needs a palette with **three properties**:

- **Warm-biased neutrals**: no pure white, no cold gray. Backgrounds shift toward cream/linen/parchment.
- **Soft primary**: the main brand color should be desaturated enough to feel natural, not LCD-bright. Sage greens, terracottas, dusty blues, and warm tans all work; saturated tech-blues and neons don't.
- **Two-tone accent**: one secondary color used sparingly for emotional peaks (thank-yous, special moments).

### Required color slots

| Slot | Purpose | ThanksPorch example | Why |
|---|---|---|---|
| Primary | Main interactive color (buttons, links) | Sage `#7A9E82` | Desaturated, natural, "garden plant" feel |
| Primary light | Hover states, light fills | Sage Light `#C4D9C8` | Soft elaboration of primary |
| Primary dark | Pressed states | Sage Dark `#4A6E52` | Grounded version |
| Accent | Emotional peaks only (thank-you, etc.) | Terracotta `#C4805A` | Warm earth tone for moments of meaning |
| Accent light | Accent backgrounds | `#E8C4AD` | Soft companion |
| Background | Whole-page background | Cream `#FAF7F2` | Has warmth from yellow undertone — never #FFFFFF |
| Surface | Cards, panels | Linen `#F0EAE0` | Slightly darker than background, layered feel |
| Border | Dividers, card borders | Warm tan `#D4C5B0` | Border with temperature, not a cold gray |
| Text primary | Main text | Ink `#2C2416` | Near-black with brown bias, softer than pure black |
| Text muted | Secondary text | Dust `#7A6E5F` | Warm gray |
| Danger | Errors, destructive actions | Clay `#B85C4A` | Muted terracotta-red — not fire-engine red |

### Anti-choices to call out explicitly

- **No pure white (#FFFFFF)** — destroys warmth instantly
- **No cold grays (`#F5F5F5`, `#E0E0E0`)** — feel like office software
- **No saturated tech blues, neon pinks, electric purples** — these are SaaS signal colors
- **No black text** — `#000000` is harsh; use a warm near-black like `#2C2416`
- **No more than 2 ramps** — warm products are quiet, not chromatic

### Sourcing inspiration

Pick palettes from physical sources: garden plants, kitchen ceramics, old paper, summer evening light, autumn leaves, dried herbs. Avoid screen-native palettes (Material Design, Tailwind defaults, etc.) — they were tuned for productivity, not warmth.

## 2. Typography

A warm product typically needs **three tiers**:

1. **A characterful serif** for headings and quoted moments (warmth, hand-set type feel)
2. **A humanist sans-serif** for body, UI, and forms (legibility without coldness — Inter is too neutral)
3. **A handwriting script** for rare emotional peaks (thank-yous, key one-time messages)

### Required font slots

| Slot | Purpose | ThanksPorch example | Why |
|---|---|---|---|
| Heading | Page titles, card titles, quoted text | Lora (serif, 400 weight) | Soft serif with calligraphic feel, not severe like Garamond |
| Body | All UI, forms, body text | DM Sans (humanist sans, 400/500) | More character than Inter, less branded than Söhne |
| Handwriting | Thank-yous, Thanks Cards, very rare emphasis | Caveat (script, 500/600) | Genuine handwriting feel, not curlicued |

### Font sizing rhythm

| Use | Size | Weight | Font |
|---|---|---|---|
| Page hero | 28–32px | 400 | Heading |
| Card title | 20–22px | 400 | Heading |
| Body | 16px | 400 | Body |
| Small body / metadata | 14px | 400 | Body |
| Tiny labels (UPPERCASE) | 11–12px, letter-spacing 0.08em | 500 | Body |
| Handwriting moment | 22–28px | 500–600 | Handwriting |

Line-height: **1.7 for body text** (warmer than the typical 1.5). This single change makes everything feel more conversational.

### Anti-choices

- **No Inter, Roboto, Arial, system fonts as the primary face** — these are the visual signature of generic AI-generated UI. Pick something with character.
- **No "Title Case Everywhere"** — sentence case only, except for the rare ALL CAPS small label.
- **No font weights above 500** for any major text — heavy weights feel corporate
- **No more than three font families** in the whole product — three is already a lot
- **No script fonts for body text** — the handwriting font is for moments, not paragraphs

## 3. Corner radius

Warm products use **organic, slightly-irregular-feeling** radius. Not toy-bubbly, not corporate-sharp.

| Slot | Value | Use |
|---|---|---|
| Small | 6px | Inputs, small badges, tags |
| Medium | 14px | Buttons, modals, dropdowns |
| Large | 20px | Cards, resource tiles, hero containers |

### Anti-choices

- **No 4px / hard-corner everything** — feels like a spreadsheet
- **No fully-rounded (pill) buttons** unless used specifically — overusing pills makes everything feel like a chat bubble
- **No mismatched radius within one component** — pick one radius per component and stick with it

## 4. Shadows

This is the most-overlooked warmth signal. **Shadows should be tinted with the product's text color**, not pure black or gray.

| Slot | CSS | Use |
|---|---|---|
| Card shadow | `0 1px 4px rgba(44,36,22,0.06)` | Default cards |
| Lifted shadow | `0 4px 16px rgba(44,36,22,0.10)` | Hover, focus |
| Float shadow | `0 12px 40px rgba(44,36,22,0.14)` | Modals, sheets, key dialogs |

The RGB value `44,36,22` is the warm-brown text color of ThanksPorch — for other products, substitute the equivalent warm near-black.

### Why this matters

Cold gray shadows (`rgba(0,0,0,...)`) make cards feel like they're floating in a void. Warm-tinted shadows make them feel like they're sitting on a wooden table in afternoon light. Same opacity, opposite emotion.

### Anti-choices

- **No pure black shadows** — `rgba(0,0,0,...)`
- **No multi-color glow effects** — neon shadows belong in gaming UI
- **No `box-shadow: 0 4px 8px rgba(0,0,0,0.1)`** (the universal Tailwind default) — replace with the warm version

## 5. Spacing

Warm products need **more whitespace than feels necessary**. The default density of SaaS is wrong here. Aim for porch-like spaciousness.

| Token | Value | Use |
|---|---|---|
| xs | 4px | Icon internal padding |
| sm | 8px | Tight element spacing |
| md | 12px | Related items |
| lg | 16px | Card internal padding |
| xl | 24px | Paragraph spacing |
| 2xl | 32px | Module spacing |
| 3xl | 48px | Section spacing |
| 4xl | 64px | Page top padding |

### Rules

- **Mobile side margins: 20px minimum** — don't crowd the edges. The whitespace at the edge is "porch step" space.
- **Body line-height: 1.7** — not 1.5. The looser line-height makes text feel like conversation.
- **Empty states get extra padding** — empty doesn't mean cramped.

## 6. Icon style

Use **outline icons only**, with a stroke weight around 1.5px. Avoid filled icons entirely.

### Why outline

Outline icons feel sketched, hand-drawn, light. Filled icons feel printed, official, corporate. The same icon as outline vs filled changes the entire perceived tone.

### Recommended set

[Tabler Icons](https://tabler.io/icons) (outline variants) is a strong default — 5000+ icons, consistent stroke, free. Other good outline sets: Lucide, Feather, Phosphor (regular weight).

### Sizing

- Inline with text: 16px
- Card-level: 20px
- Nav level: 24px (max)
- Decorative: never larger than 24px — bigger icons feel like ads

### Coloring

- Default: text primary color (warm near-black)
- On primary button: white
- Emotional icons (heart, sparkle, leaf): primary color (sage, terracotta)
- Status icons: semantic (success/danger), but use the warm versions of those colors

### Anti-choices

- **No filled icons** — corporate stamp feel
- **No 2D-3D mixed icon sets** — pick one style, stick with it
- **No emoji as icons in production UI** — emoji are inconsistent across platforms and break the visual language

## 7. Photography and illustration

The single biggest source of warmth (or lack thereof) is **the photography**. A cold product photo destroys hours of warm UI design.

### Photography rules

- **Natural light, warm tones**: photograph items in daylight, post-process slightly warm (not overexposed white-balance)
- **Hands holding objects**: a hand cradling a mug conveys more than the mug alone. Encourage users to include hands in their own uploads.
- **Textured backgrounds**: wood, linen, tile, brick, grass — never white seamless backgrounds (those are e-commerce signals)
- **Imperfect framing**: slightly off-center, with extra context (a corner of a table, a window in the background). Magazine-perfect framing reads as marketing.
- **Avatars**: real photos when possible, warm-tinted. When using initials, place on the primary color circle (never gray) — every person should feel like a real person, not a placeholder.

### Illustration rules

- Use illustrations with **hand-drawn line quality**, not 3D vector geometric figures
- Reference styles: botanical sketches, mid-century children's books, woodblock prints
- Avoid: 3D rendered isometric, gradient-filled flat illustrations (the "Corporate Memphis" style), AI-generated illustration in default styles

### Anti-choices

- **No stock photo people in business attire** — even if they're laughing
- **No white-background product shots** — turns warmth into Amazon
- **No 3D rendered illustrations** — they feel optimized, not handmade
- **No gradients in illustrations** — flat fills only

## 8. Three explicit anti-patterns

Every style guide should end with **three concrete anti-patterns** specific to this product. These are the things that, if they appear, indicate the design has drifted. Listing them explicitly creates a checkpoint for reviews.

For ThanksPorch, the three are:

1. **Pure white or cold gray backgrounds** — instantly converts "porch" into "App"
2. **Transactional button copy paired with transactional button styling** — "Submit request" in saturated blue rectangle compounds the problem; replace both at once
3. **Pressuring empty states and notifications** — "You haven't added any resources yet!" undoes all the work; rewrite as invitations

For each new product, identify the three highest-risk failure modes and write them down.

## Output

After completing this template, the output should be:

1. A **filled-in style guide document** (markdown or web page)
2. A **complete design token file** (CSS variables — see `design-tokens.md`)
3. A **list of three product-specific anti-patterns** committed to the team

This becomes the prerequisite artifact for any page design or AI-generated UI.
