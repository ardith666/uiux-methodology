# Obsidian Integration Module

Modul referensi Obsidian untuk semua agent yang memakai skill ini. **Aktif** saat agent bekerja di dalam **vault Obsidian** (folder `.obsidian/` ada di CWD atau parent) atau saat user minta memakai Obsidian (catatan, base, canvas, CLI).

Fungsi: bukan cuma mencatat — tapi **merangkum, mengkoneksikan, meretain** semua informasi yang dibaca/dihasilkan agent ke dalam vault, agar tetap ada lintas sesi dan lintas mesin.

## Design Philosophy (mengapa, bukan cuma sintaks)

Obsidian dibangun di atas 3 prinsip yang harus dijaga di setiap tulisan:

1. **Local-first / plain text** — semua informasi adalah file teks lokal yang bisa dibaca langsung.
2. **Bi-directional links** — note bukan file, tapi simpul jaringan. Wikilink `[[...]]` adalah connective tissue utama; backlink yang membuat pengetahuan terhubung.
3. **Extensibility** — properties queryable, bases, canvas, plugin. Tulis data terstruktur supaya bisa di-query & disambungkan lagi.

Setiap note/tulisan yang agent buat di vault **WAJIB**:
- Punya **frontmatter** (`title`, `tags`, `status`, `created`) — detail di `markdown.md`
- Memakai **wikilink `[[...]]`** untuk semua rujukan antar-note di vault (bukan `[text](path)`)
- Pakai **callout** untuk info penting, **embed `![[...]]`** untuk reuse konten (prinsip DRY)
- Ber-timestamp `[YYYY-MM-DD]` untuk entry append-only

## Deteksi Vault & Kemampuan

- Cek `.obsidian/` di CWD / parent → **di vault** → mode vault-native aktif.
- `which obsidian` tersedia → bisa pakai fitur CLI (search, backlinks, properties, tasks, daily, bases, dev). Detail: `cli.md`.

## Empat Alur Retain

| Alur | Kapan | Aksi |
|------|-------|------|
| **Mencatat** | Output phase-gate, keputusan, status | Tulis note project `knowledge/` vault-native (frontmatter + wikilinks). Update tracker base kalau ada |
| **Merangkum** | Riset / artikel / halaman web | `defuddle parse <url> --md` → distilasi → simpan note ringkas → wikilink ke note project. Detail: `defuddle.md` |
| **Mengkoneksikan** | Keputusan/learning baru, project mulai | `[[wikilinks]]`, embed `![[...]]`, `.base` untuk data terstruktur, `.canvas` untuk peta visual. Detail: `bases.md`, `canvas.md` |
| **Meretain** | Akhir sesi, lintas mesin | Entry append-only + timestamp di `knowledge/history.md`; sync via git; agent berikutnya baca vault dulu |

## Vault Hygiene — graph check (pola 2026-08-29)

Setiap selesai menulis/menkoneksikan note, verifikasi health graph via CLI:

```bash
obsidian unresolved   # wikilink yang menunjuk file tak ada (dangling)
obsidian orphans      # note tanpa backlink (terisolasi)
```

Aturan yang menurun dari audit nyata (vault ~27 note: 22 orphan, 10 unresolved):

1. **Wikilink harus persis nama file.** `[[Zipline]]` ≠ `zipline-upload.md` → unresolved walau note-nya ada. Kalau tampilan beda: `[[zipline-upload|Zipline]]`.
2. **Jangan me-wikilink nama file/asset** (`[[buffer_config.json]]`) → inline code `` `buffer_config.json` ``.
3. **Link markdown wajib skema lengkap** — `(zipline.digitechnesia.my.id)` tanpa `https://` dianggap file lokal → unresolved. Pakai `(https://zipline.digitechnesia.my.id)`.
4. **Folder ≠ koneksi.** Note seduluran (plan di subfolder project, cheat sheet sekelas) wajib saling di-`[[link]]` — taruh bareng tidak cukup.
5. **Duplikat/pasangan → cross-link + tandai canonical.** Dua note topik sama (mis. `coding/x` vs `project/x`) wajib saling menunjuk; kalau duplikat penuh, tandai mana yang dipertahankan.
6. **MOC/index hub.** Kalau `orphans` mulai banyak → tawarkan buat note index yang me-wikilink semua note (semua langsung dapat backlink).
7. **Target setelah masuk:** `unresolved` tinggal konsep yang memang belum punya note (catat `PENDING:`), `orphans` berisi note yang benar-benar standalone.

## Retention Policy (restraint)

Proses mencatat sendiri adalah bagian dari belajar — jangan menggantikan catatan pribadi user:

- **Agent HANYA menulis** continuity artifacts: keputusan, learning, status, ringkasan bahan yang di-ingest, index/bases/canvas, dan update `knowledge/`.
- **JANGAN** membuat catatan penuh yang meniru konten milik user (artikel pribadi, catatan kuliah, jurnal). Tawarkan outline/ringkasan, biar user yang menulis isinya.
- Ragu → tulis ringkas + `PENDING:` status.

## Dependensi & Self-Healing

Kebijakan: **setiap capability yang belum ada → tanya user dulu → bantu deploy → verifikasi.** Jangan pura-pura jalan, jangan langsung nyerah.

| # | Dependency | Cek | Jika missing → tanya + deploy | Jika gagal |
|---|-----------|-----|------------------------------|-----------|
| 1 | Obsidian app | `ls /Applications/Obsidian.app` / registry OS | Bantu unduh dari obsidian.md/download, pandu instalasi GUI | Plain markdown vault-native, `PENDING:` |
| 2 | Obsidian CLI enabled | `obsidian-cli version` (keluar pesan "not enabled"?) | Pandu toggle **Settings → General → Advanced → Command line interface**, retry 1x | Hand back `PENDING:` |
| 3 | `obsidian` di PATH | `which obsidian` | Tawarkan ekspor PATH (`/Applications/Obsidian.app/Contents/MacOS`) ke shell rc atau symlink `~/.local/bin/obsidian` (AUTH dulu) | Pakai path absolut langsung, jangan ubah rc |
| 4 | defuddle | `which defuddle` | `npm install -g defuddle` (AUTH dulu) | WebFetch internal untuk riset web, `PENDING:` |
| 5 | node/npm | `which node npm` | Pandu install Node LTS | Skip defuddle |

Verifikasi konret tiap deploy:
- `obsidian vault`, `obsidian search query=test limit=1`
- `defuddle --help`

**Yang tetap jalan tanpa dependensi apa pun:** menulis/membaca markdown vault-native (OFM) + `.base` + `.canvas` — semua cuma file teks. CLI hanya menambah search/backlinks/properties/tasks/daily.

## Setup & Update per Mesin (parity semua mesin kerja)

```bash
# 1. Pull skill repo (pembawa modul ini) di tiap mesin
git -C ~/.agents/skills/dev-methodology pull     # dan/atau uiux-methodology
# 2. Pastikan versi terbaru
cat ~/.agents/skills/dev-methodology/VERSION     # harus >= 3.0.0
# 3. Cek dependensi
which defuddle && which obsidian
# 4. Install yang kurang (tabel di atas)
npm install -g defuddle
```

**Cek update rilis saat sesi baru:** frontmatter `SKILL.md` memuat `version:` (metadata yang dibaca agent saat load). Agent di mesin mana pun bandingkan dengan remote:

```bash
git -C ~/.agents/skills/<nama-skill> fetch --tags && git tag -l | sort -V | tail -1
```

Tag lokal < remote → ada **rilis terbaru** → tawarkan `git pull` lalu lanjut kerja.

## Atribusi

Konten OFM/Bases/Canvas/CLI/defuddle diadaptasi dari [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) (MIT License). Kasus Reading List & mind-map workflow dari artikel [Addo Zhang — Obsidian Skills](https://addozhang.medium.com/obsidian-skills-empowering-ai-agents-to-master-obsidian-knowledge-management-8b4f6d844b34).