# FPS1 Product Surface Inventory

> Scope: FPS1 inventory for the first operator-facing local product surface.

## Result

- ok: True
- horizon: `firm-facing-product-surface`
- milestone: `FPS1`
- next leaf: `FPS2_operator_demo_command`

## Existing Surfaces

| Surface | Path | Category | Use |
|---|---|---|---|
| legacy markdown demo pack | `scripts/demo_poc.py` | demo | Existing multi-file markdown demo, mostly 1115-centric. |
| multi-authority runtime gate | `scripts/multi_authority_runtime_gate.py` | gate | Proves five evidence groups render separately. |
| client-private parser runtime gate | `scripts/client_private_parser_runtime_gate.py` | gate | Proves structured-facts-only private parser runtime and deletion close. |
| 1116 review pack | `kifrs/workflows/kifrs1116/review_pack.py` | workflow | Best first walkthrough because it has memo, journal entry, disclosure, checklist, and human review questions. |
| 1109 review pack | `kifrs/workflows/kifrs1109/review_pack.py` | workflow | Useful second demo for financial instruments classification. |
| 1115 review pack | `kifrs/workflows/kifrs1115/review_pack.py` | workflow | Useful second demo for revenue scenarios. |
| statement draft adapters | `kifrs/workflows/statement_draft/adapters.py` | workflow | Turns review packs into statement line candidates. |
| audit analytics | `kifrs/workflows/audit_analytics/metrics.py` | workflow | Adds analytical-procedure review links. |
| product objective | `docs/OBJECTIVE.md` | narrative | States the accounting intelligence product objective. |
| roadmap | `ROADMAP.md` | narrative | Tracks current horizon and next leaf. |

## Recommended First Demo Flow

- id: `lease-review-pack-authority-private-boundary`
- label: 1116 lease review pack with authority and private-runtime boundary
- why: It is the most complete and easiest firm-facing walkthrough: memo, journal entry, disclosure, checklist, authority boundary, and private parser boundary can be shown together.

### Steps

- Generate 1116 simple lease review pack.
- Render primary/supporting/legal/fact/client-private authority boundary.
- Show client-private parser runtime contract and deletion gate as local-only boundary.
- Attach verification status from multi-authority and client-private runtime gates.

## Implementation Gaps

| Milestone | Gap |
|---|---|
| FPS2 | No single operator demo command generates the recommended walkthrough packet yet. |
| FPS3 | Readiness checklist and local install/run path are scattered across reports and ROADMAP. |
| FPS4 | Product narrative does not yet plainly explain current capabilities, limits, and demo command in one surface. |
| FPS5 | No firm-facing surface close gate checks demo packet, readiness, narrative, and carried runtime/RAG gates together. |

## Errors

- none

## Machine Result

```json
{
  "title": "FPS1 Product Surface Inventory",
  "ok": true,
  "horizon": "firm-facing-product-surface",
  "milestone": "FPS1",
  "surfaces": [
    {
      "name": "legacy markdown demo pack",
      "path": "scripts/demo_poc.py",
      "category": "demo",
      "use": "Existing multi-file markdown demo, mostly 1115-centric.",
      "exists": true
    },
    {
      "name": "multi-authority runtime gate",
      "path": "scripts/multi_authority_runtime_gate.py",
      "category": "gate",
      "use": "Proves five evidence groups render separately.",
      "exists": true
    },
    {
      "name": "client-private parser runtime gate",
      "path": "scripts/client_private_parser_runtime_gate.py",
      "category": "gate",
      "use": "Proves structured-facts-only private parser runtime and deletion close.",
      "exists": true
    },
    {
      "name": "1116 review pack",
      "path": "kifrs/workflows/kifrs1116/review_pack.py",
      "category": "workflow",
      "use": "Best first walkthrough because it has memo, journal entry, disclosure, checklist, and human review questions.",
      "exists": true
    },
    {
      "name": "1109 review pack",
      "path": "kifrs/workflows/kifrs1109/review_pack.py",
      "category": "workflow",
      "use": "Useful second demo for financial instruments classification.",
      "exists": true
    },
    {
      "name": "1115 review pack",
      "path": "kifrs/workflows/kifrs1115/review_pack.py",
      "category": "workflow",
      "use": "Useful second demo for revenue scenarios.",
      "exists": true
    },
    {
      "name": "statement draft adapters",
      "path": "kifrs/workflows/statement_draft/adapters.py",
      "category": "workflow",
      "use": "Turns review packs into statement line candidates.",
      "exists": true
    },
    {
      "name": "audit analytics",
      "path": "kifrs/workflows/audit_analytics/metrics.py",
      "category": "workflow",
      "use": "Adds analytical-procedure review links.",
      "exists": true
    },
    {
      "name": "product objective",
      "path": "docs/OBJECTIVE.md",
      "category": "narrative",
      "use": "States the accounting intelligence product objective.",
      "exists": true
    },
    {
      "name": "roadmap",
      "path": "ROADMAP.md",
      "category": "narrative",
      "use": "Tracks current horizon and next leaf.",
      "exists": true
    }
  ],
  "recommended_flow": {
    "id": "lease-review-pack-authority-private-boundary",
    "label": "1116 lease review pack with authority and private-runtime boundary",
    "why": "It is the most complete and easiest firm-facing walkthrough: memo, journal entry, disclosure, checklist, authority boundary, and private parser boundary can be shown together.",
    "steps": [
      "Generate 1116 simple lease review pack.",
      "Render primary/supporting/legal/fact/client-private authority boundary.",
      "Show client-private parser runtime contract and deletion gate as local-only boundary.",
      "Attach verification status from multi-authority and client-private runtime gates."
    ]
  },
  "gaps": [
    {
      "milestone": "FPS2",
      "gap": "No single operator demo command generates the recommended walkthrough packet yet."
    },
    {
      "milestone": "FPS3",
      "gap": "Readiness checklist and local install/run path are scattered across reports and ROADMAP."
    },
    {
      "milestone": "FPS4",
      "gap": "Product narrative does not yet plainly explain current capabilities, limits, and demo command in one surface."
    },
    {
      "milestone": "FPS5",
      "gap": "No firm-facing surface close gate checks demo packet, readiness, narrative, and carried runtime/RAG gates together."
    }
  ],
  "errors": [],
  "next_leaf": "FPS2_operator_demo_command",
  "report_path": "docs/reports/2026-07-05-fps1-product-surface-inventory.md"
}
```
