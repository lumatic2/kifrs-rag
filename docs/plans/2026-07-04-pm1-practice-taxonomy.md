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

- [x] **Step 1 — 공개 자료 리서치 + 대분류 골격** ✅ 2026-07-04
  출처 20건(법인 구조·신입 실무·로컬 vs Big4·법인 AI 도입 현황·내부회계·실사/평가 + 사용자 1차
  관찰) + 5대분류(A 감사·인증 / B 결산·F/S 지원 / C 세무(tax-agent 경계) / D 재무자문 / E 기타
  인증·컨설팅). (verify: `docs/practice-map/sources.md` — 20건 ≥8 ✓)

- [x] **Step 2 — 세부 task 분해 + 메타 부여** ✅ 2026-07-04
  33개 task, 전 task에 빈도/판단강도/입출력/현AI활용 4필드. 핵심 관찰: 법인 AI는 A8(리서치)·
  A6(문서 대량처리)에 집중, 판단 본질 task(B3·B5·A10)는 공백 — Objective 차별점과 일치.
  (verify: `docs/practice-map/taxonomy.md` — 33 ≥30 ✓)

- [x] **Step 3 (integration) — 기존 자산 위치 표기 + 커버리지 축 0차 측정** ✅ 2026-07-04
  /accounting→A8(가능, dogfood 86%), 1109 엔진→B3(조건부, 6/10), Phase3/4 문서→B3 확장 후보.
  **커버리지 0차 = 2/33 (6%)**. (verify: taxonomy.md 자산 매핑 섹션 ✓ + `pytest tests/ -q`
  92/92 ✓)

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
