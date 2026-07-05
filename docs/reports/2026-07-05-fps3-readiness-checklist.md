# FPS3 Readiness Checklist And Local Install Path

> Scope: FPS3 operator readiness checklist for the local firm-facing demo surface.

## One-Line Result

The local demo has a concrete install/run path and explicit protected-data boundary.

## Local Install Path

- Python: Python 3.11+
- Dependencies: `uv sync`
- Runtime shape: local toolkit; protected data is indexed locally by the operator

## Run Commands

1. `uv sync`
1. `python scripts\firm_facing_operator_demo_command.py --format markdown --write`
1. `python scripts\firm_facing_readiness_checklist.py --format text --write`
1. `python scripts\quality_preflight.py --format text`
1. `python scripts\rag_quality_final_gate.py --format text`

## Required Files

| Item | Path | Exists |
|---|---|---|
| objective | `docs/OBJECTIVE.md` | True |
| horizon | `docs/horizons/firm-facing-product-surface.md` | True |
| fps1_inventory | `docs/reports/2026-07-05-fps1-product-surface-inventory.md` | True |
| fps2_demo_packet | `docs/reports/2026-07-05-fps2-operator-demo-command.md` | True |
| multi_authority_close | `docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md` | True |
| client_private_close | `docs/reports/2026-07-05-client-private-parser-runtime-close-report.md` | True |
| rag_quality_close | `docs/reports/2026-07-05-rag-quality-refresh-close-report.md` | True |
| default_retriever_guard | `docs/reports/2026-07-05-default-retriever-guard.md` | True |

## Protected Boundary

- Do not commit or publish K-IFRS PDFs, parsed text, SQLite paragraph DB dumps, or embedding indexes.
- Do not place CPA exam/dogfood materials in public reports.
- Do not include real client files, raw source body, OCR text, identifiers, private embeddings, or customer-specific locators in demo output.
- Client-private parser output is structured facts only, represented as client_private_fact authority references, with deletion-gated runtime evidence.
- The demo produces decision-prep drafts. Accountant review, sign-off, audit opinion, tax/legal conclusion, and final client communication remain human responsibilities.

## Expected Outputs

- `docs/reports/2026-07-05-fps2-operator-demo-command.md`
- `docs/reports/2026-07-05-fps3-readiness-checklist.md`
- `docs/reports/2026-07-05-firm-facing-product-surface-close-report.md`

## Missing Files

- none

## Machine Result

```json
{
  "title": "FPS3 Readiness Checklist And Local Install Path",
  "ok": true,
  "horizon": "firm-facing-product-surface",
  "milestone": "FPS3",
  "required_files": {
    "objective": {
      "path": "docs/OBJECTIVE.md",
      "exists": true
    },
    "horizon": {
      "path": "docs/horizons/firm-facing-product-surface.md",
      "exists": true
    },
    "fps1_inventory": {
      "path": "docs/reports/2026-07-05-fps1-product-surface-inventory.md",
      "exists": true
    },
    "fps2_demo_packet": {
      "path": "docs/reports/2026-07-05-fps2-operator-demo-command.md",
      "exists": true
    },
    "multi_authority_close": {
      "path": "docs/reports/2026-07-05-multi-authority-runtime-hardening-close-report.md",
      "exists": true
    },
    "client_private_close": {
      "path": "docs/reports/2026-07-05-client-private-parser-runtime-close-report.md",
      "exists": true
    },
    "rag_quality_close": {
      "path": "docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
      "exists": true
    },
    "default_retriever_guard": {
      "path": "docs/reports/2026-07-05-default-retriever-guard.md",
      "exists": true
    }
  },
  "missing_files": [],
  "local_install_path": {
    "python": "Python 3.11+",
    "dependency_command": "uv sync",
    "runtime_shape": "local toolkit; protected data is indexed locally by the operator"
  },
  "run_commands": [
    "uv sync",
    "python scripts\\firm_facing_operator_demo_command.py --format markdown --write",
    "python scripts\\firm_facing_readiness_checklist.py --format text --write",
    "python scripts\\quality_preflight.py --format text",
    "python scripts\\rag_quality_final_gate.py --format text"
  ],
  "protected_boundary": [
    "Do not commit or publish K-IFRS PDFs, parsed text, SQLite paragraph DB dumps, or embedding indexes.",
    "Do not place CPA exam/dogfood materials in public reports.",
    "Do not include real client files, raw source body, OCR text, identifiers, private embeddings, or customer-specific locators in demo output.",
    "Client-private parser output is structured facts only, represented as client_private_fact authority references, with deletion-gated runtime evidence.",
    "The demo produces decision-prep drafts. Accountant review, sign-off, audit opinion, tax/legal conclusion, and final client communication remain human responsibilities."
  ],
  "expected_outputs": [
    "docs/reports/2026-07-05-fps2-operator-demo-command.md",
    "docs/reports/2026-07-05-fps3-readiness-checklist.md",
    "docs/reports/2026-07-05-firm-facing-product-surface-close-report.md"
  ],
  "report_path": "docs/reports/2026-07-05-fps3-readiness-checklist.md",
  "next_leaf": "FPS4_product_narrative_readme_surface"
}
```
