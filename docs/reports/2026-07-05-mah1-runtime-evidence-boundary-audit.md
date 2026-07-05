# MAH1 Runtime Evidence Boundary Audit

> Scope: MAH1 audit for multi-authority runtime hardening.

## Result

- ok: True
- horizon: `multi-authority-runtime-hardening`
- milestone: `MAH1`
- next leaf: `MAH2_runtime_evidence_contract_hardening`

## What Exists Now

| Surface | Path | Roles | Meaning |
|---|---|---|---|
| runtime evidence loader | `kifrs/runtime/evidence.py` | supporting_interpretation, legal_boundary, fact_evidence | Loads the older evidence manifest into safe reference dictionaries. |
| external evidence panel | `kifrs/runtime/evidence_panel.py` | supporting_interpretation, legal_boundary, fact_evidence | Renders non-IFRS evidence by role in review-pack style markdown. |
| answer boundary | `kifrs/runtime/answer_boundary.py` | primary_kifrs_evidence, supporting_interpretation, legal_boundary, fact_evidence | Separates K-IFRS primary citations from external evidence references. |
| 1116 review pack | `kifrs/workflows/kifrs1116/review_pack.py` | supporting_interpretation, legal_boundary, fact_evidence | Accepts optional external evidence panel data. |
| 1109 review pack | `kifrs/workflows/kifrs1109/review_pack.py` | supporting_interpretation, legal_boundary, fact_evidence | Accepts optional external evidence panel data. |
| 1115 review pack | `kifrs/workflows/kifrs1115/review_pack.py` | supporting_interpretation, legal_boundary, fact_evidence | Accepts optional external evidence panel data. |
| statement draft schema | `kifrs/workflows/statement_draft/schema.py` | fact_evidence | Carries evidence references for statement line candidates. |

## NIS Handoff Compared To Runtime

| Source record type | Citation role | Authority level | Runtime support |
|---|---|---|---|
| document_metadata | supporting_interpretation | supporting | supported |
| law_locator | legal_boundary | legal_boundary | supported |
| structured_fact | fact_evidence | fact | supported |
| client_private_fact | collection_seed | client_private | gap |

## Hardening Gaps

| Milestone | Surface | Gap |
|---|---|---|
| MAH2 | runtime authority contract | NIS source records are validated but not yet converted by a shared authority boundary object. |
| MAH2 | client-private boundary | Client-private source records exist only as a public-safe handoff placeholder and are not represented in runtime output yet. |
| MAH3 | review packs | Review packs have an external evidence panel, but not a five-group authority panel with client-private placeholder support. |
| MAH4 | statement draft and analytics | Structured facts need a runtime hook that keeps calculations as fact evidence rather than primary accounting authority. |
| MAH5 | composer gate | No single gate proves primary/supporting/legal/fact/private evidence render together without protected source bodies. |

## Machine Result

```json
{
  "title": "MAH1 Runtime Evidence Boundary Audit",
  "ok": true,
  "horizon": "multi-authority-runtime-hardening",
  "milestone": "MAH1",
  "source_record_validation": {
    "ok": true,
    "errors": [],
    "total": 4,
    "by_type": {
      "client_private_fact": 1,
      "document_metadata": 1,
      "law_locator": 1,
      "structured_fact": 1
    }
  },
  "chunking_policy_lanes": [
    "client_private_fact",
    "document_metadata",
    "law_locator",
    "structured_fact"
  ],
  "runtime_surfaces": [
    {
      "name": "runtime evidence loader",
      "path": "kifrs/runtime/evidence.py",
      "exists": true,
      "category": "runtime",
      "supported_roles": [
        "supporting_interpretation",
        "legal_boundary",
        "fact_evidence"
      ],
      "note": "Loads the older evidence manifest into safe reference dictionaries."
    },
    {
      "name": "external evidence panel",
      "path": "kifrs/runtime/evidence_panel.py",
      "exists": true,
      "category": "rendering",
      "supported_roles": [
        "supporting_interpretation",
        "legal_boundary",
        "fact_evidence"
      ],
      "note": "Renders non-IFRS evidence by role in review-pack style markdown."
    },
    {
      "name": "answer boundary",
      "path": "kifrs/runtime/answer_boundary.py",
      "exists": true,
      "category": "composer",
      "supported_roles": [
        "primary_kifrs_evidence",
        "supporting_interpretation",
        "legal_boundary",
        "fact_evidence"
      ],
      "note": "Separates K-IFRS primary citations from external evidence references."
    },
    {
      "name": "1116 review pack",
      "path": "kifrs/workflows/kifrs1116/review_pack.py",
      "exists": true,
      "category": "workflow",
      "supported_roles": [
        "supporting_interpretation",
        "legal_boundary",
        "fact_evidence"
      ],
      "note": "Accepts optional external evidence panel data."
    },
    {
      "name": "1109 review pack",
      "path": "kifrs/workflows/kifrs1109/review_pack.py",
      "exists": true,
      "category": "workflow",
      "supported_roles": [
        "supporting_interpretation",
        "legal_boundary",
        "fact_evidence"
      ],
      "note": "Accepts optional external evidence panel data."
    },
    {
      "name": "1115 review pack",
      "path": "kifrs/workflows/kifrs1115/review_pack.py",
      "exists": true,
      "category": "workflow",
      "supported_roles": [
        "supporting_interpretation",
        "legal_boundary",
        "fact_evidence"
      ],
      "note": "Accepts optional external evidence panel data."
    },
    {
      "name": "statement draft schema",
      "path": "kifrs/workflows/statement_draft/schema.py",
      "exists": true,
      "category": "workflow",
      "supported_roles": [
        "fact_evidence"
      ],
      "note": "Carries evidence references for statement line candidates."
    }
  ],
  "required_roles": [
    "primary_kifrs_evidence",
    "supporting_interpretation",
    "legal_boundary",
    "fact_evidence",
    "client_private_fact"
  ],
  "runtime_supported_roles": [
    "fact_evidence",
    "legal_boundary",
    "primary_kifrs_evidence",
    "supporting_interpretation"
  ],
  "source_record_roles": {
    "document_metadata": {
      "citation_role": "supporting_interpretation",
      "authority_level": "supporting",
      "retrieval_lane": "document_metadata",
      "runtime_role": "supporting_interpretation",
      "runtime_role_supported": true
    },
    "law_locator": {
      "citation_role": "legal_boundary",
      "authority_level": "legal_boundary",
      "retrieval_lane": "law_locator",
      "runtime_role": "legal_boundary",
      "runtime_role_supported": true
    },
    "structured_fact": {
      "citation_role": "fact_evidence",
      "authority_level": "fact",
      "retrieval_lane": "structured_fact",
      "runtime_role": "fact_evidence",
      "runtime_role_supported": true
    },
    "client_private_fact": {
      "citation_role": "collection_seed",
      "authority_level": "client_private",
      "retrieval_lane": "local_private_fact",
      "runtime_role": "client_private_fact",
      "runtime_role_supported": false
    }
  },
  "gaps": [
    {
      "milestone": "MAH2",
      "surface": "runtime authority contract",
      "gap": "NIS source records are validated but not yet converted by a shared authority boundary object."
    },
    {
      "milestone": "MAH2",
      "surface": "client-private boundary",
      "gap": "Client-private source records exist only as a public-safe handoff placeholder and are not represented in runtime output yet."
    },
    {
      "milestone": "MAH3",
      "surface": "review packs",
      "gap": "Review packs have an external evidence panel, but not a five-group authority panel with client-private placeholder support."
    },
    {
      "milestone": "MAH4",
      "surface": "statement draft and analytics",
      "gap": "Structured facts need a runtime hook that keeps calculations as fact evidence rather than primary accounting authority."
    },
    {
      "milestone": "MAH5",
      "surface": "composer gate",
      "gap": "No single gate proves primary/supporting/legal/fact/private evidence render together without protected source bodies."
    }
  ],
  "next_leaf": "MAH2_runtime_evidence_contract_hardening",
  "report_path": "docs/reports/2026-07-05-mah1-runtime-evidence-boundary-audit.md"
}
```
