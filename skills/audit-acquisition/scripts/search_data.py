#!/usr/bin/env python3
"""Summarise a Search Console (or analytics) export the user supplied. Standard library only. Reads files; never fetches.

Usage:
    python3 scripts/search_data.py --queries Queries.csv --pages Pages.csv
    python3 scripts/search_data.py --queries Queries.csv --pages Pages.csv --brand "tallyhouse,tally house"
    python3 scripts/search_data.py --pages Pages-last.csv --previous-pages Pages-prev.csv
    python3 scripts/search_data.py --analytics landing-pages.csv           # sessions by channel or landing page
    Options: --min-impressions 100 (for "impressions but no clicks"), --json

Reads the Search Console performance export (Queries.csv, Pages.csv), including the "compare" export whose columns
read "Last 3 months Clicks" / "Previous 3 months Clicks", or API-style columns (query, page, clicks, impressions,
ctr, position). Reports, from the rows in the file only:
  - totals, and branded vs non-branded queries if --brand is given
  - top queries by clicks and by impressions
  - CTR by position band (1-3, 4-10, 11-20, 21+), weighted: band clicks / band impressions
  - queries in the top 3 positions whose CTR is under half their band's own CTR
  - pages with impressions but no clicks
  - pages and queries losing clicks between the two periods, with the position change
It never estimates search volume, traffic or rankings beyond the file. Row totals can be lower than the Search
Console chart totals, because Search Console leaves out anonymised queries.
"""

import csv
import json
import re
import sys

BANDS = [("1-3", 0, 3.5), ("4-10", 3.5, 10.5), ("11-20", 10.5, 20.5), ("21+", 20.5, 1e9)]


def num(v):
    v = (v or "").strip().replace(",", "").replace("%", "")
    try:
        return float(v)
    except ValueError:
        return None


def load(path):
    """Return (key_name, rows, periods). rows: {key: {period: {clicks, impressions, position}}}."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        data = list(reader)
    key_col = 0
    metrics = {}  # (period, metric) -> col
    for i, h in enumerate(header):
        hl = h.strip().lower()
        m = re.match(r"^(.*?)\s*(clicks|impressions|ctr|position)$", hl)
        if m and i != key_col:
            metrics[(m.group(1).strip() or "current", m.group(2))] = i
    periods = []
    for (p, _m) in metrics:
        if p not in periods:
            periods.append(p)
    rows = {}
    for r in data:
        if not r or not r[key_col].strip():
            continue
        k = r[key_col].strip()
        rows[k] = {}
        for p in periods:
            rec = {m: num(r[metrics[(p, m)]]) if (p, m) in metrics and metrics[(p, m)] < len(r) else None
                   for m in ("clicks", "impressions", "position")}
            rows[k][p] = rec
    return header[key_col].strip(), rows, periods


def pick_periods(periods):
    """Current period first, previous second (if any)."""
    cur = next((p for p in periods if re.search(r"last|current|this", p)), periods[0])
    prev = next((p for p in periods if p != cur), None)
    return cur, prev


def pct(c, i):
    return f"{(c / i * 100):.1f}%" if i else "n/a"


def band_of(pos):
    for name, lo, hi in BANDS:
        if pos is not None and lo <= pos < hi:
            return name
    return None


def summarise_queries(rows, cur, prev, brand, min_impr):
    out = {}
    q = {k: v[cur] for k, v in rows.items() if v[cur]["impressions"] is not None}
    tc = sum(v["clicks"] or 0 for v in q.values())
    ti = sum(v["impressions"] or 0 for v in q.values())
    out["totals"] = {"queries": len(q), "clicks": tc, "impressions": ti, "ctr": pct(tc, ti)}
    if brand:
        isb = lambda k: any(b in k.lower() for b in brand)
        bc = sum(v["clicks"] or 0 for k, v in q.items() if isb(k))
        bi = sum(v["impressions"] or 0 for k, v in q.items() if isb(k))
        out["branded"] = {"clicks": bc, "impressions": bi, "ctr": pct(bc, bi), "share_of_clicks": pct(bc, tc)}
        out["non_branded"] = {"clicks": tc - bc, "impressions": ti - bi, "ctr": pct(tc - bc, ti - bi),
                              "share_of_clicks": pct(tc - bc, tc)}
    out["top_by_clicks"] = [(k, v["clicks"], v["impressions"], pct(v["clicks"] or 0, v["impressions"]), v["position"])
                            for k, v in sorted(q.items(), key=lambda x: -(x[1]["clicks"] or 0))[:10]]
    out["top_by_impressions"] = [(k, v["clicks"], v["impressions"], pct(v["clicks"] or 0, v["impressions"]), v["position"])
                                 for k, v in sorted(q.items(), key=lambda x: -(x[1]["impressions"] or 0))[:10]]
    bands = band_table(q)
    if brand:
        out["ctr_by_position_band_non_branded"] = {b: dict(s, ctr=pct(s["clicks"], s["impressions"]))
                                                   for b, s in band_table({k: v for k, v in q.items() if not isb(k)}).items()}
    out["ctr_by_position_band"] = {b: dict(s, ctr=pct(s["clicks"], s["impressions"])) for b, s in bands.items()}
    top = bands.get("1-3")
    low = []
    if top and top["impressions"]:
        band_ctr = top["clicks"] / top["impressions"]
        for k, v in q.items():
            if band_of(v["position"]) == "1-3" and (v["impressions"] or 0) >= min_impr:
                c = (v["clicks"] or 0) / v["impressions"]
                if c < band_ctr / 2:
                    low.append((k, v["clicks"], v["impressions"], pct(v["clicks"] or 0, v["impressions"]), v["position"]))
    out["top3_low_ctr"] = low
    out["impressions_no_clicks"] = [(k, v["impressions"], v["position"]) for k, v in q.items()
                                    if (v["clicks"] or 0) == 0 and (v["impressions"] or 0) >= min_impr]
    if prev:
        out["losing_clicks"] = changes(rows, cur, prev)
    return out


def band_table(q):
    bands = {}
    for k, v in q.items():
        b = band_of(v["position"])
        if b:
            s = bands.setdefault(b, {"queries": 0, "clicks": 0, "impressions": 0})
            s["queries"] += 1
            s["clicks"] += v["clicks"] or 0
            s["impressions"] += v["impressions"] or 0
    order = [n for n, _, _ in BANDS]
    return dict(sorted(bands.items(), key=lambda x: order.index(x[0])))


def changes(rows, cur, prev):
    ch = []
    for k, v in rows.items():
        c1, c0 = v[cur]["clicks"], v.get(prev, {}).get("clicks")
        if c1 is None or c0 is None or c1 >= c0:
            continue
        p1, p0 = v[cur]["position"], v[prev]["position"]
        ch.append((k, c0, c1, c1 - c0, f"{(c1 - c0) / c0 * 100:.0f}%" if c0 else "n/a", p0, p1))
    return sorted(ch, key=lambda x: x[3])


def summarise_pages(rows, cur, prev, min_impr):
    p = {k: v[cur] for k, v in rows.items() if v[cur]["impressions"] is not None}
    tc = sum(v["clicks"] or 0 for v in p.values())
    ti = sum(v["impressions"] or 0 for v in p.values())
    out = {"totals": {"pages": len(p), "clicks": tc, "impressions": ti, "ctr": pct(tc, ti)},
           "impressions_no_clicks": [(k, v["impressions"], v["position"]) for k, v in p.items()
                                     if (v["clicks"] or 0) == 0 and (v["impressions"] or 0) >= min_impr]}
    if prev:
        out["losing_clicks"] = changes(rows, cur, prev)
    return out


def merge_previous(rows, prev_rows):
    for k, v in prev_rows.items():
        rows.setdefault(k, {"current": {"clicks": None, "impressions": None, "position": None}})
        rows[k]["previous"] = list(v.values())[0]
    for k in rows:
        rows[k].setdefault("previous", {"clicks": None, "impressions": None, "position": None})
    return rows


def analytics(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        lines = [l for l in f if l.strip() and not l.startswith("#")]
    reader = csv.reader(lines)
    header = next(reader)
    data = list(reader)
    mcol = next((i for i, h in enumerate(header) if re.search(r"sessions|users|visits", h, re.I)), None)
    if mcol is None:
        return {"error": "no Sessions, Users or Visits column found"}
    dim = header[0]
    rows = [(r[0], num(r[mcol]) or 0) for r in data if r and r[0].strip() and not r[0].lower().startswith(("total", "grand total"))]
    total = sum(v for _, v in rows)
    return {"dimension": dim, "metric": header[mcol], "total": total,
            "rows": [(k, v, pct(v, total)) for k, v in sorted(rows, key=lambda x: -x[1])[:15]]}


def fmt(v):
    if isinstance(v, float) and v.is_integer():
        return f"{int(v):,}"
    return f"{v:,}" if isinstance(v, (int, float)) else str(v)


def main():
    args = sys.argv[1:]
    opts = {}
    for flag in ("--queries", "--pages", "--previous-pages", "--previous-queries", "--brand", "--min-impressions", "--analytics"):
        if flag in args:
            i = args.index(flag)
            opts[flag] = args[i + 1]
            del args[i:i + 2]
    if not any(k in opts for k in ("--queries", "--pages", "--analytics")):
        print(__doc__)
        return 2
    brand = [b.strip().lower() for b in opts.get("--brand", "").split(",") if b.strip()]
    min_impr = int(opts.get("--min-impressions", 100))
    report = {"source": {k.strip("-"): v for k, v in opts.items() if k not in ("--brand", "--min-impressions")},
              "note": "From the export's rows only. No search volume, traffic or ranking estimates."}
    for kind, prevflag in (("queries", "--previous-queries"), ("pages", "--previous-pages")):
        if f"--{kind}" not in opts:
            continue
        _, rows, periods = load(opts[f"--{kind}"])
        if prevflag in opts:
            _, prows, _ = load(opts[prevflag])
            rows = {k: {"current": list(v.values())[0]} for k, v in rows.items()}
            rows = merge_previous(rows, prows)
            periods = ["current", "previous"]
        cur, prev = pick_periods(periods)
        report["periods"] = {"current": cur, "previous": prev}
        report[kind] = summarise_queries(rows, cur, prev, brand, min_impr) if kind == "queries" \
            else summarise_pages(rows, cur, prev, min_impr)
    if "--analytics" in opts:
        report["analytics"] = analytics(opts["--analytics"])
    if "--json" in args:
        print(json.dumps(report, indent=1))
        return 0
    per = report.get("periods", {})
    if per:
        print(f"Periods: current = '{per['current']}'" + (f", previous = '{per['previous']}'" if per.get("previous") else ""))
    print(report["note"] + "\n")
    q = report.get("queries")
    if q:
        t = q["totals"]
        print(f"QUERIES: {t['queries']} rows · {fmt(t['clicks'])} clicks · {fmt(t['impressions'])} impressions · CTR {t['ctr']}")
        if "branded" in q:
            b, n = q["branded"], q["non_branded"]
            print(f"  branded ({', '.join(brand)}): {fmt(b['clicks'])} clicks ({b['share_of_clicks']} of clicks), CTR {b['ctr']}")
            print(f"  non-branded: {fmt(n['clicks'])} clicks ({n['share_of_clicks']} of clicks), {fmt(n['impressions'])} impressions, CTR {n['ctr']}")
        print("\n  CTR by position band (clicks / impressions):")
        print("  | Band | Queries | Clicks | Impressions | CTR |\n  |---|---|---|---|---|")
        for b, s in q["ctr_by_position_band"].items():
            print(f"  | {b} | {s['queries']} | {fmt(s['clicks'])} | {fmt(s['impressions'])} | {s['ctr']} |")
        if "ctr_by_position_band_non_branded" in q:
            print("\n  CTR by position band, non-branded queries only:")
            print("  | Band | Queries | Clicks | Impressions | CTR |\n  |---|---|---|---|---|")
            for b, s in q["ctr_by_position_band_non_branded"].items():
                print(f"  | {b} | {s['queries']} | {fmt(s['clicks'])} | {fmt(s['impressions'])} | {s['ctr']} |")
        print("\n  Top queries by clicks: query · clicks · impressions · CTR · position")
        for r in q["top_by_clicks"]:
            print(f"   - {r[0]} · {fmt(r[1])} · {fmt(r[2])} · {r[3]} · {r[4]}")
        print("\n  Top queries by impressions:")
        for r in q["top_by_impressions"]:
            print(f"   - {r[0]} · {fmt(r[1])} · {fmt(r[2])} · {r[3]} · {r[4]}")
        if q["top3_low_ctr"]:
            print("\n  Top-3 positions with CTR under half the band's own CTR:")
            for r in q["top3_low_ctr"]:
                print(f"   - {r[0]}: {fmt(r[1])} clicks from {fmt(r[2])} impressions ({r[3]}) at position {r[4]}")
        if q["impressions_no_clicks"]:
            print(f"\n  Queries with {min_impr}+ impressions and no clicks:")
            for r in q["impressions_no_clicks"]:
                print(f"   - {r[0]}: {fmt(r[1])} impressions, position {r[2]}")
        if q.get("losing_clicks"):
            print("\n  Queries losing clicks: query · previous → current clicks (change) · position previous → current")
            for r in q["losing_clicks"][:10]:
                print(f"   - {r[0]} · {fmt(r[1])} → {fmt(r[2])} ({fmt(r[3])}, {r[4]}) · {r[5]} → {r[6]}")
        print()
    p = report.get("pages")
    if p:
        t = p["totals"]
        print(f"PAGES: {t['pages']} rows · {fmt(t['clicks'])} clicks · {fmt(t['impressions'])} impressions · CTR {t['ctr']}")
        if p["impressions_no_clicks"]:
            print(f"  Pages with {min_impr}+ impressions and no clicks:")
            for r in p["impressions_no_clicks"]:
                print(f"   - {r[0]}: {fmt(r[1])} impressions, position {r[2]}")
        if p.get("losing_clicks"):
            print("  Pages losing clicks: page · previous → current clicks (change) · position previous → current")
            for r in p["losing_clicks"][:10]:
                print(f"   - {r[0]} · {fmt(r[1])} → {fmt(r[2])} ({fmt(r[3])}, {r[4]}) · {r[5]} → {r[6]}")
        print()
    a = report.get("analytics")
    if a:
        if "error" in a:
            print(f"ANALYTICS: {a['error']}")
        else:
            print(f"ANALYTICS: {a['metric']} by {a['dimension']} · total {fmt(a['total'])}")
            for r in a["rows"]:
                print(f"   - {r[0]}: {fmt(r[1])} ({r[2]})")
    if q or p:
        print("Note: row totals can be lower than Search Console's chart totals (anonymised queries are left out).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
