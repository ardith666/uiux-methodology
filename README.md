# UI/UX Methodology (uiux-meth)

> Anti-slop design intelligence + dev-methodology workflow for frontend UI.

Design and ship frontend interfaces that look intentional, not templated. Covers landing pages, ecommerce, dashboards, and marketing pages across all frontend stacks.

---

## What It Combines

| Source | License | What Was Taken |
|---|---|---|
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | BM25 search, data CSVs, token scripts, brand tools, styling rules |
| [anti-ai-slop-design](https://github.com/aacassandra/anti-ai-slop-design) | MIT | P0/P1/P2 anti-slop rules, image generation, 80/20 philosophy |
| [dev-methodology](https://github.com/nextlevelbuilder/dev-methodology) | MIT | Workflow backbone (ask → spec → plan → implement → test → review → knowledge) |

---

## Install

**Global** (all projects):
```bash
cp -r uiux-methodology ~/.openclaw/workspace/skills/
```

**Per-project** (one project only):
```bash
mkdir -p .openclaw/skills
cp -r /path/to/uiux-methodology .openclaw/skills/
```

**ClawHub**:
```bash
clawhub install uiux-methodology
```

---

## API Keys

### Unsplash (Free)

1. Sign up at [unsplash.com/developers](https://unsplash.com/developers)
2. Create app → copy Access Key
3. Add to `.env`:

```env
UNSPLASH_ACCESS_KEY=your-key
```

> Free tier: 1,000 req/hour, no credit card.

### Custom Image API (Optional)

OpenAI-compatible endpoint (`POST /v1/images/generations`). Any provider works (OpenAI, Replicate, local models, etc.).

```env
MY_IMAGE_API_KEY=your-key
MY_IMAGE_API_URL=https://your-provider.com/v1/images/generations
```

`.env` search order: `SKILL_ENV_FILE` env var → project root `.env` → skill dir `.env`.

---

## Workflow (7 Phases)

Each phase has an anti-slop quality gate:

**1. Ask** — Understand context. "Does project have design system? Accent token? Serif fonts?"

**2. Spec** — Define scope + anti-slop spec:
- `accent_token` — NOT hardcoded indigo
- `font_display` — serif or sans?
- `icon_set` — Lucide / Heroicons / Radix / Tabler
- `anti_slop_profile` — minimal / standard / strict

**3. Plan** — Choose ONE bold visual move (the 20%). "What makes this NOT AI generated?"

**4. Implement** — Generate tokens → build components → images if needed. Tokens only, no hardcoded hex.

**5. Test** — Run `anti-slop-check.py`. P0 = blocking. P1 = should fix. P2 = polish.

**6. Review** — Final audit. 80/20 balance. Brand consistency.

**7. Knowledge** — Log decisions. Save patterns. Update brand guidelines.

---

## The Seven Cardinal Sins (P0)

| # | Sin | Fix |
|---|-----|-----|
| 1 | Default Tailwind indigo (`#6366f1`) | Use `--accent` token |
| 2 | Two-stop hero gradient (purple→blue) | Flat surface + type |
| 3 | Emoji as feature icons (✨🚀🔥) | SVG (Lucide/Heroicons/Radix/Tabler) |
| 4 | Sans-serif on display headings | `var(--font-display)` |
| 5 | Rounded card + left-border accent | Drop one |
| 6 | Invented metrics ("10× faster") | Real data or placeholder |
| 7 | Filler copy ("lorem ipsum") | Real microcopy |

---

## Scripts

| Script | Usage |
|---|---|
| `search.py` | `python3 scripts/search.py "saas dark minimal" --design-system -p "MyApp"` |
| `anti-slop-check.py` | `python3 scripts/anti-slop-check.py ./src --profile strict` |
| `generate-tokens.py` | `python3 scripts/generate-tokens.py --accent "#1a1a2e" --output tokens.css` |
| `validate-tokens.py` | `python3 scripts/validate-tokens.py tokens.css` |
| `inject-brand-context.py` | `python3 scripts/inject-brand-context.py --brand brand.md --output ctx.md` |
| `generate.sh` | `./scripts/generate.sh "prompt" chatgpt-web 1 1024x1024 high png` |

### Anti-Slop Profiles

| Profile | Checks | Exit Code |
|---|---|---|
| `minimal` | P0 only (blocking) | 0=no P0, 1=P0 found |
| `standard` | P0 + P1 (default) | same |
| `strict` | P0 + P1 + P2 | same |

### Search Flags

| Flag | Description |
|---|---|
| `--design-system` | Full design system output |
| `--domain <type>` | product, style, color, typography, ux, landing, chart, gsap, icons |
| `--variance 1-10` | Boldness: 1=minimal, 10=bold |
| `--motion 1-10` | Animation: 1=subtle, 10=complex |
| `--density 1-10` | Spacing: 1=spacious, 10=dense |

---

## Data Files

| File | Records | Description |
|---|---|---|
| `product-types.csv` | 192 | Product type profiles |
| `ui-styles.csv` | 84 | UI style profiles |
| `color-palettes.csv` | 192 | Palette recommendations |
| `font-pairings.csv` | 74 | Typography pairings |
| `landing-patterns.csv` | 34 | Landing page structures |
| `ux-guidelines.csv` | 98 | UX rules, 22 stacks |
| `chart-types.csv` | 25 | Chart recommendations |
| `gsap-presets.csv` | 16 | Animation presets |

---

## Priority Rules

1. Anti-slop P0 sins override everything — fix first
2. Brand guidelines override design search results
3. Existing project design system overrides skill recommendations
4. Token architecture enforces consistency
5. User preference overrides all defaults

---

## License

MIT License. Copyright (c) 2026.

See [LICENSE](LICENSE) for full text.

### Credits

| Source | License |
|---|---|
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT |
| [anti-ai-slop-design](https://github.com/aacassandra/anti-ai-slop-design) | MIT |
| [dev-methodology](https://github.com/nextlevelbuilder/dev-methodology) | MIT |
