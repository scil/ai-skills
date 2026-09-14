# Design tokens

A pattern for implementing the style guide as **CSS variables in a single file**, so the entire product can be re-themed by editing one file. This is essential for warm products because:

1. You don't yet know if your style decisions are right — and you want to be able to A/B test or replace them later without rewriting every component.
2. Warm products often need **user-customizable themes** (the product itself supports per-user or per-Porch theming).
3. Working with AI tools requires a token file as the source of truth — without it, every generated component drifts in style.

## The structure

### Option A: Single token file (simplest)

```css
/* tokens.css */
:root {
  /* Brand colors */
  --color-primary: #7A9E82;
  --color-primary-light: #C4D9C8;
  --color-primary-dark: #4A6E52;

  --color-accent: #C4805A;
  --color-accent-light: #E8C4AD;

  /* Surfaces */
  --color-background: #FAF7F2;
  --color-surface: #F0EAE0;
  --color-border: #D4C5B0;

  /* Text */
  --color-text: #2C2416;
  --color-text-muted: #7A6E5F;
  --color-danger: #B85C4A;

  /* Typography */
  --font-heading: 'Lora', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-handwrite: 'Caveat', cursive;

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 14px;
  --radius-lg: 20px;

  /* Shadows */
  --shadow-card: 0 1px 4px rgba(44, 36, 22, 0.06);
  --shadow-lifted: 0 4px 16px rgba(44, 36, 22, 0.10);
  --shadow-float: 0 12px 40px rgba(44, 36, 22, 0.14);

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 24px;
  --space-2xl: 32px;
  --space-3xl: 48px;
  --space-4xl: 64px;

  /* Line height */
  --line-body: 1.7;
  --line-tight: 1.3;
}
```

Import this file once at the app root. Every component uses `var(--color-primary)` etc. — never hardcoded values.

### Option B: Multiple theme files (for theme switching)

```
styles/
  tokens.css        ← imports the active theme
  themes/
    warm.css       ← ThanksPorch default warmth
    minimal.css    ← Alternative cleaner theme
    dark.css       ← Dark mode variant
    organization.css ← For organization Porches
```

`tokens.css` imports the active theme:

```css
@import './themes/warm.css';
```

To change the global theme, change which file is imported. To support per-user themes, swap the import or use the runtime approach below.

### Option C: Runtime theme switching (for in-product theme picker)

This pattern lets users (or admins) switch themes without rebuilding. Set a `data-theme` attribute on `<html>` or `<body>`:

```css
:root,
[data-theme="warm"] {
  --color-background: #FAF7F2;
  --color-primary: #7A9E82;
  /* ... rest of warm theme */
}

[data-theme="minimal"] {
  --color-background: #FFFFFF;
  --color-primary: #3B82F6;
  /* ... rest of minimal theme */
}

[data-theme="dark"] {
  --color-background: #1C1C1E;
  --color-primary: #9DBBA3;
  /* ... rest of dark theme */
}
```

Switching at runtime:

```javascript
document.documentElement.setAttribute('data-theme', 'minimal');
```

This is the approach to use if the product itself supports user-customizable themes (e.g., users can choose their Porch's color palette, organizations can set branded themes).

## Rules for component authors

Once tokens exist, **enforce these rules** when writing any component:

1. **No hardcoded colors** — every color value in component CSS must be `var(--color-*)`. Lint rules can enforce this.
2. **No hardcoded fonts** — every `font-family` must be `var(--font-*)`.
3. **No hardcoded radius/shadow** — same rule.
4. **Spacing can use `var(--space-*)` OR rems** — token names are preferred for warm-meaningful spacing (card padding, section gaps), rems are fine for one-off layout adjustments.
5. **Numbers used in calculations are fine** as raw values (z-index, opacity, animation timing).

The reason: any value that affects the **felt warmth** of the product (color, font, radius, shadow, surface spacing) must be themeable. Functional values (z-index, etc.) don't carry warmth so they can be raw.

## File placement in different frameworks

### Next.js (App Router)

```
src/
  app/
    globals.css     ← imports tokens.css
  styles/
    tokens.css
    themes/
      warm.css
```

In `globals.css`:
```css
@import '../styles/tokens.css';
```

### Vite / React

```
src/
  styles/
    tokens.css
  main.tsx          ← imports './styles/tokens.css'
```

### Tailwind v3+ (if using Tailwind)

Tailwind can consume CSS variables via `theme.extend`:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        accent: 'var(--color-accent)',
        background: 'var(--color-background)',
        surface: 'var(--color-surface)',
      },
      fontFamily: {
        heading: 'var(--font-heading)',
        body: 'var(--font-body)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
      },
    },
  },
};
```

This gives the best of both worlds — Tailwind ergonomics with token themeability.

### Tailwind v4

Tailwind v4 has first-class CSS variable support via `@theme`:

```css
@theme {
  --color-primary: #7A9E82;
  --font-heading: 'Lora', serif;
  /* ... */
}
```

Then use `bg-primary`, `font-heading` directly in classnames.

## Loading fonts

Pair token decisions with proper font loading. For Google Fonts:

```css
/* In tokens.css or a separate fonts.css */
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500&family=DM+Sans:wght@400;500&family=Caveat:wght@500;600&display=swap');
```

Or in Next.js with `next/font`:

```typescript
import { Lora, DM_Sans, Caveat } from 'next/font/google';

const lora = Lora({ subsets: ['latin'], weight: ['400', '500'], variable: '--font-heading' });
const dmSans = DM_Sans({ subsets: ['latin'], weight: ['400', '500'], variable: '--font-body' });
const caveat = Caveat({ subsets: ['latin'], weight: ['500', '600'], variable: '--font-handwrite' });
```

Then apply the variables on the root element so they cascade into tokens.css.

## Lint and review

To prevent drift in larger codebases, add a Stylelint or ESLint rule that forbids hardcoded color/font values in component files:

```javascript
// stylelint config
"declaration-property-value-disallowed-list": {
  "/^color/": ["/^#/", "/^rgb/"],
  "/^background/": ["/^#/", "/^rgb/"],
  "font-family": ["/^[A-Z]/"]  // forbid bare font names
}
```

This forces every contributor to use tokens.

## Token versioning

Treat the token file as a versioned artifact:

- Commit it early, before any pages are designed
- Don't change token values casually — they cascade to every component
- When changing values, change them consciously and review affected screens
- Keep old theme files around (warm-v1.css, warm-v2.css) if iterating on theme experiments

The reason: changing one token can change the emotional feel of 100 screens at once. That's a feature, but it means changes deserve thought.
