---
agent_requested: true
description: "Authoritative reference for the flat-file (CSV) schema used for documents, transactions, and allocations in KSI year-end accounting."
---

# Flat-File Data Schema Reference

This document defines the canonical CSV-based data schema used for year-end accounting
for Kefelan Solutions Inc. (KSI).

The schema is intentionally normalized and split across three core tables to clearly
separate:
1. **Evidence** (documents)
2. **Economic facts** (transactions)
3. **Judgment, classification, and tax treatment** (allocations)

These files together form a flat-file accounting database suitable for:
- Audit and traceability
- AI-assisted reconciliation and classification
- Accountant-facing summaries
- CRA compliance

---

## 1. `documents.csv` — Evidence / Audit Layer

### Purpose
- Normalized registry of **supporting evidence** for transactions
- Records invoices, receipts, and similar proof of purchase/payment
- Exists solely for **auditability and substantiation**
- Does **not** represent financial postings or sources of truth

### What Belongs Here
- Invoices (vendor-issued)
- Receipts (including scanned or OCR’d receipts)
- Order confirmations or payment confirmations
- Any document whose purpose is to **support or justify** a transaction

### What Does NOT Belong Here
`documents.csv` must **NOT** contain rows representing transaction sources, including:
- Corporate chequing account statements (CSV)
- Corporate credit card statements (Markdown converted from PDF)
- Personal chequing account statements (CSV or Markdown)
- Personal credit card statements (Markdown converted from PDF)
- Cash transaction source records

These items are **transaction sources**, not supporting evidence, and must be referenced
from `transactions.csv` via `source_file` and `source_locator`, not recorded as documents.

### Key Principles
- One row per document (invoice, receipt, confirmation, etc.)
- Documents are **never split**
- A single document may relate to:
  - zero transactions (e.g., unused receipt)
  - one transaction
  - multiple transactions (e.g., consolidated invoice)
- Documents support transactions; they do not define them

### Required Columns

| Column | Description |
|------|-------------|
| document_id | Stable unique ID (human-readable, deterministic if possible) |
| document_type | `invoice`, `receipt`, `confirmation`, `other` |
| document_date | Date shown on the document |
| vendor | Vendor or issuer name |
| amount | Total document amount (as shown) |
| currency | ISO currency code (`CAD`, `USD`, etc.) |
| source_file | Path to the Markdown file converted from PDF/DOCX |
| original_format | `pdf`, `docx`, `md` |
| notes | Conversion issues, ambiguity, or audit-relevant notes |

### Optional Columns
- tax_included_flag
- confidence (`high` / `medium` / `low`)

### Handling Missing or Statement-Only Evidence
- If no invoice or receipt exists for a transaction:
  - Do **not** create a placeholder row in `documents.csv`
  - Instead, record the condition on the transaction using:
    - `receipt_status = not_applicable` or `receipt_status = ambiguous`
- Bank and credit card statements alone are **not** considered documents for audit purposes
  and must not be duplicated in `documents.csv`.

---

## 2. `transactions.csv` — Economic Reality / Balance Sheet Layer

### Purpose
- Normalized ledger of **all financial transactions**
- Represents *what actually happened financially*
- Forms the basis of the **balance sheet and cash flow**

### Sources Covered
#### Primary
- Corporate chequing account (CSV)
- Corporate credit cards (Markdown statements)
#### Secondary (as required)
- Personal chequing account (CSV or Markdown statements) — reference-only; extract only reimbursable/mixed-use items
- Personal credit cards (Markdown statements) — reference-only; extract only reimbursable/mixed-use items
- Personal line of credit (Markdown statements) — reference-only
- Cash transactions (manually identified and verified) — only when reimbursed or corporately treated

### Key Principles
- One row per **posted transaction**
- Transactions are source-agnostic once normalized
- No tax deductibility logic lives here
- Transactions may reference **multiple documents**

### Required Columns

| Column | Description |
|------|-------------|
| transaction_id | Stable unique transaction identifier |
| fiscal_year | Fiscal year (e.g. `2025`) |
| txn_date | Posting date used for accounting |
| source_type | `bank_csv`, `cc_md`, `paypal`, `cash`, `manual` |
| source_file | Path to originating statement or source |
| source_locator | Row number or Markdown locator for traceability |
| account_owner | `corporate` or `personal` |
| account_name | Normalized account/card name |
| payment_method | `chequing`, `credit_card`, `paypal`, `cash`, `other` |
| card_last4 | Last 4 digits if applicable |
| counterparty | Merchant / payee / payer |
| description | Raw transaction description |
| amount | Signed amount (CAD or foreign) |
| currency | ISO currency code |
| cad_amount | CAD-equivalent amount used for reporting |
| fx_rate_to_cad | FX rate if currency ≠ CAD |
| linked_document_ids | Delimited list of document_ids |
| receipt_status | `found`, `missing`, `ambiguous`, `not_applicable` |
| notes | Reconciliation or interpretation notes |

### Important Notes
- **No CRA classification lives here**
- **No deductibility logic lives here**
- This table answers: *“What happened, when, and for how much?”*

---

## 3. `allocations.csv` — Classification / Tax Judgment Layer

### Purpose
- Applies **judgment and tax treatment** to transactions
- Supports CRA reporting, deductibility, and GST/HST returns
- Allows full or partial allocation of transactions

### Key Principles
- One transaction can have **multiple allocation rows**
- Allocations may:
    - Split corporate vs personal
    - Apply different CRA categories
    - Apply different deductibility rules
- Allocations are the *only* place where CRA logic is applied

### Required Columns

| Column | Description |
|------|-------------|
| allocation_id | Unique allocation row ID |
| transaction_id | Reference to `transactions.csv` |
| allocation_type | `full` or `split` |
| applies_to | `corporate` or `personal` |
| allocated_amount | Signed amount allocated |
| allocated_gst | GST/HST portion of allocated amount |
| allocated_pst | PST portion of allocated amount |
| reporting_category | Internal reporting category |
| cra_code | CRA reference code (e.g. `8523`) |
| deductible_percentage | CRA deductible percentage (e.g. `50`) |
| deductible_amount | Calculated deductible amount (ex GST/HST) |
| itc_eligible_amount | GST/HST eligible for ITC |
| tax_treatment | `standard`, `meals_50`, `capital_asset`, `shareholder_loan`, `dividend`, `non_deductible` |
| notes | Explanation of judgment or special handling |

### Important Notes
- Meals & entertainment rules (50%) are implemented **here**
- Shareholder loan vs dividend determination is recorded **here**
- Capital asset identification starts here (but depreciation remains accountant-driven)

---

## 4. Relationship Summary

```text
documents.csv
   ↑        ↑
   │        └── referenced by (0..N)
   │
transactions.csv
   ↑
   └── referenced by (1..N)
       allocations.csv
```

## 5. FY2024 Reference File: `FY2024/financials/2024_Transaction_Allocations.csv`

FY2024 includes a legacy allocation-style file used as a reference for FY2025+ automation.

- This file is a precedent for category mapping and tax handling (e.g., splits, GST/PST fields).
- It is NOT the canonical schema going forward.
- FY2025+ uses the normalized schema:
  - `documents.csv` (evidence)
  - `transactions.csv` (posted financial reality)
  - `allocations.csv` (classification & tax judgment)

### Notes for AI agents
- The `Date` column may be stored as an Excel serial date number and must be converted to YYYY-MM-DD before use.
- Fields such as `Account 1/2` and `Part 1/2` represent allocation/split logic similar to FY2025 `allocations.csv`.
- Use this file to learn vendor→category patterns and tax treatment patterns, but do not copy classifications blindly.
