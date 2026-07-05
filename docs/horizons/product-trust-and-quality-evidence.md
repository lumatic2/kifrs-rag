# Horizon: Product Trust And Quality Evidence

> Status: active
> Created: 2026-07-05
> Sequence: post `firm-facing-product-surface`

## Goal

Turn the firm-facing demo into a trustable PoC surface by making quality, evidence confidence, failure boundaries, and retriever promotion decisions visible and testable.

This horizon does not broaden workflow coverage. It answers a narrower firm-side question: "Can we trust the demo output, and where must a human stop?"

## Why Now

`firm-facing-product-surface` made the demo runnable. The remaining weakness is confidence. A reviewer can now see the demo, but the product still needs stronger evidence around:

- RAG and citation quality on current evaluation assets.
- Which retriever is default and why the repair retriever remains opt-in.
- Which review-pack sections are high confidence vs human-review gated.
- What failure modes are expected and how the operator should interpret them.

## Milestones

### PTQ1. Trust Evidence Inventory

Status: complete (`docs/reports/2026-07-05-ptq1-trust-evidence-inventory.md`)

Deliverable:

- `docs/reports/2026-07-05-ptq1-trust-evidence-inventory.md`

Acceptance:

- Existing quality, RAG, default-guard, runtime, and review-pack evidence is inventoried.
- Each evidence source is labeled as fast, heavy, private-data-dependent, or public-safe.
- Gaps to PTQ2~PTQ5 are classified.

### PTQ2. Review Pack Confidence Contract

Status: active

Deliverable:

- confidence contract module or script
- focused tests
- `docs/reports/2026-07-05-ptq2-review-pack-confidence-contract.md`

Acceptance:

- Review-pack sections can be labeled as ready, caution, or human-review-required.
- Labels are derived from existing status/citations/authority/private-boundary signals.
- The contract does not imply autonomous final accounting judgment.

### PTQ3. Failure Boundary Matrix

Deliverable:

- failure-boundary matrix report
- focused tests
- `docs/reports/2026-07-05-ptq3-failure-boundary-matrix.md`

Acceptance:

- Common failure modes are grouped by retrieval, citation, missing private facts, unsupported workflow, and human judgment boundary.
- Each failure mode has an operator action and verification command.

### PTQ4. Promotion Decision Evidence Pack

Deliverable:

- default-promotion evidence pack
- focused tests
- `docs/reports/2026-07-05-ptq4-promotion-decision-evidence.md`

Acceptance:

- Default retriever promotion remains explicitly allowed or deferred with current evidence.
- The decision cites RAG final gate, default guard, and failure matrix.
- Runtime default is not changed unless a separate explicit authorization exists.

### PTQ5. Trust And Quality Close Gate

Deliverable:

- `scripts/product_trust_quality_gate.py`
- `tests/test_product_trust_quality_gate.py`
- `docs/reports/2026-07-05-product-trust-quality-close-report.md`

Acceptance:

- PTQ1~PTQ4 reports exist and pass public-safe checks.
- `quality_preflight`, `rag_quality_final_gate`, `default_retriever_guard`, and firm-facing surface gate remain passing.

## Decision Log

- This horizon improves trust evidence, not workflow breadth.
- No default retriever promotion without explicit authorization and stronger evidence.
- Human review and final sign-off remain outside automation.
