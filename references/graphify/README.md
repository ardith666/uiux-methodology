# Graphify Integration Module

Modul referensi untuk agent yang memakai skill ini. **Aktif** saat bekerja di codebase yang punya `graphify-out/` (knowledge graph) atau saat perlu memahami arsitektur project — map dulu, query, bukan grep.

Dibuat oleh [Graphify-Labs](https://github.com/Graphify-Labs/graphify) (Apache-2.0). Paket PyPI resmi bernama **`graphifyy`** (dobel-y) — CLI-nya tetap `graphify`. Abaikan paket `graphify*` lain yang tidak berafiliasi.

## Design Philosophy

1. **Local-first / deterministic** — kode diparse via tree-sitter AST: 0 token LLM, tidak ada yang keluar mesin. (Docs/PDF/gambar/video butuh semantic pass via model sesi agent atau API key.)
2. **Real graph, bukan vector store** — no embeddings: node = konsep, edge = relasi nyata yang bisa ditelusuri.
3. **Honest audit trail** — tiap edge berlabel `EXTRACTED` (eksplisit di source) / `INFERRED` (resolusi graphify) / `AMBIGUOUS`. Jangan pernah menampilkan INFERRED sebagai fakta.
4. **Query-first** — kalau graph ada, tanya graph dulu (`query` / `path` / `explain`) sebelum baca file satu-satu.

## Output & Retention

| File | Fungsi |
|---|---|
| `graphify-out/graph.html` | Visual interaktif — klik node, filter, search, buka di browser |
| `graphify-out/GRAPH_REPORT.md` | God nodes, komunitas, koneksi mengejutkan, 4-5 pertanyaan saran |
| `graphify-out/graph.json` | Full graph (sumber query) — **commit ke git** |

**Retention policy:** `graphify-out/` di-commit ke git repo project supaya semua developer/agent mulai dari map yang sama. Tambahan `.gitignore`: `graphify-out/cost.json` (lokal saja). Setelah `git pull`: jalankan `graphify update .`. Autopilot: `graphify hook install` — rebuild otomatis saat commit & checkout branch + merge driver `graph.json` (tanpa conflict marker).

**Aturan hasil → `knowledge/`:** Semua hasil dari sesi pakai skill ini masuk ke folder `knowledge/` (di dalam project / vault). Jangan buat file hasil di luar folder itu:
- Temuan, digest, ringkasan `GRAPH_REPORT.md` → `knowledge/` (mis. `knowledge/graph-report-<project>.md`)
- Wiki graph (`graphify . --wiki`) → arahkan output ke folder `knowledge/` biar retain lintas sesi (frontmatter + wikilink kalau vault)
- Knowledge entries & log → ikuti format `knowledge/` di SKILL.md (timeline/decision/lessons)
Satunya yang BOLEH di luar `knowledge/`: `graphify-out/` itu sendiri (artefak teknis yang wajib di-commit ke repo — bukan "hasil sesi agent").

## Kapan Pakai

- Project punya `graphify-out/` → tanya graph dulu sebelum baca file (Phase 1/2 evidence).
- Belum ada graph → tawarkan build: `graphify extract . --code-only` (100% offline) atau `/graphify .`.
- Melacak alur antar dua konsep: `graphify path "A" "B"`.
- Menjelaskan satu konsep + relasinya: `graphify explain "X"`.
- Setelah banyak ngoding: `graphify update .` — **jangan query graph yang basi**.
- Pertanyaan plain-language: `graphify query "..."` → subgraph scoped.

## Perintah Inti

| Perintah | Fungsi |
|---|---|
| `graphify extract .` | Bangun graph (`--code-only` = offline penuh; `--no-viz` skip HTML) |
| `graphify cluster-only .` | Update komunitas/laporan tanpa re-extract |
| `graphify update .` | Re-extract hanya file yang berubah |
| `graphify query "<q>"` | Subgraph jawaban untuk pertanyaan plain-language |
| `graphify path "A" "B"` | Jalur terpendek antar dua node (`--undirected` kalau arah tak penting) |
| `graphify explain "X"` | Detail node + semua connection berlabel |
| `graphify . --wiki` | Ekspor wiki markdown dari graph |
| `graphify hook install` | Rebuild otomatis saat commit/checkout (per-project) |
| `graphify add <url>` | Tambah paper/video ke graph |
| `python -m graphify.serve graph.json` | Expose graph via MCP (query_graph, get_node, get_neighbors, shortest_path, ...) |

Jalankan lewat skill `/graphify` (global, `~/.agents/skills/graphify/`) atau CLI langsung.

## Dependensi & Self-Healing

Kebijakan: capability belum ada → **tanya user dulu → bantu deploy → verify.** Jangan pura-pura jalan.

| # | Dependency | Cek | Jika missing → tanya + deploy | Jika gagal |
|---|-----------|-----|------------------------------|-----------|
| 1 | Python | `python3 --version` (min 3.10) | Pandu install Python LTS | Grep/manual baca file, `PENDING:` |
| 2 | uv (recommended) | `uv --version` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` (user-scoped, `~/.local/bin`) | pipx / pip |
| 3 | graphify CLI | `which graphify` | `uv tool install graphifyy` (paket **graphifyy**, CLI `graphify`) | File ops manual |
| 4 | `graphify` di PATH | `which graphify` | `uv tool update-shell`; pastikan `~/.local/bin` di PATH | Pakai `~/.local/bin/graphify` absolut |
| 5 | API key (non-code) | env `ANTHROPIC_API_KEY`/`GEMINI_API_KEY`/dst | Hanya untuk semantic pass docs/PDF/gambar | `--code-only` (full offline, 0 token) |

Verifikasi konkret:
```bash
graphify --version
graphify extract . --code-only --no-viz && ls graphify-out/graph.json
graphify explain "<nama-konsep>"   # harus muncul edge berlabel EXTRACTED/INFERRED
```

## Cara Instalasi & Deploy (untuk agent di mesin lain)

Policy: capability belum ada → **jangan asal install, jangan pura-pura jalan.** Cek-req → **tanya user → bantu deploy → verify.** Prompt ke user WAJIB diberikan dulu kalau butuh aksi sistem (install, PATH, hook).

### 1. Cek kebutuhan

```bash
python3 --version        # min 3.10
uv --version             # recommended manager
which graphify           # CLI sudah ada?
ls graphify-out/ 2>/dev/null   # graph sudah ada di project ini?
```

### 2. Prompt AUTH ke user

Kalau `graphify` belum ada, tunjukkan prompt ini (jangan install sebelum disetujui):

> **Graphify belum terpasang di mesin ini.** Untuk bisa map & query arsitektur codebase (buat memahami project lebih cepat) saya perlu meng-install:
> 1. `graphify` CLI via uv — `curl -LsSf https://astral.sh/uv/install.sh | sh` (user-scoped, `~/.local/bin`) lalu `uv tool install graphifyy` (paket PyPI: **graphifyy** dobel-y)
> 2. Register skill assistant — `graphify install --platform agents` (global, `~/.agents/skills/graphify/`)
> 3. Hindari API key — saya akan jalan `--code-only` (offline, 0 token). Docs/PDF/gambar akan di-skip atau diproses via model sesi ini.
> Setujui? (ya / skip — kalau skip saya kerja pakai grep/manual dan catat `PENDING:`)

### 3. Deploy & verify

```bash
uv tool install graphifyy && uv tool update-shell   # install CLI (sekali per mesin)
graphify install --platform agents                  # skill global (dibaca opencode)

# per project (di dalam checkout):
graphify extract . --code-only --no-viz
graphify explain "<nama-konsep>"    # harus muncul edge berlabel EXTRACTED/INFERRED
graphify hook install               # rebuild otomatis saat commit & checkout
```

### 4. Update per mesin

```bash
git pull && graphify update .       # graph basi → update dulu sebelum query
```

Jika install gagal → kerja manual (grep/baca file), catat `PENDING:` di `knowledge/`, jangan blokir task.

## Atribusi

- Tool: [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (Apache-2.0 & MIT, YC S26).
- Modul wrapper ini ringkasan + panduan pemakaian; bukan fork.