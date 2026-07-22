# Horizon 총람 (2026-07-22 — OBJECTIVE.md `Active horizon` 절에서 이관)

> Objective 는 현황을 추적하지 않는다는 내용 계약(2026-07-22 사용자 확정)에 따라, 58줄짜리
> horizon 포인터 누적분을 여기로 옮겼다. 현재 active horizon 의 정본은 `ROADMAP.md` 다.
> 아래는 원문 그대로이며 append 로 쌓인 중복 줄도 보존했다(기록 동결).

**2026-07-12 이후 규칙**: 새 horizon은 이 레포 내부 판단이 아니라 `ai-accounting-firm`의 AX 실험에서 돌아온
결함/요구(issue-back)를 입력으로 연다. 내부 hardening horizon 자체 발제는 중단. (retriever
promotion defer 등 열린 결정도 ai-accounting-firm 실소비 증거가 생겼을 때 재판단한다.)

현재 objective-gap queue는 닫혔다. `rag-quality-fresh-validation`은 `defer`로 완료됐고 default retriever 변경은 금지 상태로 유지한다. `private-parser-realism-hardening`은 `realism_contract_ready`, `external-source-body-connector-expansion`은 `connector_body_lane_ready`, `workflow-coverage-depth-expansion`은 `coverage_depth_expanded`, `demo-rehearsal-quality-loop`은 `demo_rehearsal_quality_loop_closed`로 닫혔다.

남은 horizon 순서:

1. `rag-reliability-revalidation` — 완료. K-IFRS RAG 품질 재검증과 default promotion 기준.
2. `non-ifrs-source-dataization` — 완료. KASB/FSS/법령/DART/client-private source lane을 실제 RAG 데이터화 단위로 확장.
3. `multi-authority-runtime-hardening` — 완료. K-IFRS, 법령, 질의회신, 공시, private facts를 권위별로 분리해 답변에 쓴다.
4. `client-private-parser-runtime` — 완료. 계약서/TB/회계정책서 같은 로컬 private 파일 parser와 deletion/runtime gate.
5. `firm-facing-product-surface` — 완료. 회계법인에 보여줄 demo surface와 operator UX.
6. `product-trust-and-quality-evidence` — 완료. 품질 증거, confidence label, failure boundary, retriever promotion decision.
7. `real-local-parser-prototype` — 완료. 실제 로컬 parser prototype에 가까운 synthetic/local-safe 경로.
8. `source-body-ingestion-controlled-lane` — 완료. controlled non-IFRS source-body ingestion lane.
9. `workflow-coverage-expansion` — 완료. service map 기반 업무 coverage 확장.
10. `runtime-retriever-promotion-gate` — 완료. opt-in repair retriever의 default 승격 여부를 promote/defer/rollback gate로 판단.
11. `operator-experience-hardening` — 완료. local operator UX, run doctor, manifest, recovery.

제품 약점 기준 1~5 horizon queue: `docs/plans/2026-07-05-product-weakness-horizon-candidates.md`
완료된 통합 데모 horizon: `docs/horizons/end-to-end-demo-scenario.md`
현재 objective gap queue: `docs/reports/2026-07-05-objective-gap-horizon-candidates.md`
최근 완료 RAG 품질 horizon: `docs/horizons/rag-quality-fresh-validation.md`
최근 완료 horizon: `docs/horizons/demo-rehearsal-quality-loop.md`
현재 active milestone plan: `docs/plans/2026-07-05-demo-rehearsal-quality-loop.md`

큰 실행 순서: `docs/horizons/accounting-intelligence-expansion.md`
최근 완료 horizon 상세: `docs/horizons/rag-reliability-revalidation.md`
최근 완료 horizon 상세: `docs/horizons/non-ifrs-source-dataization.md`
최근 완료 milestone plan: `docs/plans/2026-07-05-non-ifrs-source-dataization.md`
최근 완료 horizon 상세: `docs/horizons/multi-authority-runtime-hardening.md`
최근 완료 horizon 상세: `docs/horizons/client-private-parser-runtime.md`
최근 완료 horizon 상세: `docs/horizons/firm-facing-product-surface.md`
최근 완료 milestone plan: `docs/plans/2026-07-05-firm-facing-product-surface.md`
최근 완료 horizon 상세: `docs/horizons/product-trust-and-quality-evidence.md`
최근 완료 horizon 상세: `docs/horizons/real-local-parser-prototype.md`
최근 완료 horizon 상세: `docs/horizons/source-body-ingestion-controlled-lane.md`
최근 완료 horizon 상세: `docs/horizons/workflow-coverage-expansion.md`
최근 완료 horizon 상세: `docs/horizons/runtime-retriever-promotion-gate.md`
최근 완료 horizon 상세: `docs/horizons/operator-experience-hardening.md`
최근 완료 milestone plan: `docs/plans/2026-07-05-operator-experience-hardening.md`
제품 약점 후보 queue: `docs/plans/2026-07-05-product-weakness-horizon-candidates.md`
현재 active horizon 상세: `docs/horizons/end-to-end-demo-scenario.md`
현재 active milestone plan: `docs/plans/2026-07-05-end-to-end-demo-scenario.md`
최근 완료 demo packet: `docs/reports/end-to-end-demo/INDEX.md`
최근 완료 close report: `docs/reports/2026-07-05-end-to-end-demo-scenario-close-report.md`
최근 완료 horizon 상세: `docs/horizons/field-feedback-capture.md`
최근 완료 horizon 상세: `docs/horizons/field-feedback-runbook.md`
최근 완료 horizon 상세: `docs/horizons/accountant-feedback-incorporation.md`
최근 완료 horizon 상세: `docs/horizons/real-anonymized-transaction-poc.md`
최근 완료 horizon 상세: `docs/horizons/firm-facing-poc-brief.md`
최근 완료 horizon 상세: `docs/horizons/feedback-eval-backlog-integration.md`
최근 완료 horizon 상세: `docs/horizons/real-case-feedback-loop.md`
최근 완료 horizon 상세: `docs/horizons/workflow-rebuild-on-richer-knowledge.md`
이전 field-feedback 관련 상세: `docs/horizons/field-feedback-ready-demo.md`
