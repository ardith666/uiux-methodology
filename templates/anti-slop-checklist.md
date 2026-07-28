# Anti-Slop Pre-Ship Checklist

> Run this before shipping any UI. All P0 items must pass.

## P0 — Cardinal Sins (blocking)

- [ ] **No default Tailwind indigo** — grep `#6366f1`, `#4f46e5`, `#4338ca`, `#3730a3`, `#8b5cf6`, `#7c3aed`, `#a855f7` → zero hits in components
- [ ] **No two-stop hero gradients** — no purple→blue, blue→cyan, indigo→pink in hero sections
- [ ] **No emoji as icons** — zero emoji in feature cards, buttons, nav items. Use SVG (Lucide/Heroicons/Radix/Tabler)
- [ ] **Display font matches project** — h1/h2 use `var(--font-display)`, not hardcoded sans-serif
- [ ] **No rounded card + left-border combo** — drop one or the other
- [ ] **No invented metrics** — "10× faster", "99.9% uptime" removed or clearly labelled as placeholder
- [ ] **No filler copy** — zero "lorem ipsum", "feature one/two/three", "placeholder text"

## P1 — Soft Tells (non-blocking but important)

- [ ] **Template skeleton broken** — at least one unconventional section breaks Hero→Features→Pricing→FAQ→CTA
- [ ] **No external placeholder CDNs** — no unsplash.com/source, placehold.co, picsum.photos in src/href
- [ ] **Hex count under control** — fewer than 12 raw hex values outside `:root`
- [ ] **Accent usage reasonable** — `var(--accent)` used fewer than 6 times per screen

## P2 — Polish (nice to have)

- [ ] **Section anchors** — every section has an id or identifiable hook
- [ ] **No decorative blobs** — no meaningless SVG shapes in backgrounds
- [ ] **Visual tension present** — alternating density between sections (tight → breathing)

## Quality Gates

- [ ] **cursor-pointer** on all clickable elements
- [ ] **Hover states** with smooth transitions (150-300ms)
- [ ] **Text contrast** 4.5:1 minimum (WCAG AA)
- [ ] **Focus states** visible for keyboard navigation
- [ ] **prefers-reduced-motion** respected
- [ ] **Responsive** — works at 375px, 768px, 1024px, 1440px
- [ ] **No hardcoded colors** — all colors via design tokens
- [ ] **SVG icons only** — no emoji as icons anywhere
- [ ] **Touch targets** — min 44×44px
- [ ] **Error messages** — near relevant fields, not generic

## 80/20 Balance Check

- [ ] **One bold visual move** — typography, color, or proportion choice that's distinctive
- [ ] **Voice/microcopy** — buttons and labels sound like THIS product, not generic
- [ ] **One memorable micro-interaction** — something users will notice and remember
- [ ] **Product-specific detail** — one thing only a user of this product would add

## Final Test

Show a screenshot to someone outside the project. Can they identify what product this is for?

- **Yes** → You have soul. Ship it.
- **No** → You shipped a template. Go back to Phase 3: Plan.
