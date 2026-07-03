# RAG 엔진 ↔ 에이전트 통합 Horizon

> Created: 2026-07-03
> ROADMAP goal id: `rag-agent-integration`
> Status: active
> Objective: `docs/OBJECTIVE.md`

## Why now

WA1(`workflow-automation` horizon) 완료율 리포트(`docs/reports/2026-07-03-wa1-completion-rate.md`)가
드러낸 갭: `kifrs/workflows/kifrs1109/`의 결정 엔진(`sppi.py`, `business_model.py`, `classify.py`,
`initial_entry.py`, `review_memo.py`)이 사용하는 조항 인용(`[1109-4.1.2(b)]` 등)이 전부 코드에
하드코딩된 문자열이다. 100 기준서 검색 인프라(Phase 2, `kifrs.store`/`kifrs.embed`)가 이미 서 있는데
결정 엔진과 연결돼 있지 않다 — 인용이 실제 그 문단을 가리키는지 아무것도 검증하지 않는다.

`docs/OBJECTIVE.md`의 북극성은 "K-IFRS **기반**" 결정 엔진을 전제로 한다. 인용이 grounding 안 되면
그 전제 자체가 약해진다 — recall/MRR을 더 올리는 것(RAG 최적화 후보)보다 이 갭이 Objective에 더
직결된다고 판단해 이 horizon을 먼저 연다(2026-07-03 논의, 사용자 결정).

## Goal

`kifrs/workflows/kifrs1109/`의 결정 엔진이 **런타임에** 인용 근거를 검증하도록 만든다:
- 엔진은 `kifrs.store`/`kifrs.embed`를 **직접 import**해서 호출한다(MCP stdio 프로토콜 경유 아님).
  MCP는 프로세스 경계를 넘는 외부 클라이언트(Claude Code 세션의 `/accounting` 스킬 등)를 위한
  레이어이고, 엔진은 같은 레포·같은 프로세스 안의 코드이므로 그 레이어가 필요 없다(2026-07-03 논의).
- 검증 근거(인용된 문단)와 하드코딩 인용이 불일치하거나 문단을 찾지 못하면 `NeedsHumanReview`로
  에스컬레이션한다 — 기존 WA1 패턴(scenario_05~10의 `special_case` 예외)과 동일한 철학.

## 핵심 결정 (2026-07-03 논의로 확정)

| 결정 | 선택 | 이유 |
|---|---|---|
| grounding 시점 | 런타임 검색 통합 (빌드/테스트 시점 검증 아님) | 사용자 결정 |
| 호출 경로 | `kifrs.store`/`kifrs.embed` 직접 import (MCP 프로토콜 아님) | 엔진은 프로세스 내부 코드 — MCP는 외부 세션용 레이어. 한계 #6(MCP stdio fragility) 우회 |
| 불일치 처리 | `NeedsHumanReview` 에스컬레이션 (fallback 아님) | 완료율 지표의 정직성 유지 — 검증 안 된 인용을 자동 산출로 세지 않음 |

## Milestone candidates (2~5, horizon-run continuation용)

1. **RGA1 — 런타임 grounding 레이어 구축** (first, this planning round)
   인용 추출 → `kifrs.store` 직접 조회로 존재 검증 → 근거 문단과 reason 텍스트 간 의미적 일치 확인
   → 불일치 시 `NeedsHumanReview`. 기존 10개 1109 시나리오 회귀 재실행 + 완료율 재측정.
2. **RGA2 — grounding 신뢰성/성능 굳히기** (candidate, RGA1 결과에 따라 scope)
   DB 변경에 따른 결정론성 문제(같은 입력이 시간 지나 다른 grounding 결과) 대응 전략, 검색 지연
   영향 측정, 실패 모드 테스트 확대. RGA1의 완료율/실패 패턴을 보고 scope 확정.
3. **RGA3 — 신규 도메인 grounding-first 설계 표준화** (candidate, WA2/WA3와 겹칠 수 있음)
   다음 도메인(1116 등) 이식 시 처음부터 grounding 내장 패턴을 표준 템플릿으로 반영할지 결정.
   `workflow-automation` horizon의 WA2/WA3와 통합 검토.

## Close criteria

RGA1이 닫히고, 10개 1109 시나리오의 인용이 전부 runtime grounding으로 검증되거나 명시적으로
`NeedsHumanReview`로 넘어가면(검증 안 된 하드코딩 인용이 남지 않으면), 완료율이 재측정되면
horizon 첫 phase가 닫힌다. Horizon 자체는 RGA2/RGA3 여부에 따라 계속 열어두거나, WA2/WA3와
합쳐 `workflow-automation` horizon으로 되돌아갈지 판단한다.

## 관련 horizon

`workflow-automation`(`docs/horizons/workflow-automation.md`)은 **paused** 상태로 남는다 — 닫는
기준(WA2/WA3 완료 또는 명시적 중단 결정)에 도달하지 않았다. RGA1 결과에 따라 WA2/WA3를 이
horizon과 합쳐 진행할 수 있다.
