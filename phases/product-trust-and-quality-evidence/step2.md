# Step 2: Review Pack Confidence Contract

## 읽어야 할 파일

- `docs/horizons/product-trust-and-quality-evidence.md` — 왜: PTQ2 acceptance와 human-review boundary.
- `docs/plans/2026-07-05-product-trust-and-quality-evidence.md` — 왜: PTQ2 leaf와 이후 PTQ3~PTQ5 연결.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: confidence label을 붙일 review-pack object contract.
- `tests/test_1116_review_pack.py` — 왜: 기존 automated/needs-human-review 사례와 public-safe boundary.
- `scripts/product_trust_evidence_inventory.py` — 왜: PTQ1에서 분류한 trust evidence source를 이어받음.

## 작업

기존 review pack에 새 판단 로직을 추가하지 않고, section별 confidence label adapter를 만든다. label은 `ready`, `caution`, `human_review_required`만 허용한다. 자동 산출 가능한 섹션도 최종 회계 판단으로 표현하지 말고 decision-support confidence로만 표시한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_review_pack_confidence_contract.py -q
python scripts\review_pack_confidence_contract.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-ptq2-review-pack-confidence-contract.md` 생성 확인
3. 성공 시 `phases/product-trust-and-quality-evidence/index.json` step 2를 completed로 갱신

## 금지사항

- 최종 회계 판단, 감사의견, 서명 책임을 자동화한다고 쓰지 않는다.
- protected source body, client identifier, raw private file content를 confidence evidence로 쓰지 않는다.
