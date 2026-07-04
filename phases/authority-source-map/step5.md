# AS5 — First Connector Recommendation

## Objective

AS1~AS4를 바탕으로 다음 horizon인 `multi-source-ingestion-pipeline`에서 먼저 구현할 connector 후보
1~3개를 정한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-as1-source-taxonomy.md` — 왜: source class gap.
- `docs/reports/2026-07-05-as2-authority-citation-policy.md` — 왜: citation role and conflict policy.
- `docs/reports/2026-07-05-as3-storage-boundary.md` — 왜: storage policy.
- `docs/reports/2026-07-05-as4-ingestion-feasibility.md` — 왜: connector candidate and lane matrix.
- `docs/horizons/accounting-intelligence-expansion.md` — 왜: 다음 horizon dependency.

## 작업

1. first connector candidates를 1~3개로 확정한다.
2. 각 connector의 최소 scope와 제외 범위를 적는다.
3. 다음 horizon `multi-source-ingestion-pipeline`의 첫 step 후보를 적는다.
4. `authority-source-map` horizon close 여부를 판단한다.

## Acceptance Criteria

```powershell
python scripts\validate_authority_sources.py
python scripts\validate_authority_source_pack.py
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-as5-first-connector-recommendation.md`

## 금지사항

- AS5에서 connector를 구현하지 않는다. 이유: 다음 horizon에서 pipeline contract부터 설계해야 한다.
- 첫 connector 후보를 너무 많이 고르지 않는다. 이유: ingestion pipeline horizon의 scope가 폭발한다.

