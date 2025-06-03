# CHeaT – Lightweight Defense Planting CLI

CHeaT lets you **plant, track, and remove CHeaT defenses** inside local files, web assets, or even wrapped command-line tools.
Everything is driven from a single `main.py` entry point and a small JSON database you can extend at will.

---

## ✨ Quick Features

| Action       | What it does                                                                                               |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| `plant`      | Insert a defense into a target asset. Supports random or manually chosen technique/template. |
| `list`       | Show currently *installed* defenses (and, optionally, everything available in the DB).                     |
| `remove`     | Delete one defense by its ID.                                                                              |
| `remove_all` | Wipe every installed defense in one go.                                                                    |

---

## ⚙️ Installation

```bash
git clone https://github.com/Daniel-Ayz/cheat.git
cd cheat
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

---

## 🚀 Usage

### 1. Plant a Defense

<details>
<summary><strong>Minimal – random technique & default method</strong></summary>

```bash
cheat \
  --action plant \
  --details '{
    "assettype": "web_file",
    "file_path": "tests/test.html",
    "technique": "random"
  }'
```

</details>

<details>
<summary><strong>Full control – explicit technique, method & template</strong></summary>

```bash
cheat \
  --action plant \
  --details '{
    "assettype": "web_file",
    "file_path": "tests/test.html",
    "technique": "S1i",
    "method": "prompt_injection",
    "template": "Combined_Attack"
  }'
```

</details>

#### `details` JSON schema

| Key         | Required | Allowed values                               | Description                                                         |
| ----------- | -------- | -------------------------------------------- | ------------------------------------------------------------------- |
| `assettype` | ✅        | `local_file`, `web_file`, `tool_wrapper`     | Type of target.                                                     |
| `file_path` | ✅        | Path                                         | File or binary to modify / wrap.                                    |
| `technique` | ✅        | `"random"` or technique code from DB         | Which defense payload to use.                                       |
| `method`    | ❌        | `honeytoken`, `prompt_injection`, `"random"` | Defaults to **prompt\_injection**. `"random"` picks one of the two. |
| `template`  | ❌        | `"random"` or template name from DB          | How the payload is framed. Default = `Combined_Attack`.             |

💡 **Randomisation**: supply `"random"` for `method`, `technique`, or `template` to let Gotcha PT choose.

---

### 2. List Installed Defenses

```bash
cheat --action list --type installed
```

(Use `--type available` to dump everything defined in the DB.)

---

### 3. Remove Defenses

#### a. Remove all at once

```bash
cheat --action remove_all
```

#### b. Remove one by ID

```bash
cheat --action remove --id "997df4f9-4268-45cf-b64b-f0130be0b9a9"
```

Obtain the ID column from `--action list`.

---

## 🗄️ Customising the Database

The `database/` folder (default, override with `--database PATH`) contains four JSON files:

```
├── honeytokens_defenses.json
├── honeytokens_templates.json
├── prompt_injection_defenses.json
└── prompt_injection_templates.json
```

Add or edit entries to create new techniques or templates.
Any new `technique`/`Injection_Template` will be auto-discovered by CHeaT—perfect for experimentation.

---

## 🛡️ How It Works (1-min peek)

1. **DefenseCreator** merges a *template* with a *technique* → `prefix` + `suffix`.
2. **DefenseInstaller**
   * *local / web files*: prefix is prepended, suffix appended.
   * *tool wrapper*: original binary → `*_original`; wrapper echoes prefix, calls original, echoes suffix, and keeps ownership + mode.
3. **DefenseDatabase** tracks what you installed so you can list or roll back reliably.

---

## ❓ FAQ

| Question                                        | Answer                                                                |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| *Do I need sudo?*                               | Only when wrapping binaries you don’t own (CHeaT checks & warns). |
| *What happens if I edit the DB after planting?* | Existing installs stay unchanged; new plants use updated payloads.    |
| *Can I point to a different DB?*                | Yes – `--database /path/to/dbdir`.                                    |

---

