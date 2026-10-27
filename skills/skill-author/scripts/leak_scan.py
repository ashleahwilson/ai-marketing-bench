#!/usr/bin/env python3
"""Scan files for things that must not leave the source material: secrets, personal data, client names,
revenue and internal prices. Standard library only.

Usage:
    python3 scripts/leak_scan.py <file-or-folder> [...] [--name "Client Name"] [--names names.txt]

--name / --names: terms that must not appear (real client, customer or person names found in the source).
Secrets are masked in the output: only the first 4 characters are printed.

LEAK lines must be removed before saving. CHECK lines need a decision: keep only if they are fictional
stand-ins or public facts the user approved. Exit code 1 if any LEAK, else 0.
"""

import argparse
import os
import re
import sys

SECRET = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("API key", re.compile(r"\b(?:sk|pk|rk)[-_](?:live|test|proj|ant)?[-_]?[A-Za-z0-9_-]{12,}")),
    ("AWS key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._-]{16,}")),
    ("key or password value", re.compile(
        r"(?i)\b(?:api[_ -]?key|secret|token|password|passwd|pwd|access[_ -]?key|client[_ -]?secret)\b"
        r"\s*[:=]\s*[\"']?([A-Za-z0-9_\-./+]{8,})")),
    ("long random string", re.compile(r"\b(?=[A-Za-z0-9_]*\d)(?=[A-Za-z0-9_]*[a-z])(?=[A-Za-z0-9_]*[A-Z])[A-Za-z0-9_]{28,}\b")),
]
SAFE_DOMAIN = re.compile(r"(?i)(?:\.example|example\.(?:com|org|net)|\.test|\.invalid|\.localhost)\b")
PERSONAL = [
    ("email address", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")),
    ("phone number", re.compile(r"(?<![\w.])(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b")),
]
CHECKS = [
    ("money figure", re.compile(r"(?i)(?:[$€£]\s?\d[\d,]*(?:\.\d+)?\s?(?:k|m|mm|million|billion|bn)?\b|\b\d[\d,.]*\s?(?:k|m|million)?\s?(?:cad|usd|eur|gbp|dollars)\b)")),
    ("percentage", re.compile(r"\b\d+(?:\.\d+)?\s?%")),
    ("web address", re.compile(r"(?i)\bhttps?://[^\s)\"'>]+")),
    ("person with title", re.compile(r"\b(?:Dr|Mr|Mrs|Ms|Mx|Prof)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?")),
    ("company name", re.compile(r"\b(?:[A-Z][\w&'-]+\s){1,3}(?:Inc|Ltd|LLC|Corp|GmbH|LLP|Co)\b\.?")),
    ("revenue or salary words", re.compile(r"(?i)\b(?:ARR|MRR|revenue|turnover|salary|margin|hourly rate|day rate|internal rate|our rate|cost price)\b[^.\n]{0,40}\d")),
]
TEXT_EXT = {".md", ".txt", ".json", ".py", ".html", ".htm", ".csv", ".yaml", ".yml", ".toml", ".js", ".ts", ".xml", ""}


def mask(s):
    s = s.strip()
    return (s[:4] + "…[masked]") if len(s) > 4 else "…[masked]"


def files_in(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if os.path.splitext(f)[1].lower() in TEXT_EXT:
                    yield os.path.join(root, f)


def scan(path, names):
    hits = []
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return hits
    for i, line in enumerate(lines, 1):
        found_secret = False
        for label, rx in SECRET:
            for m in rx.finditer(line):
                val = m.group(1) if m.groups() else m.group(0)
                if found_secret or (label == "long random string" and re.fullmatch(r"[a-f0-9]+", val)):
                    continue
                hits.append(("LEAK", label, i, mask(val)))
                found_secret = True
        for label, rx in PERSONAL:
            for m in rx.finditer(line):
                if not SAFE_DOMAIN.search(m.group(0)):
                    hits.append(("LEAK", label, i, m.group(0)))
        for n in names:
            if n and re.search(r"(?i)\b" + re.escape(n) + r"\b", line):
                hits.append(("LEAK", "named term", i, n))
        for label, rx in CHECKS:
            for m in rx.finditer(line):
                val = m.group(0)
                if label == "web address" and SAFE_DOMAIN.search(val):
                    continue
                hits.append(("CHECK", label, i, val.strip()))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--name", action="append", default=[])
    ap.add_argument("--names")
    a = ap.parse_args()
    names = list(a.name)
    if a.names and os.path.isfile(a.names):
        names += [l.strip() for l in open(a.names, encoding="utf-8") if l.strip() and not l.startswith("#")]
    leaks = checks = 0
    for f in files_in(a.paths):
        for lvl, label, line, val in scan(f, names):
            print(f"{lvl}  {f}:{line}  {label}: {val}")
            leaks += lvl == "LEAK"
            checks += lvl == "CHECK"
    print(f"\n{leaks} leak(s), {checks} item(s) to check." + (" Remove every LEAK before saving." if leaks else ""))
    return 1 if leaks else 0


if __name__ == "__main__":
    sys.exit(main())
