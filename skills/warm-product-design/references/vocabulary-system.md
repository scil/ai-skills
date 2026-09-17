# Vocabulary system

A method for systematically replacing transactional language with relational language across the entire product. This is the **highest-leverage** design intervention available — it costs nothing, requires zero code changes, and transforms how users emotionally experience every screen.

## The core principle

Every product is taught how to behave by its language. When a button says "Submit", users approach it as paperwork. When it says "Ask softly", they approach it as a conversation. The functional outcome is identical; the emotional outcome is opposite.

Generic SaaS vocabulary ("Submit", "Cancel", "Pending", "Accept", "Reject", "Profile", "Dashboard", "Notifications") was developed for productivity tools and e-commerce. Using it in a warm/relational product is **vestigial** — it's there because designers copy other apps, not because it serves the product.

## The substitution rules

### Rule 1: Use relational language at emotional moments, plain language elsewhere

Don't try to make every label poetic. The contrast is what makes the warm moments feel warm.

- **Use relational language for**: primary action buttons, notifications, empty states, thank-you screens, welcome moments, request initiation, request acceptance/decline, status indicators, page headers on key journeys.
- **Use plain language for**: form field labels (Email, Phone, Address), settings toggles, error messages about invalid input, technical confirmations ("Saved"), navigation labels (when no good metaphor exists, just say "Settings").

If you make every word poetic, the product feels twee and users lose trust. Reserve poetry for moments that earn it.

### Rule 2: Lead with the person, not the action

Almost every transactional notification can be rewritten by mentioning the person first.

- "You have 3 new requests" → "3 people are waiting to hear back from you"
- "Request approved" → "Sarah is on her way"
- "Message received" → "Michael left you a note"
- "New invitation" → "Ana invited you to her porch"

The grammatical structure carries emotional weight. Subject-as-person feels human; subject-as-system feels bureaucratic.

### Rule 3: Use the product's metaphor as a vocabulary source

If the metaphor extraction process has been done (see `metaphor-extraction.md`), the metaphor itself provides the vocabulary. Use it directly:

- Porch: leave a note, porch light on, leave something on the porch, neighbor stopped by
- Hearth: stoke, glow, gather, ember
- Lantern: light a lantern, dim, carry, guide

If a substitution can be made using the metaphor's vocabulary, it almost always should be — the alignment between language and visual metaphor is what creates the unified product feel.

### Rule 4: Replace counts with people

Number-counting is a marketplace pattern ("3 messages", "5 unread", "12 pending"). Warm products express the same information with human framing.

- "3 unread" → "3 people are waiting"
- "5 items in your cart" — n/a, warm products don't have carts
- "12 pending requests" → "12 neighbors hoping to hear from you"
- "0 items" → empty state with metaphor (not a zero)

### Rule 5: Make refusal kind

The single most-overlooked opportunity in warm products is the **rejection flow**. Most products make rejection brutal because they were designed for utility, not relationship.

- "Reject" / "Decline" → "Not this time, maybe next"
- "No, thanks" → "Maybe another day"
- Add structured kind reasons: "Someone else got there first" / "I'm out of town" / "Saving this for family" — and have the system phrase the auto-message kindly.

If a user rejects a request, the requester should receive a message that protects the relationship. The default "Your request was declined" sounds like an apartment application. "Sarah said she's saving it for family — maybe another day" sounds like a neighbor.

### Rule 6: Empty states invite, don't pressure

Empty states are where new users decide whether to invest. The default pattern ("You haven't added anything yet! Get started →") is pressuring. The warm pattern is to describe the empty state as a feature, not a deficiency.

- "You haven't added any resources yet!" → "Your porch is quiet today. When you're ready, you can put something out."
- "No buddies yet — invite friends!" → "Your circle hasn't formed yet. People will arrive."
- "No requests" → "Quiet morning."

The shift is: from "you should be doing more" to "what's here is fine, and more will come when it does."

### Rule 7: Onboarding asks for permission, not for completion

- "Complete your profile (3/5 steps)" → "Tell us a little about yourself, when you have time"
- "Verify your email" → "We'd love to send you the occasional note — confirm your email when you can"
- Progress bars on onboarding → remove. They turn welcomes into checklists.

## The substitution table

For each product, build a comprehensive substitution table during the design phase. Use this as the source of truth for all copy. Below is the porch example's table as a worked example — replicate this structure for any warm product.

| Transactional (generic SaaS) | Relational (warm product) | Where it appears |
|---|---|---|
| Submit request | Leave a note on the porch | Primary CTA on request flow |
| Accept | Yes, it's yours | Owner's acceptance button |
| Decline | Not this time, maybe next | Owner's decline button |
| Pending | Waiting to hear back | Request status |
| Approved | On its way | Post-acceptance status |
| You have 3 requests | 3 neighbors stopped by | Inbox header |
| Notifications | What's happening | Header |
| Profile | Your porch | Tab label / nav |
| Dashboard | Home (or just the porch view) | Main screen |
| Add resource | Put something on the porch | Button |
| Available | Porch light is on | Status indicator |
| Unavailable | Inside today | Status indicator |
| Invite link | Your porch address | Sharing UI |
| Friends / Connections | Buddies / Neighbors | List label |
| Public visibility | Visible from the street | Privacy setting (rejected; use Porch Visible instead) |
| Private visibility | Just for you | Privacy setting |
| Send | Send (or "Leave it") | Form submit |
| Submit comment | Leave a note | Comment action |
| Rating | — (remove entirely) | Don't rate humans |
| Review | A note of thanks | Post-transaction action |
| Settings | Settings (keep plain) | Nav |
| Help center | If something's not right | Support |
| Sign up | Come on in | New user flow |
| Sign in | Welcome back | Returning user |
| Log out | See you later | Logout |
| Delete account | Take down your porch | Settings → danger zone |
| Error: invalid input | (Keep plain — errors shouldn't be cute) | Form validation |

## Building your own substitution table

For each new warm product:

1. List every UI string in the product (or every string in the main flows)
2. Identify which ones occur at emotional moments (Rule 1)
3. For each emotional one, write 2–3 candidate replacements drawing from the product's metaphor
4. Pick the one that feels most natural read aloud — if a phrase sounds embarrassing spoken to a friend, reject it
5. Test the table by reading three sample screens with the new vocabulary — if it sounds like a parody, dial back; if it sounds like a slightly more thoughtful friend, you've got it right

## The read-aloud test

The single best test for warm-product copy: **read it aloud as if you were saying it to a friend you respect**.

- "Submit your request to access this resource." — would never say this. Reject.
- "Want to ask Sarah about the chair?" — could say this. Accept.
- "Your porch is glowing this evening!" — overdoing it. Reject (this is parody, not warmth).
- "Your porch is quiet today." — could say this. Accept.

The line between "warmer than typical SaaS" and "embarrassingly twee" is narrow. The read-aloud test catches both sides.

## Common failure modes

- **Twee overreach**: Every label has an emoji, every empty state has a haiku, every error message is a poem. Result: feels infantilizing. Fix: reserve warmth for emotional moments, keep functional language plain.
- **Inconsistent register**: Some buttons say "Leave a note on the porch", others say "Submit request" in the same flow. Result: feels like two products glued together. Fix: build the full substitution table before shipping.
- **Metaphor mismatch**: Using porch vocabulary in features that aren't porch-shaped (e.g., calling a settings menu "house rules" when it's really just a list of toggles). Result: feels forced. Fix: only metaphor-substitute where the mapping is genuine.
- **Pushy empty states**: "Your porch is quiet — invite friends now!" undoes all the work. Fix: empty states must invite without pressuring. If there must be a CTA, make it small and secondary.
- **Cold rejection paths**: A beautiful request flow that ends with "Your request has been declined" wipes out everything. Fix: design the decline path with the same care as the accept path. Often more.

## Integration with other stages

The vocabulary system is used by:

- **Style guide** (`style-guide-template.md`): button labels and example UI strings come from here
- **Page design** (mockups, prototypes, v0 prompts): copy on every screen pulls from this table
- **AI prompting** (`ai-prompting-workflow.md`): the substitution table is included in v0/Figma AI prompts so generated pages start with correct vocabulary

Build the table early. Update it as new flows are designed. Treat it as a versioned artifact, not a one-time exercise.
