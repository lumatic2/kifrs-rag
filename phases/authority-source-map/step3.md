# AS3 — Copyright and Storage Boundary

## Objective

AS1 taxonomy와 AS2 citation policy를 바탕으로 source class별 storage boundary를 확정한다. 무엇을 public
repo에 둘 수 있고, 무엇을 local/private namespace에만 둬야 하는지 정한다.

## 읽어야 할 파일

- `docs/reports/2026-07-05-as1-source-taxonomy.md` — 왜: source class별 storage boundary 초안을 이어받는다.
- `docs/reports/2026-07-05-as2-authority-citation-policy.md` — 왜: citation role과 insufficient evidence policy를 이어받는다.
- `docs/authority/source_pack_rules.md` — 왜: 현재 forbidden body fields와 public repo 규칙을 확인한다.
- `ROADMAP.md` — 왜: 저작권/보안 작업 원칙을 확인한다.
- `.gitignore` — 왜: protected source body, DB, embedding, dogfood boundary를 확인한다.

## 작업

1. source class별 storage policy를 `public_metadata`, `local_private_body`, `structured_public_metadata`, `no_store` 등으로 나눈다.
2. public repo에 허용되는 필드와 금지되는 필드를 정리한다.
3. private/local namespace에 들어갈 자료와 공개 fixture로 대체할 자료를 구분한다.
4. AS4 ingestion feasibility에서 필요한 storage prerequisite를 정리한다.

## Acceptance Criteria

```powershell
python scripts\validate_authority_sources.py
python scripts\validate_authority_source_pack.py
python scripts\quality_preflight.py --format text
git diff --check
```

## Deliverable

- `docs/reports/2026-07-05-as3-storage-boundary.md`

## 금지사항

- 외부 원문, 질의회신, 법령 조문, 회계법인 guide 본문을 복사하지 않는다. 이유: AS3는 storage policy step이다.
- `.gitignore` 보호 범위를 느슨하게 하지 않는다. 이유: 기준서/DB/임베딩/dogfood 비공개 원칙.

