# Defuddle - Ekstraksi Web ke Markdown

Konten bersih dari halaman web (tanpa iklan/navigasi) -> hemat token.

Diadaptasi dari kepano/obsidian-skills (MIT).

---


# Defuddle

Use Defuddle CLI to extract clean readable content from web pages. Prefer over WebFetch for standard web pages — it removes navigation, ads, and clutter, reducing token usage.

If not installed: `npm install -g defuddle`

## Usage

Always use `--md` for markdown output:

```bash
defuddle parse <url> --md
```

Save to file:

```bash
defuddle parse <url> --md -o content.md
```

Extract specific metadata:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with both HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |

---
## Setup & Self-Healing

Butuh Node.js + npm + binary `defuddle` global.

```bash
which node npm          # cek node/npm
npm install -g defuddle # install global (minta AUTH dulu)
defuddle --help         # verifikasi
```

Kalau node tidak ada → pandu install Node LTS (Homebrew `brew install node`, atau nodejs.org). Kalau defuddle tetap gagal → fallback ke WebFetch internal untuk riset web + catat `PENDING:`.

**Kapan pakai:** URL web biasa (artikel, blog, docs, berita) → `defuddle parse <url> --md`. **Jangan** untuk URL `.md`/`.txt` mentah — itu sudah markdown, langsung WebFetch.