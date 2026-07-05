# Step 1: Source Class Selection And Authorization Boundary

## 읽어야 할 파일

- `docs/horizons/source-body-ingestion-controlled-lane.md` — 왜: SBI1이 닫을 horizon/milestone 계약.
- `docs/plans/2026-07-05-source-body-ingestion-controlled-lane.md` — 왜: SBI1~SBI5 step tree와 중단 조건.
- `docs/horizons/non-ifrs-source-dataization.md` — 왜: 기존 non-IFRS source lane 조사와 storage boundary를 이어받는다.
- `docs/reports/2026-07-05-product-weakness-horizon-candidates.md` — 왜: 이 horizon이 제품 약점 queue의 2번임을 확인한다.

## 작업

후보 source class를 비교하고, 하나의 controlled lane을 선택한다. authorization status, allowed fields,
forbidden fields, fallback plan을 report로 고정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_source_class_selection.py -q
python scripts\source_class_selection.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-sbi1-source-class-selection.md` 생성 확인
3. 성공 시 `phases/source-body-ingestion-controlled-lane/index.json` step 1을 completed로 갱신

## 금지사항

- authorization 없는 protected body text를 가져오거나 저장하지 않는다.
- source selection 단계에서 parser/chunker 구현을 섞지 않는다.
