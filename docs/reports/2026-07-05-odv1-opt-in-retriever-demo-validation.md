# ODV1 Opt-In Retriever Demo Validation

> Scope: prove the final opt-in retriever stack is demo-ready without promoting it to the default retriever.

## 한 줄 결론

`ifrs1109_classification_hybrid` is ready for opt-in demo use: 50-item recall@20 is 1.000 and required-citation absent count is 0. Default retriever promotion remains deferred.

## Retrieval Result

| Retriever | recall@20 | absent required citations | top-20 misses |
|---|---:|---:|---:|
| `hybrid` | 0.887 | 9 | n/a |
| `ifrs1109_classification_hybrid` | 1.000 | 0 | 0 |

## Demo Boundary

- Use the target retriever only as an opt-in demo/evaluation path.
- Keep the default retriever unchanged until actual accountant session evidence supports promotion.
- Treat this as retrieval evidence, not answer-quality proof or final accounting judgment.

## Operator Surface Check

- run sheet next leaf: real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change
- operator proof snapshot still exposes remaining gaps.

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "baseline_retriever": "hybrid",
  "target_retriever": "ifrs1109_classification_hybrid",
  "items": 50,
  "k": 20,
  "baseline_recall20": 0.8867,
  "target_recall20": 1.0,
  "baseline_buckets": {
    "hit@5": 45,
    "hit@10": 14,
    "hit@20": 14,
    "beyond@20": 0,
    "absent": 9
  },
  "target_buckets": {
    "hit@5": 47,
    "hit@10": 18,
    "hit@20": 17,
    "beyond@20": 0,
    "absent": 0
  },
  "target_misses": [],
  "default_promotion": "deferred",
  "demo_ready_for_opt_in": true,
  "operator_snapshot_gaps": [
    "actual accountant session evidence is still external/user-owned",
    "local parser real-adapter implementation plan is present, but actual evidence and explicit authorization are still required before real upload/OCR/parser/deletion automation",
    "external source connector metadata-only lane is closed and demo-noted, but source-body connector is still not implemented",
    "opt-in retriever promotion decision gate is present, but default retriever change remains deferred until actual accountant evidence and explicit authorization"
  ],
  "run_sheet_next_leaf": "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change",
  "report_path": "docs\\reports\\2026-07-05-odv1-opt-in-retriever-demo-validation.md",
  "next_leaf": "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change"
}
```
