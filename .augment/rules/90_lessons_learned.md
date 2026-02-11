---
agent_requested: true
description: "Accumulating log of issues, resolutions, and guidelines discovered during year-end accounting for reuse in future years."
---

# Lessons Learned – Year-End Accounting

This file accumulates guidance for improving future year-end processes.

## Entry Format
- Date:
- Issue:
- Resolution:
- Guidance for Future Years:

---

(append new entries below)

## Entry
- Date: 2026-02-11
- Issue: Statement ingestion missed corporate TD Business Visa transactions when the statement source was converted PDF → DOCX → Markdown, producing HTML tables where cell content (especially blockquotes / multiple <p> lines) breaks the “one transaction per line” assumption.
- Resolution: Updated the TD Visa markdown parser to be table-aware (parse by <tr>/<td> blocks and scan per-row text), and added a non-fatal warning when rows look like transactions but fail parsing.
- Guidance for Future Years:
  - Prefer statement exports that preserve machine-readable structure (native CSV/OFX) where possible.
  - If Markdown/HTML tables must be ingested, parse at the table-row level (not line-by-line), because conversion artifacts can introduce tabs/newlines inside cells.
  - Add a coverage check (or warning) for “transaction-looking” rows that were skipped, and spot-check early/late statement periods (especially FY boundary months).

## Entry
- Date: 2026-02-11
- Issue: Some PDF → DOCX → Markdown statement conversions split a single logical card transaction across *multiple* adjacent `<tr>` rows (rowspan-like behavior): one row contains dates+amount but an empty description cell, and the next row contains the merchant/description. This led to emitted transactions with blank `description`/`counterparty` and the appearance of “missing” corporate TD Business Visa transactions.
- Resolution: Updated the table-aware parser to **stitch** the description from the next `<tr>` when the current row has valid dates+amount but blank description. If a description cannot be recovered, the row is treated as "transaction-looking" and skipped (with warning instrumentation). Recovered rows include a traceability note: `AUTO: DESC_FROM_TR=...`.
- Guidance for Future Years:
  - Do **not** emit statement transactions with blank `description` / `counterparty`; either recover (multi-row stitch) or skip-and-warn.
  - When validating statement completeness, reconcile using parser-aligned `source_locator` coverage (including both `tr=...` and `tr=...;line=...` forms), not raw `<tr>` counts.
  - Coverage checks must apply the same fiscal-year filtering and statement-period year inference as the parser; otherwise “missing/extra” results will be misleading.
