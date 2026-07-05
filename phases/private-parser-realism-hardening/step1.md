# Step 1: Authorization-Safe Adapter Proof Plan

## 읽어야 할 파일

- `docs/horizons/private-parser-realism-hardening.md` - 왜: PPR1 acceptance와 horizon boundary를 확인한다.
- `docs/plans/2026-07-05-private-parser-realism-hardening.md` - 왜: PPR milestone tree와 decision log를 따른다.
- `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` - 왜: 이전 real-adapter plan evidence다.
- `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` - 왜: fixture-heavy parser proof의 현재 close evidence다.
- `docs/reports/2026-07-05-rag-quality-fresh-validation-close-report.md` - 왜: 직전 horizon handoff evidence다.

## 작업

`scripts/private_parser_authorization_safe_adapter_proof.py`를 만들어 실제 protected payload handling 전에 필요한 authorization, local-only, deletion, leak-check, public-report boundary를 고정한다.

## Acceptance Criteria

```powershell
python -m pytest tests\test_private_parser_authorization_safe_adapter_proof.py -q
python scripts\private_parser_authorization_safe_adapter_proof.py --format text --write
```

## 검증 절차

1. AC 커맨드 실행
2. 보고서가 real protected input을 처리했다고 주장하지 않는지 확인
3. `phases/private-parser-realism-hardening/index.json` step 업데이트

## 금지사항

- 사용자 explicit authorization 없이 실제 private file을 읽거나 처리하지 마라.
- raw private payload, 기준서 원문, DB dump, embeddings, dogfood를 public report에 출력하지 마라.
