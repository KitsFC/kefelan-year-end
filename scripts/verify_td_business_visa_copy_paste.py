#!/usr/bin/env python3
"""Verifier: reconcile TD Business Visa manual copy/paste vs normalized transactions.csv.

Constraints:
- Does NOT modify generator scripts.
- Best-effort parsing of messy copy/paste formatting (multiple tx per line, continuation lines, FX lines).

Usage:
  python3 scripts/verify_td_business_visa_copy_paste.py \
    --copy FY2025/transactions/2_liabilities/TD_Business_Visa_2025_copy_paste.txt \
    --csv  FY2025/normalized/transactions.csv
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Dict, List, Tuple

MONTHS = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
          "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}
TX_START_RE = re.compile(r"\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+([0-9]{1,2})\s+"
                         r"(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+([0-9]{1,2})\b")
AMOUNT_RE = re.compile(r"(-?)\$([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+)\.([0-9]{2})")
FX1_RE = re.compile(r"^FOREIGN CURRENCY\s+([0-9][0-9,]*\.[0-9]{2})\s+([A-Z]{3})\s*$")
FX2_RE = re.compile(r"^@ EXCHANGE RATE\s+([0-9]+\.[0-9]+)\s*$")
MONTH_DAY_SMOOSH_RE = re.compile(r"\b(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)([0-9]{1,2})\b")

Q = Decimal("0.01")

def dec2(s: str) -> Decimal:
    return Decimal(s).quantize(Q, rounding=ROUND_HALF_UP)


def norm_tokens(s: str) -> set[str]:
    s = re.sub(r"[^A-Za-z0-9]+", " ", (s or "").upper()).strip()
    return {t for t in s.split() if len(t) >= 3}


@dataclass
class CopyTx:
    post_month: int
    post_day: int
    post_year: int | None
    cad_amount: Decimal
    desc: str

    def post_date(self) -> date:
        assert self.post_year is not None
        return date(self.post_year, self.post_month, self.post_day)


def parse_segment(seg: str) -> CopyTx | None:
    m = TX_START_RE.match(seg)
    if not m:
        return None
    _t_mon, _t_day, p_mon, p_day = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
    rest = seg[m.end():].strip()
    ams = list(AMOUNT_RE.finditer(rest))
    if not ams:
        return None
    am = ams[-1]
    sign = -1 if am.group(1) == "-" else 1
    val = Decimal(am.group(2).replace(",", "") + "." + am.group(3))
    copy_amt = Decimal(sign) * val
    cad_amt = (Decimal("-1") * copy_amt).quantize(Q, rounding=ROUND_HALF_UP)  # statement format => normalize to CSV sign
    desc = rest[:am.start()].strip()
    return CopyTx(post_month=MONTHS[p_mon], post_day=p_day, post_year=None, cad_amount=cad_amt, desc=desc)


def parse_copy_paste(path: Path) -> List[CopyTx]:
    txs: List[CopyTx] = []
    last: CopyTx | None = None

    def fix_line(s: str) -> str:
        # Common OCR / copy-paste artifacts observed in this file.
        s = re.sub(r"\bUL\b", "JUL", s)  # e.g. "UL 7" => "JUL 7"
        s = MONTH_DAY_SMOOSH_RE.sub(r"\1 \2", s)  # e.g. "SEP7" => "SEP 7"
        return s

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = fix_line(raw.strip())
        if not line or line.startswith("TRANSACTION POSTING DATE"):
            continue
        starts = list(TX_START_RE.finditer(line))
        if starts:
            for i, st in enumerate(starts):
                end = starts[i + 1].start() if i + 1 < len(starts) else len(line)
                seg = line[st.start():end].strip()
                tx = parse_segment(seg)
                if tx:
                    txs.append(tx)
                    last = tx
        else:
            if FX1_RE.match(line) or FX2_RE.match(line):
                # FX lines are informational; we ignore for matching.
                continue
            if last:
                last.desc = (last.desc + " " + line).strip()
    return txs


def assign_years_in_order(txs: List[CopyTx]) -> None:
    if not txs:
        return
    months = [t.post_month for t in txs]
    start_year = 2024 if (months[0] == 12 and 1 in months[1:]) else 2025
    y = start_year
    prev_m = months[0]
    for t in txs:
        if t.post_month < prev_m:
            y += 1
        t.post_year = y
        prev_m = t.post_month


def load_csv_subset(path: Path) -> List[dict]:
    with path.open('r', encoding='utf-8', newline='') as f:
        r = csv.DictReader(f)
        rows = [row for row in r if (row.get('source_file') or '').endswith('TD_Business_Visa_2025.md')]
    return rows


def best_match(copy: CopyTx, cands: List[dict]) -> int:
    ct = norm_tokens(copy.desc)
    best_i, best_s = 0, -1
    for i, row in enumerate(cands):
        s = norm_tokens((row.get('counterparty') or '') + ' ' + (row.get('description') or ''))
        score = len(ct & s)
        if score > best_s:
            best_s, best_i = score, i
    return best_i


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--copy', required=True)
    ap.add_argument('--csv', required=True)
    ap.add_argument('--year', type=int, default=2025, help='Posting year to reconcile (default: 2025)')
    args = ap.parse_args()

    copy_path = Path(args.copy)
    csv_path = Path(args.csv)

    copy_txs = parse_copy_paste(copy_path)
    assign_years_in_order(copy_txs)
    copy_yr = [t for t in copy_txs if t.post_year == args.year]

    csv_rows = load_csv_subset(csv_path)

    idx: Dict[Tuple[str, Decimal], List[dict]] = {}
    for row in csv_rows:
        d = (row.get('txn_date') or '').strip()
        a_raw = (row.get('cad_amount') or '').strip()
        if not d or not a_raw:
            continue
        try:
            a = dec2(a_raw)
        except Exception:
            continue
        k = (d, a)
        idx.setdefault(k, []).append(row)

    missing: List[CopyTx] = []
    for t in copy_yr:
        k = (t.post_date().isoformat(), t.cad_amount)
        cands = idx.get(k) or []
        if not cands:
            missing.append(t)
            continue
        j = best_match(t, cands) if len(cands) > 1 else 0
        cands.pop(j)
        if not cands:
            idx.pop(k, None)

    extra = [row for rows in idx.values() for row in rows]

    print('--- TD Business Visa copy/paste reconciliation ---')
    print('copy parsed tx:', len(copy_txs), f'(year {args.year}: {len(copy_yr)})')
    print('csv TD_Business_Visa_2025.md tx:', len(csv_rows))
    print('missing (copy->csv):', len(missing))
    print('extra (csv->copy):', len(extra))

    if missing:
        print('\nMissing sample:')
        for t in missing[:30]:
            print(f"  {t.post_date().isoformat()}  {t.cad_amount:>8}  {t.desc[:90]}")
    if extra:
        print('\nExtra sample:')
        for r in extra[:30]:
            print(f"  {r.get('txn_date')}  {r.get('cad_amount'):>8}  {(r.get('counterparty') or '')} | {(r.get('description') or '')[:70]} | {r.get('source_locator')}")

    return 0 if (not missing and not extra) else 2


if __name__ == '__main__':
    raise SystemExit(main())

