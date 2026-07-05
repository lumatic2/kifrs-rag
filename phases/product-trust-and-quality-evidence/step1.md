# Step 1: Trust Evidence Inventory

## 읽어야 할 파일

- `docs/horizons/product-trust-and-quality-evidence.md` — 왜: PTQ1이 닫을 horizon/milestone 계약.
- `docs/plans/2026-07-05-product-trust-and-quality-evidence.md` — 왜: PTQ1~PTQ5 step tree와 중단 조건.
- `scripts/quality_preflight.py` — 왜: fast public-safe baseline quality evidence.
- `scripts/rag_quality_final_gate.py` — 왜: heavy RAG/citation quality evidence.
- `scripts/default_retriever_guard.py` — 왜: default promotion safety boundary.
- `scripts/firm_facing_product_surface_gate.py` — 왜: 직전 horizon close evidence.

## 작업

기존 품질/RAG/default/runtime/review-pack evidence를 제품 신뢰 관점으로 inventory한다. 새 판단 로직을 만들지 말고, evidence source의 역할, 속도, public-safe 여부, protected-data dependency, 다음 milestone gap을 명시한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_product_trust_evidence_inventory.py -q
python scripts\product_trust_evidence_inventory.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-ptq1-trust-evidence-inventory.md` 생성 확인
3. 성공 시 `phases/product-trust-and-quality-evidence/index.json` step 1을 completed로 갱신

## 금지사항

- protected K-IFRS text, dogfood material, client data, source body를 report에 넣지 않는다.
- confidence/failure/promotion 구현을 PTQ1에 섞지 않는다. PTQ1은 inventory만 한다.
