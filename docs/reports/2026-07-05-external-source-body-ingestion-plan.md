# External Source Body Ingestion Implementation Plan

> Scope: staged implementation plan that remains blocked until explicit authorization is recorded.

## One-Line Conclusion

The next implementation is not body ingestion itself. The next implementation is a source-specific authorization gate that proves policy, plan, source review, and public-safe tests before any live body cache is touched.

## Implementation Steps

- source-specific policy record
- local cache path contract
- parser/chunker dry-run with synthetic text
- forbidden-field regression tests
- explicit authorization gate

## Proceed Gate Requirements

- source manifest ok
- evidence manifest ok
- live landing validation report present
- external source body storage policy present
- external source body ingestion implementation plan present
- explicit user authorization present

## Not Implemented Here

- live body fetching or crawling
- source body cache
- body chunker
- external body embedding namespace
- answer-time use of external body text

## Next Leaf

real-accountant-session RS2/RS3 evidence capture, or external source body-ingestion authorization gate
