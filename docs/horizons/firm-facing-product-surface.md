# Horizon: Firm-Facing Product Surface

> Status: active
> Created: 2026-07-05
> Previous: `docs/horizons/client-private-parser-runtime.md`

## Goal

Turn the accounting intelligence runtime proof into an operator-facing local toolkit surface that a firm-side reviewer can understand and run.

This horizon is not packaging-for-release yet. It creates the demo/readiness surface: what to run, what the tool can show, what remains local/private, and which workflow outputs are ready for a PoC walkthrough.

## Why Now

The core proof now exists:

- K-IFRS RAG has quality gates and default-promotion guardrails.
- Non-IFRS source lanes are dataized as public-safe records.
- Runtime outputs separate primary/supporting/legal/fact/client-private authority groups.
- Client-private parser runtime has a structured-facts-only, deletion-gated local path.

The next missing product step is an understandable operator surface that connects these pieces into one demo flow.

## Milestones

### FPS1. Product Surface Inventory And Demo Flow

Status: complete (`docs/reports/2026-07-05-fps1-product-surface-inventory.md`)

Deliverable:

- `docs/reports/2026-07-05-fps1-product-surface-inventory.md`

Acceptance:

- Existing demo surfaces, review packs, gates, reports, and run commands are inventoried.
- One recommended first demo flow is selected.
- Gaps to FPS2~FPS5 are classified.

### FPS2. Operator Demo Command

Status: active

Deliverable:

- demo command/script that renders one firm-facing walkthrough packet
- focused tests
- `docs/reports/2026-07-05-fps2-operator-demo-command.md`

Acceptance:

- A single command produces a public-safe demo packet.
- Demo packet includes workflow result, authority boundary, private-runtime boundary, and verification status.

### FPS3. Readiness Checklist And Local Install Path

Deliverable:

- readiness checklist
- local install/run guide
- `docs/reports/2026-07-05-fps3-readiness-checklist.md`

Acceptance:

- Operator can see prerequisites, protected/private boundary, commands, and expected outputs.

### FPS4. Product Narrative README Surface

Deliverable:

- README/product section refresh or dedicated product brief
- `docs/reports/2026-07-05-fps4-product-narrative.md`

Acceptance:

- The repo explains what the accounting AI can do today, what it cannot do, and how to run the demo without exposing protected assets.

### FPS5. Firm-Facing Surface Close Gate

Deliverable:

- `scripts/firm_facing_product_surface_gate.py`
- `tests/test_firm_facing_product_surface_gate.py`
- `docs/reports/2026-07-05-firm-facing-product-surface-close-report.md`

Acceptance:

- Demo/readiness/narrative artifacts exist and pass public-safe gates.
- Client-private parser runtime gate, multi-authority runtime gate, quality preflight, and RAG final gate remain passing.

## Decision Log

- This horizon builds a local operator/demo surface, not a public SaaS product.
- It does not expose K-IFRS source text, embeddings, dogfood materials, or private client files.
- The first demo should favor the most complete workflow path over a broad but shallow feature menu.
