# Changeset: DR2-S1 — 기준서 단위 갱신 경로 + amendment 이력

## Target

- ROADMAP milestone: DR2 — 단위 갱신 경로 + 개정 이력 (`kasb-drift-watch` horizon)
- Plan: `docs/plans/2026-07-12-kasb-drift-watch.md` DR2-S1

## Scope

- Files: `kifrs/drift.py` (update_standard + CLI `--update`), `kifrs/store.py` 변경 없음
  (amendment 스키마 기존 그대로 사용, standard 메타 컬럼은 drift.py 마이그레이션으로 추가)
- Reason: DR1이 실 drift 15건(수정목록 26-1)을 검출 — 감지만 하고 갱신 경로가 없으면 반쪽.
- Expected effect: `python -m kifrs.drift --update <id>` 한 커맨드로 재다운로드→재파싱→재인제스트→
  재임베딩 + amendment 문단 diff 기록 + standard 메타(KASB 파일 식별자·갱신일) 갱신.

## Contract

- Source of truth: `kifrs/drift.py`. 다운로드/파싱/인제스트/임베딩은 기존 모듈 재사용
  (download.fetch_detail_files/download_file, parse.parse_pdf, store.upsert_from_json,
  embed.build_embeddings).
- Compatibility: `standard` 테이블에 nullable 컬럼 3개 추가(kasb_file_no, kasb_file_seq,
  drift_synced_at) — ALTER TABLE ADD COLUMN, 기존 조회 경로 영향 없음. 이전 PDF는 삭제하지 않고
  `<dir>/archive/`로 이동(롤백 가능).
- Out of scope: 일괄 갱신(15건 전체 — 운영 판단), 리포트↔갱신 연결(DR2-S2), MCP 갱신 tool(무거운
  임베딩 작업이라 CLI 전용).

## Verification

- [x] Targeted tests: baseline hybrid eval — recall@10 0.747 / @20 0.910 / MRR 0.490 (`data/eval/results/retrieval_20260712_154130.json`)
- [x] CLI smoke: `--update 1024` 실 drift E2E — 다운로드(26-1)→파싱(100문단)→인제스트→임베딩 100 재색인 완주,
      기존 PDF는 `archive/` 보존
- [x] Integrated smoke: amendment 1행(1024-28A 변경, prev/new body 기록) + source 26-1 갱신 +
      kasb_file_no/file_seq/drift_synced_at 메타 기록 + `check_drift(only=1024)` 재실행 drift 해소
- [x] Failure mode: `--update 9999` → "스냅샷에서 찾지 못함" 에러 + exit 2. 갱신 후 eval 비퇴행:
      recall@10 0.7467 / @20 0.910 / MRR 0.4897 (baseline 동일)

## Result

- Status: completed (2026-07-12)
- Evidence: 위 checklist 실행 로그, `data/eval/results/retrieval_20260712_1541*.json` (로컬)
- Notes: 1024 의 26-1 개정 실체 = 문단 28A(경과규정) 1건 변경 — amendment diff 가 개정 내용을
  문단 단위로 특정함. 잔여 실 drift 14건은 운영 판단으로 순차 갱신(DR2-S2 통주 1건 포함).
