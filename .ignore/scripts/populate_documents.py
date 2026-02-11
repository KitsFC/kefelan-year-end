#!/usr/bin/env python3
"""Populate FY2025/normalized/documents.csv from FY2025/transactions/**/*.md.

Heuristic parser (best-effort). Leaves blanks + notes when uncertain.
Writes LF line endings.
"""

from __future__ import annotations

import csv
import hashlib
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[2])
TXN_DIR = os.path.join(ROOT, "FY2025", "transactions")
OUT_CSV = os.path.join(ROOT, "FY2025", "normalized", "documents.csv")

HEADER = [
    "document_id",
    "document_type",
    "document_date",
    "vendor",
    "total_amount",
    "gst_amount",
    "net_amount",
    "pre-tip_amount",
    "currency",
    "source_file",
    "original_format",
    "notes",
]

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def _norm_money(s: str) -> str:
    s = s.strip().replace(",", "")
    s = re.sub(r"[^0-9.\-]", "", s)
    return s


def _as_2dp(x: float | None) -> str:
    if x is None:
        return ""
    return f"{x:.2f}"


def _try_float(s: str) -> float | None:
    try:
        return float(_norm_money(s))
    except Exception:
        return None


def _strip_html(text: str) -> str:
    # Best-effort for OCR'd HTML-ish receipts.
    t = re.sub(r"<[^>]+>", " ", text)
    t = t.replace("&nbsp;", " ")
    return re.sub(r"[ \t]+", " ", t)


def _clean_vendor_line(ln: str) -> str:
    ln = ln.strip()
    # Remove common markdown escapes/artifacts from OCR.
    ln = ln.replace("\\", "")
    ln = re.sub(r"[\*`_]+", "", ln)
    ln = re.sub(r"\s+", " ", ln)
    return ln.strip(" -:\t")


def _parse_date(text: str) -> str | None:
    # Prefer ISO yyyy-mm-dd
    m = re.search(r"\b(20[0-9]{2})-([01][0-9])-([0-3][0-9])\b", text)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    # e.g. 02 January 2025
    m = re.search(r"\b([0-3]?[0-9])\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20[0-9]{2})\b",
                  text,
                  re.IGNORECASE)
    if m:
        day = int(m.group(1))
        month = MONTHS[m.group(2)[:3].lower()]
        year = int(m.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    # e.g. Jan 15, 2025
    m = re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+([0-3]?[0-9]),\s*(20[0-9]{2})\b",
                  text,
                  re.IGNORECASE)
    if m:
        month = MONTHS[m.group(1).lower()]
        day = int(m.group(2))
        year = int(m.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    # e.g. 1/15/25 or 01/15/2025
    m = re.search(r"\b([01]?[0-9])/([0-3]?[0-9])/(\d{2,4})\b", text)
    if m:
        month = int(m.group(1))
        day = int(m.group(2))
        year = int(m.group(3))
        year = (2000 + year) if year < 100 else year
        return f"{year:04d}-{month:02d}-{day:02d}"

    return None


def _infer_doc_type(path_base: str, text: str) -> str:
    t = text.lower()
    b = path_base.lower()
    if b.startswith("kefelan_invoice_"):
        return "invoice"
    if "confirmation" in t or "completed successfully" in t or b.startswith("tdct_"):
        return "confirmation"

    # Filename is more reliable than content (invoices may include the phrase "upon receipt")
    if "receipt" in b:
        return "receipt"
    if "invoice" in b:
        return "invoice"

    # Content heuristics
    if re.search(r"^\*\*receipt\*\*$", text, re.IGNORECASE | re.MULTILINE) or re.search(
        r"\breceipt number\b", t
    ):
        return "receipt"
    if re.search(r"\binvoice number\b", t) or re.search(r"\bpayable total\b", t):
        return "invoice"
    return "other"


def _infer_vendor(path_base: str, text: str) -> str:
    # Scanned receipts: vendor is often in the first few lines.
    if path_base.startswith("KSI_FY2025_Scanned_Receipt_"):
        first_lines = [_clean_vendor_line(ln) for ln in text.splitlines()[:40]]
        first_lines = [ln for ln in first_lines if ln]

        # Prefer bolded vendor lines, skipping generic headers.
        for ln in first_lines:
            m = re.fullmatch(r"\*\*([^*]+)\*\*", ln)
            if not m:
                continue
            cand = m.group(1).strip()
            if cand.upper() in {"TRANSACTION RECORD", "RECEIPT", "INVOICE"}:
                continue
            return cand

        # Fallback: first non-generic text line; sometimes second line is the venue.
        non_generic = [
            ln for ln in first_lines
            if ln.upper() not in {"TRANSACTION RECORD", "RECEIPT", "INVOICE"}
            and not re.search(r"\bGST\b|\bHST\b|\bPST\b", ln, re.IGNORECASE)
            and re.search(r"[A-Za-z]", ln)
            and not re.fullmatch(r"[0-9Xx\*#:\-\s\.]+", ln)
        ]
        if non_generic:
            if len(non_generic) >= 2 and re.search(r"\bhotel\b", non_generic[0], re.IGNORECASE):
                return non_generic[1]
            return non_generic[0]

    # Strong content-based cues
    m = re.search(r"Sold by\s*/\s*Vendu par:\s*([^\n>]+)", text, re.IGNORECASE)
    if m:
        v = m.group(1).strip()
        return re.sub(r"^[*\s]+|[*\s]+$", "", v)
    m = re.search(r"\*\*(Google LLC|GitHub|Amazon\.com\.ca ULC|TD Canada Trust|Expedia)\*\*", text)
    if m:
        return m.group(1).strip()
    if path_base.startswith("Kefelan_Invoice_"):
        return "Kefelan Solutions Inc."

    # Filename-based fallback (best-effort)
    # Take leading tokens before the first date-like segment.
    parts = path_base.split("_")
    lead: list[str] = []
    for p in parts:
        if re.fullmatch(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}", p) or re.fullmatch(r"20[0-9]{6}", p):
            break
        lead.append(p)
    vendor = " ".join(lead).strip() or ""
    vendor = vendor.replace("  ", " ")
    return vendor


def _currency_hint(text: str) -> str | None:
    if re.search(r"\bAll amounts in USD\b", text, re.IGNORECASE):
        return "USD"
    if re.search(r"\bAll amounts in CAD\b", text, re.IGNORECASE):
        return "CAD"
    if re.search(r"\bUSD\b", text):
        return "USD"
    if re.search(r"\bCAD\b|\bCADS\b", text):
        return "CAD"
    return None


def _infer_amounts(text: str, path_base: str) -> tuple[str, str, str, str, str, list[str]]:
    """Return (total, gst, net, pre-tip, currency, notes)."""

    notes: list[str] = []
    ccy = _currency_hint(text) or ""

    total: float | None = None
    gst: float | None = None
    tip: float | None = None
    pre_tip_from_amount_line: float | None = None

    # --- JetBrains invoices
    m = re.search(r"\|\s*\*\*Total\*\*\s*\|\s*\*\*([0-9][0-9,]*\.[0-9]{2})\s*(USD|CAD)\*\*",
                  text, re.IGNORECASE)
    if m:
        total = _try_float(m.group(1))
        ccy = m.group(2).upper()
        notes.append("total_parse=jetbrains_total")
        m2 = re.search(r"\|\s*GST/HST\s*5\s*%\s*\|\s*([0-9][0-9,]*\.[0-9]{2})\s*(USD|CAD)", text, re.IGNORECASE)
        if m2:
            gst = _try_float(m2.group(1))
            notes.append("gst_parse=jetbrains_gst")

    # --- Microsoft invoices
    if total is None:
        # Newer Microsoft HTML invoices sometimes show "Total Amount" in the header table.
        m = re.search(
            r"Total Amount</strong></td>\s*<td[^>]*>\s*<strong>\s*(CAD|USD)\s*([0-9][0-9,]*\.[0-9]{2})\s*</strong>",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if m:
            ccy = m.group(1).upper()
            total = _try_float(m.group(2))
            notes.append("total_parse=microsoft_total_amount_header")

    if total is None:
        m = re.search(r"Total\s*\(including\s*Tax\)[^0-9A-Z]*(CAD|USD)\s*([0-9][0-9,]*\.[0-9]{2})",
                      text, re.IGNORECASE | re.DOTALL)
        if m:
            ccy = m.group(1).upper()
            total = _try_float(m.group(2))
            notes.append("total_parse=microsoft_total_including_tax")
    if gst is None:
        m = re.search(r"GST/HST\s*\(\s*5\.00%\s*\)\s*\n\s*([0-9][0-9,]*\.[0-9]{2})",
                      text, re.IGNORECASE)
        if m:
            gst = _try_float(m.group(1))
            notes.append("gst_parse=microsoft_gst_block")
        else:
            m = re.search(r"GST/HST\s*5\.00%\s*([0-9][0-9,]*\.[0-9]{2})", text, re.IGNORECASE)
            if m:
                gst = _try_float(m.group(1))
                notes.append("gst_parse=microsoft_gst_inline")

    # --- ConnectWise / ScreenConnect receipts
    if total is None:
        m = re.search(r"<strong>Total:</strong>\s*</td>\s*<td[^>]*>\s*C\$([0-9][0-9,]*\.[0-9]{2})",
                      text, re.IGNORECASE | re.DOTALL)
        if m:
            total = _try_float(m.group(1))
            ccy = ccy or "CAD"
            notes.append("total_parse=connectwise_total")
    if total is None:
        # Variant where Total label is wrapped in <blockquote>/<p> and amount is in the next <td>.
        m = re.search(r"<strong>Total:</strong>[\s\S]{0,250}?C\$\s*([0-9][0-9,]*\.[0-9]{2})\b",
                      text, re.IGNORECASE)
        if m:
            total = _try_float(m.group(1))
            ccy = ccy or "CAD"
            notes.append("total_parse=connectwise_total_variant")
    if gst is None:
        m = re.search(r"<strong>Tax:</strong>\s*</td>\s*<td[^>]*>\s*C\$([0-9][0-9,]*\.[0-9]{2})",
                      text, re.IGNORECASE | re.DOTALL)
        if m:
            gst = _try_float(m.group(1))
            notes.append("gst_parse=connectwise_tax")

    # --- TD Canada Trust confirmations (transfers)
    if total is None:
        m = re.search(r"\bAmount:\s*\|\s*\$([0-9][0-9,]*\.[0-9]{2})\b", text, re.IGNORECASE)
        if m:
            total = _try_float(m.group(1))
            ccy = ccy or "CAD"
            notes.append("total_parse=tdct_amount")
    if total is None:
        m = re.search(r"\bAmount:\s*\$\s*([0-9][0-9,]*\.[0-9]{2})\b", text, re.IGNORECASE)
        if m:
            total = _try_float(m.group(1))
            ccy = ccy or "CAD"
            notes.append("total_parse=tdct_amount_simple")

    # --- Generic receipt totals
    if total is None:
        # Often on a single line
        m = re.search(r"\bTotal\s+Due\s*\$?\s*([0-9][0-9,]*\.[0-9]{2})\b", text, re.IGNORECASE)
        if m:
            total = _try_float(m.group(1))
            ccy = ccy or "CAD"
            notes.append("total_parse=total_due")

    # Some OCR receipts have Total on one line and the amount on the next (often escaped as \$ in markdown).
    if total is None:
        m = re.search(r"\bTotal\b[\s\S]{0,40}\\?\$\s*([0-9][0-9,]*\.[0-9]{2})\b", text, re.IGNORECASE)
        if m:
            total = _try_float(m.group(1))
            ccy = ccy or "CAD"
            notes.append("total_parse=total_next_line")

    # Transaction-record style receipts (Amount + TOTAL CAD...)
    m_amt = re.search(r"\bAmount\s*\\?\$\s*([0-9][0-9,]*\.[0-9]{2})\b", text, re.IGNORECASE)
    if m_amt:
        pre_tip_from_amount_line = _try_float(m_amt.group(1))
        if pre_tip_from_amount_line is not None:
            notes.append("pre_tip_parse=amount_line")

    if total is None:
        m_tot = re.search(r"\bTOTAL\b[^0-9\n\r]{0,20}(?:CAD|CADS|USD|USDS)?\s*\$?\s*([0-9][0-9,]*\.[0-9]{2})\b",
                          text, re.IGNORECASE)
        if m_tot:
            total = _try_float(m_tot.group(1))
            ccy = ccy or ("USD" if re.search(r"\bUSD\b", m_tot.group(0), re.IGNORECASE) else "CAD")
            notes.append("total_parse=transaction_record_total")

    # --- OCR HTML receipts with split decimals (e.g., Amount Due 672 / .77)
    if total is None:
        plain = _strip_html(text)
        m = re.search(r"\bAmount\s+Due\s+([0-9]{1,6})\s*\.?\s*([0-9]{2})\b", plain, re.IGNORECASE)
        if m:
            try:
                total = float(f"{int(m.group(1))}.{m.group(2)}")
            except Exception:
                total = None
            if total is not None:
                ccy = ccy or "CAD"
                notes.append("total_parse=amount_due_split")

    # --- GST from HTML table rows: GST ... </td> <td> 31.59
    if gst is None:
        m = re.search(r"\bGST\b[^<]{0,80}</td>\s*<td[^>]*>\s*([0-9][0-9,]*\.[0-9]{2})\b",
                      text, re.IGNORECASE | re.DOTALL)
        if m:
            gst = _try_float(m.group(1))
            notes.append("gst_parse=html_table_gst")

    # --- Tip/gratuity (often unreliable in OCR; we sanity-check later)
    m = re.search(r"\b(?:Tip|Gratuity)\b[^0-9\n\r]*\$?\s*([0-9][0-9,]*\.[0-9]{2})\b", text, re.IGNORECASE)
    if m:
        tip = _try_float(m.group(1))
        if tip is not None:
            notes.append("tip_parse=explicit")

    # Fallback: $x.xx USD
    if total is None:
        m = re.search(r"\$\s*([0-9][0-9,]*\.[0-9]{2})\s*USD\b", text)
        if m:
            total = _try_float(m.group(1))
            ccy = "USD"
            notes.append("total_parse=fallback_usd")

    # Fallback: first $x.xx (assume currency)
    if total is None:
        m = re.search(r"\$\s*([0-9][0-9,]*\.[0-9]{2})\b", text)
        if m:
            total = _try_float(m.group(1))
            ccy = ccy or "CAD"
            notes.append("total_parse=fallback_$assumed")
            notes.append(f"currency_assumed_{ccy}")

    total_s = _as_2dp(total)
    gst_s = _as_2dp(gst)
    net_s = _as_2dp((total - gst) if (total is not None and gst is not None) else None)

    pre_tip_s = ""
    # Best: if we have a reliable pre-tip amount line and a total.
    if pre_tip_from_amount_line is not None and total is not None and total >= pre_tip_from_amount_line:
        pre_tip_s = _as_2dp(pre_tip_from_amount_line)
    elif total is not None and tip is not None:
        # Sanity-check tip because OCR often misreads decimals (e.g., 14.50 -> 514.50)
        if 0 <= tip <= total and tip <= 0.5 * total:
            pre_tip_s = _as_2dp(total - tip)
            notes.append("pre_tip_calc=total_minus_tip")
        else:
            notes.append("tip_ignored_unreasonable")

    if not total_s:
        notes.append("total_missing")
    if not ccy:
        notes.append("currency_missing")

    return (total_s, gst_s, net_s, pre_tip_s, ccy, notes)


def main() -> int:
    md_files: list[str] = []
    for dirpath, _, filenames in os.walk(TXN_DIR):
        for fn in filenames:
            if fn.lower().endswith(".md"):
                md_files.append(os.path.join(dirpath, fn))

    md_files.sort()

    # Ensure unique ids
    used: set[str] = set()

    rows: list[list[str]] = []
    for abspath in md_files:
        rel = os.path.relpath(abspath, ROOT)
        base = os.path.splitext(os.path.basename(rel))[0]

        with open(abspath, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()

        doc_id = base
        if doc_id in used:
            suffix = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:8]
            doc_id = f"{base}__{suffix}"
        used.add(doc_id)

        doc_type = _infer_doc_type(base, text)

        # Date: filename first, then content
        date = None
        m = re.search(r"(20[0-9]{2}-[0-9]{2}-[0-9]{2})", base)
        if m:
            date = m.group(1)
        if not date:
            m = re.search(r"\b(20[0-9]{2})([01][0-9])([0-3][0-9])\b", base)
            if m:
                date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        if not date:
            date = _parse_date(text)

        vendor = _infer_vendor(base, text)
        total_amount, gst_amount, net_amount, pre_tip_amount, currency, amt_notes = _infer_amounts(text, base)

        notes = []
        notes.extend(amt_notes)
        if not vendor:
            notes.append("vendor_missing")
        if not date:
            notes.append("date_missing")

        # original_format: default unknown -> md
        original_format = "md"

        rows.append([
            doc_id,
            doc_type,
            date or "",
            vendor,
            total_amount,
            gst_amount,
            net_amount,
            pre_tip_amount,
            currency,
            rel,
            original_format,
            ";".join(notes),
        ])

    # Sort: by date then id (stable)
    def sort_key(r: list[str]):
        try:
            d = datetime.strptime(r[2], "%Y-%m-%d") if r[2] else datetime.max
        except ValueError:
            d = datetime.max
        return (d, r[0])

    rows.sort(key=sort_key)

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(rows)

    print(f"Wrote {len(rows)} documents -> {os.path.relpath(OUT_CSV, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

