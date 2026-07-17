# Horizon: Multi-Source Ingestion Pipeline

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/authority-source-map.md`

## Goal

metadata-only document sources and structured fact sources를 보호 자료 없이 등록·검증할 수 있는 ingestion
pipeline skeleton을 만든다.

## Why next

`authority-source-map`은 무엇을 넣을지, 어떤 권위로 쓸지, 무엇을 저장하면 안 되는지 정했다. 이제 다음
단계는 실제 connector contract와 manifest를 만들어 source를 안전하게 데이터화하는 것이다.

## Candidate Milestones

### MSI1. Connector Contract and Source Manifest

공통 connector output schema를 정의한다.

Deliverable:

- connector contract
- public-safe source manifest schema

### MSI2. Metadata-Only Document Catalog Prototype

KASB/FSS-style interpretive source를 body 없이 metadata catalog로 등록한다.

Deliverable:

- metadata-only catalog fixture
- validator

### MSI3. Structured Fact Fixture Prototype

OpenDART-like structured financial facts를 synthetic fixture로 만든다.

Deliverable:

- structured fact schema
- synthetic financial facts fixture

### MSI4. Provenance and Citation Manifest

source id, locator, storage policy, citation role을 evidence manifest로 연결한다.

Deliverable:

- provenance manifest
- citation role checks

### MSI5. Ingestion Gate and Close Report

보호 본문이 커밋되지 않았는지 검증하고 다음 runtime horizon으로 넘긴다.

Deliverable:

- ingestion gate
- close report
