# PTQ3 Failure Boundary Matrix

> Scope: PTQ3 operator actions for known product trust failure boundaries.

## One-Line Result

Known failure modes now map to operator actions, verification commands, and escalation boundaries.

## Matrix

| Category | Symptom | Operator Action | Verify | Escalation |
|---|---|---|---|---|
| retrieval_quality | Required citation is absent or outside the accepted retrieval window. | Run the RAG final gate and inspect target misses before trusting a generated answer. | `python scripts\rag_quality_final_gate.py --format text` | Do not promote the repair retriever or rely on the answer until misses are triaged. |
| citation_assembly | Workflow output has a memo or disclosure draft but missing or weak citations. | Check review-pack confidence labels and keep the affected section at caution or human_review_required. | `python scripts\review_pack_confidence_contract.py --format text` | Require accountant review of the affected memo/disclosure section. |
| client_private_fact_gap | The accounting conclusion depends on source facts that are only present in private client material. | Keep the private fact in the client_private_fact lane and verify deletion/runtime gate. | `python scripts\client_private_parser_runtime_gate.py --format text` | Do not copy private source body into public reports; request structured facts or local-only review. |
| unsupported_workflow | Review pack status is needs_human_review or the requested workflow has no supported adapter. | Use the human-review checklist and stop before final conclusion. | `python -m pytest tests\test_1116_review_pack.py tests\test_1109_review_pack.py tests\test_1115_review_pack.py -q` | Create a new workflow coverage milestone before claiming automation. |
| authority_boundary | Primary, supporting, legal, fact, and private authority groups are mixed or missing. | Run the multi-authority runtime gate and inspect role counts. | `python scripts\multi_authority_runtime_gate.py --format text` | Do not present the output as grounded until authority groups are separated. |
| default_promotion | The opt-in repair retriever appears better than default but promotion is not authorized. | Run the default retriever guard and keep runtime default unchanged. | `python scripts\default_retriever_guard.py --format text` | Require explicit authorization and a separate implementation before changing defaults. |

## Errors

- none

## Machine Result

```json
{
  "title": "PTQ3 Failure Boundary Matrix",
  "ok": true,
  "horizon": "product-trust-and-quality-evidence",
  "milestone": "PTQ3",
  "boundaries": [
    {
      "category": "retrieval_quality",
      "symptom": "Required citation is absent or outside the accepted retrieval window.",
      "operator_action": "Run the RAG final gate and inspect target misses before trusting a generated answer.",
      "verification_command": "python scripts\\rag_quality_final_gate.py --format text",
      "escalation": "Do not promote the repair retriever or rely on the answer until misses are triaged.",
      "public_safe": true
    },
    {
      "category": "citation_assembly",
      "symptom": "Workflow output has a memo or disclosure draft but missing or weak citations.",
      "operator_action": "Check review-pack confidence labels and keep the affected section at caution or human_review_required.",
      "verification_command": "python scripts\\review_pack_confidence_contract.py --format text",
      "escalation": "Require accountant review of the affected memo/disclosure section.",
      "public_safe": true
    },
    {
      "category": "client_private_fact_gap",
      "symptom": "The accounting conclusion depends on source facts that are only present in private client material.",
      "operator_action": "Keep the private fact in the client_private_fact lane and verify deletion/runtime gate.",
      "verification_command": "python scripts\\client_private_parser_runtime_gate.py --format text",
      "escalation": "Do not copy private source body into public reports; request structured facts or local-only review.",
      "public_safe": true
    },
    {
      "category": "unsupported_workflow",
      "symptom": "Review pack status is needs_human_review or the requested workflow has no supported adapter.",
      "operator_action": "Use the human-review checklist and stop before final conclusion.",
      "verification_command": "python -m pytest tests\\test_1116_review_pack.py tests\\test_1109_review_pack.py tests\\test_1115_review_pack.py -q",
      "escalation": "Create a new workflow coverage milestone before claiming automation.",
      "public_safe": true
    },
    {
      "category": "authority_boundary",
      "symptom": "Primary, supporting, legal, fact, and private authority groups are mixed or missing.",
      "operator_action": "Run the multi-authority runtime gate and inspect role counts.",
      "verification_command": "python scripts\\multi_authority_runtime_gate.py --format text",
      "escalation": "Do not present the output as grounded until authority groups are separated.",
      "public_safe": true
    },
    {
      "category": "default_promotion",
      "symptom": "The opt-in repair retriever appears better than default but promotion is not authorized.",
      "operator_action": "Run the default retriever guard and keep runtime default unchanged.",
      "verification_command": "python scripts\\default_retriever_guard.py --format text",
      "escalation": "Require explicit authorization and a separate implementation before changing defaults.",
      "public_safe": true
    }
  ],
  "errors": [],
  "report_path": "docs/reports/2026-07-05-ptq3-failure-boundary-matrix.md",
  "next_leaf": "PTQ4_promotion_decision_evidence_pack"
}
```
