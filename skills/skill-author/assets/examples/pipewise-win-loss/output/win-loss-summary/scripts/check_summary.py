#!/usr/bin/env python3
"""Check a win-loss summary. Standard library only.

Usage: python3 scripts/check_summary.py SUMMARY --transcript TRANSCRIPT [--max-words 300]
Prints FAIL / OK lines; exit 1 on any FAIL.
"""
import argparse
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("summary")
ap.add_argument("--transcript", required=True)
ap.add_argument("--max-words", type=int, default=300)
a = ap.parse_args()
s = open(a.summary, encoding="utf-8").read()
t = " ".join(open(a.transcript, encoding="utf-8").read().split()).lower()
fails = 0


def report(ok, msg):
    global fails
    print(("OK   " if ok else "FAIL ") + msg)
    fails += not ok


words = len(re.findall(r"\b[\w'’-]+\b", s))
report(words <= a.max_words, f"{words} words (limit {a.max_words})")
report(bool(re.search(r"deal size:\s*\S", s, re.I)), "deal size line present")
for q in re.findall(r"[\"“]([^\"”]{8,})[\"”]", s):
    report(" ".join(q.split()).lower() in t, f"quote found in transcript: \"{q[:50]}\"")
for w in ("should", "recommend", "will likely", "probably will"):
    for m in re.finditer(r"(?i)\b" + w + r"\b", s):
        line = s[:m.start()].count("\n") + 1
        report(False, f"line {line}: '{m.group(0)}' recommends or predicts")
sys.exit(1 if fails else 0)
