#!/usr/bin/env python3
"""Self-check the deliverables before replying. Standard library only.

Usage:
    python3 scripts/check_report.py audits/<domain>/measurement.md audits/<domain>/tracking-plan.md response.md \
        [--exports data/*.csv] [--spelling us|ca|uk] [--max-words 200]

Checks:
  - measurement.md has every section in order, and its checklist points add up to the stated score.
  - No personal data (email, name, phone, address) in a tracking-plan parameter or an event snippet.
  - No legal conclusions ("compliant", "illegal", "violates").
  - No internals (script or file names of this method, skill names).
  - Counts: with --exports, every number of 3+ digits must appear in an export (or be a column total); without
    exports, any count next to visitors, sessions, users, conversions, leads, trials or pageviews is flagged.
  - Spelling: with --spelling, words in the other convention are flagged (in every file passed, JSON included).
  - Length: with --max-words, response.md over that many words fails (markdown symbols ignored).
Prints FAIL lines (fix them, then rerun) or PASS.
"""

import csv
import re
import sys

SECTIONS = ["Verdict", "The three things that matter most", "What the site can measure today", "Privacy and consent",
            "Not observable", "Plan", "Measurement checklist"]
MAX = {"M1": 30, "M2": 30, "M3": 15, "M4": 15, "M5": 10}
PERSONAL = re.compile(r"\b(e-?mail|user_email|work_email|phone|full_name|first_name|last_name|name|address)\b", re.I)
LEGAL = re.compile(r"\b(non-?compliant|compliant|illegal|unlawful|violat\w+|breaking the law|in breach of)\b", re.I)
INTERNALS = re.compile(r"inspect_tracking|score_measurement|check_report|\w+\.py\b|SKILL\.md|audit-measurement|marketing-audit|\bthe script\b|\bthe checker\b", re.I)
COUNT_WORDS = r"(visitors?|sessions?|users?|conversions?|leads?|trials?|pageviews?|page views?|demo requests?|signups?|sign-ups?|submissions?|key events?)"
NOT_US = ["behaviour", "colour", "centre", "labour", "favour", "analyse", "optimise", "organisation", "prioritise", "labelled", "modelling", "catalogue", "licence"]
NOT_CA = ["behavior", "color", "center", "labor", "favor", "catalog"]


def opt_list(args, name):
    if name not in args:
        return []
    i = args.index(name)
    out = []
    j = i + 1
    while j < len(args) and not args[j].startswith("--"):
        out.append(args[j])
        j += 1
    del args[i:j]
    return out


def export_numbers(paths):
    nums = set()
    for p in paths:
        lines = [l for l in open(p, encoding="utf-8-sig") if l.strip() and not l.lstrip().startswith("#")]
        rows = list(csv.DictReader(lines))
        cols = rows[0].keys() if rows else []
        for c in cols:
            vals = [str(r[c]).replace(",", "").strip() for r in rows]
            for v in vals:
                if re.fullmatch(r"\d+(\.\d+)?", v):
                    nums.add(str(int(float(v))))
            if vals and all(re.fullmatch(r"\d+", v) for v in vals):
                nums.add(str(sum(int(v) for v in vals)))
    return nums


def main():
    args = sys.argv[1:]
    exports = opt_list(args, "--exports")
    spelling = (opt_list(args, "--spelling") or [""])[0].lower()
    max_words = int((opt_list(args, "--max-words") or ["0"])[0])
    if not args:
        print(__doc__)
        return 2
    fails = []
    known = export_numbers(exports) if exports else set()
    for path in args:
        text = open(path, encoding="utf-8").read()
        name = path.split("/")[-1]
        if max_words and name.startswith("response"):
            n = len(re.findall(r"[A-Za-z0-9][\w'’.,/-]*", re.sub(r"[`*#>|_]", " ", text)))
            if n > max_words:
                fails.append(f"{name}: {n} words, over {max_words}: cut to the answer, the evidence, the fix and how to verify")
        if name == "measurement.md":
            heads = re.findall(r"^##\s+(.+?)\s*$", text, re.M)
            pos = [next((i for i, h in enumerate(heads) if h.lower().startswith(s.lower())), None) for s in SECTIONS]
            for s, p in zip(SECTIONS, pos):
                if p is None:
                    fails.append(f"{name}: missing section '## {s}'")
            found = [p for p in pos if p is not None]
            if found != sorted(found):
                fails.append(f"{name}: sections out of order (expected: {', '.join(SECTIONS)})")
            pts = {}
            for cid in MAX:
                m = re.search(rf"^\|\s*{cid}\s*\|[^\n]*?\|\s*(\d+)\s*/\s*{MAX[cid]}\s*\|", text, re.M)
                if m:
                    pts[cid] = int(m.group(1))
                else:
                    fails.append(f"{name}: checklist row {cid} missing or not in '<points>/{MAX[cid]}' form")
            m = re.search(r"Score:\s*\**(\d+)\s*/\s*100", text[text.lower().rfind("measurement checklist"):] if "measurement checklist" in text.lower() else "")
            if pts and len(pts) == 5 and m and int(m.group(1)) != sum(pts.values()):
                fails.append(f"{name}: checklist adds to {sum(pts.values())}, but the score says {m.group(1)}")
        for i, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            quoting = re.search(r"evidence|remove|delete|drop|strip|currently|today|found", low)  # quoting the existing setup is fine
            cells = [c.strip() for c in line.split("|")]
            if line.startswith("|") and len(cells) > 5 and not re.search(r"never|not |no |excluded|exclude|don't|do not|removed?|instead", low):
                param_cells = [c for c in cells if re.search(r"^[a-z_]+(,\s*[a-z_]+)*$", c)]
                for c in param_cells:
                    for p in re.split(r",\s*", c):
                        if PERSONAL.fullmatch(p) or re.fullmatch(r"\w*(email|phone|full_name|first_name|last_name)\w*", p):
                            fails.append(f"{name}:{i}: parameter '{p}' is personal data")
            if not quoting and re.search(r"(gtag|fbq|dataLayer\.push|lintrk)\s*\(", line) and re.search(r"['\"]?(user_?email|work_email|e-?mail|phone|full_name|first_name|last_name)['\"]?\s*:", line, re.I):
                fails.append(f"{name}:{i}: event code sends personal data: {line.strip()[:90]}")
            for m in LEGAL.finditer(line):
                if not re.search(r"(never|not|isn't|no)\s+(legal|a legal)|not legal advice|whether .* (compliant|violat)", low):
                    fails.append(f"{name}:{i}: legal conclusion '{m.group(0)}': describe what loads and why it matters instead")
            if INTERNALS.search(line):
                fails.append(f"{name}:{i}: mentions internals: '{INTERNALS.search(line).group(0)}'")
            for m in re.finditer(r"(?<![\w.$/-])(\d{1,3}(?:,\d{3})+|\d{3,})(?![\w%/-])", line):
                n = m.group(1).replace(",", "")
                ctx = line[max(0, m.start() - 40):m.end() + 40]
                if re.fullmatch(r"(19|20)\d\d", n) or re.search(r"(G|GTM|UA|AW)-\w*$", line[:m.start()]) or "$" in line[max(0, m.start() - 2):m.start()]:
                    continue
                if exports:
                    if n not in known:
                        fails.append(f"{name}:{i}: {m.group(1)} isn't in the exports (or a column total): check it")
                elif re.search(COUNT_WORDS, ctx, re.I) and not re.search(r"id|pixel|partner|port|\$", ctx, re.I):
                    fails.append(f"{name}:{i}: a count ({m.group(1)}) with no export to trace it to")
            words = NOT_US if spelling == "us" else NOT_CA if spelling in ("ca", "uk") else []
            for w in words:
                if re.search(rf"\b{w}\w*", low):
                    fails.append(f"{name}:{i}: '{w}' doesn't match the {spelling.upper()} spelling convention")
    if fails:
        print("FAIL")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
