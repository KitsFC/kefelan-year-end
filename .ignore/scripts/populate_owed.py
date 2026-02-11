"""Populate FY2025/normalized/owed.csv (LF endings).

This file is a bridge for balances that *do not* map 1:1 to posted statement
transactions. For FY2025 we generate a conservative first pass:

Receivables:
- Kefelan customer invoices (document_id starts with `Kefelan_Invoice_`) that do
  not have a same-amount corporate chequing deposit (e-transfer/mobile deposit)
  on/after the invoice issue date within FY2025.

Payables:
- Large (>= 1000) vendor invoices that are unlinked and have no obvious 1:1
  same-amount payment match.

Notes
- All amount fields in owed.csv are positive magnitudes; direction is via
  owed_type.
- We only link settlements that exist in FY2025/normalized/transactions.csv via
  linked_transaction_ids.
"""

from __future__ import annotations

import csv
import os
import re
from collections import defaultdict
from pathlib import Path


ROOT = str(Path(__file__).resolve().parents[2])

DOC_CSV = os.path.join(ROOT, "FY2025", "normalized", "documents.csv")
TXN_CSV = os.path.join(ROOT, "FY2025", "normalized", "transactions.csv")
OUT_CSV = os.path.join(ROOT, "FY2025", "normalized", "owed.csv")
PERSONAL_DIR = os.path.join(ROOT, "FY2025", "reference", "personal")


HEADER = [
    "owed_id",
    "fiscal_year",
    "owed_type",
    "counterparty",
    "document_id",
    "issue_date",
    "due_date",
    "total_amount",
    "currency",
    "cad_total_amount",
    "linked_transaction_ids",
    "settled_cad_amount",
    "outstanding_cad_amount",
    "status",
    "notes",
]


def _parse_money(s: str) -> float | None:
    s = (s or "").strip()
    if not s:
        return None
    s = s.replace(",", "").replace("$", "")
    s = s.replace("(", "-").replace(")", "")
    try:
        return float(s)
    except ValueError:
        return None


def _as_2dp(x: float | None) -> str:
    return "" if x is None else f"{x:.2f}"


def _slug(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "x"


def _money_needles(amt: float) -> list[str]:
    """Return a few common string renderings for a 2dp amount."""
    s = f"{amt:.2f}"
    whole, frac = s.split(".")
    # 1149.99 -> 1,149.99
    with_commas = f"{int(whole):,}.{frac}"
    return [s, with_commas]


def _scan_personal_statements(needles: list[str]) -> list[str]:
    """Search ALL FY2025/reference/personal statement files for any needle.

    This is a best-effort text scan to satisfy the requirement that personal
    statements must be checked before concluding no settlement exists outside
    corporate statements.
    """
    d = Path(PERSONAL_DIR)
    if not d.exists():
        return []

    needles_l = [n.lower() for n in needles if (n or "").strip()]
    if not needles_l:
        return []

    hits: list[str] = []
    for p in sorted(d.glob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".csv", ".txt"}:
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            continue
        if any(n in txt for n in needles_l):
            hits.append(p.name)
    return hits


def _is_revenue_deposit(txn: dict[str, str]) -> bool:
    if (txn.get("payment_method") or "").strip().lower() != "chequing":
        return False
    cad = _parse_money(txn.get("cad_amount", "") or "")
    if cad is None or cad <= 0:
        return False
    txt = (txn.get("counterparty", "") + " " + txn.get("description", "")).lower()
    return ("e-transfer" in txt) or ("mobile dep" in txt) or ("mobile deposit" in txt)


def _is_any_chequing_deposit(txn: dict[str, str]) -> bool:
    if (txn.get("payment_method") or "").strip().lower() != "chequing":
        return False
    cad = _parse_money(txn.get("cad_amount", "") or "")
    return cad is not None and cad > 0


def _match_by_amount_after_issue(
    invoices: list[dict[str, str]],
    deposits: list[dict[str, str]],
) -> dict[str, str]:
    """Greedy 1:1 match by exact CAD amount (2dp), requiring deposit_date >= issue_date."""

    by_amt: dict[str, list[dict[str, str]]] = defaultdict(list)
    for t in deposits:
        cad = _parse_money(t.get("cad_amount") or "")
        if cad is None:
            continue
        by_amt[f"{cad:.2f}"].append(t)
    for amt in by_amt:
        by_amt[amt].sort(key=lambda r: r.get("txn_date") or "")

    used_txn_ids: set[str] = set()
    matched: dict[str, str] = {}

    for inv in sorted(invoices, key=lambda d: d.get("issue_date") or ""):
        did = inv.get("document_id") or ""
        issue = inv.get("issue_date") or ""
        amt = _parse_money(inv.get("cad_total_amount") or inv.get("total_amount") or "")
        if not did or not issue or amt is None:
            continue

        key = f"{amt:.2f}"
        pick: dict[str, str] | None = None
        for t in by_amt.get(key, []):
            tid = t.get("transaction_id") or ""
            if not tid or tid in used_txn_ids:
                continue
            if (t.get("txn_date") or "") < issue:
                continue
            pick = t
            break

        if pick is not None:
            tid = pick.get("transaction_id") or ""
            if tid:
                matched[did] = tid
                used_txn_ids.add(tid)

    return matched


def _kefelan_customer_from_doc_id(document_id: str) -> str:
    # e.g. Kefelan_Invoice_KS2025013101_Capiche -> Capiche
    parts = (document_id or "").split("_")
    # Common pattern: Kefelan_Invoice_<invoiceNo>_<Customer_Name...>
    if len(parts) >= 4 and parts[0] == "Kefelan" and parts[1] == "Invoice":
        cust = " ".join([p for p in parts[3:] if p]).strip()
        if cust:
            return cust
    if len(parts) >= 2:
        return parts[-1].strip() or "(unknown)"
    return "(unknown)"


def main() -> None:
    with open(DOC_CSV, "r", encoding="utf-8", newline="") as f:
        docs = list(csv.DictReader(f))

    with open(TXN_CSV, "r", encoding="utf-8", newline="") as f:
        txns = list(csv.DictReader(f))

    rev_deps = [t for t in txns if _is_revenue_deposit(t)]
    any_cheq_deps = [t for t in txns if _is_any_chequing_deposit(t)]

    # --- Receivables: Kefelan invoices
    kef_invs: list[dict[str, str]] = []
    for d in docs:
        if (d.get("document_type") or "").strip().lower() != "invoice":
            continue
        if not (d.get("document_date") or "").startswith("2025-"):
            continue
        did = d.get("document_id") or ""
        if not did.startswith("Kefelan_Invoice_"):
            continue
        amt = _parse_money(d.get("total_amount") or "")
        if amt is None:
            continue
        cur = (d.get("currency") or "CAD").strip() or "CAD"
        cad_amt = amt if cur == "CAD" else None

        kef_invs.append(
            {
                "document_id": did,
                "issue_date": d.get("document_date") or "",
                "due_date": "",
                "counterparty": _kefelan_customer_from_doc_id(did),
                "total_amount": _as_2dp(amt),
                "currency": cur,
                "cad_total_amount": _as_2dp(cad_amt),
            }
        )

    matched = _match_by_amount_after_issue(kef_invs, rev_deps)

    owed_rows: list[dict[str, str]] = []

    for inv in kef_invs:
        did = inv["document_id"]
        if did in matched:
            continue  # 1:1 settled in FY2025
        cad_total = _parse_money(inv.get("cad_total_amount") or "")

        # Personal statement scan (required when corporate settlement is not obvious).
        personal_hits: list[str] = []
        if cad_total is not None:
            personal_hits = _scan_personal_statements(
                _money_needles(cad_total) + [inv.get("counterparty") or ""]
            )

        # Also detect if there exist same-amount chequing deposits that are NOT
        # tagged as e-transfer/mobile-deposit (i.e., could be transfers).
        cheq_same_amt_ids: list[str] = []
        if cad_total is not None:
            key = f"{cad_total:.2f}"
            for t in any_cheq_deps:
                if f"{_parse_money(t.get('cad_amount') or '') or 0:.2f}" != key:
                    continue
                if (t.get("txn_date") or "") < (inv.get("issue_date") or ""):
                    continue
                tid = t.get("transaction_id") or ""
                if tid:
                    cheq_same_amt_ids.append(tid)

        # Be conservative: unless we can confidently exclude installments / other
        # settlement paths, default to unknown.
        status = "unknown"
        notes = "receivable_from_customer_invoice;no_1_to_1_match_to_corporate_revenue_deposit_after_issue_date"

        if cheq_same_amt_ids:
            notes += ";same_amount_chequing_deposit_candidates=" + "|".join(cheq_same_amt_ids[:10])
        if personal_hits:
            notes += ";personal_statement_hits=" + "|".join(personal_hits[:10])
        else:
            notes += ";personal_statement_hits=none"

        # Very small receivables are hard to disambiguate from common transfers.
        if cad_total is not None and cad_total < 1000:
            status = "unknown"
            notes += ";low_amount_receivable_needs_owner_review"

        owed_rows.append(
            {
                "owed_id": f"owed_{_slug(did)}",
                "fiscal_year": "2025",
                "owed_type": "receivable",
                "counterparty": inv.get("counterparty") or "(unknown)",
                "document_id": did,
                "issue_date": inv.get("issue_date") or "",
                "due_date": "",
                "total_amount": inv.get("total_amount") or "",
                "currency": inv.get("currency") or "",
                "cad_total_amount": inv.get("cad_total_amount") or "",
                "linked_transaction_ids": "",
                "settled_cad_amount": "0.00" if inv.get("cad_total_amount") else "",
                "outstanding_cad_amount": inv.get("cad_total_amount") or "",
                "status": status,
                "notes": notes + ";carry_forward_if_not_closed",
            }
        )

    # --- Payables: large unlinked vendor invoices (best-effort)
    # Only include if we can't find a same-amount payment line; otherwise it's 1:1 settled.
    linked_docs: set[str] = set()
    for t in txns:
        for x in (t.get("linked_document_ids") or "").split("|"):
            if x:
                linked_docs.add(x)

    for d in docs:
        if (d.get("document_type") or "").strip().lower() != "invoice":
            continue
        if not (d.get("document_date") or "").startswith("2025-"):
            continue
        did = d.get("document_id") or ""
        if not did or did.startswith("Kefelan_Invoice_"):
            continue
        if did in linked_docs:
            continue

        amt = _parse_money(d.get("total_amount") or "")
        if amt is None or amt < 1000:
            continue
        cur = (d.get("currency") or "CAD").strip() or "CAD"
        cad_amt = amt if cur == "CAD" else None

        # Look for exact same-magnitude payment line (e.g. credit card purchase)
        issue = d.get("document_date") or ""
        candidates: list[str] = []
        target = f"{amt:.2f}"
        for t in txns:
            if (t.get("txn_date") or "") < issue:
                continue
            cad = _parse_money(t.get("cad_amount") or "")
            if cad is None:
                continue
            if cad < 0 and f"{abs(cad):.2f}" == target:
                candidates.append(t.get("transaction_id") or "")

        if len(candidates) == 1:
            continue  # 1:1 paid

        # REQUIRED: scan personal statements before emitting an owed entry when
        # there is no clear corporate settlement.
        personal_hits = _scan_personal_statements(
            _money_needles(amt) + [(d.get("vendor") or ""), did]
        )

        status = "unknown"
        note = "payable_from_vendor_invoice;no_1_to_1_statement_match"
        if len(candidates) > 1:
            note += ";multiple_same_amount_payment_candidates=" + "|".join([c for c in candidates if c])
        if personal_hits:
            note += ";personal_statement_hits=" + "|".join(personal_hits[:10])
        else:
            note += ";personal_statement_hits=none"

        owed_rows.append(
            {
                "owed_id": f"owed_{_slug(did)}",
                "fiscal_year": "2025",
                "owed_type": "payable",
                "counterparty": (d.get("vendor") or "(unknown)").strip() or "(unknown)",
                "document_id": did,
                "issue_date": issue,
                "due_date": "",
                "total_amount": _as_2dp(amt),
                "currency": cur,
                "cad_total_amount": _as_2dp(cad_amt),
                "linked_transaction_ids": "",
                "settled_cad_amount": "0.00" if cad_amt is not None else "",
                "outstanding_cad_amount": _as_2dp(cad_amt) if cad_amt is not None else "",
                "status": status,
                "notes": note + ";requires_reconciliation_and_personal_statement_scan_if_applicable",
            }
        )

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
        w.writeheader()
        for r in owed_rows:
            w.writerow({k: r.get(k, "") for k in HEADER})

    print(f"Wrote {len(owed_rows)} owed rows -> {os.path.relpath(OUT_CSV, ROOT)}")


if __name__ == "__main__":
    main()
