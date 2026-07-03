# Workflow Automation Horizon

> Created: 2026-07-03
> ROADMAP goal id: `workflow-automation`
> Status: active
> Objective: `docs/OBJECTIVE.md`

## Why now

Engine Hardening (2026-07-03) made the search/MCP layer test-covered and non-duplicated, but
that layer only *finds* paragraphs — it doesn't apply them. Phase 3/4 built five domain
decision trees as prose (`data/scenarios/*/WORKFLOW.md`: 1109, 1116, 1115, 1113, 1019), each
meant to be walked manually (by the user or by Claude via `/accounting`) for every new
transaction. That's exactly the gap the redefined Objective (2026-07-03 discussion) names:
"결정준비 초안까지 자동" requires an executable decision engine, not a document a person
re-reads every time. Until one domain's WORKFLOW.md becomes callable code, "시나리오 완료율"
(the Objective's success axis) has nothing to measure.

## Goal

Convert one domain's decision tree into a deterministic, testable engine: structured
transaction input → classification/judgment → journal entries → review memo draft, with no
manual walk-through required. Use the domain's existing scenario fixtures as a regression
suite to measure completion rate for the first time.

## Domain choice: 1109 (금융상품 분류·측정)

1109 is the pilot domain, not a new one:

- its `WORKFLOW.md` decision tree is the most deterministic of the five (SPPI test →
  business model → 2-axis classification matrix — few free-text judgment calls compared to
  1115's multi-branch revenue recognition or 1116's reassessment triggers);
- it already has 10 scenario fixtures (`data/scenarios/1109_classification/scenario_*`) with
  known transaction inputs and known expected outputs — a ready-made regression suite;
- it was Phase 3's first "실무 시나리오 자동화" target for the same reason (decision tree,
  reusable goldset).

## Milestone candidates (2-5, for horizon-run continuation)

1. **WA1 — 1109 파일럿 결정 엔진 + 완료율 측정** (first, this planning round)
   Structured transaction input schema, SPPI classifier, business model classifier,
   classification-matrix lookup, journal entry generator, review memo template filler, and a
   regression harness against the 10 existing 1109 scenarios. Produces the first completion
   rate measurement.
2. **WA2 — 완료율 결과 기반 확장 결정** (candidate, not yet scoped)
   Depending on WA1's completion rate and failure modes: either harden the 1109 engine
   further, or port the same pattern to a second domain (1116 is the next most deterministic).
   Scoped after WA1 closes — do not pre-commit which domain now.
3. **WA3 — 사람-개입 필요 케이스의 명시적 인터페이스** (candidate, signal-triggered)
   If WA1 shows a meaningful share of transactions that can't be classified deterministically
   (ambiguous business model evidence, missing inputs), design an explicit
   "needs human judgment" flag/output shape instead of forcing a guess. Only pursued if WA1's
   regression run surfaces this as a real, recurring failure mode.

## Close criteria

This horizon's first phase (WA1) closes when: the 1109 engine reproduces all 10 existing
scenario fixtures' classification + journal entries via automated test (not manual
Claude walk-through), and a completion-rate number (however imperfect) is written down.
The horizon itself stays open for WA2/WA3 — closing the horizon happens when either (a) the
engine pattern has been proven/extended to a second domain, or (b) a deliberate decision to
stop and return to content-only scenario work is made.

## Objective 임팩트 (WA1 완료 시점, 2026-07-03)

WA1이 "시나리오 완료율" 축에 첫 측정값을 만들었다: 1109 도메인 6/10(60%) — 이전에는 이 축
자체가 측정 불가능(0/0)했다. 움직인 것: 축이 "정의만 된 개념"에서 "실제 숫자가 나오는 지표"로
바뀌었고, 그 숫자를 만드는 코드(`kifrs/workflows/kifrs1109/`)가 회귀 테스트로 고정됐다.

Objective 재측정 필요 여부: 아직 아니다. 재측정을 검토할 신호는 (a) 이 60%가 다른 도메인에도
비슷하게 재현되는지(WA2), 또는 (b) "결정준비 초안까지 자동"이라는 정의 자체가 실제 사용 중
너무 좁거나 넓다고 판명되는 경우. 지금은 horizon을 계속 열어 두고 WA2/WA3로 이어간다.
