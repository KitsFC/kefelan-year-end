---
agent_requested: true
description: "Standing classification, tax, and handling rules for KSI year-end accounting across all fiscal years."
---

# Accounting Rules and Classification Guidelines

## Corporation Details
- Legal name: Kefelan Solutions Inc. (KSI)
- Incorporated: March 18, 2025 (British Columbia)
- Fiscal year: January 1 – December 31
- GST Number: 810685594RT0001

## Owner Compensation / Shareholder Transfers
- Transfers from corporate to personal accounts are initially recorded as:
    - Loan to shareholder (temporary classification)
- Final dividend amounts are determined at year-end
- CRA shareholder loan rules apply:
    - A loan from a small business to a shareholder can only remain on the books for one year after the end of the corporation's taxation year in which the loan was made
    - If not repaid within this timeframe, the CRA considers it taxable personal income
    - The year-end split between dividend and shareholder loan is determined after analysis of the owner's personal tax liability for varying dividend amounts
- A portion of shareholder transfers is allocated to cover personal expenses incurred on behalf of the corporation (rent, utilities, etc.)
    - The monthly amount may vary by fiscal year and may change mid-year
    - Starting 2024-05-01 and throughout FY2024 and FY2025: $2,000 per month
    - The specific amount(s) for each fiscal year should be stated explicitly in the FY-specific prompts

## Raw Documents and Converted Files
- Raw statements/receipts are stored outside this repository (mostly PDFs)
- PDFs were converted to DOCX (ABBYY FineReader PDF), then to Markdown (pandoc gfm)
- Chequing transactions are CSV
- Credit card statements are CSV

## Credit Cards
- TD Business VISA ends in 5143
- TD Business VISA via Google Wallet ends in 4527
- TD Personal VISA ends in 6493
- TD Personal VISA via Google Wallet ends in 8283
- BMO Personal Mastercard ends in 9973
- BMO Personal Mastercard via Google Wallet ends in 5056
- RBC Personal VISA ends in 5672

## PayPal
- Typically funded by TD Business VISA 5143, with possible exceptions

## Cash Transactions
- All cash transactions (any currency) are paid out of personal funds
- Cash transactions must be flagged for owner review

## Tax Rules (BC / Canada)
- GST: 5%
- If KSI's GST number is provided to a vendor, KSI may not be charged GST (the vendor saves KSI the effort since KSI could claim it as an ITC)
- PST (BC): typically 7%
    - Accommodation: 8%
    - Liquor: 10%
- Some vendors charge combined 12% tax (PST 7% + GST 5%)
    - GST portion: tax × 5 ÷ 12 (round to nearest cent)
- Taxi fares (BC): GST included in fare, no PST
    - GST = fare × 5 ÷ 105 (round to nearest cent)
- Parking: may include/add GST, no PST

## Foreign Currency
- Determine invoice currency (CAD vs USD/GBP/etc.)
- Some cases require comparing invoice amount to statement amount
- If any cash transactions are foreign currency, owner must supply exchange rate
- Online services based outside Canada may or may not comply with BC/Canadian tax laws

## Classification Defaults (CRA)
- Office expenses – 8810 (Recurring SaaS defaults here)
- Advertising and promotion – 8520 (tickets for live events; gifts)
- Meals and entertainment – 8523
    - Record full amount
    - Only 50% deductible (excluding GST/HST, including all other taxes and tip)
    - Only 50% of GST/HST may be claimed as ITC
    - Most restaurant transactions have two documents/receipts: one for the food and beverage and the other for the credit card transaction (which includes the tip)
- Travel expenses – 9200 (gas, taxi, Uber, Air Canada, Expedia)
- Rental – 8910 (parking; Guardian Storage)
- Telephone and utilities – 9220 (Rogers)
- Business fees and licences – 8760 (BC Registry Service)

## Vendor-specific Notes
- Rogers: Payment of $297.22 on January 2025 credit card statement is for the 2024-12-24 bill
- Google: invoices typically end-of-month, payment first of next month
- DigitalOcean:
    - “Date of issue” is not the invoice date; use month-end payment date
    - Known PayPal transactions:
        - June 27, 2025 | PayPal Transaction | -$5.00
        - August 01, 2025 | PayPal Transaction | -$10.41
    - Related invoices:
        - July 01, 2025 | Invoice for June 2025 | $0.62
        - August 01, 2025 | Invoice for July 2025 | $14.79
