# Step RC1: Anonymized Case Intake Schema

## 읽어야 할 파일

- `docs/horizons/accounting-intelligence-expansion.md` - 왜: real feedback loop가 전체 순서에서 어떤 의존 단계인지 확인한다.
- `docs/horizons/workflow-rebuild-on-richer-knowledge.md` - 왜: source-aware workflow coverage 이후 입력 루프가 필요한 이유를 이어받는다.
- `CLAUDE.md` - 왜: 기준서 원문, 고객자료, private DB/embedding 금지 경계를 지킨다.
- `docs/PRD.md` - 왜: F-ACC review pack 사용자와 non-goal을 유지한다.

## 작업

익명화된 실제 업무 사례를 `CaseIntake`로 받는 schema와 validator를 추가한다. schema는 raw 계약서,
고객명, 주민/사업자등록번호, 원문 body 같은 보호자료를 저장하지 않고, routing에 필요한
구조화 사실과 reviewer 질문만 받는다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_real_case_feedback.py -q
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. raw payload/body/customer identifier 금지 negative test를 포함한다.
3. `phases/real-case-feedback-loop/index.json`의 RC1을 completed로 업데이트한다.

## 금지사항

- 실제 고객명, 계약 원문, DART raw filing, 기준서 본문을 sample fixture에 넣지 않는다.
- 세무 판단을 이 레포 schema의 자동화 대상으로 승격하지 않는다.
