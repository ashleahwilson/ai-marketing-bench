#!/usr/bin/env python3
"""Compute funnel step drop-off from an analytics export the user supplied. Standard library only.

Usage:
    python3 scripts/funnel.py export.csv                         # columns detected automatically
    python3 scripts/funnel.py export.csv --step event --count users --segment device
    python3 scripts/funnel.py export.csv --order landing_view,form_start,form_submit

The CSV needs one row per step (or per step and segment) with a step name and a count. Column detection:
  step:    a column named step, stage, event, event_name, page or funnel_step (else the first text column)
  count:   users, sessions, count, events, total_users or value (else the last numeric column)
  segment: device, device_category, segment, channel or source, if present
Steps keep the order they first appear in, unless --order is given.

Prints, for the total and for each segment: each step's count, the share that continued from the previous step,
the drop-off, and the share of the first step. It flags:
  - TRACKING: a step larger than the step before it (double counting, or a step tracked on another page)
  - SMALL: a step whose previous step has under 100, too few to compare or conclude from
  - BIGGEST DROP: the step-to-step transition that loses the largest share
It never projects, forecasts or estimates a lift.
"""

import argparse
import csv
import sys

STEP_NAMES = ("step", "stage", "event", "event_name", "page", "funnel_step", "step_name")
COUNT_NAMES = ("users", "sessions", "count", "events", "total_users", "value", "visitors", "conversions")
SEGMENT_NAMES = ("device", "device_category", "segment", "channel", "source", "medium")
SMALL = 100


def num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


def detect(header, rows, want, names, numeric):
    if want:
        if want not in header:
            raise SystemExit(f"column '{want}' not found; columns are: {', '.join(header)}")
        return want
    lower = {h.lower().strip(): h for h in header}
    for n in names:
        if n in lower:
            return lower[n]
    cols = [h for h in header if all((num(r[h]) is not None) == numeric for r in rows if r.get(h, "") != "")]
    if not cols:
        return None
    return cols[-1] if numeric else cols[0]


def table(steps, counts):
    out, first, worst = [], None, None
    flags = []
    print("| Step | Count | Continued from previous | Drop-off | Share of first step |")
    print("|---|---|---|---|---|")
    prev = None
    for s in steps:
        c = counts.get(s, 0)
        if first is None:
            first = c
            print(f"| {s} | {c:,.0f} | – | – | 100% |")
        else:
            cont = (c / prev * 100) if prev else 0
            share = (c / first * 100) if first else 0
            print(f"| {s} | {c:,.0f} | {cont:.1f}% | {100 - cont:.1f}% | {share:.2f}% |")
            if c > prev:
                flags.append(f"TRACKING: '{s}' ({c:,.0f}) is larger than the step before it ({prev:,.0f}). Fix the tracking before reading this step.")
            elif worst is None or (100 - cont) > worst[1]:
                worst = (f"{prev_name} -> {s}", 100 - cont)
            if prev < SMALL:
                flags.append(f"SMALL: '{prev_name}' has {prev:,.0f}; too few to compare or conclude from '{s}'.")
        prev, prev_name = c, s
    if worst:
        flags.append(f"BIGGEST DROP: {worst[0]} loses {worst[1]:.1f}%.")
    if len(steps) > 1 and first:
        print(f"\nFirst to last step: {counts.get(steps[-1], 0) / first * 100:.2f}%")
    for f in flags:
        print(f)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--step")
    ap.add_argument("--count")
    ap.add_argument("--segment")
    ap.add_argument("--order", help="comma-separated step order; steps not listed are left out")
    a = ap.parse_args()
    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("no rows in the export")
    header = list(rows[0].keys())
    step_col = detect(header, rows, a.step, STEP_NAMES, numeric=False)
    count_col = detect(header, rows, a.count, COUNT_NAMES, numeric=True)
    seg_col = a.segment or next((h for h in header if h.lower().strip() in SEGMENT_NAMES), None)
    if not step_col or not count_col:
        raise SystemExit("couldn't find a step column and a count column; name them with --step and --count")
    steps, totals, segs = [], {}, {}
    for r in rows:
        s, c = r[step_col].strip(), num(r[count_col])
        if not s or c is None:
            continue
        if s not in steps:
            steps.append(s)
        totals[s] = totals.get(s, 0) + c
        if seg_col:
            g = r[seg_col].strip() or "(blank)"
            segs.setdefault(g, {})
            segs[g][s] = segs[g].get(s, 0) + c
    if a.order:
        wanted = [x.strip() for x in a.order.split(",") if x.strip()]
        missing = [x for x in wanted if x not in steps]
        if missing:
            print(f"NOTE: steps not in the export: {', '.join(missing)}")
        steps = [x for x in wanted if x in steps]
    print(f"Columns used: step = {step_col}, count = {count_col}" + (f", segment = {seg_col}" if seg_col else ""))
    print(f"\n## All {'segments' if seg_col else 'rows'}\n")
    table(steps, totals)
    for g in sorted(segs):
        print(f"\n## {seg_col} = {g}\n")
        table(steps, segs[g])
    print("\nThese are observed counts for the export's date range only. Don't project them forward or estimate a lift from them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
