#!/usr/bin/env python3
"""Self-check acquisition.md before it reaches the user. Standard library only.

Usage:
    python3 scripts/check_report.py audits/<domain>/acquisition.md
    python3 scripts/check_report.py audits/<domain>/acquisition.md --data     # a Search Console/analytics export was supplied

Checks: the fixed sections are all there and in order; exactly three top findings; the plan has 48-hour, 2-week
and 3-month horizons; the score matches acquisition-checks.json beside it; no traffic, visit, search-volume or
ranking-position figures when no export was supplied; no ranking or traffic guarantees; no tool, file or
process names in a client-facing report; banned words. FAIL means rewrite the report, then run it again.
"""

import json
import os
import re
import sys

SECTIONS = ["## Verdict", "## Top three findings", "## Indexability and on-page basics", "## Buyer questions and content",
            "## AI search and answer engines", "## Local listings", "## Channels", "## Search data",
            "## Checklist score", "## Plan", "## Not observable", "## How this was done"]
TRAFFIC = re.compile(r"\b\d[\d,.]*\s*k?\+?\s*(?:monthly\s+|organic\s+|a month\s+)?(?:visits|visitors|sessions|users|searches|"
                     r"page ?views)\b|search volume of|\bvolume:? \d|keyword difficulty|\bKD\s?\d|domain (?:authority|rating) (?:of )?\d|"
                     r"\branks? (?:#|number |at position )\d", re.I)
GUARANTEE = re.compile(r"\bguarantee[sd]?\b|\bwill (?:rank|reach|hit) (?:#|number|first|on page|page one|the top)|"
                       r"\bpage one (?:in|within|by)\b|\btop (?:3|three|10|ten) (?:in|within|by) \d", re.I)
NEGATION = re.compile(r"\b(?:no|not|never|can't|cannot|can not|won't|doesn't|don't|isn't|nobody|no one|without|instead of)\b", re.I)
LEAKS = re.compile(r"\.py\b|\bscripts?/|check_pages|search_data|score_acquisition|check_report|audit-acquisition|"
                   r"marketing-audit|SKILL\.md|\bthe skill\b|\bthis skill\b|acquisition-checks\.json|dim-acquisition", re.I)
BANNED = re.compile(r"mid-market", re.I)


def main():
    args = [a for a in sys.argv[1:] if a != "--data"]
    data = "--data" in sys.argv
    if len(args) != 1 or not os.path.isfile(args[0]):
        print(__doc__)
        return 2
    path = args[0]
    text = open(path, encoding="utf-8").read()
    fails, warns = [], []
    if not re.search(r"^# Acquisition audit: .+", text, re.M):
        fails.append("first heading should be '# Acquisition audit: <Company>'")
    pos = -1
    for s in SECTIONS:
        i = text.find("\n" + s)
        if i == -1:
            fails.append(f"missing section '{s}'")
        elif i < pos:
            fails.append(f"section '{s}' is out of order")
        else:
            pos = i

    def section(name):
        m = re.search(r"\n" + re.escape(name) + r"[^\n]*\n(.*?)(?=\n## |\Z)", text, re.S)
        return m.group(1) if m else ""

    top = section("## Top three findings")
    n = len(re.findall(r"^\s*\d+\.\s", top, re.M))
    if n != 3:
        fails.append(f"'Top three findings' has {n} numbered findings (needs exactly 3)")
    plan = section("## Plan")
    for h in ("48 hours", "2 weeks", "3 months"):
        if h not in plan:
            fails.append(f"plan is missing the '{h}' horizon")
    checks = os.path.join(os.path.dirname(path), "acquisition-checks.json")
    if os.path.isfile(checks):
        try:
            score = json.load(open(checks, encoding="utf-8")).get("score")
            found = re.findall(r"\b(\d{1,3})/100\b", section("## Verdict") + section("## Checklist score"))
            if score is not None and str(score) not in found:
                fails.append(f"report doesn't state the checklist score {score}/100 (found: {', '.join(found) or 'none'})")
        except ValueError:
            warns.append("acquisition-checks.json beside the report isn't valid JSON")
    else:
        warns.append("no acquisition-checks.json beside the report, so the score wasn't cross-checked")
    for ln, line in enumerate(text.splitlines(), 1):
        if not data and TRAFFIC.search(line):
            fails.append(f"line {ln}: a traffic, volume or ranking figure with no export supplied: {line.strip()[:120]}")
        for sent in re.split(r"(?<=[.!?])\s+", line):
            if GUARANTEE.search(sent) and not NEGATION.search(sent):
                fails.append(f"line {ln}: reads as a ranking or traffic promise: {sent.strip()[:120]}")
        if LEAKS.search(line):
            fails.append(f"line {ln}: names a tool, file or process the reader shouldn't see: {line.strip()[:120]}")
        if BANNED.search(line):
            fails.append(f"line {ln}: banned word: {line.strip()[:120]}")
    dashes = text.count("—")
    if dashes > 2:
        warns.append(f"{dashes} em dashes; use commas, colons or full stops instead")
    words = len(re.findall(r"[A-Za-z0-9']+", text))
    if words > 1800:
        warns.append(f"{words} words; trim the detailed sections, never the top three or the plan")
    for f in fails:
        print(f"FAIL: {f}")
    for w in warns:
        print(f"WARN: {w}")
    print("PASS" if not fails else f"{len(fails)} FAIL(s): rewrite and run again")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
