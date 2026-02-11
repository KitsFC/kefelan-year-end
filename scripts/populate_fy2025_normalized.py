#!/usr/bin/env python3
"""Populate FY2025/normalized/*.csv from FY2025 source files.

This script is intentionally dependency-free (stdlib only) so it can be re-run
to regenerate normalized outputs deterministically.
"""

from __future__ import annotations

import csv
import hashlib
import html
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, Optional


ROOT = Path(__file__).resolve().parents[1]
FY = 2025
FY_START = date(FY, 1, 1)
FY_END = date(FY, 12, 31)

TX_DIR = ROOT / "FY2025" / "transactions"
NORM_DIR = ROOT / "FY2025" / "normalized"

PERSONAL_REF_DIR = ROOT / "FY2025" / "reference" / "personal"

BUS_BANK_CSV = TX_DIR / "1_assets" / "TD_Business_accountactivity_20241225-20260208.csv"
BUS_CC_MD = TX_DIR / "2_liabilities" / "TD_Business_Visa_2025.md"

TD_PERSONAL_VISA_LAST4 = "6493"
BMO_PERSONAL_MC_LAST4 = "9973"


DOC_COLUMNS = [
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

TX_COLUMNS = [
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

ALLOC_COLUMNS = [
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

ASSET_COLUMNS = [
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

OWED_COLUMNS = [
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


MONTHS = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


def short_hash(s: str, n: int = 10) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:n]


def slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "unknown"


def parse_decimal(s: str) -> Optional[Decimal]:
    s = s.strip()
    if not s:
        return None
    s = s.replace(",", "")
    s = s.replace("$", "")
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def fmt_decimal(d: Optional[Decimal]) -> str:
    if d is None:
        return ""
    # Normalize to 2 decimals for money fields
    q = d.quantize(Decimal("0.01"))
    return format(q, "f")


def in_fy(d: date) -> bool:
    return FY_START <= d <= FY_END


def strip_html_to_text(md_with_html: str) -> str:
    # Convert common HTML constructs to text; keep line breaks where useful.
    s = md_with_html
    s = re.sub(r"<\s*br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</\s*p\s*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</\s*tr\s*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</\s*td\s*>", "\t", s, flags=re.IGNORECASE)
    s = re.sub(r"</\s*th\s*>", "\t", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return s


@dataclass
class Document:
    document_id: str
    document_type: str
    document_date: str
    vendor: str
    amount: str
    currency: str
    source_file: str
    original_format: str
    notes: str


@dataclass
class Transaction:
    transaction_id: str
    fiscal_year: str
    txn_date: str
    source_type: str
    source_file: str
    source_locator: str
    account_owner: str
    account_name: str
    payment_method: str
    card_last4: str
    counterparty: str
    description: str
    amount: str
    currency: str
    cad_amount: str
    fx_rate_to_cad: str
    linked_document_ids: str
    receipt_status: str
    notes: str


def iter_evidence_md_files() -> Iterable[Path]:
    excluded = {
        BUS_BANK_CSV.resolve(),
        BUS_CC_MD.resolve(),
    }
    for p in TX_DIR.rglob("*"):
        if p.is_dir():
            continue
        if p.resolve() in excluded:
            continue
        if p.suffix.lower() != ".md":
            continue
        yield p


def guess_document_type(path: Path, text: str) -> str:
    name = path.name.lower()
    if name.startswith("kefelan_invoice_") or "invoice" in name or "invoice" in text.lower():
        return "invoice"
    if "receipt" in name or "receipt" in text.lower() or "paid" in name:
        return "receipt"
    if name.startswith("tdct_") or "completed successfully" in text.lower() or "confirmation" in text.lower():
        return "confirmation"
    return "other"


def extract_date_from_filename(path: Path) -> Optional[date]:
    s = path.name
    m = re.search(r"(20[0-9]{2})-([0-9]{2})-([0-9]{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"_(20[0-9]{2})([0-9]{2})([0-9]{2})_", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def extract_date_from_text(text: str) -> Optional[date]:
    # Common forms:
    # - Jan 15, 2025
    # - 05/27/2025
    # - 26 Jul'25
    m = re.search(r"\b([A-Z][a-z]{2})\s+([0-9]{1,2}),\s*(20[0-9]{2})\b", text)
    if m:
        mon = m.group(1).upper()
        if mon[:3] in MONTHS:
            return date(int(m.group(3)), MONTHS[mon[:3]], int(m.group(2)))

    m = re.search(r"\b([0-9]{2})/([0-9]{2})/(20[0-9]{2})\b", text)
    if m:
        return date(int(m.group(3)), int(m.group(1)), int(m.group(2)))

    m = re.search(r"\b([0-9]{1,2})\s+([A-Z][a-z]{2})'?([0-9]{2})\b", text)
    if m and m.group(2).upper()[:3] in MONTHS:
        yy = int(m.group(3))
        year = 2000 + yy
        return date(year, MONTHS[m.group(2).upper()[:3]], int(m.group(1)))

    m = re.search(r"\b([0-9]{1,2})/([0-9]{1,2})/([0-9]{2})\b", text)
    if m:
        year = 2000 + int(m.group(3))
        return date(year, int(m.group(1)), int(m.group(2)))
    return None


AMOUNT_RE = re.compile(r"\$\s*([-]?[0-9]{1,3}(?:,[0-9]{3})*\.[0-9]{2})")


def extract_best_amount_and_currency(text: str) -> tuple[Optional[Decimal], str, str]:
    """Return (amount, currency, note)."""
    t = text
    t_low = t.lower()
    currency = "CAD"
    if re.search(r"\bUSD\b", t, flags=re.IGNORECASE):
        currency = "USD"
    if re.search(r"\bGBP\b", t, flags=re.IGNORECASE):
        currency = "GBP"

    candidates: list[tuple[int, Decimal, str]] = []
    for m in AMOUNT_RE.finditer(t):
        amt = parse_decimal(m.group(1))
        if amt is None:
            continue
        # Determine keyword proximity
        start = max(0, m.start() - 60)
        end = min(len(t), m.end() + 40)
        window = t_low[start:end]
        score = 1
        if any(k in window for k in ["total due", "amount due", "total", "grand total", "amount:"]):
            score = 3
        elif any(k in window for k in ["subtotal"]):
            score = 0
        candidates.append((score, amt, window.strip()))

    if not candidates:
        return None, currency, "no amount detected"

    # Prefer highest score, then largest absolute amount.
    candidates.sort(key=lambda x: (x[0], abs(x[1])), reverse=True)
    best = candidates[0]
    note = ""
    if best[0] < 3:
        note = "amount inferred (no explicit Total/Amount Due marker nearby)"
    return best[1], currency, note


def extract_vendor(path: Path, text: str) -> str:
    name = path.name
    if name.startswith("Kefelan_Invoice_"):
        return "Kefelan Solutions Inc."
    if name.startswith("TDCT_"):
        return "TD Canada Trust"

    def vendor_from_filename() -> str:
        # Many evidence files are named like Vendor_YYYY-MM-DD(.md).
        stem = path.stem
        stem = re.sub(r"[_-](20[0-9]{2}[-]?[0-9]{2}[-]?[0-9]{2}).*$", "", stem)
        stem = stem.replace("_", " ").replace("-", " ")
        stem = re.sub(r"\s+", " ", stem).strip()
        return stem[:120]

    fn_vendor = vendor_from_filename()

    # Prefer filename vendor when it looks like a real merchant name.
    if fn_vendor and fn_vendor.lower() not in {"invoice", "receipt", "statement"}:
        # Avoid picking obviously internal/placeholder prefixes.
        if not re.match(r"^(fy|ksi)\b", fn_vendor.strip(), flags=re.IGNORECASE):
            return fn_vendor

    # Otherwise, try to extract a reasonable vendor line from the body.
    # Evidence markdown is frequently HTML-heavy (images/tables) at the top, so scan deeper.
    GENERIC = {
        "easyweb",
        "td canada trust",
        "invoice",
        "receipt",
        "tax invoice",
        "order confirmation",
    }
    for raw in text.splitlines()[:60]:
        line = raw.strip()
        if not line or line.startswith("|"):
            continue
        if line.startswith("<"):
            continue

        # Drop HTML tags and common markdown emphasis.
        line = re.sub(r"<[^>]+>", " ", line)
        line = html.unescape(line)
        line = line.strip().strip("*>#` ")
        line = re.sub(r"[*_]+", "", line)
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue
        if line.lower() in GENERIC:
            continue
        if line.lower().startswith("http"):
            continue
        if re.match(r"^[0-9$][0-9, .]*(usd|cad)?$", line.strip(), flags=re.IGNORECASE):
            continue

        # Heuristic: vendor lines are usually short and mostly alphabetic.
        if len(line) <= 80 and re.search(r"[A-Za-z]", line):
            return line[:120]

    # Last resort.
    return fn_vendor or ""


def build_document(path: Path) -> Document:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="replace")
    doc_type = guess_document_type(path, text)

    d = extract_date_from_filename(path) or extract_date_from_text(text)
    doc_date = d.isoformat() if d else ""

    vendor = extract_vendor(path, text)
    amt, currency, amt_note = extract_best_amount_and_currency(text)

    notes = []
    if not doc_date:
        notes.append("document_date missing")
    if amt is None:
        notes.append("amount missing")
    if amt_note:
        notes.append(amt_note)

    # Deterministic ID
    id_date = doc_date.replace("-", "") if doc_date else "unknown"
    id_amt = (fmt_decimal(amt) if amt is not None else "")
    doc_id = f"doc-{id_date}-{slug(vendor)}-{id_amt}{currency}-{short_hash(rel)}"

    return Document(
        document_id=doc_id,
        document_type=doc_type,
        document_date=doc_date,
        vendor=vendor,
        amount=fmt_decimal(amt),
        currency=currency,
        source_file=rel,
        original_format=(path.suffix.lstrip(".").lower() or "md"),
        notes="; ".join(notes),
    )


def parse_bank_transactions() -> list[Transaction]:
    rel = BUS_BANK_CSV.relative_to(ROOT).as_posix()
    out: list[Transaction] = []
    with BUS_BANK_CSV.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader, start=1):
            if not row or len(row) < 4:
                continue
            dt_s, desc, debit_s, credit_s, *rest = row
            dt_s = dt_s.strip()
            desc = desc.strip()
            try:
                dt = datetime.strptime(dt_s, "%m/%d/%Y").date()
            except ValueError:
                continue
            if not in_fy(dt):
                continue

            debit = parse_decimal(debit_s) or Decimal("0")
            credit = parse_decimal(credit_s) or Decimal("0")
            amount = credit - debit  # inflow positive, outflow negative

            source_locator = f"line={idx}"
            base = f"{FY}|bank_csv|{rel}|{source_locator}|{dt.isoformat()}|{desc}|{amount}"
            tx_id = f"tx-{FY}-bank-{dt.strftime('%Y%m%d')}-{short_hash(base)}"

            counterparty = "TD Business Chequing"
            if "E-TRANSFER" in desc.upper() or "E-TFR" in desc.upper():
                counterparty = "Interac e-Transfer"
            elif "GST" in desc.upper() or "TX" in desc.upper() or "TAX" in desc.upper():
                counterparty = "Tax payment/fee"
            elif "MONTHLY PLAN FEE" in desc.upper():
                counterparty = "Bank fee"
            elif "TFR-TO" in desc.upper() or "TFR-FR" in desc.upper():
                counterparty = "TD Transfer"

            out.append(
                Transaction(
                    transaction_id=tx_id,
                    fiscal_year=str(FY),
                    txn_date=dt.isoformat(),
                    source_type="bank_csv",
                    source_file=rel,
                    source_locator=source_locator,
                    account_owner="corporate",
                    account_name="TD Business Chequing",
                    payment_method="chequing",
                    card_last4="",
                    counterparty=counterparty,
                    description=desc,
                    amount=fmt_decimal(amount),
                    currency="CAD",
                    cad_amount=fmt_decimal(amount),
                    fx_rate_to_cad="",
                    linked_document_ids="",
                    receipt_status="missing",
                    notes="",
                )
            )
    return out


STATEMENT_PERIOD_RE = re.compile(
    r"STATEMENT\s+PERIOD:\s*([A-Za-z]+\s+[0-9]{1,2},\s+20[0-9]{2})\s+to\s+([A-Za-z]+\s+[0-9]{1,2},\s+20[0-9]{2})",
    re.IGNORECASE,
)

TR_BLOCK_RE = re.compile(r"<\s*tr\b[^>]*>.*?<\s*/\s*tr\s*>", re.IGNORECASE | re.DOTALL)
CELL_RE = re.compile(
    r"<\s*(td|th)\b[^>]*>(.*?)<\s*/\s*\1\s*>",
    re.IGNORECASE | re.DOTALL,
)

TX_LINE_RE = re.compile(
    r"^\s*(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+([0-9]{1,2})\s+"
    r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+([0-9]{1,2})\s+"
    r"(.+?)\s+(-?\$?[0-9]{1,3}(?:,[0-9]{3})*\.[0-9]{2})\s*$",
    re.IGNORECASE,
)

DATE_ONLY_RE = re.compile(
    r"^\s*(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+([0-9]{1,2})\s*$",
    re.IGNORECASE,
)

AMOUNT_ONLY_RE = re.compile(
    r"^\s*-?\$?[0-9]{1,3}(?:,[0-9]{3})*\.[0-9]{2}\s*$",
    re.IGNORECASE,
)

FOREIGN_RE = re.compile(
    r"FOREIGN\s+CURRENCY\s+([0-9]{1,3}(?:\.[0-9]{1,4})?)\s+([A-Z]{3})\s+@\s+EXCHANGE\s+RATE\s+([0-9]{1,2}\.[0-9]{2,6})",
    re.IGNORECASE,
)


def parse_td_visa_transactions_from_md(
    md_path: Path,
    *,
    account_owner: str,
    account_name: str,
    card_last4: str,
) -> list[Transaction]:
    rel = md_path.relative_to(ROOT).as_posix()
    raw = md_path.read_text(encoding="utf-8", errors="replace")
    out: list[Transaction] = []

    # We have seen PDF->DOCX->Markdown conversions produce HTML tables where
    # the 4 transaction columns are not reliably represented as single lines.
    # We therefore parse by <tr>/<td> blocks when present.
    tr_blocks = list(TR_BLOCK_RE.finditer(raw))
    if not tr_blocks:
        # Fallback to the legacy line-based parser for non-table statements.
        text = strip_html_to_text(raw)
        lines = [ln.rstrip() for ln in text.splitlines()]

        period_start: Optional[date] = None
        period_end: Optional[date] = None
        last_tx_idx: Optional[int] = None

        # Some statement sections render each transaction across multiple lines:
        #   <Txn date>
        #   <Post date>
        #   <Description>
        #   <Amount>
        pend_t: Optional[tuple[int, int]] = None  # (month, day)
        pend_p: Optional[tuple[int, int]] = None
        pend_desc: Optional[str] = None
        pend_start_line: Optional[int] = None

        def infer_year(mon: int) -> int:
            if not period_start or not period_end:
                return FY
            if period_start.year == period_end.year:
                return period_end.year
            start_m = period_start.month
            return period_start.year if mon >= start_m else period_end.year

        def normalize_counterparty(desc: str) -> str:
            u = desc.upper()
            if "LENOVO" in u:
                return "Lenovo"
            if u.startswith("PAYPAL") or u.startswith("PP*"):
                return "PayPal"
            if "AMZN" in u or "AMAZON" in u:
                return "Amazon"
            if "UBER" in u:
                return "Uber"
            if "ROGERS" in u:
                return "Rogers"
            if "MICROSOFT" in u:
                return "Microsoft"
            if "SLACK" in u:
                return "Slack"
            if "OPENAI" in u:
                return "OpenAI"
            return desc.split()[0][:80] if desc else ""

        for i, ln in enumerate(lines, start=1):
            m = STATEMENT_PERIOD_RE.search(ln)
            if m:
                try:
                    period_start = datetime.strptime(m.group(1), "%B %d, %Y").date()
                    period_end = datetime.strptime(m.group(2), "%B %d, %Y").date()
                except ValueError:
                    period_start = None
                    period_end = None
                # Reset any partially collected multiline row.
                pend_t = None
                pend_p = None
                pend_desc = None
                pend_start_line = None
                last_tx_idx = None
                continue

            # 1) Single-line format
            m = TX_LINE_RE.match(ln)
            if m and period_start and period_end:
                tmon = MONTHS[m.group(1).upper()]
                tday = int(m.group(2))
                pmon = MONTHS[m.group(3).upper()]
                pday = int(m.group(4))
                desc = m.group(5).strip()
                amt_raw = parse_decimal(m.group(6))
                if amt_raw is None:
                    continue

                tyear = infer_year(tmon)
                pyear = infer_year(pmon)
                _txn_dt = date(tyear, tmon, tday)
                post_dt = date(pyear, pmon, pday)
                if not in_fy(post_dt):
                    continue

                cad_amount = -amt_raw
                counterparty = normalize_counterparty(desc)

                source_locator = f"line={i}"
                base = f"{FY}|cc_md|{rel}|{source_locator}|{post_dt.isoformat()}|{desc}|{cad_amount}"
                tx_id = f"tx-{FY}-cc-{post_dt.strftime('%Y%m%d')}-{short_hash(base)}"

                out.append(
                    Transaction(
                        transaction_id=tx_id,
                        fiscal_year=str(FY),
                        txn_date=post_dt.isoformat(),
                        source_type="cc_md",
                        source_file=rel,
                        source_locator=source_locator,
                        account_owner=account_owner,
                        account_name=account_name,
                        payment_method="credit_card",
                        card_last4=card_last4,
                        counterparty=counterparty,
                        description=desc,
                        amount=fmt_decimal(cad_amount),
                        currency="CAD",
                        cad_amount=fmt_decimal(cad_amount),
                        fx_rate_to_cad="",
                        linked_document_ids="",
                        receipt_status="missing",
                        notes=(
                            "AUTO: personal statement txn (candidate; included only if linked to evidence)"
                            if account_owner == "personal"
                            else ""
                        ),
                    )
                )
                last_tx_idx = len(out) - 1
                continue

            # 2) Multiline-row format
            if period_start and period_end:
                mdate = DATE_ONLY_RE.match(ln)
                if mdate:
                    mon = MONTHS[mdate.group(1).upper()]
                    day = int(mdate.group(2))
                    if pend_t is None:
                        pend_t = (mon, day)
                        pend_start_line = i
                        continue
                    if pend_p is None:
                        pend_p = (mon, day)
                        continue
                    # If we already have both dates, start over with a new record.
                    pend_t = (mon, day)
                    pend_p = None
                    pend_desc = None
                    pend_start_line = i
                    continue

                if (
                    pend_t
                    and pend_p
                    and pend_desc is None
                    and ln.strip()
                    and not AMOUNT_ONLY_RE.match(ln)
                    and not DATE_ONLY_RE.match(ln)
                ):
                    pend_desc = ln.strip()
                    continue

                if pend_t and pend_p and pend_desc and AMOUNT_ONLY_RE.match(ln):
                    amt_raw = parse_decimal(ln)
                    if amt_raw is None:
                        pend_t = None
                        pend_p = None
                        pend_desc = None
                        pend_start_line = None
                        continue

                    tmon, tday = pend_t
                    pmon, pday = pend_p
                    tyear = infer_year(tmon)
                    pyear = infer_year(pmon)
                    _txn_dt = date(tyear, tmon, tday)
                    post_dt = date(pyear, pmon, pday)
                    if not in_fy(post_dt):
                        pend_t = None
                        pend_p = None
                        pend_desc = None
                        pend_start_line = None
                        continue

                    desc = pend_desc.strip()
                    cad_amount = -amt_raw
                    counterparty = normalize_counterparty(desc)

                    start_line = pend_start_line or i
                    source_locator = f"lines={start_line}-{i}"
                    base = f"{FY}|cc_md|{rel}|{source_locator}|{post_dt.isoformat()}|{desc}|{cad_amount}"
                    tx_id = f"tx-{FY}-cc-{post_dt.strftime('%Y%m%d')}-{short_hash(base)}"

                    out.append(
                        Transaction(
                            transaction_id=tx_id,
                            fiscal_year=str(FY),
                            txn_date=post_dt.isoformat(),
                            source_type="cc_md",
                            source_file=rel,
                            source_locator=source_locator,
                            account_owner=account_owner,
                            account_name=account_name,
                            payment_method="credit_card",
                            card_last4=card_last4,
                            counterparty=counterparty,
                            description=desc,
                            amount=fmt_decimal(cad_amount),
                            currency="CAD",
                            cad_amount=fmt_decimal(cad_amount),
                            fx_rate_to_cad="",
                            linked_document_ids="",
                            receipt_status="missing",
                            notes=(
                                "AUTO: personal statement txn (candidate; included only if linked to evidence)"
                                if account_owner == "personal"
                                else ""
                            ),
                        )
                    )
                    last_tx_idx = len(out) - 1

                    pend_t = None
                    pend_p = None
                    pend_desc = None
                    pend_start_line = None
                    continue

            # Attach FX info to previous tx if present
            mfx = FOREIGN_RE.search(ln)
            if mfx and last_tx_idx is not None:
                fc_amt = parse_decimal(mfx.group(1))
                fc_ccy = mfx.group(2).upper()
                fx = parse_decimal(mfx.group(3))
                if fc_amt is None or fx is None:
                    continue

                tx = out[last_tx_idx]
                cad = parse_decimal(tx.cad_amount) or Decimal("0")
                sign = Decimal("-1") if cad < 0 else Decimal("1")
                tx.currency = fc_ccy
                tx.amount = fmt_decimal(sign * fc_amt)
                tx.fx_rate_to_cad = fmt_decimal(fx)
                if tx.notes:
                    tx.notes += "; "
                tx.notes += f"FX: {mfx.group(1)} {fc_ccy} @ {mfx.group(3)}"

        return out

    # --- Table-aware parser ---
    period_start: Optional[date] = None
    period_end: Optional[date] = None
    last_tx_idx: Optional[int] = None
    skipped_like_tx: list[tuple[int, str]] = []

    def _norm_ws(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

    def infer_year(mon: int) -> int:
        if not period_start or not period_end:
            # Without statement period context, guessing is risky; default to FY.
            return FY
        if period_start.year == period_end.year:
            return period_end.year
        start_m = period_start.month
        return period_start.year if mon >= start_m else period_end.year

    def normalize_counterparty(desc: str) -> str:
        u = desc.upper()
        if "LENOVO" in u:
            return "Lenovo"
        if u.startswith("PAYPAL") or u.startswith("PP*"):
            return "PayPal"
        if "AMZN" in u or "AMAZON" in u:
            return "Amazon"
        if "UBER" in u:
            return "Uber"
        if "ROGERS" in u:
            return "Rogers"
        if "MICROSOFT" in u:
            return "Microsoft"
        if "SLACK" in u:
            return "Slack"
        if "OPENAI" in u:
            return "OpenAI"
        return desc.split()[0][:80] if desc else ""

    def parse_mon_day(s: str) -> Optional[tuple[int, int]]:
        m = DATE_ONLY_RE.match(_norm_ws(s))
        if not m:
            return None
        mon = MONTHS[m.group(1).upper()]
        day = int(m.group(2))
        return mon, day

    def apply_fx_to_last_from_text(text_for_fx: str) -> None:
        nonlocal last_tx_idx
        if last_tx_idx is None:
            return
        mfx = FOREIGN_RE.search(text_for_fx)
        if not mfx:
            return
        fc_amt = parse_decimal(mfx.group(1))
        fc_ccy = mfx.group(2).upper()
        fx = parse_decimal(mfx.group(3))
        if fc_amt is None or fx is None:
            return
        tx = out[last_tx_idx]
        cad = parse_decimal(tx.cad_amount) or Decimal("0")
        sign = Decimal("-1") if cad < 0 else Decimal("1")
        tx.currency = fc_ccy
        tx.amount = fmt_decimal(sign * fc_amt)
        tx.fx_rate_to_cad = fmt_decimal(fx)
        if tx.notes:
            tx.notes += "; "
        tx.notes += f"FX: {mfx.group(1)} {fc_ccy} @ {mfx.group(3)}"

    for tr_idx, tr_m in enumerate(tr_blocks, start=1):
        tr_html = tr_m.group(0)
        tr_text = strip_html_to_text(tr_html)
        tr_text_flat = _norm_ws(tr_text)

        # Update statement period when encountered
        mper = STATEMENT_PERIOD_RE.search(tr_text_flat)
        if mper:
            try:
                period_start = datetime.strptime(mper.group(1), "%B %d, %Y").date()
                period_end = datetime.strptime(mper.group(2), "%B %d, %Y").date()
            except ValueError:
                period_start = None
                period_end = None
            last_tx_idx = None
            continue

        # Extract cells (td/th) in order
        cells_html = [m.group(2) for m in CELL_RE.finditer(tr_html)]
        cells = [strip_html_to_text(c).strip() for c in cells_html]

        parsed_any_in_row = False

        # 1) Cell-based row: txn_date | post_date | description | amount
        if len(cells) >= 4 and period_start and period_end:
            t_md = parse_mon_day(cells[0])
            p_md = parse_mon_day(cells[1])
            amt_raw = parse_decimal(cells[3])
            if t_md and p_md and amt_raw is not None:
                tmon, tday = t_md
                pmon, pday = p_md
                tyear = infer_year(tmon)
                pyear = infer_year(pmon)
                _txn_dt = date(tyear, tmon, tday)
                post_dt = date(pyear, pmon, pday)
                if in_fy(post_dt):
                    desc_raw = cells[2]
                    desc_flat = _norm_ws(desc_raw.replace("\t", " "))

                    # PDF->DOCX->MD conversions sometimes split a single logical
                    # transaction across two <tr> blocks using rowspan (dates+amount
                    # on row N, description on row N+1). Avoid emitting blank
                    # description/counterparty rows; attempt to recover the
                    # description from the next <tr> when possible.
                    desc_from_tr_note = ""
                    if not desc_flat and tr_idx < len(tr_blocks):
                        next_html = tr_blocks[tr_idx].group(0)  # tr_idx is 1-based
                        next_cells_html = [m.group(2) for m in CELL_RE.finditer(next_html)]
                        next_cells = [strip_html_to_text(c).strip() for c in next_cells_html]
                        for cand in next_cells:
                            cand2 = _norm_ws(cand.replace("\t", " "))
                            if not cand2:
                                continue
                            if DATE_ONLY_RE.match(cand2):
                                continue
                            if AMOUNT_ONLY_RE.match(cand2):
                                continue
                            u = cand2.upper()
                            if u in {
                                "PREVIOUS BALANCE",
                                "PAYMENTS & CREDITS",
                                "INTEREST FEES",
                                "SUB-TOTAL",
                                "SUBTOTAL",
                                "PURCHASES & OTHER CHARGES",
                                "CASH ADVANCES",
                                "CALCULATING YOUR BALANCE",
                            }:
                                continue
                            # Found a plausible merchant/description.
                            desc_flat = cand2
                            desc_from_tr_note = f"DESC_FROM_TR={tr_idx + 1}"
                            break

                    if not desc_flat:
                        skipped_like_tx.append((tr_idx, _norm_ws(" ".join(cells[:4]))[:160]))
                        continue

                    # If FX info is embedded, keep it in notes and avoid polluting the main description.
                    if re.search(r"FOREIGN\s+CURRENCY", desc_flat, flags=re.IGNORECASE):
                        desc_flat = re.split(
                            r"FOREIGN\s+CURRENCY", desc_flat, maxsplit=1, flags=re.IGNORECASE
                        )[0].strip()

                    cad_amount = -amt_raw
                    counterparty = normalize_counterparty(desc_flat)
                    source_locator = f"tr={tr_idx}"
                    base = f"{FY}|cc_md|{rel}|{source_locator}|{post_dt.isoformat()}|{desc_flat}|{cad_amount}"
                    tx_id = f"tx-{FY}-cc-{post_dt.strftime('%Y%m%d')}-{short_hash(base)}"

                    base_notes = (
                        "AUTO: personal statement txn (candidate; included only if linked to evidence)"
                        if account_owner == "personal"
                        else ""
                    )
                    if desc_from_tr_note:
                        if base_notes:
                            base_notes += "; "
                        base_notes += f"AUTO: {desc_from_tr_note}"

                    out.append(
                        Transaction(
                            transaction_id=tx_id,
                            fiscal_year=str(FY),
                            txn_date=post_dt.isoformat(),
                            source_type="cc_md",
                            source_file=rel,
                            source_locator=source_locator,
                            account_owner=account_owner,
                            account_name=account_name,
                            payment_method="credit_card",
                            card_last4=card_last4,
                            counterparty=counterparty,
                            description=desc_flat,
                            amount=fmt_decimal(cad_amount),
                            currency="CAD",
                            cad_amount=fmt_decimal(cad_amount),
                            fx_rate_to_cad="",
                            linked_document_ids="",
                            receipt_status="missing",
                            notes=base_notes,
                        )
                    )
                    last_tx_idx = len(out) - 1
                    apply_fx_to_last_from_text(tr_text)
                    parsed_any_in_row = True
                    continue
            # If row *looks* like a transaction row but failed parsing, remember it.
            if t_md and p_md and amt_raw is None:
                skipped_like_tx.append((tr_idx, _norm_ws(" ".join(cells[:4]))[:160]))

        # 2) Text-based transaction lines inside a row (e.g. a single <td colspan=...>)
        if period_start and period_end:
            for sub_idx, ln in enumerate(tr_text.splitlines(), start=1):
                ln2 = _norm_ws(ln.replace("\t", " "))
                if not ln2:
                    continue

                m = TX_LINE_RE.match(ln2)
                if m:
                    tmon = MONTHS[m.group(1).upper()]
                    tday = int(m.group(2))
                    pmon = MONTHS[m.group(3).upper()]
                    pday = int(m.group(4))
                    desc_full = m.group(5).strip()
                    amt_raw = parse_decimal(m.group(6))
                    if amt_raw is None:
                        continue

                    # If FX info is embedded in the description line, remove it and attach via notes.
                    desc_clean = desc_full
                    if re.search(r"FOREIGN\s+CURRENCY", desc_clean, flags=re.IGNORECASE):
                        desc_clean = re.split(
                            r"FOREIGN\s+CURRENCY", desc_clean, maxsplit=1, flags=re.IGNORECASE
                        )[0].strip()

                    tyear = infer_year(tmon)
                    pyear = infer_year(pmon)
                    _txn_dt = date(tyear, tmon, tday)
                    post_dt = date(pyear, pmon, pday)
                    if not in_fy(post_dt):
                        continue

                    cad_amount = -amt_raw
                    counterparty = normalize_counterparty(desc_clean)
                    source_locator = f"tr={tr_idx};line={sub_idx}"
                    base = f"{FY}|cc_md|{rel}|{source_locator}|{post_dt.isoformat()}|{desc_clean}|{cad_amount}"
                    tx_id = f"tx-{FY}-cc-{post_dt.strftime('%Y%m%d')}-{short_hash(base)}"

                    out.append(
                        Transaction(
                            transaction_id=tx_id,
                            fiscal_year=str(FY),
                            txn_date=post_dt.isoformat(),
                            source_type="cc_md",
                            source_file=rel,
                            source_locator=source_locator,
                            account_owner=account_owner,
                            account_name=account_name,
                            payment_method="credit_card",
                            card_last4=card_last4,
                            counterparty=counterparty,
                            description=desc_clean,
                            amount=fmt_decimal(cad_amount),
                            currency="CAD",
                            cad_amount=fmt_decimal(cad_amount),
                            fx_rate_to_cad="",
                            linked_document_ids="",
                            receipt_status="missing",
                            notes=(
                                "AUTO: personal statement txn (candidate; included only if linked to evidence)"
                                if account_owner == "personal"
                                else ""
                            ),
                        )
                    )
                    last_tx_idx = len(out) - 1
                    apply_fx_to_last_from_text(ln2)
                    parsed_any_in_row = True
                    continue

                # Attach FX lines immediately following a parsed transaction within this same <tr>
                if FOREIGN_RE.search(ln2):
                    apply_fx_to_last_from_text(ln2)

        # Keep last_tx_idx scoped to the current row to reduce chance of misattachment.
        if not parsed_any_in_row:
            last_tx_idx = None

    if skipped_like_tx:
        # Non-fatal warning to help catch conversion/layout surprises.
        print(
            f"WARN: {rel}: {len(skipped_like_tx)} rows looked like txns but could not be parsed; sample: {skipped_like_tx[:3]}"
        )

    return out


def parse_td_business_visa_transactions() -> list[Transaction]:
    return parse_td_visa_transactions_from_md(
        BUS_CC_MD,
        account_owner="corporate",
        account_name="TD Business VISA",
        card_last4="5143",
    )


def parse_td_personal_visa_transactions() -> list[Transaction]:
    out: list[Transaction] = []
    for p in sorted(PERSONAL_REF_DIR.glob("TD_Personal_Visa_*.md")):
        out.extend(
            parse_td_visa_transactions_from_md(
                p,
                account_owner="personal",
                account_name="TD Personal VISA",
                card_last4=TD_PERSONAL_VISA_LAST4,
            )
        )
    return out


BMO_PERIOD_RE = re.compile(
    r"Statement\s+period\s*\|\s*([A-Za-z]{3})\.?\s*([0-9]{1,2}),\s*(20[0-9]{2})\s*-\s*([A-Za-z]{3})\.?\s*([0-9]{1,2}),\s*(20[0-9]{2})",
    re.IGNORECASE,
)

BMO_DATEPAIR_RE = re.compile(
    r"^([A-Za-z]{3})\.?\s*([0-9]{1,2})\s+([A-Za-z]{3})\.?\s*([0-9]{1,2})$",
    re.IGNORECASE,
)

BMO_AMT_RE = re.compile(
    r"^([0-9]{1,3}(?:,[0-9]{3})*\.[0-9]{2})(?:\s*(CR))?$",
    re.IGNORECASE,
)


def parse_bmo_personal_mastercard_transactions() -> list[Transaction]:
    """Parse BMO personal MC eStatements under FY2025/reference/personal.

    Output transactions are candidates; they are filtered later so only those
    linked to evidence documents are included.
    """

    month_map = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }

    def normalize_counterparty(desc: str) -> str:
        u = desc.upper()
        if "LENOVO" in u:
            return "Lenovo"
        if u.startswith("PAYPAL") or u.startswith("PP*"):
            return "PayPal"
        if "AMZN" in u or "AMAZON" in u:
            return "Amazon"
        if "UBER" in u:
            return "Uber"
        if "ROGERS" in u:
            return "Rogers"
        if "MICROSOFT" in u:
            return "Microsoft"
        if "SLACK" in u:
            return "Slack"
        if "OPENAI" in u:
            return "OpenAI"
        return desc.split()[0][:80] if desc else ""

    out: list[Transaction] = []
    for md_path in sorted(PERSONAL_REF_DIR.glob("BMO_MC_eStatement_*.md")):
        rel = md_path.relative_to(ROOT).as_posix()
        raw = md_path.read_text(encoding="utf-8", errors="replace")

        period_start: Optional[date] = None
        period_end: Optional[date] = None
        m = BMO_PERIOD_RE.search(raw)
        if m:
            try:
                s_mon = month_map[m.group(1).upper()]
                s_day = int(m.group(2))
                s_year = int(m.group(3))
                e_mon = month_map[m.group(4).upper()]
                e_day = int(m.group(5))
                e_year = int(m.group(6))
                period_start = date(s_year, s_mon, s_day)
                period_end = date(e_year, e_mon, e_day)
            except Exception:
                period_start = None
                period_end = None

        def infer_year(mon: int) -> int:
            if not period_start or not period_end:
                return FY
            if period_start.year == period_end.year:
                return period_end.year
            start_m = period_start.month
            return period_start.year if mon >= start_m else period_end.year

        text = strip_html_to_text(raw)
        lines = [ln.rstrip() for ln in text.splitlines()]
        for i, ln in enumerate(lines, start=1):
            parts = [p.strip() for p in ln.split("\t") if p.strip()]
            if len(parts) < 3:
                continue
            mdate = BMO_DATEPAIR_RE.match(parts[0])
            if not mdate:
                continue

            desc = parts[1]
            mamt = BMO_AMT_RE.match(parts[2])
            if not mamt:
                continue
            amt_raw = parse_decimal(mamt.group(1))
            if amt_raw is None:
                continue

            tmon = month_map.get(mdate.group(1).upper())
            pmon = month_map.get(mdate.group(3).upper())
            if not tmon or not pmon:
                continue
            tday = int(mdate.group(2))
            pday = int(mdate.group(4))

            tyear = infer_year(tmon)
            pyear = infer_year(pmon)
            _txn_dt = date(tyear, tmon, tday)
            post_dt = date(pyear, pmon, pday)
            if not in_fy(post_dt):
                continue

            is_credit = bool(mamt.group(2)) or "PAYMENT RECEIVED" in desc.upper()
            cad_amount = (amt_raw if is_credit else -amt_raw)

            counterparty = normalize_counterparty(desc)
            source_locator = f"line={i}"
            base = f"{FY}|cc_md|{rel}|{source_locator}|{post_dt.isoformat()}|{desc}|{cad_amount}"
            tx_id = f"tx-{FY}-cc-{post_dt.strftime('%Y%m%d')}-{short_hash(base)}"

            out.append(
                Transaction(
                    transaction_id=tx_id,
                    fiscal_year=str(FY),
                    txn_date=post_dt.isoformat(),
                    source_type="cc_md",
                    source_file=rel,
                    source_locator=source_locator,
                    account_owner="personal",
                    account_name="BMO Personal Mastercard",
                    payment_method="credit_card",
                    card_last4=BMO_PERSONAL_MC_LAST4,
                    counterparty=counterparty,
                    description=desc,
                    amount=fmt_decimal(cad_amount),
                    currency="CAD",
                    cad_amount=fmt_decimal(cad_amount),
                    fx_rate_to_cad="",
                    linked_document_ids="",
                    receipt_status="missing",
                    notes="AUTO: personal statement txn (candidate; included only if linked to evidence)",
                )
            )

    return out


def build_doc_indexes(docs: list[Document]) -> tuple[dict[str, str], dict[tuple[str, str, str], list[str]]]:
    code_to_doc: dict[str, str] = {}
    key_to_docs: dict[tuple[str, str, str], list[str]] = {}
    for d in docs:
        # Confirmation codes like HW311 in TDCT files
        # NOTE: don't use word-boundaries here because stems often contain
        # underscores, and '_' counts as a word character (so '\b' won't match).
        m = re.search(r"([A-Z]{2}[0-9]{3})", Path(d.source_file).stem)
        if m:
            code_to_doc[m.group(1)] = d.document_id
        if d.document_date and d.amount and d.currency:
            key = (d.document_date, d.amount, d.currency)
            key_to_docs.setdefault(key, []).append(d.document_id)
    return code_to_doc, key_to_docs


def link_transactions_to_documents(txs: list[Transaction], docs: list[Document]) -> None:
    code_to_doc, key_to_docs = build_doc_indexes(docs)
    docs_by_id = {d.document_id: d for d in docs}

    for tx in txs:
        linked: list[str] = []
        desc_u = tx.description.upper()
        # Evidence documents typically show positive totals; transactions store signed amounts.
        # For matching by amount, use absolute CAD amount.
        tx_cad = parse_decimal(tx.cad_amount) if tx.cad_amount else None
        tx_cad_abs_s = fmt_decimal(abs(tx_cad)) if tx_cad is not None else ""
        # 1) Match TD confirmation code
        m = re.search(r"\b([A-Z]{2}[0-9]{3})\b", desc_u)
        if m and m.group(1) in code_to_doc:
            linked = [code_to_doc[m.group(1)]]

        # 2) Match by exact date+amount (CAD)
        if not linked and tx.txn_date and tx_cad_abs_s:
            key = (tx.txn_date, tx_cad_abs_s, "CAD")
            if key in key_to_docs and len(key_to_docs[key]) == 1:
                linked = list(key_to_docs[key])

        # 3) Loose match by amount within +/- 3 days and vendor keyword
        if not linked and tx.txn_date and tx_cad_abs_s:
            try:
                txd = datetime.strptime(tx.txn_date, "%Y-%m-%d").date()
            except ValueError:
                txd = None
            if txd:
                cand: list[str] = []
                for d in docs:
                    if not d.document_date or not d.amount or d.currency != "CAD":
                        continue
                    if d.amount != tx_cad_abs_s:
                        continue
                    try:
                        dd = datetime.strptime(d.document_date, "%Y-%m-%d").date()
                    except ValueError:
                        continue
                    if abs((dd - txd).days) > 3:
                        continue
                    vend = d.vendor.upper()
                    if vend and (vend[:20] in desc_u or any(w in desc_u for w in vend.split()[:2])):
                        cand.append(d.document_id)
                if len(cand) == 1:
                    linked = cand
                elif len(cand) > 1:
                    tx.receipt_status = "ambiguous"
                    tx.notes = (tx.notes + "; " if tx.notes else "") + f"Multiple doc candidates: {', '.join(cand[:5])}"

        if linked:
            tx.linked_document_ids = ";".join(linked)
            tx.receipt_status = "found"
        else:
            # Mark some rows as not_applicable
            if tx.source_type == "bank_csv" and (
                "MONTHLY PLAN FEE" in desc_u or "TAX PYT FEE" in desc_u
            ):
                tx.receipt_status = "not_applicable"
            if tx.source_type == "bank_csv" and ("GST-" in desc_u or desc_u.startswith("TX")):
                tx.receipt_status = "not_applicable"

        # If linked, propagate some merchant info into notes when useful
        if tx.linked_document_ids and not tx.notes:
            doc0 = docs_by_id.get(tx.linked_document_ids.split(";")[0])
            if doc0 and doc0.vendor and doc0.vendor not in {tx.counterparty, "TD Canada Trust"}:
                tx.notes = f"Linked evidence vendor: {doc0.vendor}"


def write_csv(path: Path, columns: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        # IMPORTANT: enforce LF line endings (not CRLF) for repo consistency.
        w = csv.DictWriter(
            f,
            fieldnames=columns,
            extrasaction="ignore",
            lineterminator="\n",
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_text_lf(path: Path, text: str) -> None:
    """Write a text file with LF-only line endings for repo consistency."""

    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(normalized)


def _parse_iso_date(s: str) -> Optional[date]:
    try:
        if not s:
            return None
        return date.fromisoformat(s)
    except Exception:
        return None


def generate_owed_candidate_report(
    docs: list[Document],
    txs_for_matching: list[Transaction],
) -> str:
    """Conservative owed-candidate report.

    We list *invoice* documents whose CAD totals do not match 1:1 with ANY single
    eligible statement transaction that has been ingested into `transactions.csv`
    (by exact absolute CAD amount).

    This is NOT evidence of being unpaid; it is only a review aid.
    """

    # Build doc_id -> linked transactions map (from link_transactions_to_documents)
    linked_by_doc: dict[str, list[Transaction]] = {}
    for t in txs_for_matching:
        if not t.linked_document_ids:
            continue
        for doc_id in [x.strip() for x in t.linked_document_ids.split(";") if x.strip()]:
            linked_by_doc.setdefault(doc_id, []).append(t)

    # Precompute CAD absolute amounts for matching
    tx_abs: list[tuple[Decimal, Transaction]] = []
    for t in txs_for_matching:
        cad = parse_decimal(t.cad_amount)
        if cad is None:
            continue
        tx_abs.append((abs(cad), t))

    def find_exact_amount_matches(target_abs: Decimal) -> list[Transaction]:
        # Conservative: any exact match anywhere in FY means it *could* be 1:1 settled.
        return [t for a, t in tx_abs if a == target_abs]

    def nearest_by_amount(target_abs: Decimal, limit: int = 3) -> list[tuple[Decimal, Transaction]]:
        # Return closest by absolute CAD amount delta (excluding exact matches).
        cands: list[tuple[Decimal, Transaction]] = []
        for a, t in tx_abs:
            d = abs(a - target_abs)
            if d == 0:
                continue
            cands.append((d, t))
        cands.sort(key=lambda x: (x[0], x[1].txn_date, x[1].transaction_id))
        return cands[:limit]

    invoice_docs = [d for d in docs if d.document_type == "invoice"]
    cad_invoice_docs: list[Document] = [d for d in invoice_docs if (d.currency or "").upper() == "CAD"]
    noncad_invoice_docs: list[Document] = [d for d in invoice_docs if (d.currency or "").upper() != "CAD"]

    candidates: list[tuple[Optional[date], str, Document, Decimal]] = []
    for d in cad_invoice_docs:
        amt = parse_decimal(d.amount)
        if amt is None or amt == 0:
            continue
        target_abs = abs(amt)
        if find_exact_amount_matches(target_abs):
            continue
        dd = _parse_iso_date(d.document_date)
        candidates.append((dd, d.vendor or "", d, target_abs))

    candidates.sort(key=lambda x: (x[0] is None, x[0] or date.max, x[1].upper(), x[2].document_id))

    lines: list[str] = []
    lines.append(f"# FY{FY} owed-candidate report (conservative)\n")
    lines.append(
        "This report lists *invoice* evidence documents whose **CAD totals** do not match 1:1 with any single "
        "eligible statement transaction in `transactions.csv` (exact match by **absolute** CAD amount).\n\n"
        "- This is a review aid only; it is **not** proof that an invoice is unpaid.\n"
        "- The matching set includes all corporate statement transactions plus only those personal statement transactions that were included in `transactions.csv` (typically evidence-linked).\n"
        "- `nearest_statement_amounts` is a hint list and may include personal transactions; check `account_owner/account_name`.\n"
        "- Follow the repo gating rules before creating any `owed.csv` entries (confirm statement coverage).\n"
    )

    lines.append("## Summary\n")
    lines.append(f"- Invoices scanned: {len(invoice_docs)}\n")
    lines.append(f"- CAD invoices with no exact 1:1 statement amount match: {len(candidates)}\n")
    lines.append(f"- Non-CAD invoices (not evaluated for 1:1): {len(noncad_invoice_docs)}\n")

    lines.append("\n## CAD invoice candidates (no exact 1:1 match)\n")
    if not candidates:
        lines.append("(none)\n")
    else:
        for dd, _vend, d, target_abs in candidates:
            lines.append(f"### {d.document_id}\n")
            lines.append(f"- document_date: `{d.document_date or ''}`\n")
            lines.append(f"- vendor: `{d.vendor}`\n")
            lines.append(f"- amount: `{d.amount} {d.currency}`\n")
            lines.append(f"- source_file: `{d.source_file}`\n")
            if d.notes:
                lines.append(f"- doc_notes: {d.notes}\n")

            linked = linked_by_doc.get(d.document_id, [])
            if linked:
                # Sort for stable, readable output
                linked_sorted = sorted(linked, key=lambda t: (t.txn_date, t.transaction_id))
                s = sum((parse_decimal(t.cad_amount) or Decimal('0')) for t in linked_sorted)
                lines.append(f"- linked_transactions: {len(linked_sorted)} (sum cad_amount = `{fmt_decimal(s)}`)\n")
                for t in linked_sorted[:10]:
                    lines.append(
                        f"  - {t.transaction_id} | {t.txn_date} | cad_amount {t.cad_amount} | {t.account_owner}/{t.account_name} | {t.description[:120]}\n"
                    )
                if len(linked_sorted) > 10:
                    lines.append(f"  - ... ({len(linked_sorted) - 10} more)\n")
                if abs(s) == target_abs and len(linked_sorted) > 1:
                    lines.append("- note: linked transactions sum to the invoice total (possible installment/split settlement)\n")
            else:
                lines.append("- linked_transactions: 0\n")

            near = nearest_by_amount(target_abs, limit=3)
            if near:
                lines.append("- nearest_statement_amounts (by abs amount delta):\n")
                for delta, t in near:
                    lines.append(
                        f"  - delta {fmt_decimal(delta)} | {t.transaction_id} | {t.txn_date} | cad_amount {t.cad_amount} | {t.account_owner}/{t.account_name} | {t.description[:120]}\n"
                    )
            lines.append("\n")

    lines.append("## Non-CAD invoices (manual review)\n")
    if not noncad_invoice_docs:
        lines.append("(none)\n")
    else:
        for d in sorted(noncad_invoice_docs, key=lambda x: (x.document_date, x.vendor.upper(), x.document_id)):
            lines.append(
                f"- {d.document_id} | {d.document_date} | {d.vendor} | {d.amount} {d.currency} | {d.source_file}\n"
            )

    return "".join(lines)


def allocation_defaults_for_tx(tx: Transaction) -> dict[str, str]:
    desc_u = tx.description.upper()
    cp_u = tx.counterparty.upper()
    cad = parse_decimal(tx.cad_amount) or Decimal("0")
    is_expense = cad < 0

    reporting = "uncategorized"
    cra_code = ""
    tax_treatment = "standard"
    ded_pct = Decimal("0")

    # Balance sheet / transfers
    if "TFR-TO C/C" in desc_u or "PAYMENT - THANK YOU" in desc_u:
        reporting = "balance_transfer"
        tax_treatment = "non_deductible"
        ded_pct = Decimal("0")
    elif "TFR-TO 6084079" in desc_u or "TFR-FR 6084079" in desc_u:
        reporting = "shareholder_transfer"
        tax_treatment = "shareholder_loan"
        ded_pct = Decimal("0")
    elif "MONTHLY PLAN FEE" in desc_u:
        reporting = "bank_fees"
        tax_treatment = "non_deductible"
        ded_pct = Decimal("0")
    elif "TAX" in desc_u or desc_u.startswith("TX") or "GST-" in desc_u:
        reporting = "tax_payment"
        tax_treatment = "non_deductible"
        ded_pct = Decimal("0")
    elif not is_expense:
        # Inflows
        reporting = "income_or_credit"
        tax_treatment = "standard"
        ded_pct = Decimal("0")
    else:
        # Expense heuristics (defaults from 10_accounting_rules.md)
        if "UBER" in desc_u or "EXPEDIA" in desc_u:
            reporting = "travel"
            cra_code = "9200"
            ded_pct = Decimal("100")
        elif "ROGERS" in desc_u:
            reporting = "telephone_utilities"
            cra_code = "9220"
            ded_pct = Decimal("100")
        elif any(k in desc_u for k in ["TAVOLA", "RESTAURANT", "BACCHUS", "RILEYS", "MEREON"]):
            reporting = "meals_entertainment"
            cra_code = "8523"
            tax_treatment = "meals_50"
            ded_pct = Decimal("50")
        elif "GUARDIAN" in desc_u or "STORAGE" in desc_u or "PARK" in desc_u:
            reporting = "rental"
            cra_code = "8910"
            ded_pct = Decimal("100")
        elif "BC REG" in desc_u or "REGISTRY" in desc_u:
            reporting = "fees_licences"
            cra_code = "8760"
            ded_pct = Decimal("100")
        else:
            # Recurring SaaS default to office expenses
            if any(k in desc_u for k in ["GOOGLE", "SLACK", "OPENAI", "MICROSOFT", "GITHUB", "JETBRAINS", "ZOHO", "NAMESPRO", "DIGITALOCEAN", "PADDLE", "CONNECTWISE", "SPLASHTOP", "SCREENCONNECT", "OPENPHONE", "QUO"]):
                reporting = "office_expenses"
                cra_code = "8810"
                ded_pct = Decimal("100")
            else:
                reporting = "office_expenses"
                cra_code = "8810"
                ded_pct = Decimal("100")

    # Capital asset candidate (conservative)
    if is_expense and any(k in desc_u for k in ["LENOVO", "APPLE"]):
        if abs(cad) >= Decimal("500"):
            reporting = "capital_asset_candidate"
            tax_treatment = "capital_asset"
            cra_code = ""
            ded_pct = Decimal("0")

    # Applies-to: shareholder transfers treated as personal
    applies_to = "personal" if tax_treatment in {"shareholder_loan"} else "corporate"

    deductible_amount = (cad * (ded_pct / Decimal("100"))) if ded_pct else Decimal("0")

    return {
        "allocation_type": "full",
        "applies_to": applies_to,
        "allocated_amount": fmt_decimal(cad),
        "allocated_gst": "0.00",
        "allocated_pst": "0.00",
        "reporting_category": reporting,
        "cra_code": cra_code,
        "deductible_percentage": fmt_decimal(ded_pct),
        "deductible_amount": fmt_decimal(deductible_amount),
        "itc_eligible_amount": "0.00",
        "tax_treatment": tax_treatment,
        "notes": "AUTO: heuristic allocation; review GST/PST and category.",
    }


def generate_allocations(txs: list[Transaction]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for idx, tx in enumerate(txs, start=1):
        base = f"{tx.transaction_id}|{idx}"
        alloc_id = f"alloc-{FY}-{short_hash(base)}"
        d = allocation_defaults_for_tx(tx)
        row = {
            "allocation_id": alloc_id,
            "transaction_id": tx.transaction_id,
            **d,
        }
        rows.append(row)
    return rows


def parse_fy2024_assets() -> list[dict[str, str]]:
    p = ROOT / "FY2024" / "financials" / "2024_Capital_Assets.md"
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    rows: list[dict[str, str]] = []
    for ln in lines:
        if not ln.strip().startswith("|"):
            continue
        if "---" in ln or "Date" in ln:
            continue
        parts = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(parts) < 3:
            continue
        date_s, desc, total_s = parts[0], parts[1], parts[2]
        if "depreciation" in desc.lower():
            continue
        m = re.search(r"(20[0-9]{2})-([0-9]{2})-([0-9]{2})", date_s)
        acq = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""
        cost = parse_decimal(total_s.replace("$", ""))
        asset_id = f"asset-{(acq or 'unknown').replace('-', '')}-{slug(desc)[:24]}-{short_hash(desc)}"
        vendor = desc.split("-")[0].strip() if "-" in desc else desc[:80]
        rows.append(
            {
                "asset_id": asset_id,
                "description": desc,
                "acquisition_date": acq,
                "cost": fmt_decimal(cost),
                "currency": "CAD",
                "cad_cost": fmt_decimal(cost),
                "vendor": vendor,
                "cca_class": "",
                "opening_ucc": "",
                "additions": "",
                "disposals": "",
                "cca_claimed": "",
                "closing_ucc": "",
                "linked_transaction_id": "",
                "linked_document_ids": "",
                "notes": "Imported from FY2024/financials/2024_Capital_Assets.md; accountant to set CCA class and UCC (no depreciation calculated here).",
            }
        )
    return rows


def generate_asset_additions_from_allocations(
    txs: list[Transaction],
    alloc_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    tx_by_id = {t.transaction_id: t for t in txs}
    assets: list[dict[str, str]] = []
    for a in alloc_rows:
        if a.get("tax_treatment") != "capital_asset":
            continue
        tx = tx_by_id.get(a["transaction_id"])
        if not tx:
            continue
        cad = abs(parse_decimal(tx.cad_amount) or Decimal("0"))
        if cad <= 0:
            continue
        desc = f"Capital asset candidate from {tx.counterparty}: {tx.description[:80]}"
        asset_id = f"asset-{tx.txn_date.replace('-', '')}-{slug(tx.counterparty)}-{short_hash(tx.transaction_id)}"
        assets.append(
            {
                "asset_id": asset_id,
                "description": desc,
                "acquisition_date": tx.txn_date,
                "cost": fmt_decimal(cad),
                "currency": "CAD",
                "cad_cost": fmt_decimal(cad),
                "vendor": tx.counterparty,
                "cca_class": "",
                "opening_ucc": "",
                "additions": fmt_decimal(cad),
                "disposals": "",
                "cca_claimed": "",
                "closing_ucc": "",
                "linked_transaction_id": tx.transaction_id,
                "linked_document_ids": tx.linked_document_ids,
                "notes": "AUTO: flagged as capital asset candidate (no depreciation calculated). Accountant/owner to confirm asset vs expense and assign CCA class.",
            }
        )
    return assets


def main() -> int:
    # 1) Documents (evidence), excluding statement sources
    docs = [build_document(p) for p in sorted(iter_evidence_md_files())]
    write_csv(
        NORM_DIR / "documents.csv",
        DOC_COLUMNS,
        (d.__dict__ for d in docs),
    )

    # 2) Transactions (posted economic reality)
    # Corporate statement sources (always included)
    txs: list[Transaction] = []
    txs.extend(parse_bank_transactions())
    txs.extend(parse_td_business_visa_transactions())

    # Personal statement sources: parse as *candidates*, but only include rows
    # that can be linked to evidence documents (reimbursable/mixed-use only).
    personal_candidates: list[Transaction] = []
    personal_candidates.extend(parse_td_personal_visa_transactions())
    personal_candidates.extend(parse_bmo_personal_mastercard_transactions())
    txs.extend(personal_candidates)

    # Link to evidence documents where confidently matchable
    link_transactions_to_documents(txs, docs)

    # Keep an unfiltered list for owed-candidate matching/reporting.
    # This may include personal statement candidates that will NOT be written to
    # transactions.csv (because they are not linked to evidence).
    txs_for_matching = list(txs)

    # Filter personal transactions down to reimbursable/mixed-use only
    # (i.e., those with evidence links, or clearly ambiguous evidence matches).
    txs = [
        t
        for t in txs
        if (t.account_owner != "personal") or (t.receipt_status in {"found", "ambiguous"})
    ]

    # Conservative owed-candidate report (does NOT write owed.csv rows)
    owed_report = generate_owed_candidate_report(docs, txs_for_matching)
    # Write to FY2025/normalized/reports/ (preferred) and keep a copy at the
    # legacy top-level path for convenience/back-compat.
    reports_dir = NORM_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    owed_report_path = reports_dir / "owed_candidates_report.md"
    write_text_lf(owed_report_path, owed_report)
    write_text_lf(NORM_DIR / "owed_candidates_report.md", owed_report)

    write_csv(
        NORM_DIR / "transactions.csv",
        TX_COLUMNS,
        (t.__dict__ for t in txs),
    )

    # 3) Allocations (classification defaults)
    allocs = generate_allocations(txs)
    write_csv(
        NORM_DIR / "allocations.csv",
        ALLOC_COLUMNS,
        allocs,
    )

    # 4) Assets (carry-forward + additions candidates)
    assets = parse_fy2024_assets()
    assets.extend(generate_asset_additions_from_allocations(txs, allocs))
    write_csv(
        NORM_DIR / "assets.csv",
        ASSET_COLUMNS,
        assets,
    )

    # 5) Owed (A/P & A/R) — placeholder table for installment/remaining balances.
    # Populated manually or by future heuristics; keep schema present for year-end carry-forward.
    owed_rows: list[dict[str, str]] = []
    write_csv(
        NORM_DIR / "owed.csv",
        OWED_COLUMNS,
        owed_rows,
    )

    print(
        f"Wrote {len(docs)} documents, {len(txs)} transactions, {len(allocs)} allocations, {len(assets)} assets, {len(owed_rows)} owed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
