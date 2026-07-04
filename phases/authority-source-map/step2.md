# AS2 — Authority and Citation Policy

## Objective

AS1 source taxonomy를 바탕으로 source class별 authority priority와 answer citation policy를 정한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-as1-source-taxonomy.md` — 왜: source class와 missing class를 이어받는다.
- `docs/authority/source_pack_rules.md` — 왜: 현재 source pack rule을 확인한다.
- `docs/authority/sources.json` — 왜: 현재 authority_type/priority 구조를 확인한다.
- `docs/authority/source_pack.json` — 왜: allowed_use/locator/status 구조를 확인한다.
- `docs/reports/2026-07-05-rq5-quality-gate-report.md` — 왜: source expansion 중 유지해야 할 quality gate를 확인한다.

## 작업

1. source class별 authority priority를 정의한다.
2. answer composer가 evidence를 primary/supporting/legal/fact/client로 나눠 보여주는 policy를 적는다.
3. conflict handling과 "근거 부족" 선언 규칙을 적는다.
4. 현재 `docs/authority/*.json` schema에 필요한 field 후보를 정리한다.

## Acceptance Criteria

```powershell
python scripts\validate_authority_sources.py
python scripts\validate_authority_source_pack.py
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-as2-authority-citation-policy.md`

## 금지사항

- AS2에서 source registry schema를 바로 변경하지 않는다. 이유: policy를 먼저 확정하고 AS3/AS4와 함께 반영 범위를 판단한다.
- 특정 회계법인 guide를 authoritative source로 승격하지 않는다. 이유: supporting material은 primary/interpretive source보다 낮은 권위다.

