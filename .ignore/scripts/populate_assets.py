"""Populate FY2025/normalized/assets.csv (LF endings) from:

- FY2024/financials/2024_Capital_Assets.md (seed / carry-forward list)
- FY2025/normalized/transactions.csv (+ allocations.csv) to *flag* likely FY2025 additions

Notes:
- This script does NOT calculate depreciation/UCC. Unknown UCC fields are left blank.
- CCA class is inferred only when explicitly stated in FY2024 depreciation lines; FY2025 additions leave cca_class blank and are flagged for review.
"""

from __future__ import annotations

import csv
import os
import re
from collections import defaultdict


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FY2024_MD = os.path.join(ROOT, "FY2024", "financials", "2024_Capital_Assets.md")
TXN_CSV = os.path.join(ROOT, "FY2025", "normalized", "transactions.csv")
ALLOC_CSV = os.path.join(ROOT, "FY2025", "normalized", "allocations.csv")
OUT_CSV = os.path.join(ROOT, "FY2025", "normalized", "assets.csv")


HEADER = [
    "asset_id",
    "description",
    "acquisition_date",
    "cost",
    "currency",
    "cad_cost",
    "vendor",
    "cca_class",
    "opening_ucc",
    "additions",
    "disposals",
    "cca_claimed",
    "closing_ucc",
    "linked_transaction_id",
    "linked_document_ids",
    "notes",
]


_DATE_RE = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2})")


def _slug(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "x"


def _parse_date(cell: str) -> str:
    m = _DATE_RE.search(cell or "")
    return m.group(1) if m else ""


def _parse_money(cell: str) -> str:
    """Return normalized decimal string (2dp) or '' if empty."""
    s = (cell or "").strip()
    if not s:
        return ""
    s = s.replace("$", "").replace(",", "")
    s = s.replace("(", "-").replace(")", "")
    try:
        return f"{float(s):.2f}"
    except ValueError:
        return ""


def _split_vendor_desc(raw: str) -> tuple[str, str]:
    raw = (raw or "").replace("\\", "").strip()
    if " - " in raw:
        vendor, desc = raw.split(" - ", 1)
        return vendor.strip(), desc.strip()
    return raw.strip(), raw.strip()


def _alloc_category_by_txn() -> dict[str, str]:
    m: dict[str, str] = {}
    if not os.path.exists(ALLOC_CSV):
        return m
    with open(ALLOC_CSV, "r", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            tid = r.get("transaction_id", "")
            if tid and tid not in m:
                m[tid] = r.get("reporting_category", "")
    return m


def _is_transfer_like(txn: dict[str, str]) -> bool:
    if (txn.get("receipt_status") or "").strip().lower() == "not_applicable":
        return True
    txt = (txn.get("counterparty", "") + " " + txn.get("description", "")).lower()
    transfer_keys = [
        "tfr-to",
        "tfr-fr",
        "send e-tfr",
        "gst-p",
        "gst-b",
        "txins",
        "txbal",
        "payment thank you",
        "pmt",
        "tdct_",
    ]
    return any(k in txt for k in transfer_keys)


def _seed_assets_from_fy2024(md_path: str) -> list[dict[str, str]]:
    assets: list[dict[str, str]] = []
    pending_idx: int | None = None

    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or cells[0] in {"Date", ":----"}:
                continue
            if len(cells) < 3:
                continue

            d = _parse_date(cells[0])
            raw_desc = cells[1]
            total = _parse_money(cells[2])

            if not d:
                continue

            desc_l = (raw_desc or "").lower()
            if "depreciation of class" in desc_l:
                # Attach inferred class to immediately preceding asset row if present
                if pending_idx is not None:
                    m = re.search(r"class\s*([0-9]+)", desc_l)
                    if m:
                        assets[pending_idx]["cca_class"] = m.group(1)
                        assets[pending_idx]["notes"] = (assets[pending_idx]["notes"] + ";cca_class_inferred_from_FY2024")
                pending_idx = None
                continue

            vendor, desc = _split_vendor_desc(raw_desc)
            assets.append(
                {
                    "asset_id": "",  # fill later
                    "description": desc,
                    "acquisition_date": d,
                    "cost": total,
                    "currency": "CAD",
                    "cad_cost": total,
                    "vendor": vendor,
                    "cca_class": "",
                    "opening_ucc": "",
                    "additions": "0.00",
                    "disposals": "0.00",
                    "cca_claimed": "",
                    "closing_ucc": "",
                    "linked_transaction_id": "",
                    "linked_document_ids": "",
                    "notes": "carried_forward_from_FY2024;ucc_unknown",
                }
            )
            pending_idx = len(assets) - 1

    return assets


def _fy2025_addition_candidates() -> list[dict[str, str]]:
    cats = _alloc_category_by_txn()
    exclude_cats = {
        "Meals and entertainment",
        "Travel expenses",
        "Telephone and utilities",
        "Interest & Bank Charges",
        "Revenue",
        "Revenue (review)",
        "Loan to shareholder (review)",
        "Credit card payment (transfer)",
        "GST/HST remittance",
        "Tax instalment / balance adjustment",
    }

    vendor_keys = [
        "lenovo",
        "dell",
        "apple",
        "samsung",
        "amazon",
        "amzn",
        "costco",
        "ikea",
        "best buy",
        "staples",
    ]

    out: list[dict[str, str]] = []
    with open(TXN_CSV, "r", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            tid = r.get("transaction_id", "")
            try:
                cad = float(r.get("cad_amount") or r.get("amount") or 0)
                amt = float(r.get("amount") or 0)
            except ValueError:
                continue

            if cad >= 0:
                continue
            if abs(cad) < 250:
                continue
            if _is_transfer_like(r):
                continue

            cat = cats.get(tid, "")
            if cat in exclude_cats:
                continue

            txt = (r.get("counterparty", "") + " " + r.get("description", "")).lower()
            if not any(k in txt for k in vendor_keys):
                continue

            vendor = (r.get("counterparty") or "").strip() or "(unknown)"
            out.append(
                {
                    "asset_id": "",  # fill later
                    "description": f"FY2025 candidate: {vendor}",
                    "acquisition_date": (r.get("txn_date") or "").strip(),
                    "cost": f"{abs(amt):.2f}",
                    "currency": (r.get("currency") or "CAD").strip() or "CAD",
                    "cad_cost": f"{abs(cad):.2f}",
                    "vendor": vendor,
                    "cca_class": "",
                    "opening_ucc": "0.00",
                    "additions": f"{abs(cad):.2f}",
                    "disposals": "0.00",
                    "cca_claimed": "",
                    "closing_ucc": "",
                    "linked_transaction_id": tid,
                    "linked_document_ids": (r.get("linked_document_ids") or "").strip(),
                    "notes": "potential_capital_asset_FY2025_addition;needs_owner_review",
                }
            )

    return out


def _assign_asset_ids(rows: list[dict[str, str]]) -> None:
    used: defaultdict[str, int] = defaultdict(int)
    for r in rows:
        base = f"{r.get('acquisition_date','')}_{_slug(r.get('vendor',''))}_{_slug(r.get('description',''))}"
        used[base] += 1
        suffix = f"_{used[base]}" if used[base] > 1 else ""
        r["asset_id"] = f"asset_{base}{suffix}"


def main() -> None:
    rows: list[dict[str, str]] = []
    if os.path.exists(FY2024_MD):
        rows.extend(_seed_assets_from_fy2024(FY2024_MD))
    rows.extend(_fy2025_addition_candidates())
    _assign_asset_ids(rows)

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in HEADER})

    print(f"Wrote {len(rows)} assets -> {os.path.relpath(OUT_CSV, ROOT)}")


if __name__ == "__main__":
    main()
