# AS1 — Source Taxonomy

## Objective

K-IFRS 외 회계 업무 정보원을 source class로 나누고, 각 class가 RAG에서 어떤 역할을 해야 하는지
정의한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-non-ifrs-source-map.md` — 왜: 이미 조사한 비IFRS source 후보와 reference를 이어받는다.
- `docs/reports/2026-07-05-rq5-quality-gate-report.md` — 왜: source 확장 전 유지해야 할 RAG gate를 확인한다.
- `docs/horizons/accounting-intelligence-expansion.md` — 왜: 전체 sequence에서 source map의 위치를 확인한다.
- `docs/authority/sources.json` — 왜: 현재 authority registry의 schema와 existing source를 확인한다.
- `docs/authority/source_pack.json` — 왜: public-safe source pack 구조를 확인한다.

## 작업

1. source classes를 primary / interpretive / audit / law / filing-data / client-private / supporting으로 정리한다.
2. 각 class별 RAG 역할, 권위 수준, citation 용도, storage boundary를 적는다.
3. 현재 `docs/authority/*.json` 구조와 어떤 gap이 있는지 적는다.
4. AS2에서 authority/citation policy로 넘길 쟁점을 정리한다.

## Acceptance Criteria

```powershell
python scripts\validate_authority_sources.py
python scripts\validate_authority_source_pack.py
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-as1-source-taxonomy.md`

## 금지사항

- 외부 원문을 대량 복사하지 않는다. 이유: 저작권/공개 repo 경계.
- 아직 source connector를 구현하지 않는다. 이유: AS1은 taxonomy step이고 connector는 AS5 이후다.

