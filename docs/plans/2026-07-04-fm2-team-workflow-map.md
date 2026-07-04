# Plan: FM2 — 팀별 회계사 workflow 문서화

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/firm-service-map.md` (`firm-service-map`)
> Milestone: FM2 — 팀별 회계사 workflow 문서화
> Created: 2026-07-04

## Scope boundary

FM1의 service-line map을 기준으로 팀별 실제 업무 흐름을 문서화한다. 산출물은
`docs/practice-map/team-workflows.md`이며, 기존 33개 task를 service-line과 직급/역할 흐름에
재매핑한다.

Out of scope:
- 새 엔진 구현.
- 세무 자동화 상세 설계(`tax-agent` 영역).
- 현업 인터뷰 실행(PM2).

## Step tree

- [x] **Step 1 — workflow template 확정**
  각 service-line을 자료수집 → 판단 → 계산/대사 → 문서화 → 리뷰/커뮤니케이션으로 통일해 쓴다.  
  (verify: `docs/practice-map/team-workflows.md` template section)

- [x] **Step 2 — Audit / Assurance workflow 작성**
  감사계획, 내부통제, 세부테스트, 회계이슈, 보고서/KAM 흐름을 A task와 연결한다.  
  (verify: `docs/practice-map/team-workflows.md` F-AUD section)

- [x] **Step 3 — Accounting Advisory / F-S 지원 workflow 작성**
  회계처리 판단, 결산분개, 재무제표/주석 작성, 리스/금융상품 검토메모 흐름을 B task와 연결한다.  
  (verify: `docs/practice-map/team-workflows.md` F-ACC section)

- [x] **Step 4 — Tax / Deal / Risk / Consulting workflow 요약**
  자동화 실험 경계와 보류 이유를 service-line별로 분리한다.  
  (verify: `docs/practice-map/team-workflows.md` remaining sections)

- [x] **Step 5 — 기존 taxonomy 재매핑 표 작성**
  33개 task를 service-line, 산출물, AI insertion point에 다시 연결한다.  
  (verify: `docs/practice-map/team-workflows.md` remap table)

## 결정 로그

- 현재 예상되는 사용자 소유 결정은 없음. 공개자료 기반으로 먼저 쓰고, 실제 업무 비중 검증은 PM2로
  분리한다.
- F-TAX는 지도와 workflow 요약까지만 작성하고 구현 후보는 `tax-agent` 이관 여부를 FM3에서 판단한다.

## Integration verification

- `docs/practice-map/team-workflows.md` 생성.
- 기존 `docs/practice-map/taxonomy.md`의 33개 task가 누락 없이 재매핑됨.
- `python C:\\Users\\yusun\\.codex\\skills\\harness\\scripts\\roadmap_sync.py status`가 FM2 active를 감지.
