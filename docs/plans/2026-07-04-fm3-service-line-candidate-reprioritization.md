# FM3 plan — service-line 기반 AI 후보 재판정

> Date: 2026-07-04
> Horizon: `firm-service-map`
> Milestone: FM3
> Objective: `docs/OBJECTIVE.md`
> Horizon plan: `docs/horizons/firm-service-map.md`

## Scope

FM3는 기존 PM3 후보를 폐기하지 않고, FM1/FM2에서 만든 회계법인 service-line 지도 위에 다시
배치한다. 이번 산출물은 "다음에 무엇을 구현할지"를 바로 확정하는 문서가 아니라, 구현 후보를
법인 팀·업무 산출물·검증 가능성 기준으로 재채점하는 decision input이다.

## Step tree

- [x] 기존 입력 확인: `taxonomy.md`, `candidates.md`, `company-map.md`, `team-workflows.md`를 읽고 기존 PM3 후보와 FM2 결론을 대조한다. (verify: 후보 B3/B5/A5/E2/D3가 모두 재판정 표에 존재)
- [x] service-line scorecard 작성: 후보별 주 팀, 산출물, 현재 자산, 로컬 검증, PoC 설명력, 경계 리스크를 한 표에 둔다. (verify: `docs/practice-map/service-line-candidates.md`)
- [x] 다음 구현 후보 shortlist 도출: F-ACC 중심 후보와 보류/이관 후보를 분리한다. (verify: 문서에 추천 순서와 보류 이유 존재)
- [x] ROADMAP/핸드오프 동기화: FM3 완료 evidence를 ROADMAP과 `CLAUDE.local.md`에 반영한다. (verify: `git diff --check`)

## Decision log

- 결정 필요 없음. FM3는 후보 재판정 단계이며, 실제 다음 구현 horizon 선택은 FM4에서 사용자 결정으로 남긴다.
- 기본 추천은 F-ACC(Accounting Advisory / F-S support) wedge를 유지한다. 이유는 기존 1109/1116 엔진과 1116 주석 초안이 검토메모·분개·주석 산출물 흐름에 이미 붙어 있기 때문이다.

## Acceptance criteria

```powershell
git diff --check
python C:\Users\yusun\.codex\skills\harness\scripts\roadmap_sync.py status
```

## Output

- `docs/practice-map/service-line-candidates.md`
- `ROADMAP.md`
- `CLAUDE.local.md`
