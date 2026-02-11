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

---

## 2026-02-11
- Date: 2026-02-11
- Issue: Scripts were moved under `.ignore/scripts/`, breaking hardcoded repo-root resolution in multiple generators.
- Resolution: Compute repo root robustly in scripts via `ROOT = str(Path(__file__).resolve().parents[2])`.
- Guidance for Future Years:
  - Avoid `os.path.dirname(os.path.dirname(__file__))` style root detection when scripts may be relocated.
  - Prefer `Path(__file__).resolve().parents[N]` with the correct `N` for your repo layout, or accept a `--root` argument.

## 2026-02-11
- Date: 2026-02-11
- Issue: `FY2025/normalized/documents.csv` schema changed: `amount` was replaced by `total_amount`, `gst_amount`, `net_amount`, and `pre-tip_amount`.
- Resolution: Updated `.augment/rules/20_data_schema.md` + regenerated `documents.csv`; updated downstream consumers to read `total_amount` (not `amount`).
- Guidance for Future Years:
  - When changing normalized schemas, immediately update *all* downstream scripts that read those CSVs (e.g., matching/indexing logic).
  - Preserve CSV LF-only output by continuing to use Python `csv.writer(..., lineterminator="\n")` and validating `\r` byte count.

## 2026-02-11
- Date: 2026-02-11
- Issue: TD Business Visa export contains both "Posting Date" and "Transaction Date"; using posting date for `txn_date` is incorrect for economic timing.
- Resolution: In `populate_transactions.py`, use Visa "Transaction Date" for `txn_date` and FY filtering (fallback to posting date only if missing/unparseable).
- Guidance for Future Years:
  - Treat credit-card "Transaction Date" as the primary economic date; posting date can differ and should not drive fiscal-year inclusion.
  - If date formats vary across exports, parse defensively (try `%Y-%m-%d` and `%m/%d/%Y`).

## 2026-02-11
- Date: 2026-02-11
- Issue: OCR/scanned receipt Markdown may escape dollar signs as `\$` and put totals on the next line.
- Resolution: Update parsing patterns to accept optional backslash before `$` and allow a small multiline window for "Total" → amount.
- Guidance for Future Years:
  - When parsing OCR receipts, normalize/strip HTML-ish artifacts first and allow for escaped currency symbols and split-decimal artifacts.
