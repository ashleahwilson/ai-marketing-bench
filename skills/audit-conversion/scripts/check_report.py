#!/usr/bin/env python3
"""Check a conversion audit before it goes to the user. Standard library only.

Usage:
    python3 scripts/check_report.py audits/<domain>/                    # checks conversion.md and dim-conversion.json
    python3 scripts/check_report.py audits/<domain>/ --analytics        # the user supplied an analytics export
    python3 scripts/check_report.py audits/<domain>/ --spelling us      # client writes US English (or: ca, uk)

dim-conversion.json (the marketing-audit conversion format):
  - exactly C1-C6, each with the right maximum (20, 20, 20, 15, 15, 10) and an allowed point value
    (full, partial or 0: C1-C3 20/10/0, C4-C5 15/8/0, C6 10/5/0), and one line of evidence
  - "score" equals the sum of the points (it's rewritten if not)
conversion.md:
  - the fixed sections, in order
  - the checklist total in the last section matches dim-conversion.json
  - a plan with 48 hours, 2 weeks and 3 months, and a test backlog whose rows have hypothesis, change and metric
  - no predicted lift: no percentage or count tied to lift/increase/boost/more leads, no "conversion rate will be"
  - no conversion-rate figure unless --analytics
  - no internal names (script names, "the skill", file internals)
  - spelling matches the client's convention when --spelling is given
Exit 1 on any FAIL. WARN lines need a judgment call.
"""

import json
import os
import re
import sys

MAX = {"C1": 20, "C2": 20, "C3": 20, "C4": 15, "C5": 15, "C6": 10}
ALLOWED = {"C1": {20, 10, 0}, "C2": {20, 10, 0}, "C3": {20, 10, 0}, "C4": {15, 8, 0}, "C5": {15, 8, 0}, "C6": {10, 5, 0}}
SECTIONS = ["Verdict", "The three findings that matter most", "Page by page", "Forms", "Funnel", "What's working",
            "Plan", "Test backlog", "Not observable", "Conversion checklist score"]
LIFT = re.compile(r"(\d+(\.\d+)?\s?(%|percent|x\b|times)|\d[\d,]*\s+(more|extra|additional)\s+(leads|bookings|signups|sign-ups|"
                  r"trials|demos|customers|conversions|submissions))[^.\n]{0,60}\b(lift|increase|uplift|boost|improve|improvement|"
                  r"more|gain|grow)|\b(lift|increase|uplift|boost|improve|improvement|gain)\w*\b[^.\n]{0,40}?\bby\s+\d+(\.\d+)?\s?(%|percent|x\b)"
                  r"|\b(expected|predicted|projected|estimated|likely)\s+(lift|uplift|increase|impact)\b[^.\n]{0,30}\d", re.I)
RATE = re.compile(r"conversion rate[^.\n]{0,40}?\d+(\.\d+)?\s?%|\d+(\.\d+)?\s?%\s+conversion rate", re.I)
WILL_RATE = re.compile(r"conversion rate (will|would) (be|reach|rise|go up|improve)", re.I)
INTERNAL = re.compile(r"\b(inspect_conversion|check_report|funnel\.py|score\.py|SKILL\.md|audit-conversion|marketing-audit|"
                      r"the skill|this skill|\w+ skill|the script|the checker|references/)\b", re.I)
SPELL = {
    "us": re.compile(r"\b(behaviour|colour|favour|labour|centre|optimis\w*|organis\w*|prioritis\w*|analys(e|ed|ing)\b|"
                     r"licence|catalogue|cancelled|travelled|labelled|modelling|programme)\b", re.I),
    "ca": re.compile(r"\b(optimis\w*|organis\w*|prioritis\w*|programme|behavior|color|favor|center)\b", re.I),
    "uk": re.compile(r"\b(behavior|color|favor|center|optimiz\w*|organiz\w*|prioritiz\w*)\b", re.I),
}


def check_dim(path, out):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        out.append(("FAIL", f"dim-conversion.json can't be read: {e}"))
        return None
    if str(d.get("dimension", "")).lower() != "conversion":
        out.append(("FAIL", "dim-conversion.json: dimension must be \"conversion\""))
    if d.get("assessable") is False:
        out.append(("WARN", "dimension marked not assessable: say why in the report"))
        return d
    ids = [c.get("id") for c in d.get("checks", [])]
    for cid in MAX:
        if ids.count(cid) != 1:
            out.append(("FAIL", f"{cid} appears {ids.count(cid)} times (needs exactly one)"))
    for c in d.get("checks", []):
        cid = c.get("id")
        if cid not in MAX:
            out.append(("FAIL", f"unknown check {cid}: the conversion dimension has C1-C6 only"))
            continue
        if c.get("max") != MAX[cid]:
            out.append(("FAIL", f"{cid} max is {c.get('max')}, should be {MAX[cid]}"))
        if c.get("points") not in ALLOWED[cid]:
            out.append(("FAIL", f"{cid} has {c.get('points')} points; allowed: {sorted(ALLOWED[cid], reverse=True)}"))
        if not str(c.get("evidence", "")).strip():
            out.append(("FAIL", f"{cid} has no evidence"))
        if re.search(r"not observable|can't be (seen|checked)|cannot be (seen|checked)", str(c.get("evidence", "")), re.I) and c.get("points"):
            out.append(("WARN", f"{cid} says it couldn't be observed but awards points"))
    total = sum(c.get("points", 0) for c in d.get("checks", []) if c.get("id") in MAX)
    if d.get("score") != total:
        out.append(("FAIL", f"score is {d.get('score')} but the checks sum to {total}: set score to {total}"))
    for f in d.get("findings", []):
        if not (f.get("evidence") and f.get("fix")):
            out.append(("FAIL", f"finding on {f.get('check')} lacks evidence or a fix"))
    d["_total"] = total
    return d


def check_md(path, dim, analytics, spelling, out):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        out.append(("FAIL", f"conversion.md can't be read: {e}"))
        return
    heads = [h.strip() for h in re.findall(r"^##\s+(.+)$", text, re.M)]
    pos = []
    for s in SECTIONS:
        i = next((n for n, h in enumerate(heads) if h.lower().startswith(s.lower())), None)
        if i is None:
            out.append(("FAIL", f"missing section: ## {s}"))
        pos.append(i)
    found = [p for p in pos if p is not None]
    if found != sorted(found):
        out.append(("FAIL", f"sections out of order; expected: {' > '.join(SECTIONS)}"))
    if heads and not heads[-1].lower().startswith("conversion checklist score"):
        out.append(("FAIL", "the report must end with ## Conversion checklist score"))
    m = re.search(r"^##\s+Conversion checklist score.*?$(.*)", text, re.M | re.S | re.I)
    if m and dim and "_total" in dim:
        tot = re.search(r"\*{0,2}total\*{0,2}[^0-9\n]{0,20}(\d{1,3})\s*/\s*100", m.group(1), re.I)
        if not tot:
            out.append(("FAIL", "checklist section has no 'Total … X/100' line"))
        elif int(tot.group(1)) != dim["_total"]:
            out.append(("FAIL", f"checklist total says {tot.group(1)}/100 but the checks sum to {dim['_total']}"))
        for cid in MAX:
            if not re.search(rf"\b{cid}\b", m.group(1)):
                out.append(("FAIL", f"checklist table is missing {cid}"))
    plan = re.search(r"^##\s+Plan.*?$(.*?)(?=^##\s)", text, re.M | re.S)
    if plan:
        for h in ("48 hours", "2 weeks", "3 months"):
            if h not in plan.group(1):
                out.append(("FAIL", f"plan has no '{h}' horizon"))
    tb = re.search(r"^##\s+Test backlog.*?$(.*?)(?=^##\s)", text, re.M | re.S)
    if tb:
        rows = [r for r in tb.group(1).splitlines() if r.strip().startswith("|") and not re.match(r"^\|\s*-", r.strip())]
        if rows:
            head = rows[0].lower()
            for col in ("hypothesis", "change", "metric"):
                if col not in head:
                    out.append(("FAIL", f"test backlog table has no '{col}' column"))
            for r in rows[1:]:
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                if len(cells) < 3 or any(not c for c in cells[-3:]):
                    out.append(("FAIL", f"test backlog row has an empty cell: {r.strip()[:80]}"))
        elif not re.search(r"no test|not worth testing|nothing to test", tb.group(1), re.I):
            out.append(("WARN", "test backlog has no table: say why (for example, nothing worth testing)"))
    for n, line in enumerate(text.splitlines(), 1):
        if LIFT.search(line) or WILL_RATE.search(line):
            out.append(("FAIL", f"line {n} predicts a lift or outcome: {line.strip()[:100]}"))
        if not analytics and RATE.search(line):
            out.append(("FAIL", f"line {n} states a conversion rate with no analytics supplied: {line.strip()[:100]}"))
        if INTERNAL.search(line):
            out.append(("FAIL", f"line {n} mentions internals: {line.strip()[:100]}"))
        if spelling in SPELL:
            for w in SPELL[spelling].findall(line):
                word = w if isinstance(w, str) else w[0]
                out.append(("FAIL", f"line {n}: '{word}' doesn't match the client's {spelling.upper()} spelling"))
    if re.search(r"TBD|TODO|\[insert|lorem ipsum|<[a-z ]+>", text, re.I) and not re.search(r"TBD:", text):
        out.append(("WARN", "possible placeholder left in the report"))
    words = len(re.findall(r"\S+", text))
    if words > 2200:
        out.append(("WARN", f"report is {words} words; trim page-by-page detail first"))


def main():
    args = sys.argv[1:]
    analytics = "--analytics" in args
    spelling = None
    if "--spelling" in args:
        i = args.index("--spelling")
        spelling = args[i + 1].lower()
        del args[i:i + 2]
    args = [a for a in args if not a.startswith("--")]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__)
        return 2
    folder, out = args[0], []
    dim = check_dim(os.path.join(folder, "dim-conversion.json"), out)
    check_md(os.path.join(folder, "conversion.md"), dim, analytics, spelling, out)
    for lvl, msg in out:
        print(f"{lvl}: {msg}")
    fails = sum(1 for l, _ in out if l == "FAIL")
    print(f"{'PASS' if not fails else 'FAIL'}: {fails} fail(s), {len(out) - fails} warning(s)"
          + (f" · checklist total {dim['_total']}/100" if dim and '_total' in dim else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
