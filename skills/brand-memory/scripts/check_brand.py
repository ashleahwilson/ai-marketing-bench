#!/usr/bin/env python3
"""Check a brand memory folder. Standard library only. Reads files; changes nothing.

Usage:
    python3 scripts/check_brand.py brand/
    python3 scripts/check_brand.py brand/ --today 2026-10-10    # pin "today" for reproducible checks
    python3 scripts/check_brand.py brand/ --summary             # one line

Exit code: 0 if no FAIL, 1 if any FAIL (a secret, or no BRAND.md), 2 on bad input.

What it can't do: judge whether two differently worded facts contradict each other in meaning.
It flags numeric conflicts on the same subject; read the files for the rest (see references/maintenance.md).
"""

import datetime
import os
import re
import sys

CORE = ["offer.md", "audiences.md", "positioning.md", "proof.md", "voice.md"]
# A file unreviewed for ~6 months is likely out of date; proof older than ~18 months is weak evidence.
REVIEW_DAYS, PROOF_DAYS = 183, 548

SECRETS = [
    (re.compile(r"\b(sk|pk|rk)[-_](live|test|proj)?[-_]?[A-Za-z0-9]{16,}"), "API key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"\b[0-9a-f]{32}-us\d{1,2}\b"), "Mailchimp API key"),
    (re.compile(r"(api[ _-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*\S{6,}", re.I), "credential"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
]
TAG = re.compile(r"\[source:\s*([^\]]+)\]", re.I)
STATUS = re.compile(r"\b(confirmed|provisional|assumed)\b", re.I)
DATE = re.compile(r"\b(20\d\d)-(\d\d)(?:-(\d\d))?\b")
PLACEHOLDER = re.compile(r"<[^>\n]{2,60}>|\bTBD\b|\bXXX\b|\[(?:insert|todo|placeholder)[^\]]*\]", re.I)
NAMED = re.compile(r"\|\s*named:\s*(yes|no|unconfirmed)", re.I)


def parse_date(m):
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)
    try:
        return datetime.date(y, mo, d)
    except ValueError:
        return None


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def check(folder, today):
    out = []
    add = lambda lvl, f, msg: out.append((lvl, f, msg))
    files = sorted(f for f in os.listdir(folder) if f.endswith(".md"))
    if "BRAND.md" not in files:
        add("FAIL", "-", "no BRAND.md (the required summary file)")
    for f in CORE:
        if f not in files:
            add("WARN", f, "core file missing")

    numbers = {}  # (subject words) -> {value: [file:line]}
    for f in files:
        raw = open(os.path.join(folder, f), encoding="utf-8").read()
        text = strip_comments(raw)
        lines = text.splitlines()

        for i, line in enumerate(raw.splitlines(), 1):
            hit = next((label for rx, label in SECRETS if rx.search(line)), None)
            if hit:
                add("FAIL", f"{f}:{i}", f"{hit} stored in brand memory; remove it and rotate it")

        if re.search(r"YYYY-MM(-DD)?|<Company>|<Name>|<Role>|<Pillar>|<Industry|<Customer|<claim>|<Competitor>", raw):
            add("WARN", f, "template placeholder left in (YYYY-MM-DD or <…>)")
        m = re.search(r"^Last reviewed:\s*(\S+)", text, re.M)
        if f != "changelog.md":
            if not m:
                add("WARN", f, "no 'Last reviewed:' line")
            else:
                dm = DATE.search(m.group(1))
                d = parse_date(dm) if dm else None
                if d and (today - d).days > REVIEW_DAYS:
                    add("WARN", f, f"not reviewed since {d.isoformat()} ({(today - d).days} days)")

        for i, line in enumerate(lines, 1):
            s = line.strip()
            if not s.startswith("- ") or f in ("changelog.md", "results.md", "BRAND.md"):
                continue
            body = s[2:]
            if PLACEHOLDER.search(body):
                add("WARN", f"{f}:{i}", f"placeholder or TBD: {body[:70]}")
                continue
            tag = TAG.search(body)
            is_rule = f in ("rules.md", "voice.md") and not re.search(r"\d", body)
            if not tag and not is_rule and ":" in body[:40] and f not in ("senders.md",):
                add("WARN", f"{f}:{i}", f"fact with no source tag: {body[:70]}")
            elif not tag and not is_rule and f in ("offer.md", "proof.md", "audiences.md", "positioning.md", "competitors.md", "claims.md"):
                add("WARN", f"{f}:{i}", f"fact with no source tag: {body[:70]}")
            if tag:
                st = STATUS.search(tag.group(1))
                if not st:
                    add("WARN", f"{f}:{i}", "source tag has no status (confirmed / provisional / assumed)")
                elif st.group(1).lower() == "assumed" and f in ("proof.md", "claims.md"):
                    add("WARN", f"{f}:{i}", "assumed fact in proof or claims; it can't be used as evidence")
            if f == "proof.md":
                nm = NAMED.search(body)
                if nm and nm.group(1).lower() in ("no", "unconfirmed"):
                    add("WARN", f"{f}:{i}", f"named customer with permission '{nm.group(1)}': confirm before using the name")
                dates = [parse_date(x) for x in DATE.finditer(body)]
                dates = [d for d in dates if d]
                if dates and (today - max(dates)).days > PROOF_DAYS and "stale" not in body.lower():
                    add("WARN", f"{f}:{i}", f"proof dated {max(dates).isoformat()[:7]} is over 18 months old")
                # "since 2022" describes something ongoing, not an old result
                yr = re.search(r"(?<!since )\b(19|20)(\d\d)\b(?![-\d])", re.sub(TAG, "", body))
                company_fact = re.search(r"\b(founded|established|est\.|since)\b", body, re.I)
                if yr and not company_fact and today.year - int(yr.group(0)) >= 2 and "stale" not in body.lower():
                    add("WARN", f"{f}:{i}", f"proof refers to {yr.group(0)}, which may be stale")
            # Numeric facts by subject, for cross-file conflicts: "within 48 hours" vs "within 72 hours".
            for m2 in re.finditer(r"(within|under|from|in|over)\s+\$?(\d[\d,.]*)\s*(%|hours?|days?|weeks?|months?|/month|/location)?", body, re.I):
                subj = " ".join(re.findall(r"[a-z]{4,}", re.sub(TAG, "", body).lower())[:4])
                key = (m2.group(1).lower(), m2.group(3) or "", subj)
                numbers.setdefault(key, {}).setdefault(m2.group(2), []).append(f"{f}:{i}")

    # BRAND.md's file table should match what exists
    if "BRAND.md" in files:
        idx = open(os.path.join(folder, "BRAND.md"), encoding="utf-8").read()
        for name, status in re.findall(r"^\|\s*([a-z-]+\.md)\s*\|\s*([^|]+?)\s*\|", idx, re.M):
            exists = name in files
            if status.lower().startswith("missing") and exists:
                add("WARN", "BRAND.md", f"file table says {name} is missing, but it exists")
            elif not status.lower().startswith("missing") and not exists:
                add("WARN", "BRAND.md", f"file table lists {name} as '{status}', but it doesn't exist")

    for (prep, unit, subj), vals in numbers.items():
        if len(vals) > 1:
            where = "; ".join(f"{v} at {', '.join(locs)}" for v, locs in vals.items())
            add("WARN", "-", f"conflicting values for '{prep} … {unit}' ({subj}): {where}")
    return out


def main():
    args = sys.argv[1:]
    summary = "--summary" in args
    args = [a for a in args if a != "--summary"]
    today = datetime.date.today()
    if "--today" in args:
        i = args.index("--today")
        today = datetime.date.fromisoformat(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__)
        return 2
    res = check(args[0], today)
    fails = sum(r[0] == "FAIL" for r in res)
    warns = len(res) - fails
    if summary:
        print(f"check_brand: {'FAIL' if fails else 'PASS'}, {fails} fail, {warns} warn")
    else:
        for lvl, where, msg in sorted(res, key=lambda r: (r[0] != "FAIL", r[1])):
            print(f"{lvl:4} {where}: {msg}")
        print(f"\n{fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
