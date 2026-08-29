# Obsidian CLI - Referensi Perintah

Interaksi vault lewat binary obsidian. Butuh Obsidian app 1.12+ yang sedang jalan + CLI di-enable.

Diadaptasi dari kepano/obsidian-skills (MIT).

---


# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## Command reference

Run `obsidian help` to see all available commands. This is always up to date. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newline and `\t` for tab.

## File targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

## Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Plugin development

### Develop/test cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — if errors appear, fix and repeat from step 1:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually** with a screenshot or DOM inspection:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

### Additional developer commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
```

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.

---
## Prerequisites & Setup (Self-Healing)

CLI butuh: **Obsidian app 1.12+** yang sedang jalan + fitur CLI di-enable (sekali per mesin).

```bash
# Cek app ada
ls -d "/Applications/Obsidian.app"
# Cek binary + status CLI
"/Applications/Obsidian.app/Contents/MacOS/obsidian-cli" version
```

**Enable (GUI, sekali per mesin):** Obsidian → Settings → General → Advanced → **Command line interface** → on. Prompt registrasi otomatis mendaftarkan `obsidian` ke PATH.

**PATH fallback (macOS):**
```bash
echo 'export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"' >> ~/.zshrc
source ~/.zshrc
which obsidian
```

**Verifikasi:**
```bash
obsidian vault
obsidian search query=test limit=1
```

**Kalau CLI belum enable / app tidak jalan** → jangan pura-pura: pakai file ops langsung (Read/Write file di vault) untuk yang bisa, fitur CLI di-skip, dan catat `PENDING:` di report.