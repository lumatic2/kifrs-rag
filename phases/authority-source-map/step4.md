# AS4 — Ingestion Feasibility Matrix

## Objective

AS1~AS3를 바탕으로 source class별 fetch/parse/chunk/embed/index 가능성을 평가한다. 다음 horizon인
`multi-source-ingestion-pipeline`에서 어떤 connector interface가 필요한지 결정할 수 있게 만든다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-as1-source-taxonomy.md` — 왜: source classes와 missing registry classes.
- `docs/reports/2026-07-05-as2-authority-citation-policy.md` — 왜: citation role과 conflict policy.
- `docs/reports/2026-07-05-as3-storage-boundary.md` — 왜: storage labels and public/private boundary.
- `docs/reports/2026-07-05-non-ifrs-source-map.md` — 왜: first source expansion candidates.
- `docs/horizons/accounting-intelligence-expansion.md` — 왜: next horizon dependency.

## 작업

1. source class별 fetch/parse/chunk/embed/index feasibility를 표로 정리한다.
2. structured retrieval(DART/XBRL)과 document RAG(KASB/FSS/law/audit) 경계를 나눈다.
3. source class별 minimum connector fields를 정의한다.
4. AS5 first connector recommendation에서 선택할 후보를 3~5개로 줄인다.

## Acceptance Criteria

```powershell
python scripts\validate_authority_sources.py
python scripts\validate_authority_source_pack.py
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-as4-ingestion-feasibility.md`

## 금지사항

- AS4에서 실제 fetcher/parser/chunker를 구현하지 않는다. 이유: feasibility matrix가 먼저다.
- 외부 source body를 저장하지 않는다. 이유: AS3 storage boundary 유지.

