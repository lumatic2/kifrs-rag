# kifrs-rag

K-IFRS standards retrieval and MCP server prototype for evidence-grounded accounting analysis.

이 레포는 K-IFRS 기준서 원문을 직접 배포하는 레포가 아닙니다. 공개되는 범위는 RAG/MCP 서버 코드, 검색 파이프라인, 평가 하네스, 운영 문서입니다. 기준서 PDF, 파싱 텍스트, SQLite DB, 임베딩, 기출 dogfood 자료는 저작권과 사용 범위 때문에 git에서 제외됩니다.

## What It Shows

| Area | What is included |
|---|---|
| Standards retrieval | lexical, semantic, hybrid, reranked, and hierarchical retrieval experiments |
| MCP server | FastMCP tools exposing a single `search(query, mode=...)` tool covering all five retrieval modes (lexical/semantic/hybrid/hierarchical/reranked) plus standard listing, paragraph lookup, and context retrieval |
| Evaluation harness | retrieval goldset runner and before/after metrics for search improvements |
| Operating notes | roadmap, backlog, and implementation notes for accounting RAG development |

## Public Boundary

Included:

- Python package code under `kifrs/`
- evaluation and validation scripts
- roadmap/backlog/docs that describe architecture and metrics
- `.gitignore` rules for protected data

Excluded:

- K-IFRS PDF files
- parsed standard text and paragraph DB dumps
- embedding indexes
- CPA exam/dogfood material
- local `.env` files and API keys

## Setup

```powershell
uv sync
```

To build a local database, place source materials in `data/` according to the project docs. `data/` is intentionally ignored and is not part of this public repository.

## Run

```powershell
uv run python -m kifrs.mcp_server
```

## Evaluation

```powershell
uv run python -m kifrs.eval.retrieval --k 20
```

Some evaluation paths require local data that is not included in the repository.

Public-safe quality preflight:

```powershell
uv run python scripts/quality_preflight.py --format text
```

This preflight runs focused tests, the no-network `local-rag` threshold gate, authority metadata validators, and the `user_note_v2` audit. `docs/ci/quality.yml` provides a GitHub Actions template that runs the same command. The preflight does not require protected PDFs, parsed source text, embeddings, DB dumps, dogfood questions, API keys, or network access.

## Firm-Facing Local Demo

This repository is now shaped as a local accounting-intelligence toolkit prototype for a firm-side PoC. The current
showable surface is a public-safe K-IFRS 1116 lease review-pack walkthrough. It demonstrates what the tool can do today:
generate a review memo, journal-entry draft, disclosure draft, review checklist, authority boundary panel, client-private
runtime boundary summary, and verification status from invented fixture data.

Generate the operator walkthrough packet:

```powershell
python scripts/firm_facing_operator_demo_command.py --format markdown --write
```

Check local readiness:

```powershell
python scripts/firm_facing_readiness_checklist.py --format text --write
```

Read the generated reports from:

- `docs/reports/2026-07-05-fps2-operator-demo-command.md`
- `docs/reports/2026-07-05-fps3-readiness-checklist.md`
- `docs/reports/2026-07-05-firm-facing-product-surface-close-report.md`

What it can do now:

- Prepare decision-support drafts for K-IFRS review-pack workflows, especially 1116 lease cases.
- Render K-IFRS primary evidence separately from supporting interpretation, legal boundary, structured fact evidence, and client-private fact references.
- Show the client-private parser path as structured-facts-only and deletion-gated, without publishing real private files.
- Keep RAG quality and default retriever promotion behind explicit gates.

What it does not do:

- It does not replace accountant judgment, partner review, audit opinion, tax/legal conclusion, sign-off, or client communication.
- It does not publish K-IFRS source text, parsed standards, embeddings, dogfood questions, real client files, private identifiers, or private-source payloads.
- It is not a packaged SaaS product yet; it is a local toolkit surface for technical PoC walkthroughs.

## License

Code in this repository is MIT licensed. The license does not cover third-party accounting standards, PDFs, parsed text, exam materials, or other excluded source data.
