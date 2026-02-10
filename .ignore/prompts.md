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
