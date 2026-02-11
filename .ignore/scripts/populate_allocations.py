#!/usr/bin/env python3
"""Populate FY2025/normalized/allocations.csv from normalized transactions.

Goal: best-effort, *suggested* CRA/category/tax treatment defaults.
- Uses FY2024/financials/2024_Transaction_Allocations.csv as a loose vendor->category hint.
- Uses .augment/rules/10_accounting_rules.md defaults (e.g., meals 50%).
- Tries to extract GST/PST from linked evidence Markdown; otherwise leaves as 0 and notes.
- Writes LF line endings.
"""

from __future__ import annotations

import csv
import os
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[2])
TXN_CSV = os.path.join(ROOT, "FY2025", "normalized", "transactions.csv")
DOC_CSV = os.path.join(ROOT, "FY2025", "normalized", "documents.csv")
FY2024_ALLOC = os.path.join(ROOT, "FY2024", "financials", "2024_Transaction_Allocations.csv")
OUT_CSV = os.path.join(ROOT, "FY2025", "normalized", "allocations.csv")

HEADER = [
    "allocation_id",
    "transaction_id",
    "allocation_type",
    "applies_to",
    "allocated_amount",
    "allocated_gst",
    "allocated_pst",
    "reporting_category",
    "cra_code",
    "deductible_percentage",
    "deductible_amount",
    "itc_eligible_amount",
    "tax_treatment",
    "notes",
]

STOPWORDS = {
    "inc",
    "llc",
    "ltd",
    "ulc",
    "co",
    "company",
    "the",
    "and",
    "paypal",
    "pp",
    "ca",
    "com",
    "net",
    # statement noise / transfer tokens (avoid polluting vendor hint matching)
    "tfr",
    "to",
    "fr",
    "from",
    "send",
    "transfer",
    "etrf",
    "e",
    "mobile",
    "deposit",
}


def _tokens(s: str) -> set[str]:
    s = re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
    out: set[str] = set()
    for t in s.split():
        if not t or t in STOPWORDS:
            continue
        if len(t) < 2:
            continue
        if t.isdigit():
            continue
        # TD transfer reference tokens like HW293 / JJ005
        if re.match(r"^[a-z]{2}[0-9]{3}$", t):
            continue
        out.add(t)
    return out


def _f2(x: float) -> str:
    return f"{x:.2f}"


def _parse_lookup(lookup: str) -> tuple[str, str]:
    # examples:
    #  "56950 | [8810] Office expenses"
    #  "40200 | Category A Revenue"
    m = re.search(r"\[(\d{4})\]\s*(.+)$", lookup or "")
    if m:
        return (m.group(2).strip(), m.group(1))
    if lookup and "|" in lookup:
        return (lookup.split("|", 1)[1].strip(), "")
    return ("", "")


def _load_vendor_hints() -> dict[str, tuple[str, str]]:
    if not os.path.exists(FY2024_ALLOC):
        return {}
    by_vendor: dict[str, Counter] = {}
    with open(FY2024_ALLOC, "r", encoding="utf-8", newline="") as f:
        dr = csv.DictReader(f)
        for r in dr:
            vendor = (r.get("Description") or "").strip()
            lookup = (r.get("Lookup") or "").strip()
            if not vendor or not lookup:
                continue
            cat, cra = _parse_lookup(lookup)
            if not cat:
                continue
            by_vendor.setdefault(vendor, Counter())[(cat, cra)] += 1
    out: dict[str, tuple[str, str]] = {}
    for v, c in by_vendor.items():
        out[v] = c.most_common(1)[0][0]
    return out


@lru_cache(maxsize=2048)
def _extract_tax_from_md(rel_path: str) -> tuple[float, float, str]:
    # returns (gst, pst, note) as positive magnitudes
    p = os.path.join(ROOT, rel_path)
    try:
        text = open(p, "r", encoding="utf-8", errors="ignore").read()
    except Exception:
        return (0.0, 0.0, "tax_md_unreadable")

    def grab(label: str) -> float:
        m = re.search(rf"\b{label}\b[^0-9]*([0-9]+\.[0-9]{{2}})", text, flags=re.IGNORECASE)
        return float(m.group(1)) if m else 0.0

    gst = grab("GST") or grab("HST")
    pst = grab("PST")
    if gst or pst:
        return (gst, pst, "tax_from_doc")
    return (0.0, 0.0, "tax_not_found_in_doc")


def _suggest(txn: dict, vendor_hints: dict[str, tuple[str, str]], invoice_docs_by_amt: dict[str, list[dict]]) -> tuple[str, str, int, str, str]:
    """Return (reporting_category, cra_code, deductible_pct, tax_treatment, notes)."""
    cp = txn.get("counterparty", "")
    desc = txn.get("description", "")
    amt = float(txn.get("cad_amount") or txn.get("amount") or 0.0)
    text = (cp + " " + desc).lower()

    # Transfers / balance-sheet style items
    if txn.get("receipt_status") == "not_applicable" and re.search(r"\bgst-[pb]\b", text):
        return ("GST/HST remittance", "", 0, "non_deductible", "gst_remittance")
    if txn.get("receipt_status") == "not_applicable" and re.search(r"\btxins\b|\btxbal\b", text):
        return ("Tax instalment / balance adjustment", "", 0, "non_deductible", "tax_instalment_or_balance_adj")
    if txn.get("payment_method") == "credit_card" and cp.strip().lower() == "td" and txn.get("receipt_status") == "not_applicable":
        return ("Credit card payment (transfer)", "", 0, "non_deductible", "cc_payment")
    if txn.get("payment_method") == "chequing" and txn.get("receipt_status") == "not_applicable" and re.search(r"tfr-to\s+.*c/c", text):
        return ("Credit card payment (transfer)", "", 0, "non_deductible", "cc_payment")
    # Shareholder transfer heuristics (default: loan to shareholder; final dividend decision later)
    if txn.get("payment_method") == "chequing" and ("send e-tfr" in text or "tfr-to" in text or "tfr-fr" in text):
        if amt < 0 and "c/c" not in text:
            return ("Loan to shareholder (review)", "", 0, "shareholder_loan", "shareholder_transfer_out")
        if amt > 0:
            return ("Shareholder contribution/repayment (review)", "", 0, "shareholder_loan", "shareholder_transfer_in")

    # Revenue-ish deposits (best-effort)
    if txn.get("payment_method") == "chequing" and amt > 0 and ("e-transfer" in text or "mobile deposit" in text):
        key = f"{abs(amt):.2f}"
        cand = invoice_docs_by_amt.get(key, [])
        if cand:
            return ("Revenue", "", 0, "standard", "revenue_match_by_amount")
        return ("Revenue (review)", "", 0, "standard", "revenue_unlinked")

    # Meals 50%
    if re.search(r"restaurant|cafe|bistro|bar|pub|bc liquor", text):
        return ("Meals and entertainment", "8523", 50, "meals_50", "meals_default")

    # Defaults from 10_accounting_rules.md
    if re.search(r"uber", text):
        return ("Travel expenses", "9200", 100, "standard", "travel_default")
    if re.search(r"guardian storag|parking", text):
        return ("Rental", "8910", 100, "standard", "rental_default")
    if re.search(r"rogers", text):
        return ("Telephone and utilities", "9220", 100, "standard", "telco_default")
    if re.search(r"bc registry|registry service", text):
        return ("Business fees and licences", "8760", 100, "standard", "fees_default")
    if re.search(r"slack|google|github|jetbrains|dropbox|openphone|lastpass|adobe|microsoft|namespro|screenconnect|digitalocea", text):
        return ("Office expenses", "8810", 100, "standard", "saas_default")

    # FY2024 vendor hint fallback (best overlap match)
    tset = _tokens(cp) or _tokens(desc)
    best_cat = best_cra = ""
    best_score = 0
    if tset:
        for v, (cat, cra) in vendor_hints.items():
            score = len(_tokens(v) & tset)
            if score > best_score:
                best_score = score
                best_cat, best_cra = cat, cra
    if best_score > 0:
        cat, cra = best_cat, best_cra
        # normalize a couple FY2024 label variants
        if cra == "8523":
            cat = "Meals and entertainment"
        dpct = 50 if cra == "8523" else 100
        tt = "meals_50" if cra == "8523" else "standard"
        # Revenue categories are not deductible (set dpct=0 so deductible_amount stays 0)
        if ("revenue" in (cat or "").lower()) and amt > 0:
            dpct = 0
        return (cat, cra, dpct, tt, "fy2024_vendor_hint")

    return ("UNCLASSIFIED", "", 100, "standard", "needs_review")


def main() -> int:
    # documents index for invoice-by-amount (revenue hint) + id->source_file
    doc_by_id: dict[str, dict] = {}
    invoice_docs_by_amt: dict[str, list[dict]] = {}
    with open(DOC_CSV, "r", encoding="utf-8", newline="") as f:
        for d in csv.DictReader(f):
            did = d.get("document_id") or ""
            if did:
                doc_by_id[did] = d
            if (d.get("document_type") or "").lower() == "invoice" and d.get("total_amount") and (d.get("currency") == "CAD"):
                invoice_docs_by_amt.setdefault(f"{float(d['total_amount']):.2f}", []).append(d)

    vendor_hints = _load_vendor_hints()

    rows: list[list[str]] = []
    with open(TXN_CSV, "r", encoding="utf-8", newline="") as f:
        for t in csv.DictReader(f):
            txn_id = t["transaction_id"]
            applies_to = t.get("account_owner") or "corporate"
            alloc_id = f"alloc_{txn_id}_a"

            cat, cra, dpct, tt, note0 = _suggest(t, vendor_hints, invoice_docs_by_amt)
            allocated_amount = float(t.get("cad_amount") or t.get("amount") or 0.0)

            # Tax from linked evidence, if any
            gst = pst = 0.0
            tax_note = "tax_unknown_assumed0"
            doc_ids = [x for x in (t.get("linked_document_ids") or "").split("|") if x]
            if doc_ids:
                gn = pn = 0.0
                notes = []
                for did in doc_ids:
                    doc = doc_by_id.get(did) or {}
                    # only attempt GST/PST extraction for CAD evidence
                    if (doc.get("currency") or "").upper() != "CAD":
                        continue
                    rel = doc.get("source_file")
                    if rel:
                        g, p, n = _extract_tax_from_md(rel)
                        gn += g
                        pn += p
                        if n and n not in notes:
                            notes.append(n)
                if gn or pn:
                    s = -1.0 if allocated_amount < 0 else 1.0
                    gst, pst = s * gn, s * pn
                    tax_note = ";".join(notes) or "tax_from_doc"
                else:
                    tax_note = "tax_not_found_in_linked_docs"

            # Deductible amount is ex-GST/HST per schema
            allocated_gst = gst
            allocated_pst = pst
            base_ex_gst = allocated_amount - allocated_gst
            deductible_amount = base_ex_gst * (dpct / 100.0)

            itc = 0.0
            if applies_to == "corporate" and allocated_amount < 0 and allocated_gst != 0 and dpct > 0:
                itc = abs(allocated_gst) * (0.5 if tt == "meals_50" else 1.0)

            rows.append([
                alloc_id,
                txn_id,
                "full",
                applies_to,
                _f2(allocated_amount),
                _f2(allocated_gst),
                _f2(allocated_pst),
                cat,
                cra,
                str(dpct),
                _f2(deductible_amount),
                _f2(itc),
                tt,
                ";".join(x for x in [note0, tax_note] if x),
            ])

    rows.sort(key=lambda r: r[1])
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(rows)

    print(f"Wrote {len(rows)} allocations -> {os.path.relpath(OUT_CSV, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

