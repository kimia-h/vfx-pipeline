# VFX Asset Pipeline CLI

A command-line pipeline tool for validating, ingesting, and versioning VFX assets — modeled on real studio asset management workflows used in production environments like film and television VFX.

Built with Python, Click, and SQLite. Designed for Linux/Mac/Windows terminal environments.

---

## The problem it solves

In a VFX production, hundreds of artists save thousands of files across dozens of shots. Without enforcement, filenames become inconsistent, versions get overwritten, and pipeline tools break because they can't parse asset metadata from filenames.

This tool acts as the enforcement and tracking layer — validating naming conventions, registering assets into a versioned registry, locking approved versions, and reporting pipeline status at a glance.

---

## Installation

```bash
git clone https://github.com/yourusername/vfx-pipeline.git
cd vfx-pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

---

## Naming convention

All assets must follow this pattern:
PROJECT_sq###\_sh####\_assettype_assetname_v###.ext

Example:
SPM_sq010_sh0020_model_body_v001.abc

| Part      | Description                                        | Example |
| --------- | -------------------------------------------------- | ------- |
| PROJECT   | 2–6 uppercase letters                              | SPM     |
| sq###     | Sequence number                                    | sq010   |
| sh####    | Shot number                                        | sh0020  |
| assettype | One of: model, rig, texture, render, cache, layout | model   |
| assetname | Lowercase asset identifier                         | body    |
| v###      | 3-digit version                                    | v001    |
| .ext      | Valid extension for asset type                     | .abc    |

---

## Commands

### Validate a filename

```bash
vfx-pipe validate "SPM_sq010_sh0020_model_body_v001.abc"
```

### Ingest a directory of assets

```bash
vfx-pipe ingest ./mock_assets
```

### View pipeline status report

```bash
vfx-pipe report
```

### Lock an asset version

```bash
vfx-pipe lock "path/to/SPM_sq010_sh0020_model_body_v001.abc"
```

### View version history

```bash
vfx-pipe history "path/to/SPM_sq010_sh0020_model_body_v001.abc"
```

---

## Running tests

```bash
pytest tests/ -v
```

---

## Tech stack

- Python 3.9+
- Click — CLI framework
- Rich — terminal formatting
- SQLite — asset registry
- pytest — test suite

---

## Design decisions

- **Structured validation errors** — errors tell you exactly what is wrong and how to fix it, not just that something failed
- **Checksum tracking** — MD5 checksums detect if a file changes after ingestion
- **Version locking** — once a version is locked it cannot be overwritten, mirroring picture-lock workflows in real productions
- **SQLite registry** — lightweight, portable, no server required — appropriate for a pipeline tool running on a single workstation or render node
