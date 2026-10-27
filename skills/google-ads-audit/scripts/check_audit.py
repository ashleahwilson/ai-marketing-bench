#!/usr/bin/env python3
"""Self-check an AUDIT.md (and fixes.md) against the figures ads_audit.py computed. Standard library only.

Usage:
    python3 check_audit.py AUDIT.md --metrics metrics.json [--fixes fixes.md] [--allow 349,299]

FAIL when:
  - a dollar figure doesn't trace to a computed figure (or a sum of up to three of them)
  - a required section is missing, or the top three findings don't come before the scorecard
  - the report promises or forecasts a result, or projects a figure per month or year
  - an internal name (script, irrelevant.txt, metrics.json) appears, or a fix line contains TBD
  - a fixes.md line doesn't match: <n>. [P1|P2|P3] <area> · <problem> · <fix>
WARN for a percentage benchmark with no named source nearby.
Exit code 0 PASS, 1 FAIL.
"""
import argparse, itertools, json, re, sys

SECTIONS = ["## Top three findings", "## Scorecard", "## Findings by check", "## Plan", "## Not checked", "## Sources and assumptions"]
AREAS = "structure|keywords|negatives|ads|assets|settings|budget|tracking|landing"
FIX_RE = re.compile(rf"^\d+\. \[P[123]\] ({AREAS}) · .+ · .+$")
PROMISE = re.compile(r"\b(guarantee[ds]?|we promise|will (reach|hit|achieve|deliver|get you to|double|triple)|expect(ed)? roas of|projected (roas|revenue|conversions))\b", re.I)
PROJECT = re.compile(r"\$\s?[\d,.]+k?\s*(a|per|each)\s*(year|month|quarter)|\b(annuali[sz]ed|per year|a year|yearly)\b", re.I)
BENCH = re.compile(r"(industry|average|benchmark|typical)[^.\n]{0,60}\d+(\.\d+)?%|\d+(\.\d+)?%[^.\n]{0,60}(industry average|benchmark)", re.I)


def numbers(o, acc):
    if isinstance(o, bool):
        return acc
    if isinstance(o, (int, float)):
        acc.add(round(float(o), 2))
    elif isinstance(o, dict):
        for v in o.values():
            numbers(v, acc)
    elif isinstance(o, (list, tuple)):
        for v in o:
            numbers(v, acc)
    elif isinstance(o, str):
        for m in re.findall(r"\d[\d,]*\.\d{2}", o):
            acc.add(round(float(m.replace(",", "")), 2))
    return acc


def traced(x, vals, small):
    if any(abs(x - v) < 0.006 or (x == round(x) and abs(x - v) < 0.5) for v in vals):
        return True
    for k in (2, 3):
        for combo in itertools.combinations(small, k):
            if abs(x - sum(combo)) < 0.006:
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audit")
    ap.add_argument("--metrics", required=True)
    ap.add_argument("--fixes")
    ap.add_argument("--allow", default="", help="comma-separated amounts quoted from brand memory or the user, e.g. 349,299")
    a = ap.parse_args()
    m = json.load(open(a.metrics, encoding="utf-8"))
    vals = sorted(numbers(m, set()) | {round(float(x), 2) for x in a.allow.replace("$", "").split(",") if x.strip()})
    small = [v for v in vals if v >= 1][:200]
    problems, warns = [], []
    docs = [(a.audit, open(a.audit, encoding="utf-8").read())]
    if a.fixes:
        docs.append((a.fixes, open(a.fixes, encoding="utf-8").read()))
    for name, text in docs:
        for mm in re.finditer(r"\$\s?(\d[\d,]*(?:\.\d+)?)(k)?", text):
            x = float(mm.group(1).replace(",", "")) * (1000 if mm.group(2) else 1)
            if not traced(round(x, 2), vals, small):
                line = text[:mm.start()].count("\n") + 1
                problems.append(f"{name}:{line} ${mm.group(1)}{mm.group(2) or ''} doesn't trace to a computed figure")
        for mm in PROMISE.finditer(text):
            line = text[:mm.start()].count("\n") + 1
            ctx = text[max(0, mm.start() - 40):mm.end() + 20].lower()
            if not re.search(r"\b(not|never|can't|cannot|won't|no one can)\b", ctx):
                problems.append(f"{name}:{line} promise or forecast: '{mm.group(0)}'")
        for mm in re.finditer(r"\b(the script|scripts?/|ads_audit|check_audit|irrelevant\.txt|metrics\.json|checks\.md|exports\.md|output-format\.md)\b", text, re.I):
            problems.append(f"{name}:{text[:mm.start()].count(chr(10)) + 1} internal name in client-facing file: '{mm.group(0)}'")
        if name == a.fixes:
            for l in text.splitlines():
                if re.match(r"^\d+\.", l) and "TBD" in l:
                    problems.append(f"fixes.md fix line contains TBD (say what's needed and end with '(confirm first)'): {l[:70]}")
        for mm in PROJECT.finditer(text):
            problems.append(f"{name}:{text[:mm.start()].count(chr(10)) + 1} projection beyond the export's date range: '{mm.group(0)}'")
        for mm in BENCH.finditer(text):
            seg = text[mm.start():mm.end() + 80]
            if not re.search(r"source:|according to|\(source", seg, re.I):
                warns.append(f"{name}:{text[:mm.start()].count(chr(10)) + 1} percentage benchmark with no named source: '{mm.group(0)[:60]}'")
    audit = docs[0][1]
    pos = [audit.find(s) for s in SECTIONS]
    for s, p in zip(SECTIONS, pos):
        if p < 0:
            problems.append(f"AUDIT.md is missing the section '{s}'")
    if all(p >= 0 for p in pos[:2]) and pos[0] > pos[1]:
        problems.append("Top three findings must come before the scorecard")
    if a.fixes:
        lines = [l for l in docs[1][1].splitlines() if re.match(r"^\d+\.", l)]
        if not lines:
            problems.append("fixes.md has no numbered fixes")
        for l in lines:
            if not FIX_RE.match(l.strip()):
                problems.append(f"fixes.md line doesn't match the format: {l[:80]}")
    for w in warns:
        print("WARN", w)
    for p in problems:
        print("FAIL", p)
    print("RESULT:", "FAIL" if problems else "PASS")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
