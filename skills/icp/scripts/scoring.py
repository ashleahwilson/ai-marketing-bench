#!/usr/bin/env python3
"""Parse, check, apply and back-test an ICP scoring rubric (icp/scoring.md). Standard library only.

Usage:
    python3 scripts/scoring.py check icp/scoring.md
    python3 scripts/scoring.py apply icp/scoring.md <list.csv> [--out scored.csv] [--map industry=Vertical]
    python3 scripts/scoring.py backtest icp/scoring.md <customers.csv>   # tiers against real outcomes
    python3 scripts/scoring.py json icp/scoring.md                       # the parsed rubric

The format is in references/scoring-format.md. It is the line grammar the list builder reads:
`| Criterion | Points | ... |` table rows, criteria written `Field: a, b`, `Field 2-15`, `Field 15+`, `Field over 15`,
`Field under 10` or `Field 1`, points a whole number or DQ, and a `Tiers: A 70+, B 45+` line.
"""

import argparse
import csv
import json
import re
import sys

STATUSES = ("evidence-based", "provisional", "user-directed")
NUM = r"(-?\d+(?:\.\d+)?)"


def _sibling(name):
    """Load a script that sits beside this one (keeps the skill to plain files, no package)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_synonyms():
    try:
        return dict(_sibling("analyze_customers").FIELDS, revenue=["revenue", "annual revenue", "sales"])
    except (OSError, AttributeError):
        return {}


SYNONYMS = _load_synonyms()


def norm_h(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def parse_numeric(v):
    v = v.lower().replace("–", "-").replace("—", "-").strip()
    pats = [(rf"^(?:between\s*)?{NUM}\s*(?:-|to|and)\s*{NUM}$", lambda a, b: (float(a), float(b))),
            (rf"^{NUM}\s*(?:\+|or more|and up|plus)$", lambda a: (float(a), float("inf"))),
            (rf"^(?:at least|>=)\s*{NUM}$", lambda a: (float(a), float("inf"))),
            (rf"^(?:over|more than|above|>)\s*{NUM}$", lambda a: (float(a) + 1e-9, float("inf"))),
            (rf"^(?:under|less than|below|fewer than|<)\s*{NUM}$", lambda a: (float("-inf"), float(a) - 1e-9)),
            (rf"^(?:at most|<=|up to)\s*{NUM}$", lambda a: (float("-inf"), float(a))),
            (rf"^{NUM}$", lambda a: (float(a), float(a)))]
    for p, f in pats:
        m = re.match(p, v)
        if m:
            return f(*m.groups())
    return None


def parse_rule(text):
    """'Industry: a, b' -> values; 'Locations 2-15', 'Locations: 2 to 15', 'Locations 15+', 'over 15' -> range."""
    t = text.replace("–", "-").replace("—", "-").strip()
    m = re.match(r"^(.+?)\s*:\s*(.+)$", t)
    if m:
        field, val = m.group(1).strip(), m.group(2).strip()
        rng = parse_numeric(val)
        if rng:
            return {"field": field, "num": rng}
        vals = [x.strip().lower() for x in re.split(r",|/|\bor\b|;", val) if x.strip()]
        return {"field": field, "vals": vals} if vals else None
    m = re.match(r"^([a-z][a-z /_]*?)\s+((?:over|under|more than|less than|fewer than|at least|at most|up to|above|"
                 r"below|between|>=|<=|>|<)?\s*\d[\d.]*\s*(?:\+|or more|and up|-\s*\d+|to\s*\d+|and\s*\d+)?)$", t, re.I)
    if m:
        rng = parse_numeric(m.group(2))
        if rng:
            return {"field": m.group(1).strip(), "num": rng}
    return None


def parse_points(s):
    s = s.strip().lower()
    if re.fullmatch(r"dq|disqualif\w*|exclude\w*", s):
        return "DQ"
    m = re.fullmatch(r"([+-]?\s*\d+)\s*(?:pts?|points?)?", s)
    return int(m.group(1).replace(" ", "")) if m else None


HEADER = (("version", r"\bVersion\s+(\d+)"), ("updated", r"\b(?:written|updated)\s+(\d{4}-\d{2}-\d{2})"),
          ("status", r"\bStatus:\s*([a-z-]+)"), ("basis", r"^Basis:\s*(.+)$"), ("max points", r"\bMax points:\s*(\d+)"))


def parse(text):
    """Return (rubric, errors)."""
    rub = {"title": "", "header": {}, "tiers": [], "criteria": [], "disqualifiers": [], "sections": []}
    errors, section, cols = [], None, None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line.startswith("# "):
            rub["title"] = line[2:].strip()
            continue
        if line.startswith("## "):
            section, cols = line[3:].strip().lower(), None
            rub["sections"].append(section)
            continue
        if section is None:
            for key, pat in HEADER:
                m = re.search(pat, line, re.I)
                if m:
                    rub["header"][key] = m.group(1).strip()
        m = re.match(r"^Tiers?:\s*(.+)$", line, re.I)
        if m:
            for t, v in re.findall(r"\b([A-D])\s+(\d+)\s*\+", m.group(1)):
                rub["tiers"].append({"tier": t, "min": int(v)})
            continue
        if not line.startswith("|") or section not in ("criteria", "disqualifiers"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if norm_h(cells[0]) in ("criterion", "criteria"):
            cols = [norm_h(c) for c in cells]
            continue
        row = dict(zip(cols or ["criterion", "points", "evidence"], cells))
        item = {"id": cells[0], "criterion": cells[0], "line": n, "points": parse_points(row.get("points", "")),
                "evidence": row.get("evidence", ""), "reason": row.get("reason", "")}
        item["rule"] = parse_rule(cells[0])
        if item["rule"] is None:
            errors.append(f"line {n}: '{cells[0]}' isn't a criterion the list builder can read "
                          "(Field: a, b | Field 2-15 | Field 15+ | Field over 15 | Field under 10 | Field 1)")
        if section == "disqualifiers":
            if item["points"] != "DQ":
                errors.append(f"line {n}: disqualifier '{cells[0]}' needs DQ in the Points column")
            if not item["reason"]:
                errors.append(f"line {n}: disqualifier '{cells[0]}' has no reason")
            rub["disqualifiers"].append(item)
        else:
            if not isinstance(item["points"], int):
                errors.append(f"line {n}: '{cells[0]}' needs whole-number points")
            rub["criteria"].append(item)
        if not item["evidence"]:
            errors.append(f"line {n}: '{cells[0]}' has no evidence")
    return rub, errors


def max_points(rub):
    """Criteria on the same field are alternatives: count the best one per field."""
    best = {}
    for c in rub["criteria"]:
        if isinstance(c["points"], int) and c["points"] > 0 and c["rule"]:
            f = norm_h(c["rule"]["field"])
            best[f] = max(best.get(f, 0), c["points"])
    return sum(best.values())


def check(rub, errors):
    out = [("FAIL", e) for e in errors]
    h = rub["header"]
    for k, example in (("version", "Version 1, written 2026-10-23."), ("updated", "Version 1, written 2026-10-23."),
                       ("status", "Status: evidence-based."), ("basis", "Basis: 46 closed records from ..."),
                       ("max points", "Max points: 100 (unknown values score nothing).")):
        if k not in h:
            out.append(("FAIL", f"header is missing {k} (a line like '{example}')"))
    if h.get("status") and not any(h["status"].lower().startswith(s) for s in STATUSES):
        out.append(("FAIL", f"Status must be one of: {', '.join(STATUSES)}"))
    for s in ("criteria", "disqualifiers"):
        if s not in rub["sections"]:
            out.append(("FAIL", f"no '## {s.title()}' section (keep the heading even when it's empty)"))
    if not rub["criteria"]:
        out.append(("FAIL", "no criteria rows"))
    if not rub["tiers"]:
        out.append(("FAIL", "no 'Tiers: A 70+, B 50+, C 30+' line"))
    mins = [t["min"] for t in rub["tiers"]]
    if mins != sorted(mins, reverse=True):
        out.append(("FAIL", "tiers must run from A down"))
    mx = max_points(rub)
    try:
        stated = int(h.get("max points", "0"))
    except ValueError:
        stated = 0
    if stated and mx != stated:
        out.append(("FAIL", f"the most a row can score is {mx} (best criterion per field), but Max points says {stated}"))
    if mins and mx and max(mins) > mx:
        out.append(("FAIL", f"tier A needs {max(mins)} but the most a row can score is {mx}"))
    ranges = {}
    for c in rub["criteria"]:
        if c["rule"] and "num" in c["rule"]:
            ranges.setdefault(norm_h(c["rule"]["field"]), []).append((c["rule"]["num"], c["criterion"]))
    for rngs in ranges.values():
        rngs.sort()
        for (a, an), (b, bn) in zip(rngs, rngs[1:]):
            if b[0] <= a[1]:
                out.append(("FAIL", f"'{an}' and '{bn}' overlap, so a row would score both"))
    return out


def get(row, field, cmap):
    f = norm_h(field)
    col = cmap.get(f)
    if col is None:
        col = next((k for k in row if k and norm_h(k) == f), None)
    if col is None:
        syn = next((v for k, v in SYNONYMS.items() if norm_h(k) == f or f in {norm_h(x) for x in v}), None)
        if syn:
            names = {norm_h(x) for x in syn}
            col = next((k for k in row if k and norm_h(k) in names), None)
    return None if col is None else (row.get(col) or "").strip()


def first_range(v):
    v = v.replace("–", "-").replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", v)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"\d+(?:\.\d+)?", v)
    return (float(m.group(0)), float(m.group(0))) if m else None


def matches(rule, v):
    """True, False, or None when the value is blank or unclear (the list builder's rule)."""
    if v is None or v.strip().lower() in ("", "unknown", "n/a", "na"):
        return None
    if "num" in rule:
        r = first_range(v)
        if not r:
            return None
        lo, hi = rule["num"]
        if lo <= r[0] and r[1] <= hi:
            return True
        return False if (r[1] < lo or r[0] > hi) else None
    lv = v.lower()
    return any(re.search(rf"\b{re.escape(x)}\b", lv) for x in rule["vals"])


def score_row(rub, row, cmap):
    dq = [d["criterion"] for d in rub["disqualifiers"] if d["rule"] and matches(d["rule"], get(row, d["rule"]["field"], cmap))]
    pts, hit, unknown = 0, [], []
    for c in rub["criteria"]:
        if not c["rule"] or not isinstance(c["points"], int):
            continue
        r = matches(c["rule"], get(row, c["rule"]["field"], cmap))
        if r:
            pts += c["points"]
            hit.append(c["criterion"])
        elif r is None:
            unknown.append(c["criterion"])
    tier = "disqualified" if dq else next((t["tier"] for t in rub["tiers"] if pts >= t["min"]), "below tiers")
    return {"icp_score": pts, "icp_tier": tier, "icp_disqualified_by": "; ".join(dq), "icp_matched": "; ".join(hit),
            "icp_unknown": "; ".join(unknown)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "apply", "backtest", "json"])
    ap.add_argument("rubric")
    ap.add_argument("list", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--map", default="", help="field=Column pairs")
    a = ap.parse_args()
    rub, errors = parse(open(a.rubric, encoding="utf-8").read())
    if a.cmd == "json":
        print(json.dumps(rub, indent=1, default=str))
        return 0
    if a.cmd == "check":
        res = check(rub, errors)
        for lvl, msg in res:
            print(f"{lvl}: {msg}")
        print(f"{len(rub['criteria'])} criteria, {len(rub['disqualifiers'])} disqualifiers, {len(rub['tiers'])} tiers, "
              f"max {max_points(rub)}. " + ("FAIL" if res else "PASS"))
        return 1 if res else 0
    if not a.list:
        sys.exit(f"{a.cmd} needs a CSV")
    cmap = {norm_h(k): v.strip().strip('"') for k, v in re.findall(r'(\w+)=("[^"]*"|[^,]+)', a.map)}
    with open(a.list, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    scored = [dict(r, **score_row(rub, r, cmap)) for r in rows]
    if a.cmd == "backtest":
        ac = _sibling("analyze_customers")
        cols = ac.match_columns(list(rows[0].keys()) if rows else [], {})
        table, seen = {}, set()
        for r in scored:
            o = ac.outcome(r, cols)
            key = (r.get(cols.get("company", ""), ""), o)
            if o in (None, "open") or key in seen:
                continue
            seen.add(key)
            table.setdefault(r["icp_tier"], {"won": 0, "churned": 0, "lost": 0})[o] += 1
        print("| Tier | Won and kept | Churned | Lost |\n|---|---|---|---|")
        for t in [t["tier"] for t in rub["tiers"]] + ["below tiers", "disqualified"]:
            if t in table:
                print(f"| {t} | {table[t]['won']} | {table[t]['churned']} | {table[t]['lost']} |")
        return 0
    out = open(a.out, "w", newline="", encoding="utf-8") if a.out else sys.stdout
    w = csv.DictWriter(out, fieldnames=list(scored[0].keys()) if scored else ["icp_score"])
    w.writeheader()
    w.writerows(scored)
    return 0


if __name__ == "__main__":
    sys.exit(main())
