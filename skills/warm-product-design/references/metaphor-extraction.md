# Metaphor extraction

A method for turning a product name (or core concept) into a complete design language. Use this when the product name contains a spatial, sensory, or domestic metaphor that can be mined for visual and interaction logic.

## Why metaphor matters

A metaphor that's only used in marketing copy is shallow. A metaphor that drives feature naming, copy, visual motifs, and interaction patterns becomes the **unifying logic** of the product. Users sense the coherence without being able to articulate it — every screen reinforces every other screen.

Conversely, a product that has a metaphor in its name but doesn't extend it into the design wastes its strongest asset. ThanksPorch could be a generic resource-sharing app with a cute name, or it could be a product where users genuinely feel they're standing on a porch. The methodology below produces the second outcome.

## The extraction process

### Step 1: Inventory the physical properties

List every concrete property of the metaphor — physical objects, sensory qualities, social conventions, temporal patterns. Don't filter; aim for 15+ items. The goal is raw material.

For ThanksPorch, the inventory includes:

- A door (entry to the private space)
- A threshold (the boundary between public and private)
- A porch light (signals welcome / availability)
- A railing (defines the space, allows leaning and chatting)
- Screen mesh (lets air through, lets sight through partially)
- Wooden floorboards (worn, walked on, familiar)
- A doormat or welcome mat
- Chairs or a bench (suggests sitting, lingering)
- Plants in pots
- A house number / address
- Mail or packages left at the door
- Things left out for others (a bowl of candy, a free pile, garden vegetables)
- Neighbors passing by on the street
- Seasonal weather (porch is half-indoor, half-outdoor — seasons matter)
- Time of day (porch light at evening, sunlight in afternoon)
- Sound of knocking
- The convention of "stopping by"
- Lemonade in summer
- The way porches face the street, not the backyard
- Holiday decorations

### Step 2: Map physical properties to product concepts

For each physical property, ask: *what existing or potential product concept does this map to?* Some will map directly, some will spark new feature ideas, some won't map at all (discard those).

Example mapping for ThanksPorch:

| Physical property | Product concept |
|---|---|
| Door | Entry into private profile / settings |
| Threshold | Semi-public visibility (Porch Visible) — not street, not living room |
| Porch light | User availability indicator (on = open to requests, off = not now) |
| Railing | Section dividers in the UI |
| Screen mesh | Visual texture for "limited visibility" states (can see, can't enter) |
| House number | The unique Porch Invite link / QR code |
| Things left out | Resources / items being shared |
| Passing neighbors | Pass-through chain — visitors who continue past your porch |
| Knocking | Initiating a request |
| Time/season | Availability windows (effectiveAvailability) |
| Faces the street | Half-public stance — visible to those who walk by, not searchable to the world |

This table becomes the **conceptual spine** of the product. Reference it whenever naming features, writing copy, or designing visuals.

### Step 3: Derive copy from the mapping

Use the mapped concepts to generate concrete UI copy. The metaphor gives you specific verbs, nouns, and phrases that no generic SaaS product can match.

From the mapping above:

- "Submit request" → "Leave a note on the porch"
- "Available for requests" → "Porch light is on"
- "Not available right now" → "Inside today"
- "Pending requests inbox" → "Who stopped by"
- "Share link" → "Give them your porch address"
- "Public marketplace" (rejected concept) — explicitly NOT this, because porches face the street but aren't streets

See `vocabulary-system.md` for how to structure these into a complete substitution table.

### Step 4: Derive visual motifs from the mapping

Pick 3–5 physical elements that can become recurring visual motifs. **Use them sparingly** — overuse kills the meaning. The motifs should appear in specific, semantically-loaded places, not as decoration everywhere.

From ThanksPorch:

| Motif | Where it appears | Why there |
|---|---|---|
| Porch light (small glowing dot) | User availability status indicator | Direct semantic match — light = welcome |
| Railing pattern (horizontal slats) | Section dividers between content areas | Echoes the spatial sense of being on a porch |
| Screen mesh texture | Backgrounds of "restricted visibility" cards | Visually conveys "you can see through but not into" |
| Wood grain (subtle) | Porch homepage background only | Reinforces the spatial metaphor in the one place users dwell |
| Handwritten script | Thank-you moments only | Echoes the convention of handwritten notes left on doors |

The discipline of "this motif appears here and nowhere else" is what gives each motif weight. A porch light icon on every screen becomes decoration. A porch light icon only on the availability toggle becomes meaning.

## Working with other product names

The same process works for any metaphorical product name. Quick examples:

**Hearth** (hypothetical family communication app):
- Physical: fire, warmth radiating outward, gathering around, embers, stoking, hearthside conversation, the mantel, photos on the mantel
- Maps: family member presence → glow intensity around their avatar; archived memories → mantel; recent conversations → fire (active); old conversations → embers (still warm but quieter); "stoke" → bumping a thread back up
- Visuals: warm amber glow, embers-fading-to-gray timeline visualization, photo frames as memory containers

**Lantern** (hypothetical mental health journaling):
- Physical: light in darkness, carried by hand, fuel reserves, dimming and brightening, casting shadows, guiding the way
- Maps: journaling streak → fuel level; difficult days → low light, easier days → bright; private vs shared entries → covered vs uncovered lantern
- Visuals: warm yellow glow, dark-mode-first (lanterns work at night), gentle fade animations

**Doorstep** (hypothetical neighborhood favor app):
- Physical: the place between inside and outside, leaving things, finding things, stepping out briefly, the welcome mat
- Maps: very similar to Porch but smaller scale — emphasis on quick favors rather than ongoing relationships

The process is always: **inventory → map → derive copy → derive visuals**, in that order.

## Pitfalls to avoid

- **Don't force every property to map.** Some physical properties won't have a useful product analog. Discard them. Forcing maps creates contrived features.
- **Don't make the metaphor literal.** A skeuomorphic porch app with wood textures everywhere is worse than a clean app that uses the metaphor in copy and a few key motifs. The metaphor should be felt, not depicted.
- **Don't let the metaphor lock you out of necessary functionality.** If users need a settings page, they need a settings page — call it "House rules" or just "Settings", but don't refuse to build it because porches don't have settings panels.
- **Don't overuse motifs.** Five motifs used in five specific places beats five motifs used everywhere. Sparseness is what makes each one meaningful.
- **Don't mix metaphors.** If the product is Porch, don't pull in unrelated metaphors (campfire, library, etc.). One metaphor, fully extracted, beats three half-extracted ones.

## Output of this stage

After running this process, you should have three artifacts:

1. A **physical inventory** (15+ items)
2. A **concept mapping table** (physical → product, ~10 rows)
3. A **motif plan** (3–5 visual motifs with specific placement rules)

These three artifacts feed directly into the vocabulary system (next reference) and the style guide.
