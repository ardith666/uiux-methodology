# Anti-Slop Rules — Detailed Reference

> Source: aacassandra/anti-ai-slop-design (MIT License)
> Integrated into uiux-methodology skill.

## Philosophy: ~80/20

80% proven patterns + 20% distinctive choice. The 20% lives in:

1. **One bold visual move** — a typography choice, a single color decision, an unexpected proportion
2. **Voice and microcopy** — "Start tracking" beats "Get started"
3. **One micro-interaction** — button press that moves 2px, a number that counts up
4. **One product-specific detail** — `kbd` shortcut hint, status badge with product-specific phrasing

**Test:** If someone can identify your product from a screenshot → you have soul. Otherwise → template.

---

## P0 — Cardinal Sins (must fix)

### Sin #1: Default Tailwind Indigo Accent
**Colors:** `#6366f1`, `#4f46e5`, `#4338ca`, `#3730a3`, `#8b5cf6`, `#7c3aed`, `#a855f7`

**Why:** Indigo is the #1 AI tell. Every AI-generated UI defaults to it.

**Fix:** Use project's `--accent` token. Define accent in design system before writing any component.

**Detection:**
```bash
grep -rn '#6366f1\|#4f46e5\|#4338ca\|#3730a3\|#8b5cf6\|#7c3aed\|#a855f7' --include='*.css' --include='*.scss' --include='*.tsx' --include='*.jsx'
```

---

### Sin #2: Two-Stop "Trust" Hero Gradient
**Patterns:** purple→blue, blue→cyan, indigo→pink, violet→fuchsia

**Why:** The "trust gradient" is the AI equivalent of a stock photo.

**Fix:** Flat surface + intentional type. One solid background color with a strong typography choice beats any gradient.

**Detection:**
```bash
grep -rn 'linear-gradient.*#[0-9a-f].*#[0-9a-f]' --include='*.css' --include='*.scss'
```
Look for two-stop gradients with purple/blue/cyan hue range.

---

### Sin #3: Emoji as Feature Icons
**Emoji:** ✨ 🚀 🎯 ⚡ 🔥 💡 🎨 🚀 💎 🌟 🔑 📊 🛡️

**Why:** Emoji in feature cards, buttons, or navigation is an instant AI tell.

**Fix:** Monoline SVG icons with `currentColor`. Use Lucide, Heroicons Outline, Radix Icons, or Tabler Icons.

**Detection:**
```bash
# Look for emoji in h*, button, li, or icon containers
grep -rn '[✨🚀🎯⚡🔥💡🎨💎🌟🔑📊🛡️]' --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.html'
```

---

### Sin #4: Sans-Serif Display Text (When Project Has Serif)
**Pattern:** h1/h2 using Inter, Roboto, `system-ui` when `--font-display` is a serif

**Why:** Inconsistent typography hierarchy. Serif display + sans body is intentional; sans display + sans body is default.

**Fix:** h1/h2 must use `var(--font-display)`. Never hardcode `font-family` on headings.

**Detection:**
```bash
grep -rn 'font-family.*Inter\|font-family.*Roboto\|font-family.*system-ui' --include='*.css' --include='*.scss'
```
Check if applied to h1/h2 selectors.

---

### Sin #5: Rounded Card with Colored Left-Border
**Pattern:** `border-radius: 0.75rem` + `border-left: 4px solid var(--accent)`

**Why:** The canonical "AI dashboard tile" shape. Instantly recognizable.

**Fix:** Drop either the border-radius OR the left border. Pick one:
- Sharp corners + left border → editorial feel
- Rounded corners + no border → modern/clean feel
- No border-radius + subtle shadow → sophisticated feel

---

### Sin #6: Invented Metrics
**Patterns:** "10× faster", "99.9% uptime", "3× more productive", "500+ companies"

**Why:** Fake metrics destroy trust. Users know when numbers are made up.

**Fix:** Use real data or clearly labelled placeholders:
- `[Your metric here]`
- "Join 0+ early users" (honest zero)
- Remove the metric entirely and let the product speak

---

### Sin #7: Filler Copy
**Patterns:** "lorem ipsum", "feature one / two / three", "placeholder text", "sample content", "Get started", "Learn more"

**Why:** Empty sections are a design problem. Filler copy masks the problem instead of solving it.

**Fix:** Solve with composition:
- Remove the section if it adds no value
- Use real microcopy that describes the actual product
- Use placeholder that acknowledges itself: "Your headline here"

---

## P1 — Soft Tells (should fix)

### Tell #1: Template Skeleton
**Pattern:** Hero → Features (3 cards) → Pricing (3 tiers) → FAQ (5 items) → CTA

**Fix:** Introduce at least one unconventional section:
- Testimonial wall as full-bleed quote
- Pricing as comparison-against-status-quo
- Inline mini-product-demo
- Feature comparison table instead of cards

---

### Tell #2: External Placeholder CDNs
**Patterns:** `unsplash.com/source`, `placehold.co`, `placekitten.com`, `picsum.photos`

**Fix:** Use generated images (scripts/generate.sh) or Unsplash companion skill with proper attribution.

---

### Tell #3: Hex Outside :root
**Rule:** More than ~12 raw hex values in selectors (not in `:root` or token definitions).

**Fix:** Move all colors to `:root` as CSS custom properties. Reference tokens, never raw hex.

---

### Tell #4: Accent Overuse
**Rule:** `var(--accent)` used 6+ times in rendered body.

**Fix:** Cap at 2 visible accent uses per screen. Accent is seasoning, not the main ingredient.

---

## P2 — Polish Tells (nice to fix)

### Tell #5: Sections Without Anchors
**Rule:** Every section should have an `id` or identifiable hook for review/interaction.

---

### Tell #6: Decorative Blob/Wave SVGs
**Rule:** If a shape has no reason to exist, remove it. Meaningless geometry = AI slop.

---

### Tell #7: Perfect Symmetric Layout
**Rule:** No visual tension = looks automated. Introduce alternating density: one tight section, one breathing section.

---

## Anti-Slop Prompt Pattern (for Image Generation)

Structure prompts as art-direction prose, NOT keyword piles:

```
[Medium] of [specific subject] in [specific environment], [composition], [lighting], [material detail], [mood], [anti-slop constraints]
```

**Good:**
```
Editorial photograph of a matte black desk lamp beside stacked wireframes on a warm oak table, eye-level 50mm lens, soft window light, quiet design-studio mood, no text overlays
```

**Weak:**
```
Amazing futuristic product, cinematic, ultra detailed, 8k, masterpiece, trending
```

### Prompt Template
```
[PHOTO_TYPE] of [SPECIFIC_SUBJECT] in [ENVIRONMENT],
[COMPOSITION], [LIGHTING], [MATERIAL_DETAIL],
[MOOD], no text, no logos, no watermarks
```

### Photo Types
- `Editorial photograph` — clean, professional
- `Lifestyle photograph` — warm, human
- `Product photograph` — studio, precise
- `Architectural photograph` — structured, geometric

---

## Integration with dev-methodology

| Phase | Anti-Slop Gate |
|-------|---------------|
| Ask | "Does this project have a design system?" |
| Spec | Define accent_token, font_display, icon_set, anti_slop_profile |
| Plan | "What makes this NOT look like AI generated?" |
| Implement | Use tokens, not hardcoded values |
| Test | Run anti-slop-check.py |
| Review | Final audit against P0/P1/P2 |
| Knowledge | Log anti-slop decisions that worked |
