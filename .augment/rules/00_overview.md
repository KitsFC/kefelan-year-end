---
agent_requested: true
description: "High-level overview of the KSI year-end accounting repository purpose, roles, and fiscal scope."
---

# Kefelan Solutions Inc. – Year-End Accounting Overview

This repository exists to support annual year-end accounting for Kefelan Solutions Inc. (KSI).

## Purpose
- Maintain a complete, auditable record of all corporate financial activity
- Provide classified, reconciled information to the corporation’s accountant
- Support CRA filings including T2, T4A, T5, and GST/HST returns

## Roles
- Owner (Kevin "Felix" Chan): provides complete transaction data and judgments where required
- AI tools (primarily Aggie, secondarily Junie): assist with reconciliation, classification, and summarization
- Accountant: prepares financial statements and files returns with CRA

## Accounting Authority
- CRA rules override any assumptions made in this repository
- Accountant’s interpretation takes precedence over AI output

## Fiscal Year
- January 1 to December 31

## Scope: Personal Transactions
- `FY????/reference/personal` is provided for reconciliation context only.
- Do NOT record or normalize all personal transactions.
- Only personal transactions that are wholly or partially reimbursed by KSI (i.e., those that belong in corporate records under `FY????/transactions`) should be captured in the normalized database (`transactions.csv` / `allocations.csv`).
- Personal transactions that are not reimbursed are out of scope and should not be classified or summarized.
