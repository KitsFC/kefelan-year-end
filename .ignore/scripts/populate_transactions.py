#!/usr/bin/env python3
"""Populate FY2025/normalized/transactions.csv from statement CSVs.

- TD Business chequing: FY2025/transactions/1_assets/TD_Business_accountactivity_*.csv
- TD Business Visa: FY2025/transactions/2_liabilities/TD_Business_Visa_accountactivity_*.csv
- TD Personal chequing (limited): FY2025/reference/personal/TD_Personal_accountactivity_*.csv

Best-effort matching to FY2025/normalized/documents.csv (linked_document_ids).
Writes LF line endings.
"""

from __future__ import annotations

import csv
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = str(Path(__file__).resolve().parents[2])
DOC_CSV = os.path.join(ROOT, "FY2025", "normalized", "documents.csv")
OUT_CSV = os.path.join(ROOT, "FY2025", "normalized", "transactions.csv")
TD_BIZ_CHQ = os.path.join(ROOT, "FY2025", "transactions", "1_assets", "TD_Business_accountactivity_20241225-20260208.csv")
TD_BIZ_VISA = os.path.join(ROOT, "FY2025", "transactions", "2_liabilities", "TD_Business_Visa_accountactivity_20241225-20260210.csv")
TD_PERSONAL_CHQ = os.path.join(ROOT, "FY2025", "reference", "personal", "TD_Personal_accountactivity_20241225-20260208.csv")

HEADER = [
    "transaction_id",
    "fiscal_year",
    "txn_date",
    "source_type",
    "source_file",
    "source_locator",
    "account_owner",
    "account_name",
    "payment_method",
    "card_last4",
    "counterparty",
    "description",
    "amount",
    "currency",
    "cad_amount",
    "fx_rate_to_cad",
    "linked_document_ids",
    "receipt_status",
    "notes",
]

STOPWORDS = {"inc", "llc", "ltd", "ulc", "co", "company", "com", "ca", "net", "the", "and", "paypal", "pp"}


def _in_fy2025(iso_date: str) -> bool:
    # Fiscal year per .augment/rules/10_accounting_rules.md: Jan 1 – Dec 31
    return (iso_date or "").startswith("2025-")


def _num(s: str) -> float:
    return float(s.replace(",", "").strip())


def _date_mmddyyyy(s: str) -> str:
    return datetime.strptime(s.strip(), "%m/%d/%Y").date().isoformat()


def _date_yyyy_mm_dd(s: str) -> str:
    return datetime.strptime(s.strip(), "%Y-%m-%d").date().isoformat()


def _date_any(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except Exception:
            pass
    return ""


def _tokens(s: str) -> set[str]:
    s = (s or "").lower()
    s = s.replace("*", " ").replace("#", " ").replace("/", " ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    toks = {t for t in s.split() if len(t) > 2 and t not in STOPWORDS}
    return toks


def _amt_key(x: float) -> str:
    return f"{abs(x):.2f}"


def _match_docs(doc_index, txn_date: str, amount: float, currency: str, counterparty: str) -> tuple[str, str, str]:
    cand = doc_index.get((currency, _amt_key(amount)), [])
    if not cand:
        return ("", "", "")
    tset = _tokens(counterparty)
    hits = []
    for d in cand:
        if d["date"] and txn_date:
            try:
                dd = abs((datetime.fromisoformat(d["date"]) - datetime.fromisoformat(txn_date)).days)
                if dd > 10:
                    continue
            except Exception:
                pass
        if tset and d["vendor_tokens"] and not (tset & d["vendor_tokens"]):
            continue
        hits.append(d["id"])
    if not hits:
        return ("", "", "")
    if len(hits) == 1:
        return (hits[0], "found", "")
    return ("|".join(sorted(hits)), "ambiguous", f"doc_match_multiple={len(hits)}")


def main() -> int:
    # Load documents and build (currency, amount)->candidates index
    doc_index: dict[tuple[str, str], list[dict]] = {}
    with open(DOC_CSV, "r", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if not r.get("total_amount") or not r.get("currency"):
                continue
            try:
                amt = float(r["total_amount"])
            except Exception:
                continue
            k = (r["currency"], _amt_key(amt))
            doc_index.setdefault(k, []).append({
                "id": r["document_id"],
                "date": r.get("document_date", ""),
                "vendor_tokens": _tokens(r.get("vendor", "")),
            })

    rows: list[list[str]] = []
    corp_fingerprints: set[tuple[str, str, str]] = set()  # (date, cad_abs, token)

    # 1) Corporate chequing
    with open(TD_BIZ_CHQ, "r", encoding="utf-8", newline="") as f:
        for i, r in enumerate(csv.reader(f), start=1):
            if len(r) < 4:
                continue
            txn_date = _date_mmddyyyy(r[0])
            if not _in_fy2025(txn_date):
                continue
            desc = (r[1] or "").strip()
            wd = (r[2] or "").strip()
            dep = (r[3] or "").strip() if len(r) > 3 else ""
            amount = -_num(wd) if wd else (_num(dep) if dep else 0.0)
            if amount == 0.0:
                continue
            counterparty = desc
            linked, status, note = _match_docs(doc_index, txn_date, amount, "CAD", counterparty)
            is_transfer_fee = bool(
                re.search(r"\b(TFR-|MONTHLY PLAN FEE|TAX PYT FEE|TXINS|GST-|TXBAL)\b", desc)
            )
            receipt_status = status or ("not_applicable" if is_transfer_fee else "missing")
            txn_id = f"2025_tdbiz_chq_{txn_date.replace('-', '')}_{i:04d}"
            rows.append([
                txn_id, "2025", txn_date, "bank_csv", os.path.relpath(TD_BIZ_CHQ, ROOT), f"line:{i}",
                "corporate", "TD Business Chequing", "chequing", "", counterparty, desc,
                f"{amount:.2f}", "CAD", f"{amount:.2f}", "1", linked, receipt_status, note,
            ])
            tok = next(iter(_tokens(counterparty) or {""}))
            corp_fingerprints.add((txn_date, f"{abs(amount):.2f}", tok))

    # 2) Corporate Visa
    with open(TD_BIZ_VISA, "r", encoding="utf-8-sig", newline="") as f:
        dr = csv.DictReader(f)
        for i, r in enumerate(dr, start=2):  # line numbers (header is 1)
            # IMPORTANT: use Visa "Transaction Date" (economic date), not "Posting Date".
            txn_date = _date_any(r.get("Transaction Date") or "")
            if not txn_date:
                txn_date = _date_any(r.get("Posting Date") or "")
            if not _in_fy2025(txn_date):
                continue
            ttype = (r.get("Transaction Type") or "").strip()
            supplier = (r.get("Supplier") or "").strip()
            card = (r.get("Account") or "")
            last4 = re.sub(r"[^0-9]", "", card)[-4:]
            ccy = (r.get("Source Currency") or r.get("Billing Currency") or "CAD").strip() or "CAD"
            src_amt = _num(r.get("Source Amount") or r.get("Amount") or "0")
            bill_amt = _num(r.get("Amount") or "0")
            ttype_l = ttype.lower()
            # Economic sign convention (best-effort): outflows negative, inflows positive.
            # TD export typically uses positive for purchases and negative for credits/payments.
            if ttype_l == "payment":
                amount, cad_amount = src_amt, bill_amt
            else:
                if bill_amt < 0 or src_amt < 0:
                    amount, cad_amount = abs(src_amt), abs(bill_amt)
                else:
                    amount, cad_amount = -abs(src_amt), -abs(bill_amt)
            fx = "1" if ccy == "CAD" or amount == 0 else f"{abs(cad_amount) / abs(amount):.6f}"
            counterparty = supplier if supplier and supplier != "-" else ("TD" if ttype_l == "payment" else "")
            linked, status, note = _match_docs(doc_index, txn_date, amount, ccy, counterparty)
            receipt_status = "not_applicable" if ttype_l == "payment" else (status or "missing")
            txn_id = f"2025_tdbiz_visa_{txn_date.replace('-', '')}_{i:04d}"
            rows.append([
                txn_id, "2025", txn_date, "cc_csv", os.path.relpath(TD_BIZ_VISA, ROOT), f"line:{i}",
                "corporate", "TD Business Visa", "credit_card", last4, counterparty, supplier,
                f"{amount:.2f}", ccy, f"{cad_amount:.2f}", fx, linked, receipt_status, note,
            ])
            tok = next(iter(_tokens(counterparty) or {""}))
            corp_fingerprints.add((txn_date, f"{abs(cad_amount):.2f}", tok))

    # 3) Personal chequing (only include if it matches a doc AND not already in corporate)
    with open(TD_PERSONAL_CHQ, "r", encoding="utf-8", newline="") as f:
        for i, r in enumerate(csv.reader(f), start=1):
            if len(r) < 4:
                continue
            txn_date = _date_yyyy_mm_dd(r[0].strip('"'))
            if not _in_fy2025(txn_date):
                continue
            desc = (r[1] or "").strip('"').strip()
            wd = (r[2] or "").strip('"').strip()
            if not wd:
                continue
            amount = -_num(wd)
            counterparty = desc
            linked, status, note = _match_docs(doc_index, txn_date, amount, "CAD", counterparty)
            if not linked:
                continue
            tok = next(iter(_tokens(counterparty) or {""}))
            if (txn_date, f"{abs(amount):.2f}", tok) in corp_fingerprints:
                continue
            txn_id = f"2025_tdpers_chq_{txn_date.replace('-', '')}_{i:04d}"
            rows.append([
                txn_id, "2025", txn_date, "bank_csv", os.path.relpath(TD_PERSONAL_CHQ, ROOT), f"line:{i}",
                "personal", "TD Personal Chequing", "chequing", "", counterparty, desc,
                f"{amount:.2f}", "CAD", f"{amount:.2f}", "1", linked, status or "found",
                (note + ";" if note else "") + "personal_reimbursable_candidate",
            ])

    rows.sort(key=lambda x: (x[2], x[0]))
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(rows)

    print(f"Wrote {len(rows)} transactions -> {os.path.relpath(OUT_CSV, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

