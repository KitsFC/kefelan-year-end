# FY2025 Planned AI Prompts

## A) Reconcile all transactions with corporate chequing and credit card statements

```text
Reconcile all FY2025 corporate transactions.

Data sources:
- Corporate chequing account transactions (CSV)
- Corporate credit card statements (Markdown converted from PDF)
- Corporate invoices/receipts (Markdown converted from PDF)

Instructions:
- Build a matched set across sources using date, amount, and merchant/description.
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
- Apply known defaults from context/10_accounting_rules.md.
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
Track capital assets for FY2025 and prepare depreciation-ready information.

Instructions:
- Use FY2024/financials/2024_Capital_Assets.md as the starting asset register.
- Identify:
  - additions in FY2025 (new assets)
  - disposals in FY2025
  - assets that may have changed use or ownership
- Output an updated register table with:
  - asset_id
  - description
  - acquisition date
  - cost
  - currency
  - vendor
  - supporting document references
  - suggested CCA class (if inferable; otherwise leave blank and flag)
- Do NOT calculate depreciation unless all required inputs are present; flag for accountant.
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
  4) Capital assets changes summary (additions/disposals)
  5) GST/HST summary (collected, ITCs, net)
  6) Open issues/questions requiring owner/accountant decision
- Every total must reference underlying transaction_ids and source files.
```
