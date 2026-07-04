# MSI5 — Ingestion Gate and Close Report

## Objective

`multi-source-ingestion-pipeline` horizon을 닫는다. MSI1~MSI4에서 만든 connector contract, source manifest,
structured fact fixture, evidence manifest가 public-safe gate를 통과하는지 묶어서 검증하고 다음 runtime
horizon으로 넘길 입력을 정리한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-msi1-connector-contract.md` — 왜: close report의 contract 기준.
- `docs/reports/2026-07-05-msi2-metadata-catalog-prototype.md` — 왜: document metadata prototype 결과.
- `docs/reports/2026-07-05-msi3-structured-fact-fixture.md` — 왜: structured fact prototype 결과.
- `docs/reports/2026-07-05-msi4-provenance-citation-manifest.md` — 왜: evidence manifest 결과.
- `docs/ingestion/source_manifest.example.json` — 왜: close gate 대상.
- `docs/ingestion/evidence_manifest.example.json` — 왜: close gate 대상.
- `scripts/quality_preflight.py` — 왜: public-safe gate와 기존 quality checks.
- `ROADMAP.md` — 왜: horizon close 상태 반영.

## 작업

1. ingestion close gate를 실행한다.
   - authority registry
   - authority source pack
   - source manifest
   - evidence manifest
   - focused tests
   - quality preflight
   - git diff check
2. close report를 작성한다.
   - 구현된 capability
   - 아직 out-of-scope인 것
   - 다음 runtime horizon 제안
3. `ROADMAP.md`의 current horizon을 closed로 옮기고 다음 후보를 제안한다.
   - 단 새 horizon을 active로 만들지는 않는다. 다음 방향은 MSI5 close report에서 제안만 한다.

## Acceptance Criteria

```powershell
python scripts\validate_authority_sources.py
python scripts\validate_authority_source_pack.py
python scripts\validate_ingestion_manifest.py docs\ingestion\source_manifest.example.json
python scripts\validate_ingestion_evidence.py docs\ingestion\evidence_manifest.example.json
python -m pytest tests\test_ingestion_manifest.py tests\test_ingestion_evidence.py tests\test_authority.py tests\test_authority_source_pack.py -q
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-msi5-ingestion-gate-close-report.md`
- `ROADMAP.md`
- `phases/multi-source-ingestion-pipeline/index.json`

## 금지사항

- MSI5에서 외부 API를 호출하지 않는다.
- protected body, raw filing, embedding, PDF, DB dump를 새로 추가하지 않는다.
- 다음 horizon을 추정으로 active 처리하지 않는다. close report에서 후보와 이유를 제안한다.

