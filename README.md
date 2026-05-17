# Loki — Heimdall CLI

A Python CLI tool for processing [Gitleaks](https://github.com/gitleaks/gitleaks) secret scanning output. It takes raw Gitleaks JSON results and either **normalizes them into a clean JSON file** or **renders them into an HTML report** — useful for including security findings in audit reports.

---

## Overview

Gitleaks produces verbose JSON output with many fields. Heimdall strips that down to only what matters (`RuleID`, `File`, `StartLine`, `Description`), validates every entry against a Pydantic schema, and writes the result to either a filtered JSON file or a styled HTML table — ready to drop into a security audit document.

---

## Project Structure

```
loki/
├── Makefile
└── heimdall/
    ├── pyproject.toml
    └── src/heimdall/
        ├── cli.py                        # Entry point
        ├── command/
        │   ├── args.py                   # Typed dataclasses for CLI args
        │   └── parser.py                 # argparse subcommand definitions
        ├── enums/
        │   └── args.py                   # ArgsEnum (TEMPLATE | JSON)
        ├── lib/
        │   ├── factory/
        │   │   ├── args.py               # ArgsFactory — builds typed arg objects
        │   │   ├── json.py               # JSONNormalizerFactory — builder pattern
        │   │   └── template.py           # TemplateFactory — builder pattern
        │   └── parser/
        │       └── json.py               # JSONParser — loads and validates JSON file
        ├── service/
        │   ├── json/
        │   │   ├── schema.py             # GitLeaksSchema (Pydantic model)
        │   │   ├── normalizer.py         # JSONNormalizerService — filters & writes JSON
        │   │   └── config.py             # JSONNormalizerConfig dataclass
        │   └── template/
        │       ├── generator.py          # TemplateGeneratorService — renders Jinja2 HTML
        │       └── config.py             # TemplateGeneratorConfig dataclass
        ├── static/css/                   # Styles for the HTML report
        └── templates/
            └── gitleaks_report.html      # Jinja2 HTML template
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.13+ | Runtime |
| [uv](https://github.com/astral-sh/uv) | Package manager & runner |
| Pydantic v2 | Schema validation of Gitleaks JSON entries |
| Jinja2 | HTML report templating |
| Ruff | Linting and formatting |
| argparse | CLI argument parsing |

---

## Features

### Two Subcommands

**`json`** — Filter & normalize a raw Gitleaks JSON file

Takes the full Gitleaks output, validates each entry against the `GitLeaksSchema`, keeps only the 4 relevant fields (`RuleID`, `File`, `StartLine`, `Description`), and writes a clean JSON file.

**`template`** — Render a Gitleaks JSON file into an HTML report

Parses the (normalized or raw) JSON and renders it into a styled HTML table using a Jinja2 template, ready for inclusion in a security audit report.

### GitLeaks Schema (Pydantic)
Every JSON entry is validated against this schema before processing:

```python
class GitLeaksSchema(BaseModel):
    RuleID: str
    File: str
    StartLine: int
    Description: str
```

Invalid entries cause validation errors rather than silently passing through.

### Design Patterns
- **Factory pattern** for constructing services (`JSONNormalizerFactory`, `TemplateFactory`, `ArgsFactory`) — each uses a fluent builder interface
- **Frozen dataclasses** for all config objects — immutable after creation
- **Strategy-like dispatch** via `match` on `ArgsEnum` in the CLI

---

## Getting Started

### Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install

```bash
cd heimdall
uv sync
```

### Lint & Format

```bash
# From the repo root
make lint
```

---

## Usage

### Subcommand: `json` — Normalize Gitleaks output

Filters a raw Gitleaks JSON report down to the 4 key fields and writes a clean output file.

```bash
uv run heimdall json \
  --json-file-path path/to/gitleaks_output.json \
  --output-file-path path/to/filtered_output.json
```

**Input:** Full Gitleaks JSON (array of finding objects)  
**Output:** Array of objects with only `RuleID`, `File`, `StartLine`, `Description`

---

### Subcommand: `template` — Generate HTML report

Renders the Gitleaks findings into a styled HTML table using the built-in Jinja2 template.

```bash
uv run heimdall template \
  --json-file-path path/to/gitleaks_output.json \
  --template-file-name gitleaks_report.html \
  --output-file-path path/to/output_report.html
```

**Input:** Gitleaks JSON file + a template name from the `templates/` directory  
**Output:** A styled HTML file with a findings table (Rule ID, File, Line, Description)

---

## Typical Workflow

```
gitleaks detect --report-format json --report-path raw.json
       │
       ▼
heimdall json --json-file-path raw.json --output-file-path filtered.json
       │
       ▼
heimdall template --json-file-path filtered.json \
                  --template-file-name gitleaks_report.html \
                  --output-file-path report.html
       │
       ▼
  Paste report.html section into your security audit document
```

---

## HTML Report

The generated HTML report is styled for inclusion in security audit documents. It renders a table under the heading **"4. Secrets & Leakage Audit"** with columns for Rule ID, File, Line, and Description — covering Gitleaks findings as part of a broader secrets and credential leak audit.

---

## Notes

- The package entry point is `heimdall = "heimdall.cli:app"` — run with `uv run heimdall <subcommand>`
- Output directories are created automatically if they don't exist (`mkdir(parents=True, exist_ok=True)`)
- The access token lifetime in `pyproject.toml` lists `ruff` as a runtime dependency — this is likely intended as a dev dependency; move it to `[dependency-groups]` if separating dev and prod installs
- To add a new report type, add a new Pydantic schema in `service/json/schema.py`, a new Jinja2 template in `templates/`, and wire it up in `cli.py`
