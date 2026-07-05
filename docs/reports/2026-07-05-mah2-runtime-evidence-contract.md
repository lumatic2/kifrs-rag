# MAH2 Runtime Evidence Contract

> Scope: MAH2 contract hardening for separated runtime authority evidence.

## Result

- ok: True
- horizon: `multi-authority-runtime-hardening`
- milestone: `MAH2`
- next leaf: `MAH3_review_pack_authority_panel`

## Authority Roles

| Role | Count | Meaning |
|---|---:|---|
| `primary_kifrs_evidence` | 2 | K-IFRS paragraph citation; accounting conclusion anchor. |
| `supporting_interpretation` | 1 | KASB/FSS-style metadata; interpretation aid only. |
| `legal_boundary` | 1 | Law/regulation locator; legal boundary only. |
| `fact_evidence` | 1 | DART/OpenDART-style structured fact; calculation input only. |
| `client_private_fact` | 1 | Local-only client placeholder; no private material stored. |

## Contract Effect

- Primary K-IFRS evidence is provided only through explicit citations.
- Source records convert into non-primary roles only.
- Client-private records are represented as local-only placeholders.
- Runtime references omit source record bodies and protected payload fields.

## Machine Result

```json
{
  "title": "MAH2 Runtime Evidence Contract",
  "ok": true,
  "horizon": "multi-authority-runtime-hardening",
  "milestone": "MAH2",
  "authority_roles": [
    "primary_kifrs_evidence",
    "supporting_interpretation",
    "legal_boundary",
    "fact_evidence",
    "client_private_fact"
  ],
  "role_counts": {
    "primary_kifrs_evidence": 2,
    "supporting_interpretation": 1,
    "legal_boundary": 1,
    "fact_evidence": 1,
    "client_private_fact": 1
  },
  "primary_fixture_citations": [
    "[1115-B39~B43]",
    "[1116-53]"
  ],
  "public_safe": true,
  "errors": [],
  "next_leaf": "MAH3_review_pack_authority_panel",
  "report_path": "docs/reports/2026-07-05-mah2-runtime-evidence-contract.md"
}
```
