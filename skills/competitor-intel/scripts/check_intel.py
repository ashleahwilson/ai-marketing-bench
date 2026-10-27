#!/usr/bin/env python3
"""Check a battlecard or a brand/competitors.md file for sourcing, staleness and claims. Standard library only.

Usage:
    python3 scripts/check_intel.py competitors/<name>-battlecard.md --brand brand/ --intel intel/ [--today YYYY-MM-DD]
    python3 scripts/check_intel.py brand/competitors.md [--today YYYY-MM-DD]

The file type is detected from its first heading ("# Battlecard: ..." or "# Competitors").

Battlecard checks:
  - every required section is present
  - every fact line in a fact section carries [source: <where>, <date> ...]
  - every price carries a source (or is written as "not shown")
  - rumour terms (going out of business, breach, lawsuit ...) appear only under "Don't say", or with a public source
  - comparison claims (2x, faster than, cheaper than, the only, #1) in our sections carry proof from brand memory,
    and any number in them appears in brand memory
  - "No" for the competitor in the feature table is flagged: absent from a page is "not shown"
  - cited files exist in --intel, and captures older than 90 days are flagged
competitors.md checks:
  - every fact bullet under a competitor carries a source, a date and a status (confirmed, provisional, assumed)
  - lines older than 90 days are marked stale, superseded, or sit under a "Price history" heading

Prints FAIL / WARN lines with line numbers, then RESULT: PASS or RESULT: FAIL. Exit code 1 on any FAIL.
"""

import argparse
import datetime
import os
import re
import sys

STALE_DAYS = 90
DATE = re.compile(r"\b(20\d\d)-(\d\d)(?:-(\d\d))?\b")
SOURCE = re.compile(r"\[source:([^\]]*)\]", re.I)
PRICE = re.compile(r"[$€£]\s?\d")
RUMOUR = re.compile(
    r"going out of business|out of business|bankrupt|insolven|running out of (money|cash)|financial trouble|"
    r"layoffs?|breach|hacked|security (problem|issue|incident)s?|lawsuit|being sued|\bsued\b|fraud|\bscam\b",
    re.I)
PUBLIC = re.compile(r"public|filing|disclosure|news|court record|regulator", re.I)
COMPARE = re.compile(
    r"\b\d+(\.\d+)?\s?x\b|\b\d+(\.\d+)?\s?times\b|\d+\s?% (faster|cheaper|more|less|better|fewer)|"
    r"\b(faster|cheaper|better|easier|more accurate|more reliable|less expensive) than\b|\bthe only\b|#1\b|"
    r"\bnumber one\b|\bbest in\b|\bunlike (them|[A-Z]\w+), we\b", re.I)

BATTLECARD_SECTIONS = ["Recommendation", "Who they are", "Pricing as shown", "Where they're strong", "Where we win",
                       "When we lose to them and why", "Landmines", "Objections", "Feature comparison",
                       "Don't say", "Sources", "Open"]
FACT_SECTIONS = {"who they are", "where they're strong", "when we lose to them and why", "landmines"}
OUR_SECTIONS = {"recommendation", "where we win", "objections", "feature comparison"}
NO_SOURCE_OK = re.compile(r"\bnot shown\b|\bTBD\b|\bnone in (the )?sources\b|\bunknown\b", re.I)


def norm(h):
    return h.strip().lower().replace("’", "'")


def parse_date(m):
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)
    try:
        return datetime.date(y, mo, d)
    except ValueError:
        return None


def read_brand(brand_dir):
    """Brand memory that can substantiate a claim: skips competitors.md, rules.md, and claims still needing proof."""
    text = ""
    if brand_dir and os.path.isdir(brand_dir):
        for f in sorted(os.listdir(brand_dir)):
            if not f.endswith(".md") or f in ("competitors.md", "rules.md", "changelog.md"):
                continue
            skip = False
            for line in open(os.path.join(brand_dir, f), encoding="utf-8").read().splitlines():
                if line.startswith("## "):
                    skip = bool(re.search(r"needs substantiation|restricted", line, re.I))
                if not skip and "provisional" not in line and "assumed" not in line:
                    text += line + "\n"
    return text


def is_fact_line(line):
    s = line.strip()
    return (s.startswith(("- ", "* ")) or re.match(r"^\d+\.\s", s) or (s.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", s)))


def check_dates(line, n, today, out, stale_ok=False):
    for m in DATE.finditer(" ".join(SOURCE.findall(line))):
        d = parse_date(m)
        if d and (today - d).days > STALE_DAYS and not stale_ok:
            out.append(("WARN", n, f"capture dated {d.isoformat()} is over {STALE_DAYS} days old: re-verify or mark it stale"))


def check_battlecard(lines, brand_text, intel, today):
    out = []
    heads = [norm(l[3:]) for l in lines if l.startswith("## ")]
    for s in BATTLECARD_SECTIONS:
        if norm(s) not in heads:
            out.append(("FAIL", 0, f"missing section: ## {s}"))
    if not any(l.lower().startswith("status:") for l in lines[:12]):
        out.append(("FAIL", 0, "no 'Status:' line under the title"))
    if not any("refresh by" in l.lower() for l in lines[:12]):
        out.append(("FAIL", 0, "no 'Refresh by' date under the title"))
    section, table_header = "", []
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            section, table_header = norm(line[3:]), []
            continue
        if not line.strip():
            continue
        if line.strip().startswith("|") and not table_header:
            table_header = [c.strip().lower() for c in line.strip().strip("|").split("|")]
            continue
        fact = is_fact_line(line)
        has_src = bool(SOURCE.search(line)) or (section in ("pricing as shown", "feature comparison", "sources")
                                                 and bool(DATE.search(line)))
        if section in FACT_SECTIONS and fact and not has_src and not NO_SOURCE_OK.search(line):
            out.append(("FAIL", i, "fact line without [source: <where>, <date>]"))
        if PRICE.search(line) and not has_src and section not in ("don't say", "open") and section in FACT_SECTIONS | {"pricing as shown"}:
            out.append(("FAIL", i, "price without a source and capture date"))
        if RUMOUR.search(line) and section not in ("don't say", "open"):
            src = " ".join(SOURCE.findall(line))
            if not (src and PUBLIC.search(src)):
                out.append(("FAIL", i, "rumour term outside 'Don't say' with no public source: remove it"))
        if section in OUR_SECTIONS and COMPARE.search(line):
            proof = re.search(r"proof:|brand/|\[source:", line, re.I)
            claim = COMPARE.search(line).group(0)
            token = re.sub(r"\s+", "", claim.lower())
            if not proof:
                out.append(("FAIL", i, f"comparison claim '{claim}' with no proof from brand memory"))
            elif re.search(r"\d", claim) and token not in re.sub(r"\s+", "", brand_text.lower()):
                out.append(("FAIL", i, f"comparison '{claim}' isn't substantiated in brand memory (confirmed proof or approved claims)"))
        if section == "feature comparison" and line.strip().startswith("|") and table_header:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            for col, cell in zip(table_header[1:], cells[1:]):
                if col not in ("source", "sources", "us", "notes") and not col.startswith(("we", "our")) and re.fullmatch(r"(no|✗|❌|x)", cell, re.I):
                    out.append(("WARN", i, "competitor marked 'No': if the page just doesn't mention it, write 'not shown'"))
        if intel:
            for src in SOURCE.findall(line):
                for f in re.findall(r"[\w.-]+\.(?:md|csv|html|txt|pdf)\b", src):
                    if not os.path.exists(os.path.join(intel, f)) and not f.startswith(("proof", "claims", "offer", "positioning", "BRAND")):
                        out.append(("FAIL", i, f"cites {f}, which isn't in {intel}"))
        check_dates(line, i, today, out)
    return out


def check_competitors(lines, today):
    out = []
    if not any(l.lower().startswith("last reviewed:") for l in lines[:5]):
        out.append(("FAIL", 0, "no 'Last reviewed:' line"))
    comp, sub = None, ""
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            comp, sub = line[3:].strip(), ""
            continue
        if line.startswith("### "):
            sub = norm(line[4:])
            continue
        if not comp or not line.strip().startswith(("- ", "* ")):
            continue
        if "our read" in sub:
            continue
        if line.strip().startswith(("- TBD", "* TBD")):
            continue
        tag = SOURCE.search(line)
        if not tag:
            out.append(("FAIL", i, f"{comp}: fact without a [source: …] tag"))
            continue
        body = tag.group(1)
        if not DATE.search(body):
            out.append(("FAIL", i, f"{comp}: source tag has no capture date"))
        if not re.search(r"\b(confirmed|provisional|assumed)\b", body):
            out.append(("FAIL", i, f"{comp}: source tag has no status (confirmed, provisional, assumed)"))
        history = "history" in sub or re.search(r"\b(stale|superseded|was |previously|replaced)\b", line, re.I)
        for m in DATE.finditer(body):
            d = parse_date(m)
            if d and (today - d).days > STALE_DAYS and not history:
                out.append(("FAIL", i, f"{comp}: captured {d.isoformat()}, over {STALE_DAYS} days ago, and not marked stale"))
            if d and d > today:
                out.append(("FAIL", i, f"{comp}: capture date {d.isoformat()} is in the future"))
        if PRICE.search(line) and not DATE.search(body):
            out.append(("FAIL", i, f"{comp}: price without a capture date"))
        if RUMOUR.search(line) and not PUBLIC.search(body):
            out.append(("FAIL", i, f"{comp}: rumour term with no public source"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--brand")
    ap.add_argument("--intel")
    ap.add_argument("--today")
    a = ap.parse_args()
    today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()
    if not os.path.isfile(a.file):
        print(f"FAIL: {a.file} not found")
        return 2
    lines = open(a.file, encoding="utf-8").read().splitlines()
    title = next((l for l in lines if l.startswith("# ")), "")
    if title.lower().startswith("# battlecard"):
        res = check_battlecard(lines, read_brand(a.brand), a.intel, today)
    elif title.lower().startswith("# competitors"):
        res = check_competitors(lines, today)
    else:
        print("FAIL: first heading must be '# Battlecard: <name>' or '# Competitors'")
        return 1
    for level, n, msg in res:
        print(f"{level} {'line ' + str(n) if n else 'file'}: {msg}")
    fails = sum(1 for r in res if r[0] == "FAIL")
    print(f"RESULT: {'FAIL' if fails else 'PASS'} ({fails} fail, {len(res) - fails} warn)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
