# Step 1: Parser Prototype Asset Inventory

## 읽어야 할 파일

- `docs/horizons/real-local-parser-prototype.md` — 왜: RLP1이 닫을 horizon/milestone 계약.
- `docs/plans/2026-07-05-real-local-parser-prototype.md` — 왜: RLP1~RLP5 step tree와 중단 조건.
- `kifrs/feedback/case_intake.py` — 왜: local private intake, redaction, routing, deletion attestation 자산.
- `kifrs/feedback/local_parser.py` — 왜: 기존 parser prototype input/result, adapter contract, dry-run gate.
- `docs/reports/2026-07-05-client-private-parser-runtime-close-report.md` — 왜: 직전 private parser runtime close evidence.

## 작업

기존 parser contract, adapter scaffold, deletion gate, dry-run fixture, runtime close gate를 inventory한다.
각 자산을 RLP2~RLP5에 재사용할 수 있는지와 남은 gap을 분류하고 report를 작성한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_parser_prototype_asset_inventory.py -q
python scripts\parser_prototype_asset_inventory.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-rlp1-parser-prototype-asset-inventory.md` 생성 확인
3. 성공 시 `phases/real-local-parser-prototype/index.json` step 1을 completed로 갱신

## 금지사항

- real client file, OCR text, source body, private identifier, embedding payload를 report에 넣지 않는다.
- RLP1에서 adapter를 구현하지 않는다. RLP1은 inventory와 gap 확정만 한다.
