# Step TK1: Readiness Manifest

## 읽어야 할 파일

- `docs/OBJECTIVE.md` - 왜: 로컬 도구킷 형태와 PoC 성공 기준을 확인한다.
- `ROADMAP.md` - 왜: 직전 feedback/eval queue까지 닫힌 상태를 이어받는다.
- `CLAUDE.md` - 왜: protected source data boundary를 readiness manifest에 반영한다.
- `docs/reports/demo-poc/MANIFEST.md` - 왜: demo bundle 경계와 재현 명령을 연결한다.

## 작업

도구킷 readiness manifest와 README를 만든다. manifest는 공개 산출물, 재생성 command, protected-data
boundary를 구조화한다.

## Acceptance Criteria

```powershell
Test-Path docs\toolkit\readiness_manifest.json
Test-Path docs\toolkit\README.md
```

## 검증 절차

1. AC 커맨드를 실행한다.
2. manifest가 protected assets를 required artifact로 요구하지 않는지 확인한다.
3. TK1을 completed로 업데이트한다.

## 금지사항

- 기준서 원문, DB, 임베딩, dogfood 자료를 toolkit artifact로 요구하지 않는다.
