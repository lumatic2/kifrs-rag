# Step 3: sample-input-output-bundle

Status: pending

## 읽어야 할 파일

- `phases/product-packaging-poc/step2.md` — 왜: demo command와 생성된 markdown 산출물이 있다.
- `docs/reports/demo-poc/index.md` — 왜: 현재 demo output bundle의 entrypoint다.
- `scripts/demo_poc.py` — 왜: sample bundle 재생성 command다.
- `tests/test_demo_poc.py` — 왜: output bundle 검증 기대값이 있다.

## 작업

PK2에서 생성한 demo output을 sample input/output bundle로 정리한다. README 또는 manifest를 추가해
어떤 파일이 어떤 demo 단계에 쓰이는지 설명하고, 재생성 command를 명시한다.

## Acceptance Criteria

```powershell
python scripts/demo_poc.py --scenario revenue-financing --out docs/reports/demo-poc
python -m pytest tests/test_demo_poc.py
git diff --check
```

## 금지사항

- 기준서 원문, DB, embedding, dogfood 자료를 bundle에 포함하지 않는다.
