# Changeset: DR1-S1 — KASB drift 감지 코어 (`kifrs/drift.py`)

## Target

- ROADMAP milestone: DR1 — Drift 감지 코어 + MCP tool (`kasb-drift-watch` horizon)
- Plan: `docs/plans/2026-07-12-kasb-drift-watch.md` DR1-S1

## Scope

- Files: `kifrs/drift.py` (신규), `.gitignore` 확인(data/ 하위라 추가 불요 예상)
- Reason: 로컬 DB 기준서가 KASB 제·개정 공표 대비 stale한지 감지할 수단이 전무.
- Expected effect: `python -m kifrs.drift` 실행으로 KASB 현행 PDF 파일 목록 vs `standard.source` 대조
  리포트 생성 + `data/drift/snapshot.json` 스냅샷 누적(재게시 감지용).

## Contract

- Source of truth: 이 레포 `kifrs/drift.py`. fetch 로직은 `kifrs/download.py`의
  `build_session/fetch_list/fetch_detail_files` 재사용(중복 구현 금지).
- Compatibility: DB 스키마 변경 없음(읽기 전용). MCP 표면 변경 없음(DR1-S2에서).
- Out of scope: MCP tool 노출(DR1-S2), 갱신 경로·amendment 기록(DR2), 스케줄 자동화(horizon 밖).

## Verification

- [x] Targeted tests: synthetic drift 4종(filename_changed/fileref_changed/fetch_empty/not_in_db) 주입 검출 PASS
      + drifts(actionable)/uncovered(참고) 분리 + gaap `제NN장`·special id 매핑 검증 PASS
- [x] CLI smoke: `--category kifrs --only 1115` 실 KASB E2E — 대조 1건, drift 없음, 리포트 생성
- [x] Integrated smoke: 전체 3 카테고리 — KASB 105건 / DB 100건 / **matched 100 (db_unmatched 0)**,
      drift 15건 검출(전부 filename_changed, 수정목록 26-1 개정 배치 — 실 drift), uncovered 5건, snapshot 생성
- [x] Failure mode: invalid host 시 graceful fatal + exit code 2 + drift 오탐 0건, "일치" 문구 억제 확인

## Result

- Status: completed (2026-07-12)
- Evidence: `data/drift/report-20260712-153324.json` (로컬), 위 checklist 실행 로그
- Notes: **실 drift 발견** — K-IFRS 15개 기준서(1001/1101/1103/1109/1110/1116/1012/1024/1034/1036/1037/1039/1041/2101/2106)가
  KASB에서 수정목록 26-1로 갱신됨 (DB는 23-1~25-1). DR2 갱신 경로의 실전 입력이 됨 — synthetic 불필요.
