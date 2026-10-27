#!/usr/bin/env python3
"""Recompute the acquisition checklist score (checks A1-A6, the same checks as the full marketing health audit).
Standard library only.

Usage:
    python3 scripts/score_acquisition.py audits/<domain>/

Reads audits/<domain>/acquisition-checks.json, which uses the dimension-file format:
    {"dimension": "acquisition", "maturity": "founder-led|first hire|small team|full function",
     "assessable": true, "confidence": "high|medium|low",
     "checks": [{"id": "A1", "points": 10, "max": 20, "evidence": "..."}, ...],
     "blockers": ["/pricing: robots meta 'noindex, nofollow'"], "findings": [...], "strengths": [...],
     "not_observable": [...]}

It checks every A1-A6 check is present once, with full, partial or zero points as the rubric allows, applies the
founder-led relief rule on A4 and A5, writes the summed score back to the file, and prints the table.
If an earlier full audit sits in the same folder (dim-acquisition.json, and score.json with the other
dimensions), it prints the earlier acquisition score and what the overall score and grade would become if the
new acquisition score replaced it. It never edits those earlier files.
Exit code: 0 OK, 1 if the checks file breaks a rule (fix it and rerun), 2 on bad input.
"""

import json
import os
import sys

RUBRIC = {  # id: (name, full, partial, relief_for_founder_led)
    "A1": ("Titles and meta descriptions", 20, 10, False),
    "A2": ("On-page structure", 15, 8, False),
    "A3": ("Answer-engine readiness", 15, 8, False),
    "A4": ("Content engine", 20, 10, True),
    "A5": ("Channel evidence", 15, 8, True),
    "A6": ("Navigation and linking", 15, 8, False),
}
WEIGHTS = {"positioning": 25, "acquisition": 20, "conversion": 20, "brand": 15, "measurement": 20}
BANDS = [(85, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "F")]


def grade(total):
    return next(g for cut, g in BANDS if total >= cut)


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print(__doc__)
        return 2
    folder = sys.argv[1]
    path = os.path.join(folder, "acquisition-checks.json")
    if not os.path.isfile(path):
        print(f"FAIL: {path} not found. Write the checks file first.")
        return 2
    try:
        d = json.load(open(path, encoding="utf-8"))
    except ValueError as e:
        print(f"FAIL: {path} is not valid JSON: {e}")
        return 1
    problems = []
    maturity = str(d.get("maturity", "")).lower()
    if not maturity:
        problems.append("no maturity given (founder-led, first hire, small team or full function)")
    founder = "founder" in maturity
    seen = {}
    for c in d.get("checks", []):
        cid = str(c.get("id", "")).upper()
        if cid not in RUBRIC:
            problems.append(f"unknown check id {cid!r}")
            continue
        if cid in seen:
            problems.append(f"{cid} appears twice (score each issue once, each check once)")
        name, full, partial, relief = RUBRIC[cid]
        pts = c.get("points")
        if pts not in (full, partial, 0):
            problems.append(f"{cid} has {pts} points; allowed: {full} (full), {partial} (partial) or 0")
        if relief and founder and pts == 0:
            problems.append(f"{cid}: founder-led relief applies, so a 0 here scores the partial {partial}")
        if not str(c.get("evidence", "")).strip():
            problems.append(f"{cid} has no evidence line")
        c["max"] = full
        seen[cid] = pts if isinstance(pts, int) else 0
    missing = [k for k in RUBRIC if k not in seen]
    if missing:
        problems.append(f"missing checks: {', '.join(missing)}")
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        return 1
    score = sum(seen.values())
    d["score"] = score
    d["dimension"] = "acquisition"
    json.dump(d, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"Acquisition checklist score: {score}/100 ({maturity})")
    print("| Check | Points | Max |\n|---|---|---|")
    for k, (name, full, _, relief) in RUBRIC.items():
        print(f"| {k} {name}{' †' if relief else ''} | {seen[k]} | {full} |")
    if founder:
        print("† founder-led relief applied where a check would otherwise score 0")
    for b in d.get("blockers", []):
        print(f"BLOCKER (outside the score, leads the report): {b}")
    earlier = os.path.join(folder, "dim-acquisition.json")
    overall = os.path.join(folder, "score.json")
    if os.path.isfile(earlier):
        try:
            old = json.load(open(earlier, encoding="utf-8"))
            old_score = sum(c.get("points", 0) for c in old.get("checks", [])) if old.get("checks") else old.get("score")
            print(f"\nEarlier acquisition score (dim-acquisition.json): {old_score} -> now {score} ({score - old_score:+d})")
            changed = {c["id"]: (c.get("points"), seen.get(c["id"])) for c in old.get("checks", [])
                       if c.get("id") in seen and c.get("points") != seen.get(c["id"])}
            for cid, (a, b) in changed.items():
                print(f"  {cid}: {a} -> {b}")
        except (ValueError, KeyError, TypeError) as e:
            print(f"NOTE: couldn't read the earlier acquisition file: {e}")
    if os.path.isfile(overall):
        try:
            s = json.load(open(overall, encoding="utf-8"))
            dims = s["dimensions"]
            new_total = round(sum((score if n == "acquisition" else dims[n]["score"]) * w / 100 for n, w in WEIGHTS.items()))
            old_total = s.get("total")
            print(f"Overall marketing health: {old_total} (grade {s.get('grade', grade(old_total))}) -> {new_total} "
                  f"(grade {grade(new_total)}) if this acquisition score replaces the earlier one. Earlier files left unchanged.")
        except (ValueError, KeyError, TypeError) as e:
            print(f"NOTE: couldn't recompute the overall score from score.json: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
