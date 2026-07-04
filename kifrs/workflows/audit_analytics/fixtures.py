"""Synthetic financial-statement fixture for AP2 regression tests."""

from .schema import AnalyticalProcedureInput, FinancialStatementLine


SYNTHETIC_FS = AnalyticalProcedureInput(
    entity="synthetic 제조업",
    periods=["20x1", "20x2"],
    lines=[
        FinancialStatementLine("20x1", "balance_sheet", "현금및현금성자산", 120_000),
        FinancialStatementLine("20x2", "balance_sheet", "현금및현금성자산", 80_000),
        FinancialStatementLine("20x1", "balance_sheet", "매출채권", 210_000),
        FinancialStatementLine("20x2", "balance_sheet", "매출채권", 360_000),
        FinancialStatementLine("20x1", "balance_sheet", "재고자산", 180_000),
        FinancialStatementLine("20x2", "balance_sheet", "재고자산", 260_000),
        FinancialStatementLine("20x1", "balance_sheet", "유동자산", 620_000),
        FinancialStatementLine("20x2", "balance_sheet", "유동자산", 810_000),
        FinancialStatementLine("20x1", "balance_sheet", "유동부채", 310_000),
        FinancialStatementLine("20x2", "balance_sheet", "유동부채", 450_000),
        FinancialStatementLine("20x1", "balance_sheet", "총부채", 700_000),
        FinancialStatementLine("20x2", "balance_sheet", "총부채", 1_020_000),
        FinancialStatementLine("20x1", "balance_sheet", "자본총계", 900_000),
        FinancialStatementLine("20x2", "balance_sheet", "자본총계", 880_000),
        FinancialStatementLine("20x1", "income_statement", "수익", 1_500_000),
        FinancialStatementLine("20x2", "income_statement", "수익", 2_100_000),
        FinancialStatementLine("20x1", "income_statement", "매출원가", 980_000),
        FinancialStatementLine("20x2", "income_statement", "매출원가", 1_520_000),
        FinancialStatementLine("20x1", "income_statement", "매출총이익", 520_000),
        FinancialStatementLine("20x2", "income_statement", "매출총이익", 580_000),
        FinancialStatementLine("20x1", "income_statement", "판매비와관리비", 300_000),
        FinancialStatementLine("20x2", "income_statement", "판매비와관리비", 430_000),
        FinancialStatementLine("20x1", "income_statement", "영업이익", 220_000),
        FinancialStatementLine("20x2", "income_statement", "영업이익", 150_000),
        FinancialStatementLine("20x1", "income_statement", "금융비용", 25_000),
        FinancialStatementLine("20x2", "income_statement", "금융비용", 75_000),
    ],
)
