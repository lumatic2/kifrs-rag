# Plan: PM3 — 자동화 가능성 매핑 + 다음 자동화 대상 선정

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/practice-map.md` (`practice-map`)
> Milestone: PM3 — 자동화 가능성 매핑 + 다음 자동화 대상 선정
> Created: 2026-07-04

## Scope boundary

PM1 taxonomy(33 task)의 각 task에 자동화 가능성 판정과 근거를 붙이고, 다음 자동화 대상을
실무 가치 기준으로 1~2개 추천한다. **제약(사용자, 2026-07-04): 현업 회계사·법인 접촉 없이
로컬에서 AI + 웹검색으로 검증 가능한 범위에 집중** — 따라서 판정에 "로컬 검증 가능성" 차원을
포함하고, 실제 법인 데이터(조서·내부 문서)가 필요한 task는 후보에서 후순위로 내린다.

판정 체계 (4단계):
- **가능** — 이 레포 또는 업계 도구로 이미 실증됨
- **조건부** — 부분 실증 또는 명확한 경로 있음 (제약·실패 모드 알려짐)
- **불가** — 대면·현장·법적 책임 등 구조적 사유
- **미실험-유망 / 미실험-보류** — 실증 없음, 로컬 검증 가능성·기존 자산 재사용성으로 이분

Out of scope:
- **현업 인터뷰(PM2)** — 사용자 결정으로 보류. 지도의 "미검증(공개자료 기반)" 상태를 명시하고
  PM2는 이월.
- **선정된 대상의 실제 구현** — 다음 horizon(자동화 확장). PM3는 추천까지.
- **세무(C그룹) task의 심층 판정** — tax-agent 경계. 표면 판정만 붙이고 상세는 그쪽 레포.

## Step tree

- [ ] **Step 1 — 33개 task 전수 판정** (`docs/practice-map/taxonomy.md` 갱신 — 판정+근거 컬럼)
  판정 rubric: ① 입출력이 디지털 문서/데이터인가 ② 판단이 규칙·기준서로 환원되는가 ③ 로컬에서
  검증 가능한 데이터가 있는가(공개 기준서·본인 작성 fixture로 충분한가) ④ 대면·현장·서명 책임
  요소가 있는가. 필요 시 개별 task 웹검색으로 근거 보강. (verify: 33/33 task에 판정+근거 한 줄,
  "미실험" 잔존 0)

- [ ] **Step 2 — 유망 후보 심층 분석** (`docs/practice-map/candidates.md` 신규)
  Step 1에서 "미실험-유망" + "조건부" 중 상위 3~5개를 뽑아 각각: 필요 입력 데이터(로컬 확보
  가능성), 기존 자산 재사용(검색 인프라·1109 엔진 패턴·goldset), 검증 방법(fixture·회귀), 예상
  실패 모드. PM1이 지목한 초기 후보 B5(주석 작성)를 반드시 포함해 검증. (verify: 후보별 4개
  항목이 채워진 candidates.md)

- [ ] **Step 3 (integration) — 다음 대상 추천 + 커버리지 1차 측정 + horizon close 판정**
  다음 자동화 대상 1~2개를 근거와 함께 추천(최종 선택은 사용자 — 다음 horizon 논의 입력).
  커버리지 축 1차 측정(판정 붙은 task / 33) 기록. horizon close criteria 대조: PM1+PM3 충족,
  PM2 미검증 상태 명시 후 이월. horizon doc에 Objective 임팩트 기록.
  (verify: taxonomy.md 측정값 갱신 + horizon doc 갱신 + `python -m pytest tests/ -q` 92/92 비퇴행)

## 결정 로그

- **현업 접촉 없이 로컬 검증 범위로 한정** — 사용자 결정(2026-07-04). PM2 보류·이월, 판정
  rubric에 "로컬 검증 가능성" 차원 포함, 법인 내부 데이터 필요 task는 후보 후순위.
- **판정 4단계 체계(가능/조건부/불가/미실험-유망·보류)** — 계획 단계 기본값. 실행 중 변경 없음.
- **다음 자동화 대상의 최종 선택은 사용자 소유** — PM3는 추천+근거까지. milestone close 보고에서
  선택지를 제시하고, 다음 horizon(자동화 확장) 논의에서 확정.
- 이 외 예상되는 사용자 소유 결정 없음.

## Integration verification (milestone close)

- `docs/practice-map/taxonomy.md` — 33/33 판정+근거, 커버리지 1차 측정값
- `docs/practice-map/candidates.md` — 상위 후보 심층 분석 (각 4항목)
- `docs/horizons/practice-map.md` — close 판정 + Objective 임팩트 + PM2 이월 명시
- `python -m pytest tests/ -q` — 92/92 비퇴행 (문서 작업)
