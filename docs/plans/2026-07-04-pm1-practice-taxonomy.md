# Plan: PM1 — 회계사 업무 taxonomy 초안

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/practice-map.md` (`practice-map`)
> Milestone: PM1 — 회계사 업무 taxonomy 초안
> Created: 2026-07-04

## Scope boundary

공개 자료 기반으로 한국 회계사(회계법인 소속 중심)의 실무 업무를 세부 task 단위까지 분해한
taxonomy 문서를 작성한다. 각 task에 메타(빈도 추정·판단 강도·입출력 형태·현재 AI 활용 여부)를
붙이고, 이 레포의 기존 자산이 지도 어디에 있는지 표기한다. 산출물은 마크다운 문서
(`docs/practice-map/taxonomy.md`) — 이후 PM2(현업 검증)의 인터뷰 재료이자 PM3(가능성 매핑)의
뼈대가 된다.

Out of scope:
- **현업 인터뷰** — PM2 (사용자 액션 필요).
- **자동화 가능성 판정** — PM3. 이번엔 "무슨 업무가 있는가"만, "되는가"는 다음.
- **세무 업무의 자동화 실험** — 지도에 표기만 (tax-agent 경계, Objective 결정 ⑤).

## Step tree

- [ ] **Step 1 — 공개 자료 리서치 + 대분류 골격** (WebSearch/ncli: 한공회 자료, 회계법인
  서비스 소개·채용 JD, 감사 실무 가이드, 회계사 수험/실무 커뮤니티)
  대분류(감사 / 재무제표 작성·결산 지원 / 재무자문(FAS) / 세무 / 기타) 골격과 출처 목록 확정.
  (verify: `docs/practice-map/sources.md`에 출처 ≥8건 + 대분류 골격 기록)

- [ ] **Step 2 — 세부 task 분해 + 메타 부여** (`docs/practice-map/taxonomy.md`)
  대분류별 세부 task(예: 감사 → 계정별 실증절차, 조서 작성, 왕복문서 관리, 감사보고서 작성 …)
  분해. 각 task에 빈도 추정 / 판단 강도(기계적~고판단) / 입출력 형태(문서→문서, 데이터→분개 등)
  / 현재 법인 AI 활용 여부(리서치·자료정리 관찰 반영) 메타. (verify: task ≥30개, 전 task에
  4개 메타 필드)

- [ ] **Step 3 (integration) — 기존 자산 위치 표기 + 커버리지 축 0차 측정**
  1109 결정 엔진, Phase 3/4 시나리오(1116/1115/1113/1019 문서), /accounting 스킬(리서치),
  검색 인프라가 taxonomy의 어느 task에 해당하는지 표기. "실험이 닿은 task 수 / 전체 task 수"로
  축 1의 0차 측정값 기록. (verify: taxonomy.md에 자산 매핑 섹션 + 측정값 한 줄,
  `python -m pytest tests/ -q` 비퇴행 — 문서 작업이므로 92개 그대로)

## 결정 로그

- **공개 자료 우선, 인터뷰는 PM2로 분리** — 사용자 결정(2026-07-04 논의): 업무 지도 정식 트랙
  채택 시 "공개 자료 + 주변 회계사 인터뷰" 중 인터뷰는 사용자 소유 액션이라 별도 milestone.
- **taxonomy 위치: `docs/practice-map/`** — 공개 가능 산출물(업무 분류는 저작권 무관). 계획
  단계 기본값, 이견 없으면 진행.
- **세무 task 포함하되 표기만** — Objective 결정 ⑤ 반영.
- 이 외 예상되는 사용자 소유 결정 없음.

## Integration verification (milestone close)

- `docs/practice-map/taxonomy.md` — task ≥30, 메타 4필드, 자산 매핑, 커버리지 0차 측정값
- `docs/practice-map/sources.md` — 출처 ≥8건
- `python -m pytest tests/ -q` — 92개 비퇴행
