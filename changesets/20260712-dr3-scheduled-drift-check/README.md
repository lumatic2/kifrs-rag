# Changeset: DR3-S1 — PENDING 상태 산출 + 주간 스케줄 등록

## Target

- ROADMAP milestone: DR3 — 주간 감지 + 세션 자동 경고 (`drift-watch-automation` horizon)
- Plan: `docs/plans/2026-07-12-drift-watch-automation.md` DR3-S1

## Scope

- Files: `kifrs/drift.py` (PENDING.json 산출), `scripts/register_drift_task.ps1` (스케줄 등록 스크립트),
  Windows 작업 스케줄러 task `kifrs-drift-weekly` (레포 밖 시스템 상태)
- Reason: 감지 트리거가 사람의 질문뿐 — 주기 실행 + 상태 파일이 있어야 세션 자동 경고(DR3-S2)가 가능.
- Expected effect: 매주 월 09:00(놓치면 다음 기회에) 전체 감지 → `data/drift/PENDING.json` 갱신 +
  `data/drift/cron.log` 누적.

## Contract

- Source of truth: `kifrs/drift.py` + `scripts/register_drift_task.ps1` (task 는 이 스크립트로 재등록
  가능 — 시스템 상태의 재현 경로를 레포에 보존).
- Compatibility: PENDING.json 은 전체 감지(only 없음)에서만 갱신 — 부분 감지는 상태를 덮지 않음.
  기존 리포트/스냅샷 동작 불변.
- Out of scope: MCP 경고 표면(DR3-S2), 자동 갱신(사용자 결정으로 제외).

## Verification

- [x] Targeted tests: 전체 감지 후 PENDING.json 생성(checked_at + drifts 0) + `--only 1115` 실행이
      PENDING checked_at 을 안 덮음 확인
- [x] CLI smoke: `Register-ScheduledTask` 등록 → `schtasks /query` — Weekly MON 09:00, Next Run 2026-07-13
- [x] Integrated smoke: `Start-ScheduledTask` 1회 — LastTaskResult 0, cron.log 기록, 리포트+PENDING 생성
- [x] Failure mode: `Settings.StartWhenAvailable == True` (놓친 실행은 다음 기회에)

## Result

- Status: completed (2026-07-12)
- Evidence: `data/drift/cron.log` (로컬), schtasks 등록 확인 로그, 위 checklist
- Notes: task 는 `scripts/register_drift_task.ps1` 로 재등록 가능 (시스템 상태의 재현 경로).
