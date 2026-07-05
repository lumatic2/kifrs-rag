# Default Retriever Guard

> Scope: code-level invariant that prevents accidental default promotion of the opt-in repair retriever.

## One-Line Result

The runtime default remains `hybrid`; the repair retriever is still opt-in only.

## Runtime Boundary

- MCP search default mode: `hybrid`
- Expected default mode: `hybrid`
- MCP search modes: `lexical, semantic, hybrid, hierarchical, reranked`
- Opt-in target retriever: `ifrs1109_classification_hybrid`
- Target available in eval retrievers: True
- Target exposed in MCP modes: False
- Promotion decision: defer
- Promote to default: False

## Boundary

- This guard does not change runtime defaults.
- The target repair stack remains an opt-in evaluation/demo path.
- A future default change requires stronger internal evaluation evidence, explicit authorization, and a separate implementation.

## Machine Result

```json
{
  "ok": true,
  "errors": [],
  "title": "Default Retriever Guard",
  "default_mode": "hybrid",
  "expected_default_mode": "hybrid",
  "mcp_search_modes": [
    "lexical",
    "semantic",
    "hybrid",
    "hierarchical",
    "reranked"
  ],
  "target_retriever": "ifrs1109_classification_hybrid",
  "target_retriever_opt_in_available": true,
  "target_retriever_exposed_in_mcp": false,
  "promotion_report": "docs/reports/2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md",
  "promotion_decision": "defer",
  "promote_to_default": false,
  "report_path": "docs/reports/2026-07-05-default-retriever-guard.md",
  "next_leaf": "RAG reliability revalidation RR2/RR3/RR5, then explicit authorization before default retriever change"
}
```
