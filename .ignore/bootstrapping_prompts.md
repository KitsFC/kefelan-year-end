# ChatGPT | KSI | KSI ~ Year-end Accounting

## [2026-02-09 16:10 PST]

I have created a repository, `kefelan-year-end`, to help perform the year-end accounting for my corporation, Kefelan Solutions Inc. (KSI), annually. Each year, I need to provide a summary of this information with sufficient detail to my accountant so that it can be entered into their accounting system. In most cases, the level of detail can be annual; in some cases, monthly; in rare cases, transactional. In any case, the information must be classified. For my own records, I need a detailed record of all transactions, grouped logically. My accountant will then prepare year-end financial statements ("financials") and issue and/or file the following as required by the Canada Revenue Agency (CRA):

- T4A "Statement of Pension, Retirement, Annuity, and Other Income" slip(s) for unincorporated subcontractors (individuals or sole proprietors)
- T5 "Statement of Investment Income" slip for dividends paid to me (sole shareholder)
- T2 Corporate Income Tax return
- Simple GST return for Goods and Services Tax/Harmonized Sales Tax (GST/HST) collected less Input Tax Credits (ITCs)

For FY2025, I have provided the following:

1. Last year's financials, `FY2024/financials/...`, for reference. (To reiterate, preparing this year's financials is a job for the accountant—my job is to provide the information required by the accountant to do this along with the CRA slips and returns.)

2. Financial transactions according to type in `FY2025/transactions`:

   - `1_assets`: transactions related to assets such as bank accounts
   - `2_equity`: transactions related to equity
   - `3_liabilities`: transactions related to liabilities such as credit card statements
   - `4_revenue`: transactions related to revenue such as sales invoices
   - `5_expenses`: transactions related to expenses such sa purchase invoices

3. Personal financial transactions in `FY2025/reference/personal` for reference. This is needed in case a transaction in the corporate records needs to be reconciled with a personal transaction.

Important notes about how I am paid by KSI:

- Twice—rarely, more than twice—per month, I transfer Funds from my corporate chequing account to my personal chequing account—these are effectively short-term loans to the shareholder (me). Taken as a whole for the year:

    - $2,000 per month covers the cost of running the corporation (rent, utilities, etc.).
    - Some may cover expenses that I paid out of my personal chequing account or personal credit cards. 
    - The remainder is divided between a dividend or a loan to the shareholder (me), but this is determined after the year-end accounting is done and an analysis of my personal tax liability for varying dividend amounts—a dividend amount is certain, but a loan is not, especially if there is an outstanding loan amount from the previous year as a loan from a small business to a shareholder can only remain on the books for one year after the end of the corporation's taxation year in which the loan was made; if not repaid within this timeframe, the CRA considers it taxable personal income.

Occasionally, I will also transfer money from my one of my personal accounts to my corporate chequing account; either to cover a shortfall in the corporate account or to make a loan to the corporation.

Here is additional but not exhaustive detailed information about the corporation, its operations, and some exceptional transactions:

- Kefelan Solutions Inc. (KSI)
    - Incorporated in British Columbia March 18, 2025
    - Fiscal year: January 1 to December 31
    - Canada Revenue Agency (CRA) Goods and Services Tax (GST) Registration Number: 810685594RT0001
- Credit cards
    - TD Business VISA ends in 5143
    - TD Business VISA via Google Wallet ends in 4527
    - TD Personal VISA ends in 6493
    - TD Personal VISA via Google Wallet ends in 8283
    - BMO Personal Mastercard ends in 9973
    - BMO Personal Mastercard via Google Wallet ends in 5056
    - RBC Personal VISA ends in 5672
- PayPal
    - In almost all cases, the method of payment will be the Business VISA ending in 5143, but there could be exceptions
- Cash
    - All cash transactions, regardless of currency, were paid out of personal funds
- Tax
    - British Columbia Provincial Sales Tax (PST) is 7% for almost everything
    - 8% for accommodation
    - 10% for liquor
    - British Columbia federal Goods and Services Tax (GST) is 5%
    - If KSI's GST number is provided to a vendor, KSI may not be charged GST because KSI would be able to claim it as an Input Tax Credit (ITC) so the vendor is saving KSI the effort
    - In BC, taxi fares, before tip, include GST, but no PST applies (fare × 5 ÷ 105, round to the nearest cent)
    - In BC, parking fees may include or add GST, but no PST applies
    - Many online services are based outside of Canada; some comply with BC/Canadian tax laws while some do not
    - Some vendors may charge 12% tax—combining PST 7% and GST 5%—but GST must be separated out (tax × 5 ÷ 12, round to the nearest cent)
- Foreign currency transactions
    - Pay attention to whether an invoice is in Canadian Dollars (CAD) or perhaps a foreign currency like U.S. Dollars (USD) or Great British Pounds (GBP)
    - Sometimes this can only be determined by comparing the invoice amount with the amount on the bank chequing account or credit card statement
    - If there are any cash transactions, I will need to be notified so that I can provide the foreign currency exchange rate 
- Recurring SAAS transactions
    - Classify as "Office expenses" (CRA reference 8810)
- Tickets for live events (Eventbrite, Ticketmaster, etc.)
    - Classify as "Advertising and promotion" (CRA reference 8520)
- Gas (Chevron, Esso, Petro Canada, Shell, etc.)
    - Classify as "Travel expenses" (CRA reference 9200)
- Gifts such as flowers, chocolates, liquor, etc.
    - Classify as "Advertising and promotion" (CRA reference 8520)
- Parking (City of Vancouver, Honk Mobile, ZipBy, etc.)
    - Classify as "Rental" (CRA reference 8910)
- Restaurants, coffee shops, etc.
    - Classify as "Meals and entertainment" (CRA reference 8523)
    - Record full amounts, but note that only 50% of the amount, less GST/HST is tax deductible
    - Only 50% of the GST/HST may be used for the Input Tax Credit (ITC)
    - Most transactions have two documents/receipts: one for the food and beverage and the other for the credit card transaction, which includes the tip
- Taxicabs (Black Top & Checker Cabs, Yellow Cabs, etc.)
    - Classify as "Travel expenses" (CRA reference 9200)
- Air Canada
    - Classify as "Travel expenses" (CRA reference 9200)
- BC Registry Service
    - Classify as "Business fees and licences" (CRA reference 8760)
- Expedia
    - Classify as "Travel expenses" (CRA reference 9200)
- Guardian Storage
    - Classify as "Rental" (CRA reference 8910)
- Rogers Communications or Rogers Wireless
    - Classify as "Telephone and utilities" (CRA reference 9220)
    - Payment of $297.22 on the January 2025 credit card statement is for the 2024-12-24 bill
- Google
    - Invoices are typically end of the month with payment the first of the next month
- DigitalOcean
    - "Date of issue" is not the invoice date because payment is taken on the last day of the month, which should be used as the invoice/receipt date
    - Note the following PayPal transactions:
        - June, 27 2025 | PayPal Transaction | -$5.00
        - August, 01 2025 | PayPal Transaction | -$10.41
    - Those PayPal transactions are related to the following invoices:
        - July, 01 2025 | Invoice for June 2025 | $0.62
        - August, 01 2025 | Invoice for July 2025 | $14.79
- Uber
    - Classify as "Travel expenses" (CRA reference 9200)

I am going to use AI tools such as Augment Code (Aggie) and JetBrains Junie to help me analyze and summarize the information in these files so that I can provide the required information to my accountant.

Questions and requests:

1. What is/are the best AI model(s) for this task?
2. Please help create one or more general context markdown files—not specific to any fiscal year—for Aggie and Junie to help them understand the task and the data.
    - This should include a specific instruction for the Ai tool to add notes to a separate file that contains lessons learned throughout the year-end accounting process and guidelines for future years.  
3. How should the detailed information be stored or recorded? Tables in `.md` files? `.csv` or `.json` flat files? Lowdb or SQLite database (could be good for long-term storage and analysis)?
4. Please help create one or more prompts for the AI tool to achieve the following tasks for FY2025:
    a. Reconcile all transactions with corporate chequing and credit card statements.
    b. Identify any transactions that appear in personal chequing or credit card statements that do not appear in the corporate records, or cash transactions, so that I can decide how to handle them.
    c. Identify any foreign currency cash transactions to that I can provide the foreign currency exchange rate.
    d. Identify any transactions in the corporate chequing and/or credit card statements that are missing an invoice or receipt.
    e. Pre-classify all transactions according to the FY2024 Statements of Income and Retained Earnings (including expenses) so that I can review and adjust as necessary.
    f. Keep track of capital assets and their depreciation, using the information in `FY2024/financials/2024_Capital_Assets.md` as a starting point.
    f. Identify GST/HST collected and paid.
    g. A summary report for the accountant. 

---

# ChatGPT | KSI | KSI ~ Year-end Accounting

## [2026-02-09 16:51 PST]

1. Please add at the top of each Markdown file, before the level-one heading:

```markdown
---
agent_requested: true
description: "..."
---
```

2. The raw documents, mostly PDF, are stored outside the repository, but all of those PDF files were converted to DOCX using ABBYY FineReader PDF, and then to `.md` files using pandoc with the `gfm` output format using the following PowerShell command:

```powershell
Get-ChildItem *.docx | ForEach-Object { pandoc $_.FullName -t gfm -o (Join-Path $_.DirectoryName (($_.BaseName -replace ' ', '_') + ".md")) }
```

3. Chequing account transactions are in CSV format, but credit card statemens are in Markdown format (coverted from PDF).

4. Please combine all of the prompts into one Markdown file with each prompt separated by `---`; add a comment (heading) before each prompt.

5. Please design the exact CSB schema for `FY2025/normalized/transactions.csv` (or whatever files).

---

# ChatGPT | KSI | KSI ~ Year-end Accounting

## [2026-02-10 10:10 PST]

This is how I think the CSV flat-file database schema should be structured:

- `documents.csv`
    - should be a normalized table of invoices and receipts
    - is important for audit
- `transactions.csv`
    - should be a normalized table of transactions from the following sources:
        - Corporate chequing account statement (CSV)
        - Corporate credit card statements (Markdown converted from PDF)
        - Personal:
            - chequing account statement (CSV)
            - credit card statements (Markdown converted from PDF)
            - cash (manually identified/verified)
    - references `documents.csv`
    - is important for the balance sheet
- `allocations.csv`
    - should be a table that allocates transactions—unsplit (whole) or split (part)—to:
        - corporate or personal
        - reporting category
        - CRA reference code
        - CRA deductible percentage (applies to total amount less GST/HST as well as to GST/HST)
        - CRA deductible amount
        - CRA GST/HST ITC eligible amount
    - references `transactions.csv`
    - is important for classifications and tax treatment

Please create a single Markdown reference file that describes the schema and fits somewhere within the following:

- `.augment/rules/00_overview.md`
- `.augment/rules/10_accounting_rules.md`
- `.augment/rules/20_ai_instructions.md`
- `.augment/rules/90_lessons_learned.md`

---

# ChatGPT | KSI | KSI ~ Year-end Accounting

## [2026-02-10 10:15 PST]

In one or more of the `.augment/rules` Markdown files, let's make it very clear that not all personal transactions (contained within `FY????/reference/personal`) need to be recorded. Only the ones that are wholly or partially reimbursed by the corporation (i.e. contained within `FY????/transactions`) need to be recorded. Which file(s) should I update?

---

# ChatGPT | KSI | KSI ~ Year-end Accounting

## [2026-02-10 10:20 PST]

Is it ok that I renamed `.augment/rules/15_data_schema.md` to `.augment/rules/20_data_schema.md` and `.augment/rules/20_ai_instructions.md` to `.augment/rules/30_ai_instructions.md`?

---

# ChatGPT | KSI | KSI ~ Year-end Accounting

## [2026-02-10 10:30 PST]

I have now added the file `FY2024/financials/2024_Transaction_Allocations.csv` (attached) for reference. Should I update any of the `.augment/rules` Markdown files or the `.ignore/FY2025_planned_prompts.md` file (also attached)? 

---

# ChatGPT | KSI | KSI ~ Year-end Accounting

## [2026-02-10 11:00 PST]

I need to clarify that `FY2025/normalized/documents.csv` should not contain any rows/references to the following "transaction sources":

- Corporate chequing account (CSV)
- Corporate credit cards (Markdown statements)
- Personal chequing account (CSV or Markdown statements)
- Personal credit cards (Markdown statements)
- Cash transactions (manually identified and verified)

because `FY2025/normalized/documents.csv` records evidence of transactions that would be found in the transaction sources. Therefore, `.augment/rules/20_data_schema.md` should be updated to reflect this.

Also, are my additional subheadings "Primary" and "Secondary" under "Sources Covered" in the following section of `.augment/rules/20_data_schema.md` ok?

```markdown
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
- Personal chequing account (CSV or Markdown statements)
- Personal credit cards (Markdown statements)
- Cash transactions (manually identified and verified)
```

---

# Junie | Claude Opus 4.6

## [2026-02-10 11:30 PST]

Please review all the documents under `.augment/rules` and reference the original instructions in `.ignore/prompts.md`. Please identify any discrepancies and make any necessary obvious changes. For anything that is not obvious, please ask me for clarification. Please also make a list of omissions from the original instructions and any suggestions for improvement. DO NOT modify `.ignore/prompts.md`.

---

# Junie | Claude Opus 4.6

## [2026-02-10 11:57 PST]

You wrote:
```
### Items Needing Clarification

2. 10_accounting_rules.md line 63 — Meals deductibility wording: The original instructions (prompts.md line 80) say "only 50% of the amount, less GST/HST is tax deductible" and "Only 50% of the GST/HST may be used for the Input Tax Credit (ITC)". The rules file condensed this to "Only 50% deductible (net of GST/HST rules per accountant)". Should I restore the more explicit two-part wording from the original?
3. Folder ordering in prompts.md: The original prompt (line 19) lists 2_equity before 3_liabilities, but the actual folder structure is 2_liabilities then 3_equity. This is in prompts.md which I'm not modifying — just flagging it as a known discrepancy in the original.

### Omissions from the Original Instructions Not Covered in Rules Files

4. GST vendor exemption rule (prompts.md line 59): "If KSI's GST number is provided to a vendor, KSI may not be charged GST because KSI would be able to claim it as an Input Tax Credit (ITC) so the vendor is saving KSI the effort" — not mentioned in 10_accounting_rules.md.
5. Restaurant dual-receipt note (prompts.md line 82): "Most transactions have two documents/receipts: one for the food and beverage and the other for the credit card transaction, which includes the tip" — not mentioned anywhere in the rules.
6. Specific CRA filings list (prompts.md lines 7-11): T4A for unincorporated subcontractors, T5 for dividends, T2 corporate return, simple GST return — 00_overview.md mentions these generically but doesn't include the specific descriptions (e.g., T4A is for unincorporated subcontractors/individuals/sole proprietors).
7. Level of detail guidance (prompts.md line 5): "the level of detail can be annual; in some cases, monthly; in rare cases, transactional" — not captured in any rules file.
8. Capital assets and depreciation tracking (prompts.md line 123): "Keep track of capital assets and their depreciation, using the information in FY2024/financials/2024_Capital_Assets.md as a starting point" — only briefly mentioned in 20_data_schema.md line 178 but not as a standing instruction.
9. Shareholder loan one-year repayment rule detail (prompts.md line 32): The detailed explanation about CRA treating unpaid shareholder loans as taxable personal income is condensed to just "CRA shareholder loan rules apply (one-year repayment rule)" in 10_accounting_rules.md line 18. Should I expand this?

### Suggestions for Improvement
- Add the GST vendor exemption rule (#4) and restaurant dual-receipt note (#5) to 10_accounting_rules.md.
- Add more detail to the CRA filings descriptions in 00_overview.md (#6).
- Consider adding a "reporting granularity" note (#7) to 00_overview.md or 30_ai_instructions.md.

Which of these would you like me to address?
```

2. I changed it to "Only 50% deductible (excluding GST/HST, including all other taxes and tip)". Is it clear? "Only 50% of GST/HST may be claimed as ITC" is fine.
3. `2_liabilities` then `3_equity` is correct. The prompt is wrong, but it is historical.
4. Add to `10_accounting_rules.md`.
5. Add to one or more of the `.augment/rules` documents.
6. Add more detail descriptpions to `00_overview.md`.
7. What do you think should be added and where?
8. The important part is "Keep track of capital assets and their depreciation"—perhaps another table `FY????/normalized/capital_assets.csv` is required?
9. Yes, expand this.

---

# Junie | Claude Opus 4.6

## [2026-02-10 12:17 PST]

You wrote:

```
For item #8 (capital assets tracking), I have two questions:

1. Should I add a capital_assets.csv schema section to 20_data_schema.md as a fourth normalized table? This would track capital assets and their depreciation with columns like asset_id, description, acquisition_date, cost, cca_class, opening_ucc, additions, disposals, cca_claimed, closing_ucc, etc.
2. Should I add a standing instruction in 30_ai_instructions.md to track capital assets using FY2024/financials/2024_Capital_Assets.md as a starting point?

Or would you prefer a simpler approach?
```

1. Yes, please add a `capital_assets.csv` schema section to `20_data_schema.md` as a fourth normalized table with the columns you specified, etc.
2. Yes, please add a standing instruction in `30_ai_instructions.md` to track capital assets; however, the instruction to use `FY2024/financials/2024_Capital_Assets.md` as a starting point should be in `.ignore/FY2025_planned_prompts.md`.
3. Please review `.ignore/FY2025_planned_prompts.md` in consideration of `.ignore/prompts.md` and the `.augment/rules` files—same as before:
    - Please identify any discrepancies and make any necessary obvious changes.
    - For anything that is not obvious, please ask me for clarification.
    - Please also make a list of omissions from the original instructions and any suggestions for improvement.

---

# Junie | Claude Opus 4.6

## [2026-02-10 12:27 PST]

You wrote:

```
5. Prompt F output columns: The planned prompt lists asset_id, description, acquisition date, cost, currency, vendor, supporting document references, suggested CCA class. The new capital_assets.csv schema in 20_data_schema.md has additional columns (cad_cost, opening_ucc, additions, disposals, cca_claimed, closing_ucc, linked_transaction_id, linked_document_ids, notes). Should I update Prompt F to align with the full schema, or is the prompt intentionally lighter (asking the AI to populate what it can)?
6. Missing: $2,000/month personal expense allocation rule: The original instructions (prompts.md line 31) mention "$2,000 per month covers the cost of running the corporation (rent, utilities, etc.)". This isn't referenced in any planned prompt or rules file. Should it be added somewhere (e.g., 10_accounting_rules.md under Owner Compensation, or in Prompt B/H)?
7. Missing: Prompt for documents.csv population: The planned prompts cover transactions, allocations, capital assets, and GST — but there's no explicit prompt for populating documents.csv (the evidence/audit layer). Should there be one, or is it assumed to be populated as part of Prompt A (reconciliation)?
```

5. Please update Prompt F to align with the full schema in `20_data_schema.md`.
6. Please add the monthly personal expense allocation rule to `10_accounting_rules.md` under Owner Compensation, but note that the amount may be different for each fiscal year. It can also be noted that starting 2024-05-01 and throughout the rest of FY2024 and FY2025, the amount is $2,000 per month. In Prompt B/H, the specific amount (or amounts if there is a mid-year change) for the fiscal year should be explicitly stated.   
7. Please add the instruction to Prompt A.

Also:

- Add a "Prompt 0" (preamble) that instructs the AI to first populate the four normalized CSV files before running the analysis prompts.
- Prompt H (accountant summary) should reference `capital_assets.csv` explicitly now that it exists as a formal table.

---

# Junie | Claude Opus 4.6

## [2026-02-10 12:30 PST]

When using Augement Code CLI (Auggie), do I need to explictly tell the AI tool to read the files under `.augment/rules`?

---

No, you do **not** need to explicitly tell Augment Code CLI (Auggie) to read the files under `.augment/rules`. That directory is a **convention recognized by Augment Code** — files placed in `.augment/rules/` are automatically loaded as context/instructions for the AI agent at the start of each session.

This is why the files have the frontmatter:

```yaml
---
agent_requested: true
description: "..."
---
```

The `agent_requested: true` flag and the `.augment/rules/` path together signal to Augment Code that these are standing instructions to be ingested automatically. You can simply start a conversation with Auggie and it will already have the context from all the rules files.

---

# Aggie | GPT-5.2

## [2026-02-10 18:05 PST]

1. There needs to be an instruction/guideline—probably in `.augment/rules/30_ai_instructions.md`—to ensure that line separations in CSV files use `LF` instead of `CRLF`. 
2. I need one or more new CSV flat-file database tables/files for accounts payables and accounts receivables—preferrably one file, such as `FY2025/normalized/owed.csv`. For example, if there is an invoice that is paid in installments, then the amount of that invoice would not appear in a chequing account or credit card statement, but the installment payment amount(s) would appear instead. If there are any remaining payables or receivables at the end of the fiscal year, they would have to be carried over to the next fiscal year. Please update the following to reflect this:
    - the appropriate file(s) under `.augment/rules`
    - `.ignore/FY2025_planned_prompts.md`

---

● Done: LF-only CSV line endings + new owed.csv (A/P & A/R) table

1) LF (not CRLF) CSV guideline
   Updated `.augment/rules/30_ai_instructions.md` with a “CSV File Hygiene (IMPORTANT)” section requiring:
   • CSV line endings must be LF (`\n`)
   • generators should explicitly set the CSV writer line terminator to \n
2) New normalized table for A/P & A/R: owed.csv
   Updated `.augment/rules/20_data_schema.md` to introduce `owed.csv` for:
   • invoices/contracts that don’t match 1:1 with any single statement transaction (e.g., installments)
   • tracking settlement via linked transaction ids
   • year-end carry-forward of any open/partial/etc. items to the next fiscal year
   Generator now produces `FY2025/normalized/owed.csv` with the schema header (currently header-only / 0 rows).
3) Planned prompts updated
   Updated `.ignore/FY2025_planned_prompts.md` to:
   • refer to five normalized CSVs (adds owed.csv)
   • include an explicit LF line ending requirement
   • instruct that “invoice exists but no single statement line matches total” should be treated as installment / A/P / A/R and represented in owed.csv
4) Generator updated + verified outputs
   Updated `scripts/populate_fy2025_normalized.py` to:
   • enforce LF line endings via csv.DictWriter(..., lineterminator="\n")
   • write FY2025/normalized/owed.csv using OWED_COLUMNS

I re-ran the generator and verified line endings; all normalized CSVs have CRLF=0 and CR=0 (LF-only). owed.csv header is present:
owed_id,fiscal_year,owed_type,...,status,notes

---

# Aggie | GPT-5.2

## [2026-02-10 18:18 PST]

1. All tables/files have been cleared because we need to start again from the top, which I will prompt later.
2. Do we need to add instructions somewhere to ensure that all statements (corporate and personal) are checked first before assuming that an invoice has not been paid in full by the end of the fiscal year and as a result, added to the `FY2025/normalized/owed.csv` table/file.

● 1) Re: “tables/files have been cleared”
Understood. I won’t regenerate or repopulate any normalized outputs until you prompt to start again. The changes below are instructions-only updates.
2) Yes — we should add that instruction (and I just did)
   To prevent false “unpaid at year-end” entries, I added an explicit rule: only create an `owed.csv` row after confirming statement coverage is complete for the fiscal year.
   Where this guidance now lives
   • `.augment/rules/30_ai_instructions.md`
   • In the Accounts Payable / Receivable (A/P & A/R) section:
   • requires checking all relevant statements/sources (corporate chequing, corporate credit cards, any relevant personal statements for reimbursements/mixed-use, PayPal/other in-scope sources)
   • if coverage might be incomplete: do not conclude unpaid → use status=unknown + clear owner follow-up note instead
   • `.augment/rules/20_data_schema.md`
   • In owed.csv Key Principles:
   • reinforces the same “statement coverage complete first” requirement; otherwise status=unknown
   • `.ignore/FY2025_planned_prompts.md`
   • In Prompt A (Reconcile...):
   • changed the instruction so the “no single statement line matches invoice total → likely installment/A/P/A/R → add to owed.csv” only happens after confirming statement ingestion/coverage
   Quick clarification question (so the rule matches your process)
   When you say “all statements (corporate and personal)”, do you want “personal” to mean:
   • only personal statements that might contain reimbursable/mixed-use items, or
   • all personal statements in FY2025/reference/personal must be fully scanned before any owed.csv entry is allowed?
   I can tighten the wording accordingly if you tell me which you prefer.

---

# Aggie | GPT-5.2

## [2026-02-10 18:21 PST]

If, and only if, a partial or installment payment has not already been made according to a corporate statement, all personal statements in `FY2025/reference/personal` must be fully scanned before any `owed.csv` entry is allowed.

---

● Updated: “scan all personal statements first” gating rule for owed.csv

I incorporated your stricter rule into the repo guidance:
What the rule now says (in effect)
• Always check corporate statements first (chequing + corporate credit card).
• If (and only if) there is no partial/installment payment visible on any corporate statement, then all personal statements under `FY2025/reference/personal` must be fully scanned before any `owed.csv` entry is allowed.
• If statement coverage might still be incomplete, do not mark something as unpaid; record it as `status = unknown` with a follow-up note instead.
Where I made the updates
• `.augment/rules/30_ai_instructions.md`
Updated the A/P & A/R section to encode the conditional “full personal scan” requirement.
• `.augment/rules/20_data_schema.md`
Added a owed.csv key principle that repeats the same gating condition.
• `.ignore/FY2025_planned_prompts.md`
Prompt A now explicitly instructs: corporate first, and only if no corporate partial payment exists, then scan all personal statements before creating owed rows.
Next step (whenever you prompt to restart)
Since you cleared all tables and will prompt later, I won’t regenerate anything now. When you’re ready to restart, tell me whether you want the workflow to include an explicit “statement coverage checklist” artifact (e.g., a
small markdown checklist per FY) so it’s auditable that coverage was complete before owed.csv gets populated.

---

# Note to self

## [2026-01-10 20:35 PST]

Corporate credit card statements are now in CSV format instead of Markdown. 
