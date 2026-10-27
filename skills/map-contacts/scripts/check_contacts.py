#!/usr/bin/env python3
"""Check an accounts/<company>/contacts.md file before it's handed on. Standard library only.

Usage:
    python3 scripts/check_contacts.py accounts/<company>/contacts.md [--sources accounts/<company>/] [--allow "Name"] [--summary]

Checks (format in references/contacts-format.md):
  FAIL  no "As of:" date, no "## Contacts" or "## Gaps" section
  FAIL  a contact block (### Name) missing Title, Role, Persona, Status, Source or Signal
  FAIL  a Role outside (text in brackets ignored, e.g. '(proposed)'): economic buyer, champion, user, technical evaluator, blocker, influencer, unknown
  FAIL  a Status outside: current, left, stale, unconfirmed
  FAIL  a Source line with no date (YYYY-MM-DD or YYYY-MM, or the word 'undated', which WARNs)
  FAIL  an email on a personal domain (gmail, outlook.com, hotmail, yahoo, icloud, ...)
  FAIL  an email that is neither sourced (a dated source on the same line) nor labelled "unverified"
  FAIL  a phone number with no dated source on the same line
  FAIL  a contact with Status left or stale listed in "## Contact order"
  FAIL  with --sources: a contact name that appears in no source file (and isn't passed with --allow)
  WARN  a source date more than 12 months before "As of"
  WARN  a phone number at all (keep only work numbers the user supplied)
  WARN  confidence high on a role whose evidence is only a title

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import os
import re
import sys

ROLES = {"economic buyer", "champion", "user", "technical evaluator", "blocker", "influencer", "unknown"}
STATUSES = {"current", "left", "stale", "unconfirmed"}
REQUIRED = ["Title", "Role", "Persona", "Status", "Source", "Signal"]
PERSONAL = {"gmail.com", "googlemail.com", "outlook.com", "hotmail.com", "live.com", "msn.com", "yahoo.com",
            "yahoo.ca", "icloud.com", "me.com", "mac.com", "aol.com", "proton.me", "protonmail.com", "gmx.com",
            "shaw.ca", "rogers.com", "sympatico.ca", "comcast.net"}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
PHONE = re.compile(r"(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")
DATE = re.compile(r"\b(20\d\d)-(0[1-9]|1[0-2])(?:-(\d\d))?\b")


def months(m):
    return int(m.group(1)) * 12 + int(m.group(2))


def sourced(line):
    low = line.lower()
    return (bool(DATE.search(line)) or "undated" in low) and ("source" in low or "on file" in low)


def parse(text):
    sections, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip().lower()
            sections.setdefault(cur, [])
        elif cur is not None:
            sections[cur].append(line)
    contacts, name = {}, None
    for line in text.splitlines():
        if line.startswith("### "):
            name = line[4:].strip()
            contacts[name] = {}
        elif line.startswith("## "):
            name = None
        elif name:
            m = re.match(r"^\s*-\s*\**([A-Za-z ]+?)\**\s*:\s*(.*)$", line)
            if m:
                contacts[name][m.group(1).strip().title()] = m.group(2).strip()
    return sections, contacts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--sources", help="folder of source files; every contact name must appear in one")
    ap.add_argument("--allow", action="append", default=[], help="a name the user gave in conversation")
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.file):
        print(f"no such file: {a.file}")
        return 2
    text = open(a.file, encoding="utf-8").read()
    out = []
    add = lambda lvl, msg: out.append((lvl, msg))

    asof = re.search(r"^As of:\s*(.*)$", text, re.M)
    asof_m = DATE.search(asof.group(1)) if asof else None
    if not asof_m:
        add("FAIL", "no 'As of: YYYY-MM-DD' line")
    sections, contacts = parse(text)
    for sec in ("contacts", "gaps"):
        if sec not in sections:
            add("FAIL", f"no '## {sec.title()}' section")

    for name, f in contacts.items():
        for k in REQUIRED:
            if not f.get(k):
                add("FAIL", f"{name}: no {k} line")
        role_text = re.sub(r"\(.*?\)", "", f.get("Role", ""))
        roles = [r.strip().lower() for r in re.split(r"[,/;+]| and ", role_text) if r.strip()]
        bad = [r for r in roles if r not in ROLES]
        if bad:
            add("FAIL", f"{name}: role '{', '.join(bad)}' isn't one of: {', '.join(sorted(ROLES))}")
        status = f.get("Status", "").split()[0].lower().strip(".,") if f.get("Status") else ""
        if status and status not in STATUSES:
            add("FAIL", f"{name}: status '{status}' isn't one of: {', '.join(sorted(STATUSES))}")
        src = f.get("Source", "")
        if src and not DATE.search(src):
            if "undated" in src.lower():
                add("WARN", f"{name}: source is undated; say so in Check before outreach")
            else:
                add("FAIL", f"{name}: source has no date (write 'undated' if the file has none)")
        if asof_m:
            for d in DATE.finditer(src):
                if months(asof_m) - months(d) > 12:
                    add("WARN", f"{name}: source dated {d.group(0)} is over 12 months old; confirm title and status")
        ev = (f.get("Evidence", "") + " " + f.get("Confidence", "")).lower()
        if "high" in f.get("Confidence", "").lower() and ("title" in ev and "call" not in ev and "notes" not in ev):
            add("WARN", f"{name}: high confidence on a role that rests on a title")

    for i, line in enumerate(text.splitlines(), 1):
        for m in EMAIL.finditer(line):
            dom = m.group(1).lower()
            if dom in PERSONAL:
                add("FAIL", f"line {i}: personal email address ({m.group(0)}); remove it, use a work channel")
            elif "unverified" not in line.lower() and not sourced(line):
                add("FAIL", f"line {i}: {m.group(0)} has no dated source and isn't labelled unverified")
        for m in PHONE.finditer(line):
            if not sourced(line):
                add("FAIL", f"line {i}: phone number {m.group(0)} with no dated source")
            else:
                add("WARN", f"line {i}: phone number present; keep only work numbers the user supplied")

    order = "\n".join(sections.get("contact order", []))
    for name, f in contacts.items():
        st = f.get("Status", "").lower()
        if (st.startswith("left") or st.startswith("stale")) and name in order:
            add("FAIL", f"{name}: status is {st.split()[0]} but listed in the contact order")

    if a.sources:
        corpus = ""
        for root, _, files in os.walk(a.sources):
            for fn in files:
                p = os.path.join(root, fn)
                if os.path.abspath(p) == os.path.abspath(a.file):
                    continue
                try:
                    corpus += open(p, encoding="utf-8", errors="ignore").read().lower() + "\n"
                except OSError:
                    pass
        allowed = {n.lower() for n in a.allow}
        lines = corpus.splitlines()
        for name in contacts:
            low = name.lower()
            tokens = [t for t in re.findall(r"[a-zà-ÿ'-]+", low) if t not in ("dr", "mr", "ms", "mrs")]
            found = low in corpus or any(all(t in ln for t in tokens) for ln in lines)
            if low not in allowed and not found:
                add("FAIL", f"{name}: name not found in any source file; remove, or confirm the source")

    fails = sum(1 for l, _ in out if l == "FAIL")
    warns = sum(1 for l, _ in out if l == "WARN")
    if a.summary:
        print(f"{'FAIL' if fails else 'PASS'}: {len(contacts)} contacts, {fails} fail, {warns} warn")
    else:
        for lvl, msg in out:
            print(f"{lvl}  {msg}")
        print(f"\n{'FAIL' if fails else 'PASS'}: {len(contacts)} contacts checked, {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
