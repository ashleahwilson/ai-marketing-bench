#!/usr/bin/env python3
"""Find which customer segments win, how big and how fast their deals are, and which churn. Standard library only.

Usage:
    python3 scripts/analyze_customers.py <customers.csv> [more.csv ...]
        [--map outcome="Deal Stage",deal="ARR (CAD)"] [--by industry,locations_band]
        [--cross industry,locations_band] [--out icp/analysis.json]

Reads a customer list or CRM export. Columns are matched by common names (see FIELDS); use --map for others.
Each row needs an outcome: won / active customer, lost, churned (or a churn date), or open (excluded).

Prints a markdown report and writes JSON (--out) that the self-check uses to trace every percentage.
Sample-size rules, applied everywhere:
  - a rate is shown as a percentage only when its denominator is 10 or more; otherwise as "3 of 4"
  - a median is shown only when there are 5 or more values; otherwise the values are listed
  - each segment is labelled by its closed records: under 5 "anecdote", 5-9 "hypothesis", 10+ "evidence"
  - under 10 closed records in total, the whole dataset is a small sample: counts only, every finding a hypothesis
"""

import argparse
import csv
import datetime as dt
import json
import re
import statistics
import sys
from collections import Counter, defaultdict

FIELDS = {
    "company": ["company", "account", "account name", "customer", "company name", "organization", "organisation", "name", "client"],
    "outcome": ["stage", "deal stage", "status", "outcome", "result", "closed won", "won", "opportunity stage", "lifecycle stage"],
    "industry": ["industry", "vertical", "sector", "segment", "category", "practice type", "type"],
    "employees": ["employees", "headcount", "staff", "employee count", "company size", "size", "fte", "team size"],
    "locations": ["locations", "sites", "clinics", "stores", "branches", "number of locations", "location count", "offices"],
    "country": ["country"],
    "region": ["region", "province", "state", "province state", "geography", "geo", "territory"],
    "tech": ["current scheduling", "tech", "tech stack", "stack", "system", "current system", "platform", "current tool", "crm", "pms", "incumbent"],
    "source": ["lead source", "source", "channel", "origin", "acquisition channel"],
    "deal": ["acv", "acv cad", "arr", "arr cad", "deal size", "amount", "contract value", "annual value", "deal value", "value", "revenue"],
    "cycle": ["sales cycle days", "sales cycle", "cycle", "days to close", "cycle days", "time to close"],
    "created": ["created", "created date", "opened", "create date", "first contact"],
    "closed": ["closed", "close date", "closed date", "won date"],
    "since": ["customer since", "start date", "since", "go live", "contract start"],
    "churn_date": ["churn date", "churned date", "cancelled", "canceled", "cancel date", "end date", "churned on"],
    "reason": ["reason", "loss reason", "churn reason", "lost reason", "closed lost reason", "notes"],
}
WON = {"won", "closed won", "customer", "active", "active customer", "yes", "true", "y", "1", "live", "signed", "current"}
LOST = {"lost", "closed lost", "no", "false", "n", "0", "dead", "disqualified lost", "rejected"}
CHURNED = {"churned", "churn", "cancelled", "canceled", "former customer", "inactive", "lapsed", "closed churned"}
OPEN = {"open", "negotiation", "proposal", "demo", "discovery", "qualified", "pipeline", "in progress", "trial", "evaluation"}


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def match_columns(headers, overrides):
    cols, used = {}, set()
    for f, col in overrides.items():
        hit = next((h for h in headers if norm(h) == norm(col)), None)
        if hit is None:
            sys.exit(f"--map: no column named '{col}'. Columns are: {', '.join(headers)}")
        cols[f], used = hit, used | {hit}
    for exact in (True, False):
        for f, syns in FIELDS.items():
            if f in cols:
                continue
            for h in headers:
                if h in used:
                    continue
                n = norm(h)
                if (exact and n in syns) or (not exact and any(re.search(rf"\b{re.escape(s)}\b", n) for s in syns if len(s) > 3)):
                    cols[f] = h
                    used.add(h)
                    break
    return cols


def num(v):
    if v is None:
        return None
    s = str(v).strip().lower().replace(",", "")
    s = re.sub(r"(cad|usd|eur|gbp|\$|€|£|days?|d)\s*$", "", s).strip()
    s = s.lstrip("$€£").strip()
    mult = 1
    if s.endswith("k"):
        s, mult = s[:-1], 1000
    elif s.endswith("m"):
        s, mult = s[:-1], 1000000
    try:
        return float(s) * mult
    except ValueError:
        return None


AMBIGUOUS = Counter()


def date(v):
    s = (v or "").strip()
    m = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$", s)
    if m:
        a, b, y = (int(x) for x in m.groups())
        if a > 12:
            a, b = b, a
        elif b <= 12 and a != b:
            AMBIGUOUS["dates read as month/day (could be day/month)"] += 1
        try:
            return dt.date(y, a, b)
        except ValueError:
            return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d %Y", "%d %b %Y", "%Y-%m"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def band(n, edges):
    if n is None:
        return None
    for lo, hi, label in edges:
        if lo <= n <= hi:
            return label
    return None


LOC_BANDS = [(0, 1, "1"), (2, 4, "2-4"), (5, 19, "5-19"), (20, 10 ** 9, "20+")]
EMP_BANDS = [(0, 9, "1-9"), (10, 49, "10-49"), (50, 199, "50-199"), (200, 999, "200-999"), (1000, 10 ** 9, "1000+")]


def outcome(row, cols):
    raw = norm(row.get(cols.get("outcome", ""), ""))
    churn = (row.get(cols.get("churn_date", ""), "") or "").strip()
    if raw in CHURNED or (churn and raw not in LOST and raw not in OPEN):
        return "churned"
    if raw in WON:
        return "won"
    if raw in LOST:
        return "lost"
    if raw in OPEN or not raw:
        return "open" if raw else None
    if "won" in raw:
        return "won"
    if "lost" in raw:
        return "lost"
    if "churn" in raw or "cancel" in raw:
        return "churned"
    return None


def load(paths, overrides):
    rows, cols, excluded, seen = [], None, Counter(), set()
    for p in paths:
        with open(p, newline="", encoding="utf-8-sig") as f:
            r = csv.DictReader(f)
            headers = r.fieldnames or []
            c = match_columns(headers, overrides)
            cols = cols or c
            for raw in r:
                if not any((v or "").strip() for v in raw.values()):
                    continue
                key = norm(raw.get(c.get("company", ""), "")) or json.dumps(raw, sort_keys=True)
                o = outcome(raw, c)
                if o is None:
                    excluded["no recognizable outcome"] += 1
                    continue
                if o == "open":
                    excluded["open deal (not closed)"] += 1
                    continue
                dkey = (key, o)
                if dkey in seen:
                    excluded["duplicate row"] += 1
                    continue
                seen.add(dkey)
                rec = {"outcome": o}
                for f in ("company", "industry", "country", "region", "tech", "source", "reason"):
                    v = (raw.get(c.get(f, ""), "") or "").strip()
                    rec[f] = v.lower() if f not in ("company", "reason") and v else (v or None)
                for f in ("employees", "locations", "deal", "cycle"):
                    rec[f] = num(raw.get(c.get(f, ""), "")) if f in c else None
                for f in ("created", "closed", "since", "churn_date"):
                    rec[f] = date(raw.get(c.get(f, ""), "")) if f in c else None
                if rec["cycle"] is None and rec["created"] and rec["closed"]:
                    rec["cycle"] = float((rec["closed"] - rec["created"]).days)
                if rec["deal"] is not None and rec["deal"] <= 0:
                    rec["deal"] = None
                rec["locations_band"] = band(rec["locations"], LOC_BANDS)
                rec["employees_band"] = band(rec["employees"], EMP_BANDS)
                rows.append(rec)
    return rows, cols or {}, excluded


def label(n):
    return "anecdote" if n < 5 else "hypothesis" if n < 10 else "evidence"


def rate(k, n):
    if n == 0:
        return {"k": 0, "n": 0, "pct": None, "text": "none closed"}
    pct = round(100 * k / n) if n >= 10 else None
    return {"k": k, "n": n, "pct": pct, "text": f"{k} of {n}" + (f" ({pct}%)" if pct is not None else "")}


def med(vals, money=False):
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return {"n": 0, "median": None, "text": "no data"}
    fmt = (lambda v: f"${v:,.0f}") if money else (lambda v: f"{v:,.0f}")
    if len(vals) < 5:
        return {"n": len(vals), "median": None, "values": vals, "text": "values: " + ", ".join(fmt(v) for v in vals)}
    m = statistics.median(vals)
    return {"n": len(vals), "median": m, "text": f"median {fmt(m)} (n={len(vals)})"}


def stats(rs):
    won = [r for r in rs if r["outcome"] in ("won", "churned")]
    lost = [r for r in rs if r["outcome"] == "lost"]
    churned = [r for r in rs if r["outcome"] == "churned"]
    tenure = [((r["churn_date"] - r["since"]).days / 30.44) for r in churned if r["churn_date"] and r["since"]]
    by_year = Counter(str((r["closed"] or r["since"]).year) for r in won if (r["closed"] or r["since"]))
    return {
        "closed": len(rs), "label": label(len(rs)),
        "win_rate": rate(len(won), len(rs)),
        "churn_rate": rate(len(churned), len(won)),
        "deal_size": med([r["deal"] for r in won], money=True),
        "cycle_days_won": med([r["cycle"] for r in won]),
        "cycle_days_lost": med([r["cycle"] for r in lost]),
        "months_to_churn": med(tenure),
        "wins_by_year": dict(sorted(by_year.items())),
        "loss_reasons": Counter(r["reason"] for r in lost if r["reason"]).most_common(5),
        "churn_reasons": Counter(r["reason"] for r in churned if r["reason"]).most_common(5),
    }


def group(rows, keys):
    g = defaultdict(list)
    for r in rows:
        vals = [r.get(k) for k in keys]
        g[" / ".join(v if v is not None else "unknown" for v in vals)].append(r)
    return {k: stats(v) for k, v in sorted(g.items(), key=lambda kv: -len(kv[1]))}


def table(title, groups):
    out = [f"\n### {title}\n", "| Segment | Closed | Label | Won | Churned (of won) | Deal size | Cycle, won (days) | Wins by year |",
           "|---|---|---|---|---|---|---|---|"]
    for k, s in groups.items():
        out.append(f"| {k} | {s['closed']} | {s['label']} | {s['win_rate']['text']} | {s['churn_rate']['text']} | "
                   f"{s['deal_size']['text']} | {s['cycle_days_won']['text']} | "
                   f"{', '.join(f'{y}: {c}' for y, c in s['wins_by_year'].items()) or '-'} |")
    reasons = [(k, s) for k, s in groups.items() if s["loss_reasons"] or s["churn_reasons"]]
    if reasons:
        out.append("")
        for k, s in reasons:
            bits = []
            if s["loss_reasons"]:
                bits.append("lost: " + "; ".join(f"{r} ({c})" for r, c in s["loss_reasons"]))
            if s["churn_reasons"]:
                bits.append("churned: " + "; ".join(f"{r} ({c})" for r, c in s["churn_reasons"]))
            out.append(f"- {k}: " + " | ".join(bits))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+")
    ap.add_argument("--map", default="", help='field=Column pairs, e.g. outcome="Deal Stage",deal="ARR"')
    ap.add_argument("--by", default="", help="segment fields (default: every one present)")
    ap.add_argument("--cross", default="", help="two fields to cross, e.g. industry,locations_band")
    ap.add_argument("--out", help="write JSON here (e.g. icp/analysis.json)")
    a = ap.parse_args()
    overrides = {}
    for part in re.findall(r'(\w+)=("[^"]*"|[^,]+)', a.map):
        overrides[part[0]] = part[1].strip('"')
    rows, cols, excluded = load(a.csv, overrides)
    if not cols.get("outcome") and not cols.get("churn_date"):
        sys.exit("No outcome column found (won / lost / churned). Use --map outcome=\"<column>\".")
    dims = [d for d in (a.by.split(",") if a.by else
            ["industry", "locations_band", "employees_band", "country", "region", "tech", "source"]) if d]
    dims = [d for d in dims if any(r.get(d) for r in rows)]
    cross = a.cross.split(",") if a.cross else [d for d in ("industry", "locations_band" if any(r.get("locations_band") for r in rows) else "employees_band") if d in dims]
    overall = stats(rows)
    closed = len(rows)
    sample = "small" if closed < 10 else "moderate" if closed < 30 else "workable"
    basis = {"files": a.csv, "rows_used": closed, "excluded": dict(excluded), "columns": cols,
             "missing_fields": [f for f in ("industry", "employees", "locations", "country", "deal", "cycle", "churn_date") if f not in cols],
             "sample": sample, "warnings": dict(AMBIGUOUS), "run_date": dt.date.today().isoformat()}
    result = {"basis": basis, "overall": overall, "segments": {d: group(rows, [d]) for d in dims}}
    if len(cross) == 2 and all(c in dims for c in cross):
        result["cross"] = {" x ".join(cross): group(rows, cross)}

    print(f"# Customer analysis\n\nBasis: {closed} closed records from {', '.join(a.csv)}"
          + (f"; excluded {', '.join(f'{v} {k}' for k, v in excluded.items())}" if excluded else ""))
    print(f"Columns used: {', '.join(f'{k}={v}' for k, v in cols.items())}")
    for k, v in AMBIGUOUS.items():
        print(f"Warning: {v} {k}")
    if basis["missing_fields"]:
        print(f"Not in the data: {', '.join(basis['missing_fields'])}")
    if sample == "small":
        print("\n**Small sample:** fewer than 10 closed records. Report counts (\"3 of 4\"), never percentages. Every finding is a hypothesis.")
    elif sample == "moderate":
        print("\n**Moderate sample:** 10-29 closed records. Segment-level findings are hypotheses unless the segment has 10+ closed records.")
    print(f"\nOverall: won {overall['win_rate']['text']}; churned {overall['churn_rate']['text']} of won; "
          f"deal size {overall['deal_size']['text']}; cycle (won) {overall['cycle_days_won']['text']}")
    for d, g in result["segments"].items():
        print(table(f"By {d}", g))
    for k, g in result.get("cross", {}).items():
        print(table(f"By {k}", g))
    if a.out:
        import os
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        json.dump(result, open(a.out, "w", encoding="utf-8"), indent=1, default=str)
        print(f"\nWrote {a.out}")


if __name__ == "__main__":
    main()
