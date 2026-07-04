# Source-Aware Workflow Rebuild Report

## Summary

- Total review packs: 24
- Automated packs: 20
- Needs human review packs: 4
- Source manifest: `docs/ingestion/source_manifest.example.json`
- Evidence manifest: `docs/ingestion/evidence_manifest.example.json`

## External Evidence Roles

| Role | Count |
|---|---:|
| fact_evidence | 24 |
| legal_boundary | 24 |
| supporting_interpretation | 24 |

## By Standard

| Standard | Packs | Automated | Needs human review | Citations | Fact evidence refs | Human-review items |
|---|---:|---:|---:|---:|---:|---:|
| KIFRS1109 | 10 | 7 | 3 | 16 | 10 | 17 |
| KIFRS1115 | 4 | 4 | 0 | 28 | 4 | 4 |
| KIFRS1116 | 10 | 9 | 1 | 81 | 10 | 16 |

## Pack Detail

| Standard | Case | Status | Citations | External evidence roles | Fact evidence | Human-review items |
|---|---|---|---:|---|---:|---:|
| KIFRS1109 | scenario_01_corporate_bond_ac | automated | 3 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1109 | scenario_02_corporate_bond_fvoci | automated | 4 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1109 | scenario_03_credit_linked_note_fvpl | automated | 1 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1109 | scenario_04_listed_equity_fvoci_irrevocable | automated | 2 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1109 | scenario_05_ifric19_debt_equity_swap | needs_human_review | 0 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1109 | scenario_06_floating_rate_bond_sppi_nuance | automated | 3 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1109 | scenario_07_convertible_bond_holder | automated | 1 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1109 | scenario_08_business_model_change_reclassification | needs_human_review | 0 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1109 | scenario_09_fvpl_designation_accounting_mismatch | automated | 2 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1109 | scenario_10_foreign_currency_bond_1109_1021 | needs_human_review | 0 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1115 | scenario_01_renewal_option | automated | 7 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1115 | scenario_02_discount_right | automated | 8 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1115 | scenario_03_significant_financing | automated | 9 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1115 | scenario_04_repurchase_call_option | automated | 4 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1116 | scenario_01_simple_office_lease | automated | 11 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1116 | scenario_02_restoration_prepaid | automated | 11 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1116 | scenario_03_short_low_value_exemption | automated | 7 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1116 | scenario_04_lessor_finance_to_operating | automated | 5 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1116 | scenario_05_lessor_op_to_finance | automated | 5 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1116 | scenario_06_lessor_finance_to_finance_payment_change | automated | 6 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1116 | scenario_07_lessee_term_reassessment | automated | 12 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1116 | scenario_08_lessee_purchase_option_reasonably_certain | automated | 12 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |
| KIFRS1116 | scenario_09_lessee_modification_expand_shrink | needs_human_review | 0 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 1 |
| KIFRS1116 | scenario_10_lessee_modification_extend | automated | 12 | fact_evidence:1, legal_boundary:1, supporting_interpretation:1 | 1 | 2 |

## Boundary

- External evidence remains supporting metadata or synthetic fact evidence.
- K-IFRS citations remain the primary accounting evidence.
- Human-review items are counted, not removed.
- This report does not include source document payloads, private filings, parsed standards, embeddings, or customer data.
