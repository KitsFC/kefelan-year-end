# FY2025 Planned AI Prompts

## 0) Preamble — Populate Normalized CSV Files

```text
Before running any analysis prompts, populate the five normalized CSV files
under FY2025/normalized/ according to the schema defined in
.augment/rules/20_data_schema.md:

IMPORTANT: Ensure CSV files use LF (`\n`) line endings (not CRLF).

1. documents.csv — Evidence / Audit Layer
   - Scan all invoices, receipts, and confirmations under FY2025/transactions/
   - Create one row per document
   - Do NOT include transaction source records (bank/credit card statements)

2. transactions.csv — Economic Reality / Balance Sheet Layer
   - Ingest all corporate chequing (CSV) and credit card (Markdown) transactions
   - Extract reimbursable/mixed-use personal transactions only
   - Link to documents.csv where evidence exists

3. allocations.csv — Classification / Tax Judgment Layer
   - Pre-populate with suggested allocations (full or split)
   - Apply known defaults from .augment/rules/10_accounting_rules.md
   - Flag uncertain classifications for owner review

4. assets.csv — Capital Asset Register
   - Use FY2024/financials/2024_Capital_Assets.md as the starting asset register
   - Identify FY2025 additions and disposals from transactions
   - Do NOT calculate depreciation; flag for accountant

5. owed.csv — Accounts Payable / Accounts Receivable
   - Track invoices/amounts owed that do not map 1:1 to posted statement transactions
     (e.g., invoices paid/collected in installments)
   - Link settlement activity using `linked_transaction_ids`
   - Carry forward any open balances at FY-end into next fiscal year’s owed.csv

All subsequent prompts assume these files are populated and up to date.
```

## A) Reconcile all transactions with corporate chequing and credit card statements

```text
Reconcile all FY2025 corporate transactions.

Data sources:
- Corporate chequing account transactions (CSV)
- Corporate credit card statements (Markdown converted from PDF)
- Corporate invoices/receipts (Markdown converted from PDF)

Instructions:
- Build a matched set across sources using date, amount, and merchant/description.
- If an invoice/contract evidence document exists but no single statement line matches the total amount,
  first confirm that **all relevant statements have been ingested/checked** for the fiscal year.
  - Check corporate chequing + corporate credit card statements first.
  - If (and only if) there is **no partial/installment payment** visible on corporate statements, fully scan **all** personal statements under `FY2025/reference/personal` before allowing any `owed.csv` entry.
  Only then treat it as a likely **installment / A/P / A/R** case and ensure it is represented in `FY2025/normalized/owed.csv`.
  If statement coverage is not yet complete, do not add an owed row as “unpaid”; instead flag it as `unknown` for follow-up.
- Output three lists:
  1) Matched (confident match)
  2) Needs review (partial match, ambiguous, or conflicting)
  3) Unmatched (appears in one source but not the others)
- For each item include:
  - normalized transaction_id (or a generated stable ID)
  - source references: file path + line/section if available
  - match confidence (high/medium/low)
  - discrepancy reason if any (date shift, tip, FX, partial posting, etc.)
- Do NOT assume missing items are personal or corporate; flag and ask for owner decision.
- Watch out for receipts for most hospitality transactions. These receipts were scanned as images before being processed via OCR and converted to Markdown. Most of these transactions are split into two (rarely more) receipts: one for the food and beverage and the other for the credit card transaction, which includes the tip. Multiple receipts for the same transaction constitutes multiple sources, not multiple transactions.
- As part of reconciliation, ensure FY2025/normalized/documents.csv is populated with all supporting evidence (invoices, receipts, confirmations) found under FY2025/transactions/. Do NOT add transaction source records (bank/credit card statements) to documents.csv.
```

## B) Identify personal transactions not in corporate records (and cash)

```text
Identify FY2025 transactions that appear in personal chequing or personal credit card records
but do not appear in corporate records (and/or indicate cash spending).

Instructions:
- Compare personal records (reference/personal) against corporate normalized transactions.
- Produce a decision list grouped into:
  - Likely reimbursable corporate expense paid personally
  - Likely shareholder activity (loan/dividend-related)
  - Likely personal/non-corporate
  - Cash transaction candidates (no electronic trace)
- Note: For FY2025, $2,000 per month of shareholder transfers covers personal expenses on behalf of the corporation (rent, utilities, etc.). Use this when evaluating whether personal transactions may be reimbursable.
- For each item include:
  - date, amount, merchant/description
  - which personal account/card it came from
  - whether a receipt exists in corporate docs
  - recommended handling (reimburse / leave personal / shareholder loan / unknown)
- Do not finalize; present for owner judgment.
```

## C) Identify foreign currency cash transactions requiring exchange rates

```text
Identify all FY2025 transactions involving foreign currency, with emphasis on cash transactions.

Instructions:
- Scan invoices/receipts and statement lines for currency indicators (USD, GBP, EUR, etc.).
- If currency is unclear, compare the invoice amount to the statement amount to infer currency.
- Output a list of transactions requiring owner-supplied FX rate, including:
  - date
  - original currency amount (if known)
  - suspected currency (if inferred)
  - CAD amount posted (if any)
  - evidence notes and source references
- Flag cash transactions separately as highest priority.
```

## D) Identify corporate statement transactions missing an invoice/receipt

```text
Find corporate transactions (bank or corporate credit card) that are missing supporting documentation.

Instructions:
- For each bank/credit-card transaction, check whether there is an invoice/receipt MD file.
- Output a checklist with:
  - date, amount, vendor, payment method (bank/card)
  - receipt status: found / missing / ambiguous
  - what would satisfy the documentation (invoice PDF/receipt screenshot/email receipt)
  - exceptions: interest/fees that may not have receipts (still list, mark as exception)
- Do not fabricate receipts; only link to files that exist.
```

## E) Pre-classify all transactions (using FY2024 financials as reference)

```text
Pre-classify FY2025 transactions according to categories used in FY2024 financials.

Instructions:
- Use FY2024 Statements of Income and Retained Earnings categories as the target taxonomy.
- Use `FY2024/financials/2024_Transaction_Allocations.csv` as a reference mapping for vendor→category/CRA code patterns and split patterns.
- Do not copy blindly; verify against FY2025 source evidence and flag differences.
- Apply known defaults from .augment/rules/10_accounting_rules.md.
- Output a table with:
  - transaction_id
  - date, vendor, description, amount
  - suggested category + CRA code (if applicable)
  - confidence (high/medium/low)
  - notes about why classification was chosen
- Flag transactions that might be:
  - capital assets
  - shareholder loan/dividend related
  - mixed-use or meal/entertainment (50% rules)
```

## F) Track capital assets and depreciation (starting from FY2024)

```text
Track capital assets for FY2025 and populate FY2025/normalized/assets.csv
per the schema in .augment/rules/20_data_schema.md §4.

Instructions:
- Use FY2024/financials/2024_Capital_Assets.md as the starting asset register.
- Identify:
  - additions in FY2025 (new assets)
  - disposals in FY2025
  - assets that may have changed use or ownership
- Populate assets.csv with the full schema columns:
  - asset_id, description, acquisition_date, cost, currency, cad_cost, vendor
  - cca_class (if inferable; otherwise leave blank and flag)
  - opening_ucc, additions, disposals, cca_claimed, closing_ucc
  - linked_transaction_id, linked_document_ids, notes
- For existing assets carried forward from FY2024, populate opening_ucc from prior year data.
- Do NOT calculate depreciation (cca_claimed / closing_ucc) unless all required inputs are present; flag for accountant.
```

## G) Identify GST/HST collected and paid (and ITCs)

```text
Summarize FY2025 GST/HST collected and paid, including ITC-eligible GST/HST.

Instructions:
- For revenue invoices, extract GST collected (5% GST unless otherwise indicated).
- For expenses, extract GST paid and determine ITC eligibility.
- Special handling:
  - Meals & entertainment: only 50% of GST/HST eligible for ITC
  - Combined 12% tax: separate GST portion = tax × 5 ÷ 12 (round to nearest cent)
  - Taxi fares (BC): GST included in fare, no PST; GST = fare × 5 ÷ 105
- Output:
  - total GST collected
  - total GST paid (ITC-eligible)
  - net GST payable/refundable estimate
  - list of transactions with unclear tax treatment
```

## H) Produce an accountant-facing summary report

```text
Prepare an accountant-facing FY2025 summary suitable for year-end entry.

Instructions:
- Use tables, not narrative.
- Include:
  1) Revenue summary (totals + GST collected)
  2) Expense summary by category (matching FY2024 taxonomy + CRA codes)
  3) Shareholder loan activity summary (transfers, repayments, outstanding)
  4) Capital assets summary (from assets.csv: additions, disposals, opening/closing UCC)
  5) GST/HST summary (collected, ITCs, net)
  6) Open issues/questions requiring owner/accountant decision
- Every total must reference underlying transaction_ids and source files.
- Note: For FY2025, $2,000 per month of shareholder transfers covers personal expenses on behalf of the corporation (rent, utilities, etc.).
```
