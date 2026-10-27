#!/usr/bin/env python3
"""Self-check an ICP before it's handed over. Standard library only.

Usage:
    python3 scripts/check_icp.py --scoring icp/scoring.md --audiences brand/audiences.md
        [--analysis icp/analysis.json] [--sources notes/calls.md notes/win-loss.md brand/proof.md ...]
        [--reply response.md]

FAIL (fix before replying):
  - the rubric doesn't parse or doesn't add up (see scoring.py)
  - the rubric says evidence-based but there's no analysis, or fewer than 10 closed records
  - a percentage that isn't in the analysis or a source, or any percentage built on a small sample
  - a market size, TAM/SAM/SOM, or industry benchmark with a number that no source contains
  - a quote under "Their words" that doesn't appear word for word in a source
  - an audiences bullet with no [source: …] tag and no TBD
  - a criterion whose evidence gives no count ("12 of 14", "n=12") and isn't marked provisional, assumed or user
  - the reply names a script, a file format internal, or a skill
CHECK lines are for judgment: read each one and decide.
"""

import argparse
import json
import os
import re
import sys

def _sibling(name):
    """Load a script that sits beside this one (keeps the skill to plain files, no package)."""
    import importlib.util
    import os
    spec = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


scoring = _sibling("scoring")

PCT = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d)?)\s?%")
MARKET = re.compile(r"\b(TAM|SAM|SOM|total addressable|serviceable (?:available|obtainable)|addressable market|market size|market is worth"
                    r"|industry (?:average|benchmark|norm)s?|benchmark churn|average churn (?:rate )?(?:in|for|across))\b", re.I)
BIGNUM = re.compile(r"(\$\s?\d[\d,.]*\s?(?:k|m|b|bn|million|billion|thousand)?\b|\b\d[\d,]{3,}\b|\b\d+(?:\.\d+)?\s?(?:million|billion|thousand)\b|\d+\s?%)", re.I)
QUOTE = re.compile(r"[\"“]([^\"”]{6,})[\"”]")
INTERNALS = re.compile(r"\b(analy[sz]e_customers|check_icp|scoring\.py|analysis\.json|references/|SKILL\.md|build-list|brand-memory skill|icp skill|source tags?)\b", re.I)
COUNT = re.compile(r"\b\d+\s+of\s+\d+\b|\bn\s?=\s?\d+", re.I)
SOFT = re.compile(r"\b(provisional|assumed|assumption|hypothesis|user|TBD)\b|brand/|offer\.md|audiences\.md|rules\.md", re.I)


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError):
        return ""


def analysis_pcts(a):
    out = set()

    def walk(x):
        if isinstance(x, dict):
            if "pct" in x and isinstance(x["pct"], (int, float)):
                out.add(int(x["pct"]))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(a)
    return out


def analysis_pairs(a):
    """Every 'k of n' the analysis printed: win rates and churn rates for every segment."""
    out = set()

    def walk(x):
        if isinstance(x, dict):
            if "k" in x and "n" in x:
                out.add((x["k"], x["n"]))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(a)
    return out


KOFN = re.compile(r"\b(\d+)\s+of\s+(\d+)\b")
OUTCOME_WORDS = re.compile(r"\b(won|win|wins|churn\w*|lost|loss\w*|closed|retained|stayed|left)\b", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scoring", required=True)
    ap.add_argument("--audiences")
    ap.add_argument("--analysis")
    ap.add_argument("--sources", nargs="*", default=[])
    ap.add_argument("--reply")
    a = ap.parse_args()
    res = []

    stext = read(a.scoring)
    if not stext:
        print(f"FAIL: can't read {a.scoring}")
        return 1
    rub, errs = scoring.parse(stext)
    res += scoring.check(rub, errs)

    analysis = json.load(open(a.analysis, encoding="utf-8")) if a.analysis and os.path.isfile(a.analysis) else None
    closed = analysis["basis"]["rows_used"] if analysis else 0
    status = rub["header"].get("status", "").lower()
    if status.startswith("evidence-based") and (analysis is None or closed < 10):
        res.append(("FAIL", f"Status is evidence-based but the analysis has {closed} closed records (under 10): use provisional"))
    if analysis and 10 <= closed < 30 and status.startswith("evidence-based") and "hypothes" not in rub["header"].get("basis", "").lower():
        res.append(("CHECK", f"only {closed} closed records: say in Basis which findings are hypotheses"))
    basis = rub["header"].get("basis", "")
    if analysis and str(closed) not in basis:
        res.append(("CHECK", f"Basis line doesn't mention the {closed} closed records analyzed"))

    src_text = norm("\n".join(read(p) for p in a.sources))
    allowed = analysis_pcts(analysis) if analysis else set()
    allowed |= {int(float(x)) for x in PCT.findall("\n".join(read(p) for p in a.sources))}

    docs = {a.scoring: stext}
    if a.audiences:
        docs[a.audiences] = read(a.audiences)
    if a.reply:
        docs[a.reply] = read(a.reply)
    for path, text in docs.items():
        name = os.path.basename(path)
        for n, line in enumerate(text.splitlines(), 1):
            for p in PCT.findall(line):
                v = int(float(p))
                if analysis is not None and closed < 10:
                    res.append(("FAIL", f"{name}:{n}: {p}% on a small sample ({closed} closed records); use counts like '3 of 4'"))
                elif v not in allowed and not re.search(r"\[source: (user|doc|interview)", line):
                    res.append(("FAIL", f"{name}:{n}: {p}% isn't in the analysis or a source"))
            if MARKET.search(line) and BIGNUM.search(MARKET.sub("", line)) and not re.search(r"TBD|not estimated|no data|won't estimate", line, re.I):
                if norm(line) not in src_text:
                    res.append(("FAIL", f"{name}:{n}: market size or benchmark with a number and no source: {line.strip()[:90]}"))

    if analysis is not None:
        pairs = analysis_pairs(analysis)
        for path, text in docs.items():
            for n, line in enumerate(text.splitlines(), 1):
                if not OUTCOME_WORDS.search(line) or re.search(r"\bnotes?\b|back-test|backtest|score [A-D]\b", line, re.I):
                    continue
                for k, m in KOFN.findall(line):
                    if (int(k), int(m)) not in pairs:
                        res.append(("CHECK", f"{os.path.basename(path)}:{n}: '{k} of {m}' isn't a count the analysis printed; trace it to a segment row or a note count, or remove it"))

    if a.audiences:
        atext = docs[a.audiences]
        section = ""
        for n, line in enumerate(atext.splitlines(), 1):
            if line.startswith("## "):
                section = line[3:].strip().lower()
            if re.match(r"^\s*- ", line):
                tracked = any(section.startswith(s) for s in ("segments", "not for", "triggers", "personas", "fit", "disqualifiers"))
                if tracked and "[source:" not in line and "TBD" not in line and not line.strip().endswith(":"):
                    res.append(("FAIL", f"{os.path.basename(a.audiences)}:{n}: no source tag or TBD: {line.strip()[:80]}"))
            if re.search(r"their words|in their words|quotes?:", line, re.I):
                for q in QUOTE.findall(line):
                    if norm(q) not in src_text:
                        res.append(("FAIL", f"{os.path.basename(a.audiences)}:{n}: quote not found word for word in any source: \"{q[:60]}\""))
        if not a.sources:
            res.append(("CHECK", "no --sources given: quotes and percentages weren't traced"))

    for c in rub["criteria"] + rub["disqualifiers"]:
        ev = c.get("evidence", "")
        if ev and not COUNT.search(ev) and not SOFT.search(ev):
            res.append(("FAIL", f"{c['id']}: evidence gives no count and isn't marked provisional, assumed or user: {ev[:70]}"))
        if analysis and closed < 10 and COUNT.search(ev) and "hypothesis" not in ev.lower():
            res.append(("CHECK", f"{c['id']}: small sample; label the evidence a hypothesis"))

    if a.reply:
        for n, line in enumerate(docs[a.reply].splitlines(), 1):
            m = INTERNALS.search(line)
            if m:
                res.append(("FAIL", f"reply:{n}: mentions an internal ('{m.group(0)}'); say it in plain words"))

    for lvl, msg in res:
        print(f"{lvl}: {msg}")
    fails = sum(1 for l, _ in res if l == "FAIL")
    print(f"{fails} FAIL, {sum(1 for l, _ in res if l == 'CHECK')} CHECK. " + ("FAIL" if fails else "PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
