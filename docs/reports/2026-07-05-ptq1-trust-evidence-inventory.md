# PTQ1 Trust Evidence Inventory

> Scope: PTQ1 inventory of evidence sources used to make the firm-facing demo trustable.

## One-Line Result

Trust evidence sources are present and classified by product role, speed, public safety, and protected-data dependency.

## Evidence Sources

| Source | Path | Role | Speed | Public Safe | Protected Data Required | Exists |
|---|---|---|---|---|---|---|
| quality preflight | `scripts/quality_preflight.py` | baseline public-safe quality gate | fast | True | False | True |
| RAG quality final gate | `scripts/rag_quality_final_gate.py` | retrieval and citation quality gate | heavy | True | True | True |
| default retriever guard | `scripts/default_retriever_guard.py` | default-promotion safety gate | fast | True | False | True |
| firm-facing product surface close gate | `scripts/firm_facing_product_surface_gate.py` | demo surface integration gate | fast | True | False | True |
| multi-authority runtime gate | `scripts/multi_authority_runtime_gate.py` | authority-boundary runtime gate | heavy | True | True | True |
| client-private parser runtime gate | `scripts/client_private_parser_runtime_gate.py` | private-runtime boundary gate | heavy | True | True | True |
| FPS2 operator demo packet | `docs/reports/2026-07-05-fps2-operator-demo-command.md` | operator-visible demo evidence | fast | True | False | True |
| firm-facing README narrative | `README.md` | product claims and non-goals | fast | True | False | True |

## Categories

### fast_public_safe
- quality preflight
- default retriever guard
- firm-facing product surface close gate
- FPS2 operator demo packet
- firm-facing README narrative

### heavy_regression
- RAG quality final gate
- multi-authority runtime gate
- client-private parser runtime gate

### protected_data_dependent
- RAG quality final gate
- multi-authority runtime gate
- client-private parser runtime gate

### operator_visible
- FPS2 operator demo packet
- firm-facing README narrative

## Gaps To Next Milestones

| Milestone | Gap |
|---|---|
| PTQ2 | Review-pack sections do not yet expose ready/caution/human-review-required confidence labels. |
| PTQ3 | Failure modes are known across reports but not normalized into one operator action matrix. |
| PTQ4 | Retriever promotion decision exists as guardrails but not as a product-facing evidence pack. |
| PTQ5 | No trust-quality close gate yet ties PTQ reports to carried RAG/runtime/product gates. |

## Missing

- none

## Machine Result

```json
{
  "title": "PTQ1 Trust Evidence Inventory",
  "ok": true,
  "horizon": "product-trust-and-quality-evidence",
  "milestone": "PTQ1",
  "sources": [
    {
      "name": "quality preflight",
      "path": "scripts/quality_preflight.py",
      "exists": true,
      "evidence_role": "baseline public-safe quality gate",
      "speed": "fast",
      "public_safe": true,
      "protected_data_required": false,
      "use_in_product_trust": "Shows focused tests, local-rag threshold, authority validators, and user_note audit are passing."
    },
    {
      "name": "RAG quality final gate",
      "path": "scripts/rag_quality_final_gate.py",
      "exists": true,
      "evidence_role": "retrieval and citation quality gate",
      "speed": "heavy",
      "public_safe": true,
      "protected_data_required": true,
      "use_in_product_trust": "Shows opt-in repair retriever reaches recall@20 1.000 and absent required citations 0 when local eval data exists."
    },
    {
      "name": "default retriever guard",
      "path": "scripts/default_retriever_guard.py",
      "exists": true,
      "evidence_role": "default-promotion safety gate",
      "speed": "fast",
      "public_safe": true,
      "protected_data_required": false,
      "use_in_product_trust": "Shows runtime default remains hybrid and repair retriever is not exposed as MCP default."
    },
    {
      "name": "firm-facing product surface close gate",
      "path": "scripts/firm_facing_product_surface_gate.py",
      "exists": true,
      "evidence_role": "demo surface integration gate",
      "speed": "fast",
      "public_safe": true,
      "protected_data_required": false,
      "use_in_product_trust": "Shows demo command, readiness checklist, README narrative, and carried evidence reports are connected."
    },
    {
      "name": "multi-authority runtime gate",
      "path": "scripts/multi_authority_runtime_gate.py",
      "exists": true,
      "evidence_role": "authority-boundary runtime gate",
      "speed": "heavy",
      "public_safe": true,
      "protected_data_required": true,
      "use_in_product_trust": "Shows primary/supporting/legal/fact/client-private authority groups are separated and carried regressions pass."
    },
    {
      "name": "client-private parser runtime gate",
      "path": "scripts/client_private_parser_runtime_gate.py",
      "exists": true,
      "evidence_role": "private-runtime boundary gate",
      "speed": "heavy",
      "public_safe": true,
      "protected_data_required": true,
      "use_in_product_trust": "Shows structured-facts-only private parser runtime, client_private_fact references, and deletion gate remain connected."
    },
    {
      "name": "FPS2 operator demo packet",
      "path": "docs/reports/2026-07-05-fps2-operator-demo-command.md",
      "exists": true,
      "evidence_role": "operator-visible demo evidence",
      "speed": "fast",
      "public_safe": true,
      "protected_data_required": false,
      "use_in_product_trust": "Shows the concrete 1116 walkthrough output a firm-side reviewer sees."
    },
    {
      "name": "firm-facing README narrative",
      "path": "README.md",
      "exists": true,
      "evidence_role": "product claims and non-goals",
      "speed": "fast",
      "public_safe": true,
      "protected_data_required": false,
      "use_in_product_trust": "Shows what the product claims, what it does not claim, and the demo command."
    }
  ],
  "categories": {
    "fast_public_safe": [
      "quality preflight",
      "default retriever guard",
      "firm-facing product surface close gate",
      "FPS2 operator demo packet",
      "firm-facing README narrative"
    ],
    "heavy_regression": [
      "RAG quality final gate",
      "multi-authority runtime gate",
      "client-private parser runtime gate"
    ],
    "protected_data_dependent": [
      "RAG quality final gate",
      "multi-authority runtime gate",
      "client-private parser runtime gate"
    ],
    "operator_visible": [
      "FPS2 operator demo packet",
      "firm-facing README narrative"
    ]
  },
  "missing": [],
  "gaps": [
    {
      "milestone": "PTQ2",
      "gap": "Review-pack sections do not yet expose ready/caution/human-review-required confidence labels."
    },
    {
      "milestone": "PTQ3",
      "gap": "Failure modes are known across reports but not normalized into one operator action matrix."
    },
    {
      "milestone": "PTQ4",
      "gap": "Retriever promotion decision exists as guardrails but not as a product-facing evidence pack."
    },
    {
      "milestone": "PTQ5",
      "gap": "No trust-quality close gate yet ties PTQ reports to carried RAG/runtime/product gates."
    }
  ],
  "report_path": "docs/reports/2026-07-05-ptq1-trust-evidence-inventory.md",
  "next_leaf": "PTQ2_review_pack_confidence_contract"
}
```
