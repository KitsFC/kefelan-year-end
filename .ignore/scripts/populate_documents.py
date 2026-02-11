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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXN_DIR = os.path.join(ROOT, "FY2025", "transactions")
OUT_CSV = os.path.join(ROOT, "FY2025", "normalized", "documents.csv")

HEADER = [
    "document_id",
    "document_type",
    "document_date",
    "vendor",
    "amount",
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


def _infer_amount_currency(text: str) -> tuple[str, str, str]:
    # Returns (amount, currency, note)
    currency_hint = None
    if re.search(r"\bAll amounts in USD\b", text, re.IGNORECASE):
        currency_hint = "USD"
    elif re.search(r"\bAll amounts in CAD\b", text, re.IGNORECASE):
        currency_hint = "CAD"

    patterns = [
        (r"Payable Total:\s*</strong>\s*</td>\s*<td[^>]*>\s*<strong>\$([0-9][0-9,]*\.[0-9]{2})", "CAD", "payable_total"),
        (r"Total payable[^$]*\$([0-9][0-9,]*\.[0-9]{2})", "CAD", "total_payable"),
        (r"Total in CAD[^\d]*\s*\*\*CA\$([0-9][0-9,]*\.[0-9]{2})\*\*", "CAD", "total_in_cad"),
        (r"\bTotal\b[^\n\r]*\*\*\$([0-9][0-9,]*\.[0-9]{2})\s*USD", "USD", "total_usd"),
        (r"\bTotal\b[^\n\r]*\bCA\s*\$([0-9][0-9,]*\.[0-9]{2})", "CAD", "total_ca"),
        (r"\bAmount:\s*\$([0-9][0-9,]*\.[0-9]{2})\b", "CAD", "amount"),
    ]

    for pat, ccy, note in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            return (_norm_money(m.group(1)), ccy, note)

    # Fallback: any $x.xx USD
    m = re.search(r"\$([0-9][0-9,]*\.[0-9]{2})\s*USD\b", text)
    if m:
        return (_norm_money(m.group(1)), "USD", "fallback_usd")

    # Fallback: first $x.xx assumes CAD
    m = re.search(r"\$([0-9][0-9,]*\.[0-9]{2})\b", text)
    if m:
        ccy = currency_hint or "CAD"
        note = "fallback_$assumed_" + (ccy or "")
        return (_norm_money(m.group(1)), ccy, note)

    return ("", "", "amount_not_found")


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
        amount, currency, amt_note = _infer_amount_currency(text)

        notes = []
        if amt_note and amt_note not in {"", "amount_not_found"}:
            notes.append(f"amount_parse={amt_note}")
        if amt_note == "amount_not_found":
            notes.append("amount_missing")
        if not vendor:
            notes.append("vendor_missing")
        if not date:
            notes.append("date_missing")
        if amt_note.startswith("fallback_$assumed_") and currency:
            notes.append(f"currency_assumed_{currency}")
        if not currency:
            notes.append("currency_missing")

        # original_format: default unknown -> md
        original_format = "md"

        rows.append([
            doc_id,
            doc_type,
            date or "",
            vendor,
            amount,
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

