# Step 3: Deletion Automation Simulation

## 읽어야 할 파일

- `phases/real-local-parser-prototype/step2.md` — 왜: adapter output이 deletion gate와 연결되는 방식.
- `kifrs/feedback/case_intake.py` — 왜: deletion attestation 계약.
- `kifrs/feedback/local_parser.py` — 왜: parser dry-run result와 retention boundary.

## 작업

parser prototype output이 deletion/retention attestation 없이 close되지 않도록 deletion automation simulation gate를 만든다.
실제 파일 삭제 자동화가 아니라 public-safe 상태 전이 simulation으로 구현한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_deletion_automation_simulation.py -q
python scripts\deletion_automation_simulation.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. `docs/reports/2026-07-05-rlp3-deletion-automation-simulation.md` 생성 확인
3. 성공 시 `phases/real-local-parser-prototype/index.json` step 3을 completed로 갱신

## 금지사항

- 실제 파일 삭제 루틴을 public repo 기본 동작으로 넣지 않는다.
- 삭제 attestation 없이 close되는 happy path를 만들지 않는다.
