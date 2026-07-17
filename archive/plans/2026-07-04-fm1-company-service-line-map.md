# Plan: FM1 — 회계법인 company/service-line map

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/firm-service-map.md` (`firm-service-map`)
> Milestone: FM1 — 회계법인 company/service-line map
> Created: 2026-07-04

## Scope boundary

기존 `practice-map` 앞단에 빠져 있던 회계법인 조직/service-line 지도를 공개자료 기반 v0로 만든다.
이번 milestone은 구현을 하지 않고, 다음 FM2 workflow 재작성의 입력 문서를 만든다.

Out of scope:
- 현업 인터뷰와 실제 법인 내부 팀명 검증.
- 팀별 상세 workflow 분해(FM2).
- AI 후보 재판정(FM3).

## Step tree

- [x] **Step 1 — 기존 문서 gap 확인**  
  `sources.md`, `taxonomy.md`, `candidates.md`를 읽고 별도 company-map 부재를 확인한다.  
  (verify: `docs/practice-map/company-map.md` "왜 다시 만들었나")

- [x] **Step 2 — 공개 service-line 소스 재확인**  
  Big4/로컬 공개 서비스 구조를 기준으로 service-line 축을 정리한다.  
  (verify: `docs/practice-map/company-map.md` "소스")

- [x] **Step 3 — company-map v0 작성**  
  팀별 고객·산출물·AI insertion point·기존 자산 위치를 표로 작성한다.  
  (verify: `docs/practice-map/company-map.md`)

- [x] **Step 4 — cascade/ROADMAP 반영**  
  새 horizon과 다음 FM2 milestone을 ROADMAP에 연결한다.  
  (verify: `docs/horizons/firm-service-map.md`; `ROADMAP.md`)

## 결정 로그

- 기존 `practice-map`은 폐기하지 않고, `company-map.md` → `taxonomy.md` → `candidates.md` 순서로
  읽도록 재해석한다.
- 세무 service-line은 지도에 포함하되 자동화 실험은 계속 sibling `tax-agent` 경계로 둔다.
- FM1은 공개자료 기반 v0로 닫고, 실제 업무 비중은 PM2/FM2 후속 검증 대상으로 남긴다.

## Integration verification

- `docs/practice-map/company-map.md` 존재.
- `docs/horizons/firm-service-map.md` 존재.
- ROADMAP에 FM2 active marker와 FM1 completed evidence가 존재.
- 문서 작업이므로 pytest는 전체 재실행 대신 `roadmap_sync.py status`와 line budget으로 검증한다.
