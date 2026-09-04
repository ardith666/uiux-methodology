---
name: uiux-methodology
alias: uiux-meth
version: 3.1.1
description: "UI/UX design intelligence: design system generator, brand identity, styling guidelines, banner design, and UX best practices. Searchable database of 84 styles, 192 color palettes, 74 font pairings, 192 product types, 99 UX guidelines across 22 tech stacks + 21st.dev MCP registry + Obsidian Integration (vault-native design knowledge & retain). Use when designing, building, or reviewing UI/UX."
---

# UI/UX Methodology (uiux-meth)

> Alias: **uiux-meth** — same pattern as `dev-meth` for `dev-methodology`.

Anti-slop design intelligence + dev-methodology workflow for frontend UI.

## Trigger

User asks to design UI, review frontend code, check for AI slop, generate design system, create brand guidelines, or says "uiux mode", "design review", "anti-slop", "uiux-meth".

### ⚠️ MANDATORY: Display Logo First

**YOU MUST RUN these `echo` commands immediately when triggered — this is your identity display. This is NOT optional.**

```bash
echo '▖▖▄▖▖▖▖▖ ▖ ▖▄▖▄▖▖▖'
echo '▌▌▐ ▌▌▚▘ ▛▖▞▌▙▖▐ ▙▌'
echo '▙▌▟▖▙▌▌▌ ▌▝ ▌▙▖▐ ▌▌'
echo ''
echo '  UI/UX Design Intelligence + Anti-Slop Quality Gates'
echo '  84 styles · 192 palettes · 74 fonts · 98 UX rules · 13 anti-slop checks'
echo ''
```

No other actions until these lines are printed.

## What This Skill Does

Design and ship frontend interfaces that look intentional, not templated. Covers landing pages, ecommerce, dashboards, and marketing pages across all frontend stacks. Actively avoids "AI slop" (default Tailwind indigo, two-stop hero gradients, emoji icons, filler copy, fake metrics, rounded left-border cards).

Combines 5 design domains into one unified workflow:
1. **Design Intelligence** — BM25 search for styles, palettes, typography, patterns
2. **Design System** — Token architecture (3-layer: global → alias → component)
3. **Brand Identity** — Voice, messaging, visual language, asset management
4. **Banner Design** — Multi-format asset generation with anti-slop prompts
5. **UI Styling** — shadcn/ui + Tailwind + canvas, with anti-slop enforcement

## Trigger

Activate when: designing UI, reviewing frontend code, generating design systems, creating brand guidelines, building component libraries, or checking for AI slop in existing code.

## The ~80/20 Philosophy

Aim for **~80% proven patterns + ~20% distinctive choice**. The 20% lives in:
- One bold visual move — typography, color, proportion
- Voice and microcopy — "Start tracking" beats "Get started"
- One micro-interaction — button press that moves 2px, number that counts up
- One detail only a product user would add — `kbd` shortcut hints, product-specific phrasing

If someone can identify your product from a screenshot — you have soul. Otherwise you shipped a template.

## Fable Design Loop

Tugas non-trivial dijalankan lewat loop fable (dari [fable-method](https://github.com/Sahir619/fable-method)), diadaptasi buat design: verifikasi = **render, bukan cuma script**. Script anti-slop cek kode; mata ngecek hasil. Dua-duanya wajib.

```
ask ─► 0 classify ─► 1 define done ─► 2 evidence ─► 3 decide ─► 4 act ─► 5 verify ─► 6 report
```

| Step | Isi (versi design) | Hook ke phase |
|---|---|---|
| 0 classify | question/assessment ("review", "menurutmu") = findings doang, jangan ubah. Task ("buat", "redesign") = ubah + verify | Sebelum Phase 1 |
| 1 define done | observasi konkret: anti-slop strict pass, render bener di 375/768/1024/1440, konsisten sama `DESIGN.md` | Phase 1-2 |
| 2 evidence | buka `knowledge/DESIGN.md` + komponen existing + brand context DULU, baru desain. Jangan desain dari memory. BM25 search = evidence | Phase 2 |
| 3 decide | satu arah desain; alternatif disebut 1 baris kenapa kalah | Phase 3 |
| 4 act | INTENT gate versi design (di bawah), smallest change | Phase 4 |
| 5 verify | **render + lihat sendiri**, bukan cuma anti-slop script pass | Phase 5 |
| 6 report | outcome-first + artifact gate | Phase 6 |

### Triviality Gate (jalan duluan)

Task trivial kalau SEMUA ini true: satu file, <~10 baris berubah, gak ada behavior/visual baru, dan udah tau persis apa yang diubah tanpa searching (ganti 1 token warna, tweak padding). Kalau trivial: kerjakan, render cek 1 breakpoint, lapor 1-2 kalimat. Selain itu — full loop.

### INTENT Gate (versi design)

Sebelum ubah behavior/visual: `INTENT: design does <X>; anti-slop check expects <Y>; brand guidelines say <Z>`. Wajib beneran buka `knowledge/DESIGN.md` / brand guidelines buat isi slot Z. X/Y/Z gak cocok → jangan edit dulu: ketidakcocokan itu temuannya. Authority order: explicit user statement > brand guidelines > anti-slop check > design saat ini.

### Artifact Gate (laporan)

`INTENT:` muncul verbatim kalau behavior/visual berubah; `AUTH: user said "..."` kalau aksi outward (publish/deploy/upload asset publik) diambil; `PENDING:` kalau follow-up prescribed sengaja gak diambil. Twin check gak perlu terpisah — `anti-slop-check.py` scan seluruh project = twin check bawaan.

## Workflow (dev-methodology backbone)

## Communication Rules (berlaku semua phase)

Gaya komunikasi ADHD-friendly — action first, tanpa basa-basi:

1. **Lead with the action** — apa yang berubah / apa yang harus dilakukan, baru konteks
2. **Numbered steps** — multi-step task / progress report → nomorin langkahnya
3. **End with one concrete next step** — tutup reply dengan langkah berikutnya + estimasi waktu (±menit)
4. **Restate state** — di debugging/review panjang, ulang state sekarang tiap turn biar konteks gak ilang
5. **Matter-of-fact errors** — kegagalan ditulis polos (`PENDING:` / error), tanpa pembelaan atau dramatisasi
6. **Suppress tangents** — info sampingan simpen di akhir sebagai "kalau perlu", jangan naruh di tengah
7. **No preamble, no recap, no closers** — langsung inti, gak usah "jadi kesimpulannya"

### Phase 1: Ask

- **Read `knowledge/README.md` first** — entry point, tau state + metodologi aktif
- **If `knowledge/` doesn't exist, create it with templates** (`knowledge-README.md`, `KNOWLEDGE.md`, `DESIGN.md`)
- **Check for `knowledge/DESIGN.md`** — design system context
- Understand project context, constraints, existing design system
- Anti-slop gate: "Does this project have a design system? What's the accent token? Any serif fonts?"
- Load brand context if available
- Extract: product type, target audience, style keywords, stack

### Phase 2: Spec

- **Define done** (Step 1): observasi konkret — "anti-slop strict pass, render bener di 375/768/1024/1440, konsisten sama `DESIGN.md`". Bukan "udah keliatan bagus"
- **Evidence dulu** (Step 2): buka `knowledge/DESIGN.md`, komponen existing, brand context SEBELUM desain. Jangan desain dari memory
- Define scope: landing page / ecommerce / dashboard / marketing
- Anti-slop spec (MUST include):
  - `accent_token` — project accent color (NOT hardcoded indigo)
  - `font_display` — serif or sans for display text
  - `icon_set` — Lucide / Heroicons / Radix / Tabler
  - `anti_slop_profile` — minimal / standard / strict
- Run BM25 search for style inspiration
- Design dials (optional): `--variance`, `--motion`, `--density` (1-10 each)

### Phase 3: Plan

- Choose ONE bold visual move (the 20% distinctive)
- Plan token architecture (3-layer)
- Plan brand voice + microcopy
- **Generate `knowledge/DESIGN.md` using templates/knowledge-DESIGN.md** — fill with project-specific values
- **Generate or update `knowledge/README.md` using templates/knowledge-README.md** — entry point for other agents
- Anti-slop gate: "What makes this NOT look like AI generated?"
- Break into tasks with dependencies

### Phase 4: Implement

- Generate design tokens (scripts/generate-tokens.py)
- Generate brand context (scripts/inject-brand-context.py)
- Build UI components using tokens, NOT hardcoded values
- Generate images with anti-slop prompts (scripts/generate.sh) when needed
- Enforce: SVG icons only, no emoji, no hardcoded hex in components

### Phase 5: Test (Step 5 — verify by observation)

- **Render + lihat sendiri**: screenshot/canvas di 4 breakpoint (375/768/1024/1440). Script pass tapi visual broken = verifikasi GAGAL
- Run anti-slop-check.py (automated validation)
- Check P0 sins: indigo, gradients, emoji icons, serif mismatch, left-border cards, invented metrics, filler copy
- Check P1 tells: template skeleton, placeholder CDNs, hex outside :root, accent overuse
- Check P2 polish: section anchors, decorative blobs, layout tension
- Validate tokens (scripts/validate-tokens.py)

### Phase 6: Review (Step 6 — outcome-first)

- **Artifact gate**: `INTENT:` line kalau visual berubah; `AUTH:` kalau aksi outward; `PENDING:` kalau follow-up di-skip
- Final anti-slop audit
- **Anti-slop writing (opsional, auto-install):** kalau output task = user-facing copy blok (headline, hero, microcopy, error message, atau teks panjang) → cek skill `no-ai-slop`. Belum ada? Install langsung tanpa tanya: `npx skills add petergyang/no-ai-slop --skill no-ai-slop --yes`. Lalu jalankan aturannya — anti-slop visual (P0 "Filler Copy") cuma nangkep lorem ipsum / "Get started", gak nangkep binary contrast ("It's not X. It's Y."), importance puffery ("Unlock your potential"), atau fake-profound ending — itu domain-nya no-ai-slop
- Check 80/20 balance
- **Verify brand consistency against `knowledge/DESIGN.md`**
- Self-critique checklist (from dev-methodology)

## Optional Dependencies

Skill-skill berikut dipakai sebagai quality gate opsional — bukan bundel, tapi referensi. Install di agent masing-masing (bukan di repo ini) biar update upstream selalu nyampe.

| Skill | Sumber | Kapan dipakai | Install | Perlu tanya user? |
|---|---|---|---|---|
| `no-ai-slop` | petergyang/no-ai-slop | Phase 6: user-facing copy blok (headline/microcopy) | `npx skills add petergyang/no-ai-slop --skill no-ai-slop --yes` | ❌ gak perlu (cuma file rules) |
| `diagram-design` | ardith666/diagram-design (mirror upstream cathrynlavery) | Phase 2: user journey / story map / swimlane buat riset UX. Phase 3: high-level stack / wireframe-ish. Phase 5: render diagram diverifikasi mata (4 breakpoint), konsisten sama `DESIGN.md` tokens | via aggregator `ardith666/agent-skills` (`./setup.sh`) | ❌ gak perlu |
| `penetration-testing-with-strix` | usestrix/strix | Task nyentuh web/API/auth/input | `npx skills add usestrix/strix --skill penetration-testing-with-strix --yes` | ✅ WAJIB (butuh Docker + LLM API key) |

Kalau skill belum terinstall dan hook kepanggil: ikuti kebijakan di atas (auto-install / tanya). Kalau gak jadi jalan → catat `PENDING:` di report, jangan di-skip diam-diam.

## Diagram Design Integration

Pakai skill `diagram-design` (39 tipe diagram editorial, output HTML+SVG self-contained, bisa redraw Mermaid/draw.io) saat dokumen design butuh visual — user journey, story map, swimlane, arsitektur UI.

**Aturan output — WAJIB ke `knowledge/`:**

- **Phase 2 (Evidence)** — user journey / story map / swimlane hasil riset → `knowledge/diagrams/<nama>.html` + `.svg`, link dari `DESIGN.md`
- **Phase 3 (Plan)** — high-level stack / arsitektur UI → `knowledge/diagrams/`
- **Phase 5 (Test)** — diagram dirender + diverifikasi mata di 4 breakpoint (375/768/1024/1440), konsisten sama design tokens
- File diagram vault-native (frontmatter + wikilink) biar ter-indeks Obsidian, mengikuti alur Obsidian Integration

### Phase 7: Knowledge

- Log design decisions to `knowledge/KNOWLEDGE.md` (same pattern as dev-methodology)
- Save anti-slop patterns that worked
- **Update `knowledge/DESIGN.md`** with final design system specs
- **Update `knowledge/README.md`** jika ada perubahan metodologi
- Update brand guidelines if needed

### Knowledge Folder Structure

```
project-root/
├── knowledge/
│   ├── README.md        ← Entry point. Agent WAJIB baca ini dulu
│   ├── KNOWLEDGE.md     ← Context, decisions, progress (dev-meth standard)
│   └── DESIGN.md        ← Design system spec (uiux-meth standard)
```

| File | Isi | Dibaca oleh |
|------|-----|-------------|
| `README.md` | Metodologi aktif, file list, aturan agent | Semua agent (entry point) |
| `KNOWLEDGE.md` | Vision, decisions, progress, learnings | dev-methodology agents |
| `DESIGN.md` | Brand, tokens, typography, components | uiux-methodology agents |

## The Seven Cardinal Sins (P0 — must fix)

| # | Sin | Fix |
|---|-----|-----|
| 1 | Default Tailwind indigo accent (`#6366f1` etc.) | Use project `--accent` token |
| 2 | Two-stop "trust" hero gradient (purple→blue) | Flat surface + intentional type |
| 3 | Emoji as feature icons (✨🚀🔥) | Monoline SVG (Lucide, Heroicons, Radix, Tabler) |
| 4 | Sans-serif display text when project has a serif | Use `var(--font-display)` |
| 5 | Rounded card with colored left-border accent | Drop radius or left border |
| 6 | Invented metrics ("10× faster") | Real source or labelled placeholder |
| 7 | Filler copy ("lorem ipsum", "feature one") | Solve with composition, not invented words |

## Soft Tells (P1 — should fix)

- Standard "Hero → Features → Pricing → FAQ → CTA" with no variation
- External placeholder image CDNs (unsplash.com, placehold.co, picsum.photos)
- More than ~12 raw hex values outside `:root`
- `var(--accent)` used 6+ times in rendered body

## Polish Tells (P2 — nice to fix)

- Sections without identifiable anchors or hooks
- Decorative blob/wave SVG backgrounds
- Perfect symmetric layout with no visual tension

## Loading State (Skeleton UI)

Kalau UI nampilin data async (fetch, image, list) — wajib ada loading state, jangan blank/spinner doang:

- **Skeleton > spinner:** skeleton tunjukin struktur konten yang bakal muncul (layout match), spinner cuma bilang "tunggu". Skeleton buat layout shift lebih kecil pas data datang
- **Skeleton match layout aslinya:** card → card-shaped skeleton, list → baris-baris. Jangan asal kotak abstrak
- **Shimmer halus:** animasi gradient sweep ±1.5-2s loop, `prefers-reduced-motion` → matiin shimmer, cukup block statis
- **Jangan overshoot:** skeleton cuma buat initial load (atau pagination). Loading tambahan di tengah (refresh, filter) cukup subtle — jangan blinker seluruh halaman
- **Accessibility:** `aria-busy="true"` + jangan sembunyikan konten lama sebelum punya pengganti (kalau refresh, keep old data + subtle indicator)
- **Verifikasi (Phase 5):** throttle network ke Slow 3G → skeleton muncul, gak ada layout jump pas data render

## Design Dials

Three 1-10 sliders to tune output:

| Dial | Low (1-3) | Mid (4-7) | High (8-10) |
|------|-----------|-----------|-------------|
| `--variance` | Centered/minimal | Balanced | Bold/asymmetric |
| `--motion` | Subtle micro-interactions | Standard scroll/stagger | Complex choreography |
| `--density` | Spacious (24-96px) | Standard (16-64px) | Dense/dashboard (8-32px) |

## Domain Search

| Need | Domain flag | Example |
|------|------------|---------|
| Product patterns | `--domain product` | `"entertainment social"` |
| Style options | `--domain style` | `"glassmorphism dark"` |
| Color palettes | `--domain color` | `"entertainment vibrant"` |
| Font pairings | `--domain typography` | `"playful modern"` |
| Individual Google Fonts | `--domain fonts` | `"monospace technical"` |
| UX best practices | `--domain ux` | `"animation accessibility"` |
| UI decision reasoning | `--domain reasoning` | `"ecommerce conversion"` |
| Icon recommendations + import code | `--domain icons` | `"navigation outline"` |
| Mobile app guidelines (iOS/RN/Flutter) | `--domain app` | `"accessibility label"` |
| Stack-specific guidelines | `--stack react` | `"layout state"` |
| Landing page structure | `--domain landing` | `"hero social-proof"` |
| Chart recommendations | `--domain chart` | `"real-time dashboard"` |
| GSAP animations | `--domain gsap` | `"scroll reveal stagger"` |
| Framer Motion presets (React + vanilla) | `--domain framer` | `"hero stagger"` |

## Scripts

All scripts are in `scripts/` relative to this SKILL.md.

### BM25 Design Search

```bash
python3 scripts/search.py "query" [--design-system] [-p "Project Name"] [--variance 0-10] [--motion 0-10] [--density 0-10]
```

Options:
- `--design-system` — Generate full design system output
- `-p "Name"` — Project name for generated system
- `--domain <type>` — Restrict search to specific domain
`--stack <stack>` — Stack-specific guidelines (react, nextjs, vue, svelte, flutter, swiftui, react-native, shadcn, threejs, html-tailwind…)

Domain is auto-detected when `--domain` is omitted (synonym-aware: `dark-mode` = `dark`, `e-commerce` = `ecommerce`, `a11y` = `accessibility`).
- `--variance`, `--motion`, `--density` — Design dials (1-10)
- `--persist` — Save design system to project root
- `--output-dir` — Where to save (with --persist)

### Anti-Slop Check

```bash
python3 scripts/anti-slop-check.py <directory> [--format json|text] [--profile minimal|standard|strict]
```

Profiles:
- `minimal` — P0 sins only
- `standard` — P0 + P1 tells (default)
- `strict` — P0 + P1 + P2 polish

### Token Generator

Takes a nested JSON config and flattens it into `:root` CSS variables.

```bash
python3 scripts/generate-tokens.py --config tokens.json -o tokens.css
```

Example `tokens.json`:
```json
{
  "color": { "accent": "#1a1a2e", "bg": "#ffffff", "text": "#1e293b" },
  "font": { "display": "Playfair Display", "body": "Inter" },
  "radius": "8px"
}
```

Generates:
```css
:root {
  --color-accent: #1a1a2e;
  --color-bg: #ffffff;
  --color-text: #1e293b;
  --font-display: Playfair Display;
  --font-body: Inter;
  --radius: 8px;
}
```

### Search Self-Check

```bash
python3 scripts/test_search.py
```

Verifies synonym normalization, auto domain detection, ranked results, stack search, design system dials, and data integrity across all CSV files.

### Token Validator

Scans a directory for hardcoded hex/rgb color values that should be tokens.

```bash
python3 scripts/validate-tokens.py --dir src/
# optional: --ext ".css,.scss,.tsx,.jsx,.vue,.svelte" (default)
```

### Brand Context Injector

Extracts brand context from `brand-guidelines.md` for prompt injection. Output goes to stdout; use `--json` for structured output.

```bash
python3 scripts/inject-brand-context.py --brand-file docs/brand-guidelines.md
python3 scripts/inject-brand-context.py --brand-file docs/brand-guidelines.md --json
```

### Image Generation

```bash
./scripts/generate.sh "PROMPT" [model] [n] [size] [quality] [format]
```

## Data Files

In `data/` relative to this SKILL.md:

| File | Contents |
|------|----------|
| `ui-styles.csv` | 84 UI style profiles (full specs, prompts, CSS keywords) |
| `color-palettes.csv` | 192 palettes with full token set (on-primary, card, muted, border, ring…) |
| `font-pairings.csv` | 74 typography pairings |
| `google-fonts.csv` | 1900+ Google Fonts (popularity, variable axes, subsets, URLs) |
| `landing-patterns.csv` | 34 landing page structures with CTA strategy |
| `ux-guidelines.csv` | 99 UX rules with do/don't + code examples |
| `ui-reasoning.csv` | 161 product-type decision rules (pattern, style, anti-patterns) |
| `app-interface.csv` | 30 mobile app guidelines (iOS/Android/RN) |
| `icons.csv` | 105 icon recommendations with import code (Phosphor/Lucide/Heroicons…) |
| `chart-types.csv` | 25 chart recommendations (a11y notes, thresholds, libraries) |
| `gsap-presets.csv` | 16 GSAP presets by intensity tier (subtle/standard/complex) |
| `framer-motion-presets.csv` | 14 Framer Motion presets (React + vanilla code) |
| `stacks/` | 22 stack guideline files (react, nextjs, vue, svelte, flutter…) |

## Reference Docs

In `references/`:

| Topic | File |
|-------|------|
| UX Quick Reference | `references/quick-reference.md` |
| Pro Rules & Anti-Slop P0/P1/P2 | `references/pro-rules.md` |
| Component Specifications | `references/component-specs.md` |
| Token Architecture (3-layer) | `references/token-architecture.md` |
| Anti-Slop Detailed Reference | `references/anti-slop-rules.md` |

## Templates

In `templates/`:

| Template | Purpose |
|----------|---------|
| `brand-guidelines-starter.md` | Brand guidelines template |
| `design-tokens-starter.json` | Design tokens starter |
| `anti-slop-checklist.md` | Pre-ship anti-slop checklist |

## Priority Rules

0. Explicit user statement > brand guidelines > anti-slop check > design saat ini (INTENT authority order)
1. Anti-slop P0 sins override everything — always fix first
2. Brand guidelines override design search results
3. Existing project design system overrides skill recommendations
4. Token architecture enforces consistency
5. User preference overrides all defaults

## Component Registry (21st.dev MCP)

21st.dev = registry 12.000+ React components / themes / templates (shadcn registry format, MIT-style copy-into-repo, bukan dependency). Tiap komponen punya prompt + `npx shadcn@latest add` command.

### MCP Integration (OpenClaw)

21st MCP = plain HTTP server, butuh API key (gratis, dari https://21st.dev/mcp):

```json
{
  "mcp": {
    "servers": {
      "21st": {
        "url": "https://21st.dev/api/mcp",
        "transport": "streamable-http",
        "headers": { "x-api-key": "YOUR_21ST_API_KEY" }
      }
    }
  }
}
```

Atau CLI: `openclaw mcp set 21st '{"url":"https://21st.dev/api/mcp","headers":{"x-api-key":"KEY"}}'`.
Tools MCP keluar sebagai plugin-owned tools (`bundle-mcp`); pastikan `tools.sandbox.tools` allowlist berisi `bundle-mcp` kalau sandbox aktif.

Tool utama: `search` (catalog components/themes/templates), `generate` (UI generation dengan variants), `get_inspiration`, `search_logo`. Legacy Magic names (`21st_magic_component_builder`) masih diterima.

### Penggunaan dalam workflow

1. Design system phase: `search` 21st buat component inspiration yang match `DESIGN.md` tokens
2. Implement phase: `generate` / shadcn add — komponen masuk repo, adapt ke design tokens project
3. Anti-slop check tetap jalan setelah install (P0/P1/P2 scan)

Catatan: 21st = paid registry (2 free copy/hari, membership buat unlimited). Data gak bisa di-port offline — beda dari ui-ux-pro-max (MIT CSV).

## Anti-Patterns to Avoid

- Emoji as icons → use SVG (Lucide/Heroicons/Radix/Tabler)
- Removing focus rings → keep visible focus states
- Placeholder-only labels → use real, descriptive labels
- Gray-on-gray text → maintain 4.5:1 contrast minimum
- Hardcoded hex in components → always use design tokens
- Animating width/height → use transform/opacity
- Horizontal scroll on mobile → overflow-x hidden or responsive layout
- Disabling zoom → never set maximum-scale
- Layout thrashing / CLS → reserve space, use aspect-ratio

## Pre-Ship Checklist

- [ ] cursor-pointer on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard nav
- [ ] prefers-reduced-motion respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No hardcoded colors (use design tokens)
- [ ] SVG icons (no emoji as icons)
- [ ] Min touch target 44×44px
- [ ] Error messages near relevant fields
- [ ] No P0 cardinal sins present
- [ ] No P1 soft tells present
- [ ] Brand voice consistent across copy
- [ ] Accent token used, not hardcoded indigo
- [ ] Display font loaded and applied via tokens

## Environment

Some scripts need API keys. See `.env.example` in this skill directory.

## Obsidian Integration (vault-aware)

Modul aktif saat CWD ada di dalam **vault Obsidian** (folder `.obsidian/` di CWD atau parent) atau user minta pakai Obsidian. Referensi lengkap: `references/obsidian/` di skill ini — `README.md` = gateway (filosofi, 4 alur retain, retention policy, dependency & self-healing), `markdown.md` / `bases.md` / `canvas.md` / `cli.md` / `defuddle.md` = detail sintaks.

### Prinsip

1. **Vault-native writing** — semua output design ditulis vault-native: `knowledge/DESIGN.md`, brand guidelines, keputusan, hasil anti-slop check, evidence BM25 → frontmatter (`title/tags/status/created`) + `[[wikilinks]]` + `#tag`.
2. **Empat alur retain** — mencatat, merangkum (defuddle → distilasi → note), mengkoneksikan (wikilink/base/canvas), meretain (append-only + timestamp). Detail: `references/obsidian/README.md`.
3. **Retention restraint** — HANYA tulis continuity artifacts (design decisions, learnings, evidence ringkas, asset index). JANGAN duplikasi atau meniru konten milik user.
4. **Progressive disclosure** — `SKILL.md` ini tetap ringkas; baca `references/obsidian/*` on-demand saat fitur dibutuhkan.

### Hook per phase

- **Phase 1 (Ask)** — baca `knowledge/DESIGN.md` + vault dulu; simpan brand context sebagai note vault-native.
- **Phase 2 (Spec)** — evidence: BM25 search + note terkait di vault; hasil riset web via `defuddle parse <url> --md` → ringkas → simpan note → wikilink.
- **Phase 3 (Plan)** — generate `knowledge/DESIGN.md` vault-native; asset/token berulang → `design-assets.base`.
- **Phase 4 (Implement)** — log keputusan design ke `knowledge/KNOWLEDGE.md` vault-native.
- **Phase 5 (Test)** — simpan hasil anti-slop check + catatan render review (4 breakpoint) ke note status.
- **Phase 6 (Review)** — entry append-only `[YYYY-MM-DD]`; update `DESIGN.md` final + sambungkan wikilink; galeri/referensi visual → `.canvas`. Verifikasi health graph setelahnya: `obsidian unresolved` + `obsidian orphans` (aturan di `references/obsidian/README.md` § Vault Hygiene).

`knowledge/` folder structure di atas tetap berlaku; saat di vault semua file-nya ikut **vault-native** supaya terindeks & ter-retain Obsidian.

### Dependency & Self-Healing
 
 Cek-req → **tanya user → bantu deploy → verify**. Kurang sesuatu (Obsidian app, CLI belum enabled, PATH, defuddle, node)? Pakai tabel + perintah di `references/obsidian/README.md`. Aksi sistem (npm install -g, ubah shell rc, symlink) butuh AUTH. Gagal → pakai yang tersedia (file ops selalu jalan), fitur yang kurang di-skip dan dicatat `PENDING:`.

## Graphify Integration (codebase intelligence)

Saat redesign/refactor codebase **existing**, pahami dulu sistemnya lewat knowledge graph, bukan baca file satu-satu. Referensi lengkap (perintah inti, instalasi & deploy per mesin, prompt AUTH ke user): `references/graphify/README.md`.

### Kapan

- **Phase 2 (Spec/evidence)** — kalau project punya `graphify-out/`: buka dengan `graphify query "..."` / `explain` buat lihat logika, dependensi, dan pola komponen yang mau didesain ulang.
- Belum ada graph → tawarkan `/graphify .` (bisa `--code-only`, offline 0 token) — jangan install diam-diam; ikuti prompt AUTH di referensi.
- Setelah implementasi: `graphify update .` biar `GRAPH_REPORT.md` tetap mencerminkan struktur final.
- Melacak alur antar konsep UI/state: `graphify path "A" "B"`.

### Aturan

- **Hasil → `knowledge/`** — temuan & digest dari graph (arsitektur, dependensi, pola) masuk folder `knowledge/` (contoh `knowledge/graph-report-<project>.md`, frontmatter + wikilink biar nyambung di vault). Jangan bikin file hasil di luar folder itu. Satu-satunya pengecualian: `graphify-out/` (artefak teknis yang wajib di-commit ke repo, bukan "hasil sesi").
- **Git: commit vs ignore `graphify-out/`** — commit `graph.json`, `graph.html`, `GRAPH_REPORT.md`, `manifest.json`, `cost.json`, `.graphify_labels.json`. Ignore `graphify-out/cache/`, `.graphify_python`, `.graphify_root` (state mesin lokal + cache build, path absolut beda per mesin, regenerable — graphify punya interpreter-guard yg re-resolve otomatis). Blok gitignore:
  ```gitignore
  graphify-out/cache/
  graphify-out/.graphify_python
  graphify-out/.graphify_root
  ```
- **Self-healing** — `uv tool install graphifyy` (CLI `graphify`) + PATH `~/.local/bin` + `graphify install --platform agents`; butuh AUTH. Gagal → tool lain / manual, dicatat `PENDING:`.
- **Offline dulu** — `--code-only` (0 token) kecuali user minta semantic pass docs/media.
