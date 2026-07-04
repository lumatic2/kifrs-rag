# Step 4: readme-setup-guide

Status: pending

## 읽어야 할 파일

- `docs/horizons/product-packaging-poc.md` — 왜: packaging PoC boundary와 목표.
- `docs/reports/demo-poc/MANIFEST.md` — 왜: sample bundle entrypoint와 재생성 명령.
- `README.md` — 왜: 기존 프로젝트 소개와 설치 안내가 있다.
- `scripts/demo_poc.py` — 왜: README에 적을 demo command.

## 작업

README 또는 별도 setup guide에 product packaging PoC 실행법을 추가한다. protected K-IFRS assets는 포함되지
않고 사용자가 직접 인덱싱해야 한다는 경계를 명시한다.

## Acceptance Criteria

```powershell
python -m pytest tests/test_demo_poc.py
git diff --check
```

## 금지사항

- 실제 배포/릴리즈를 하지 않는다.
- 기준서 원문, DB, embedding, dogfood 자료 위치나 내용을 노출하지 않는다.
