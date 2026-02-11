---
agent_requested: true
description: "Operational instructions for AI agents (Aggie/Junie) to analyze, reconcile, classify, and summarize year-end accounting data."
---

# AI Instructions – Year-End Accounting Assistance

## General Behavior
- Do NOT invent transactions, amounts, dates, currencies, vendors, or tax treatment.
- If information is missing or ambiguous, flag it explicitly.
- Prefer consistency over guesswork.
- Preserve original filenames and paths when referencing documents.

## Working With Converted Documents
- Many statements/receipts are in Markdown converted from PDF→DOCX→MD.
- Treat statement Markdown as the authoritative source if it matches other evidence.
- If statement text looks corrupted/ambiguous due to conversion, mark it as "needs manual verification".

## Working With Personal Records
- `FY????/reference/personal` is reference-only.
- Do NOT attempt to ingest, normalize, classify, or summarize all personal spending.
- Only extract personal transactions when they appear to be:
    - reimbursed by KSI, or
    - partially reimbursed / mixed-use and therefore require allocation.
- When a personal transaction appears relevant, flag it for owner decision and only record it if it maps to corporate reimbursement or corporate treatment.

## Output Rules
- Use tables for summaries.
- Clearly label facts vs assumptions.
- Include transaction IDs / references to enable traceability back to source files.

## CSV File Hygiene (IMPORTANT)
- All CSV files in this repo MUST use **LF** (`\n`) line endings, not CRLF (`\r\n`).
- When generating CSVs in code, explicitly set the CSV writer line terminator to `\n`.
- When editing CSVs manually, avoid tools that silently rewrite line endings (common with spreadsheet apps).

## Reconciliation Requirements
Every transaction should trace to one or more of:
- Bank statement line (CSV)
- Credit card statement line (CSV)
- Invoice or receipt (MD)

If a transaction is missing a receipt, record a "missing_document" flag and list what would satisfy it.

## Using FY2024 Allocations as Reference
- `FY2024/financials/2024_Transaction_Allocations.csv` may be used as a reference dataset to:
  - infer vendor→category mappings
  - infer typical tax treatment patterns (GST/PST, meals/tips, split handling)
- Do NOT assume FY2024 treatment applies to FY2025 without verifying source documents.
- If using FY2024 patterns, label the result as "suggested (based on FY2024 precedent)" and set confidence accordingly.

## Capital Assets
- Track capital assets and their depreciation in `FY????/normalized/assets.csv`.
- Identify potential new capital assets from transactions and flag them for owner review.
- Do NOT calculate depreciation or assign CCA classes unless all required inputs are present and verified — flag for accountant.
- See `20_data_schema.md` §4 for the canonical schema.

## Accounts Payable / Receivable (A/P & A/R)
- Some invoices are paid/collected in **installments**; in those cases:
  - `documents.csv` contains the invoice evidence (full invoice amount)
  - `transactions.csv` contains the installment payment(s) (posted cash movements)
  - The invoice total will not match any single statement line
- Track these accrual-style balances in `FY????/normalized/owed.csv` (see `20_data_schema.md`).
- IMPORTANT: Only add an item to `owed.csv` after you have confirmed **statement coverage is complete** for the fiscal year.
  1) First, check all **corporate** statements (chequing + credit card).
  2) If (and only if) **no partial/installment payment** for that invoice/obligation appears on any corporate statement, then you MUST fully scan **all personal statements** under `FY????/reference/personal` before allowing an `owed.csv` entry.
  3) Also check any other in-scope sources (e.g., PayPal).
  If statement ingestion/coverage may be incomplete, do **not** conclude an invoice is unpaid; instead use `status = unknown` (in `owed.csv`) and leave a clear note for owner follow-up.
- At fiscal year end, any remaining open payables/receivables must be carried forward to the next fiscal year’s `owed.csv`.

## Notes and Learnings
Any recurring ambiguity, correction, or clarification discovered during analysis MUST be recorded in:
- `.augment/rules/90_lessons_learned.md`

Each entry must include:
- Date
- Issue
- Resolution
- Guidance for Future Years

## Accountant-Facing Output
- Assume the reader is a CPA familiar with CRA filings.
- Prefer structured tables over narrative.
- Use CRA terminology and CRA account/category codes when available.
