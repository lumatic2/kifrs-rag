# RT1 — Runtime Evidence Loader

## Objective

MSI에서 만든 `source_manifest`와 `evidence_manifest`를 workflow runtime이 바로 쓸 수 있는 immutable
evidence object로 변환한다. 이 step은 review pack이나 answer composer를 수정하지 않고 공통 loader만 만든다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md` — 왜: runtime integration으로 넘겨야 하는 계약과 out-of-scope.
- `docs/ingestion/source_manifest.example.json` — 왜: loader가 source record payload를 결합해야 함.
- `docs/ingestion/evidence_manifest.example.json` — 왜: loader가 evidence trail을 runtime object로 변환해야 함.
- `kifrs/ingestion/manifest.py` — 왜: source manifest validation을 재사용해야 함.
- `kifrs/ingestion/evidence.py` — 왜: evidence manifest validation을 재사용해야 함.

## 작업

1. `kifrs/runtime/evidence.py`를 추가한다.
   - `RuntimeEvidence` dataclass
   - `EvidenceBundle` dataclass
   - `load_runtime_evidence()` helper
2. loader는 source/evidence validators를 먼저 통과시킨다.
3. evidence item을 source record payload와 결합한다.
4. role별 query helper를 제공한다.
   - `by_role(role)`
   - `supporting_interpretations`
   - `legal_boundaries`
   - `fact_evidence`
5. tests를 추가한다.
   - default fixture load
   - role grouping
   - invalid evidence path raises clear error

## Acceptance Criteria

```powershell
python -m pytest tests\test_runtime_evidence.py tests\test_ingestion_manifest.py tests\test_ingestion_evidence.py -q
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `kifrs/runtime/evidence.py`
- `kifrs/runtime/__init__.py`
- `tests/test_runtime_evidence.py`
- `docs/reports/2026-07-05-rt1-runtime-evidence-loader.md`

## 금지사항

- review pack, statement draft, answer composer는 RT1에서 수정하지 않는다. 이유: loader layer를 먼저 안정화.
- source body, copied quote, raw filing, embedding, credential을 runtime object에 추가하지 않는다.

