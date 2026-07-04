# RT2 — Review-Pack Evidence Panel

## Objective

RT1의 runtime evidence loader를 사용해 1116/1109/1115 review pack 산출물에 external evidence panel을
추가한다. 판단 로직은 바꾸지 않고, 산출물에 primary K-IFRS evidence와 external evidence의 구분을 표시한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-rt1-runtime-evidence-loader.md` — 왜: RT2가 사용할 loader API와 경계.
- `kifrs/runtime/evidence.py` — 왜: runtime evidence object와 query helper.
- `kifrs/workflows/kifrs1116/review_pack.py` — 왜: 첫 review pack output/markdown pattern.
- `kifrs/workflows/kifrs1109/review_pack.py` — 왜: 두 번째 review pack output/markdown pattern.
- `kifrs/workflows/kifrs1115/review_pack.py` — 왜: 수익 review pack output/markdown pattern.
- `tests/test_1116_review_pack.py`, `tests/test_1109_review_pack.py`, `tests/test_1115_review_pack.py` — 왜: 기존 review pack regression.

## 작업

1. review pack에 optional external evidence panel을 추가한다.
   - runtime bundle을 주입받거나 default loader를 사용한다.
   - 판단 로직에는 영향을 주지 않는다.
2. markdown/json output에 evidence section을 추가한다.
   - `supporting_interpretation`
   - `legal_boundary`
   - `fact_evidence`
3. tests를 추가/수정한다.
   - 기존 review pack regression 유지.
   - external evidence section이 role별로 분리되어 표시되는지 확인.
   - source body/quote가 출력되지 않는지 확인.

## Acceptance Criteria

```powershell
python -m pytest tests\test_1116_review_pack.py tests\test_1109_review_pack.py tests\test_1115_review_pack.py tests\test_runtime_evidence.py -q
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- review pack evidence panel code
- updated review pack tests
- `docs/reports/2026-07-05-rt2-review-pack-evidence-panel.md`

## 금지사항

- external evidence를 K-IFRS primary evidence처럼 렌더링하지 않는다.
- source body, quote, 법령 조문, 질의회신 본문을 markdown/json output에 넣지 않는다.
- RT2에서 statement draft는 수정하지 않는다. 이유: RT3 범위다.

