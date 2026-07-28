# Project Design System

> Design system spec for this project. Dibaca oleh AI agent untuk generate UI yang konsisten.
> Reference tokens, never raw literals.

---

## Brand & Voice

### Philosophy

[Describe what this project does and how the design reflects it. One paragraph.]

### Voice & Tone

| Dimension | Guideline |
|-----------|-----------|
| Tone | [Professional / Friendly / Technical / Playful] |
| Audience | [Developers / Designers / General users / Enterprise] |
| Copy style | Direct — lead with benefit. Avoid superlatives. |
| CTAs | [Action-oriented: "Start building", "View pricing"] |

### Content Rules

| Rule | Standard |
|------|----------|
| Case | Sentence case for all headings |
| Numerals | Always digits: `50,000`, `$20/mo` |
| Oxford comma | Yes |
| Exclamation marks | Avoid in main copy |

---

## Color System

### Brand Palette

[Fill in your brand colors — light and dark variants.]

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--color-brand-50` | ... | ... | Subtle tint backgrounds |
| `--color-brand-100` | ... | ... | Light tag/badge bg |
| `--color-brand-200` | ... | ... | Borders on light |
| `--color-brand-300` | ... | ... | Hover states |
| `--color-brand-400` | ... | ... | Active states |
| **`--color-brand-500`** | **...** | **...** | **Primary CTAs, logomark** |
| `--color-brand-600` | ... | ... | Pressed state |
| `--color-brand-700` | ... | ... | Active accent |
| `--color-brand-800` | ... | ... | Dark surface variant |
| `--color-brand-900` | ... | ... | Deep dark accent |

### Semantic Colors

| Token | Role | Mapping |
|-------|------|---------|
| `--color-primary` | CTAs, links | brand-500 |
| `--color-success` | Positive feedback | green |
| `--color-warning` | Warnings | amber |
| `--color-error` | Errors | red |

---

## Typography

| Role | Family | CSS Variable |
|------|--------|-------------|
| Display | ... | `--font-display` |
| Body | ... | `--font-body` |
| Mono | ... | `--font-mono` |

### Type Scale

| Level | Size | Line Height | Weight | Font |
|-------|------|-------------|--------|------|
| h1 | 3.5rem | 1.1 | 700 | display |
| h2 | 2.5rem | 1.15 | 600 | display |
| h3 | 2rem | 1.2 | 600 | display |
| h4 | 1.5rem | 1.25 | 600 | body |
| Body | 1rem | 1.6 | 400 | body |
| Small | 0.875rem | 1.5 | 400 | body |
| Code | 0.875rem | 1.5 | 400 | mono |

---

## Spacing & Layout

- Max container width: 1200px (75rem)
- Gutter: 24px (1.5rem)
- Columns: 12

### Spacing Scale

| Token | Value | Px |
|-------|-------|----|
| `--space-1` | 0.25rem | 4px |
| `--space-2` | 0.5rem | 8px |
| `--space-3` | 0.75rem | 12px |
| `--space-4` | 1rem | 16px |
| `--space-6` | 1.5rem | 24px |
| `--space-8` | 2rem | 32px |
| `--space-12` | 3rem | 48px |
| `--space-16` | 4rem | 64px |
| `--space-20` | 5rem | 80px |
| `--space-24` | 6rem | 96px |

---

## Anti-Slop Rules

Project ini pakai **anti-slop quality gates**:

- **P0 (blocking):** No indigo accent (`#6366f1`), no hero gradients, no emoji icons, no sans-serif display heading, no rounded+left-border cards, no invented metrics, no filler copy
- **P1 (should fix):** No template skeleton layout, no placeholder CDNs, no hex outside `:root`, no accent overuse
- **P2 (polish):** Section anchors present, no decorative blobs, intentional asymmetry

## Priority Rules

1. Anti-slop P0 sins override everything
2. This DESIGN.md overrides generic design search results
3. Tokens > raw values — always use CSS variables
4. Brand voice consistent across all copy
